import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from dataclasses_json import dataclass_json
from deep_learning_compression.Compression.Compression import (
    ConvCompressor,
    JpegCompressor,
    JpegXrCommpressor,
)
from deep_learning_compression.Compression.CompressionDl import DeepLearningCompressor
from deep_learning_compression.Storage.CompressStorage import CompressStorage
from deep_learning_compression.Storage.Storage import Storage


@dataclass_json
@dataclass
class Compressed:

    CompressedWithDl: bool
    CompressMethod: str
    FilePathCompressed: str
    FilePathDecompressed: str
    FileSizeCompressedBytes: int
    FileSizeDeCompressedBytes: int

    ConventionalCompressions: Optional[List["Compressed"]]


@dataclass_json
@dataclass
class Image:

    OriginalFilePath: str
    FileSizeByptes: int

    DeepLearningCompressions: List[Compressed]


@dataclass_json
@dataclass
class AllCompressImage:

    Images: List[Image]
    DlMethods: List[str]
    ConvMethods: List[str]


if __name__ == "__main__":

    s = Storage()
    cs = CompressStorage()

    dataSetName = "ImageCompressionBenchmark8BitRGB"

    files = s.GetAllFileInformationOfASingleDataSet(setName=dataSetName)

    # Define models that should be used for compression
    dl_model_names = ["b2018-gdn-128-1", "b2018-gdn-128-2"]
    conv_methods: List[ConvCompressor] = [JpegXrCommpressor, JpegCompressor]

    all_processed = AllCompressImage(
        Images=[],
        DlMethods=dl_model_names,
        ConvMethods=[m.METHOD_NAME for m in conv_methods],
    )

    for currFile in files:  # Iterate over images in dataset

        orgFilePath = currFile.Filepath
        curr_proces_image = Image(
            OriginalFilePath=orgFilePath.as_posix(),
            FileSizeByptes=s.GetSingleFileInformation(orgFilePath).FileSizeBytes,
            DeepLearningCompressions=[],
        )

        for currDlName in dl_model_names:  # Iterate over Deep Learning Methods
            model = DeepLearningCompressor(currDlName)  # Instantiate Model

            compFilePath = cs.CreateAndPrepareCompressedPathDL(
                dataSetName=dataSetName, modelName=currDlName, filePath=orgFilePath
            )
            decompFilePath = cs.CreateAndPrepareDecompressedPathDL(
                dataSetName=dataSetName, modelName=currDlName, filePath=compFilePath
            )

            model.compress(input_file_path=orgFilePath, output_file_path=compFilePath)
            model.decompress(
                input_file_path=compFilePath, output_file_path=decompFilePath
            )

            compInfo = s.GetSingleFileInformation(compFilePath)
            decompInfo = s.GetSingleFileInformation(decompFilePath)

            currDlCompression = Compressed(  # Image with current DeepLearning Method
                CompressedWithDl=True,
                CompressMethod=currDlName,
                FilePathCompressed=compFilePath.as_posix(),
                FilePathDecompressed=decompFilePath.as_posix(),
                FileSizeCompressedBytes=compInfo.FileSizeBytes,
                FileSizeDeCompressedBytes=decompInfo.FileSizeBytes,
                ConventionalCompressions=[],
            )

            for convMeth in conv_methods:  # Iterate over conventional Methods

                currConvOout = cs.CreateAndPrepareCompressedPathConventional(
                    dataSetName=dataSetName,
                    filePath=compFilePath,
                    DLmodelName=currDlName,
                    methodName=convMeth.METHOD_NAME,
                )
                convMeth.compress(
                    input_file=orgFilePath.as_posix(),
                    output_file=currConvOout,
                    target_ratio=currFile.FileSizeBytes / compInfo.FileSizeBytes,
                )
                # TODO: Decompress!
                currConvCompression = Compressed(
                    CompressedWithDl=False,
                    CompressMethod=convMeth.METHOD_NAME,
                    FilePathCompressed=currConvOout.as_posix(),
                    FilePathDecompressed="",
                    FileSizeCompressedBytes=s.GetSingleFileInformation(
                        currConvOout
                    ).FileSizeBytes,
                    FileSizeDeCompressedBytes=-1,
                    ConventionalCompressions=None,
                )

                currDlCompression.ConventionalCompressions.append(currConvCompression)
            curr_proces_image.DeepLearningCompressions.append(currDlCompression)
        all_processed.Images.append(curr_proces_image)

    # Write summary to json file
    with open("./tmp/compressed_datasets/last_run_info.json", "w") as f:
        json.dump(all_processed.to_dict(), f, indent=4)
