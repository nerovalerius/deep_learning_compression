import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import cv2
import pandas as pd
import sewar.full_ref as full_ref
import torch
from dataclasses_json import dataclass_json
from piq import brisque, vsi
from RunCompression import AllCompressImage

from image_metrics.no_ref import niqe, piqe


def calculate_metrics(reference_img, compressed_img, device):

    vsi_r = vsi(
        torch.tensor(reference_img).to(device).permute(2, 0, 1)[None, ...] / 255.0,
        torch.tensor(compressed_img).to(device).permute(2, 0, 1)[None, ...] / 255.0,
        data_range=1.0,
    )  # Visual Saliency-induced Index
    uqi = full_ref.uqi(
        reference_img, compressed_img
    )  # Universal Quality Image Index (UQI)
    vifp = full_ref.vifp(
        reference_img, compressed_img
    )  # Visual Information Fidelity (VIF)

    # No Reference Metrics
    piqe_score, _, _, _ = piqe.piqe(
        compressed_img
    )  # Perception-based Image Quality Evaluator (PIQE)
    niqe_score = niqe.niqe(compressed_img)  # Natural Image Quality Evaluator (NIQE)
    brisque_r = brisque(
        torch.tensor(compressed_img).permute(2, 0, 1)[None, ...] / 255.0,
        data_range=1.0,
        reduction="none",
    )  # Blind/Referenceless Image Spatial Quality Evaluator (BRISQUE)

    new_row = {
        "uqi": uqi,
        "vifp": vifp,
        "vsi": vsi_r.item(),
        "piqe": piqe_score,
        "niqe": niqe_score,
        "brisque": brisque_r.item(),
    }

    return new_row


def load_image(path: str):
    return cv2.imread(path)


@dataclass_json
@dataclass
class MetricResultRow:

    DeepLearningModel: str  # Name of Dl Model, to know what was referenced
    CompressionMethod: str  # Name of Compression (e.g. Dl Model, Jpeg, ...)
    ReferenceFilePath: str
    DecompressedFilePath: str
    CompressedFilePath: str
    FileSizeOriginal: int
    FileSizeCompressed: int
    Metrics: dict


@dataclass_json
@dataclass
class MetricResults:
    Results: List[MetricResultRow]


if __name__ == "__main__":

    # check cuda availability
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    path_to_json = "./tmp/compressed_datasets/last_run_info.json"

    # Load Json Data and convert to object
    with open(path_to_json, "r") as f:
        data_dict = json.load(f)

    data: AllCompressImage = AllCompressImage.from_dict(data_dict)
    data.Images = [
        img for i, img in enumerate(data.Images) if i not in [8]
    ]  # exclude deer.ppm because it fucks up brisque
    all_results = MetricResults(Results=[])

    for it, reference_image_obj in enumerate(data.Images):
        print(f"Processing {it}/{len(data.Images)} ...")

        reference_img = load_image(reference_image_obj.OriginalFilePath)

        for dl_method_obj in reference_image_obj.DeepLearningCompressions:

            currDlCompressed = load_image(dl_method_obj.FilePathDecompressed)

            m = calculate_metrics(
                reference_img=reference_img,
                compressed_img=currDlCompressed,
                device=device,
            )

            currDlRes = MetricResultRow(
                CompressionMethod=dl_method_obj.CompressMethod,
                DeepLearningModel=dl_method_obj.CompressMethod,
                CompressedFilePath=dl_method_obj.FilePathCompressed,
                ReferenceFilePath=reference_image_obj.OriginalFilePath,
                Metrics=m,
                FileSizeOriginal=reference_image_obj.FileSizeByptes,
                FileSizeCompressed=dl_method_obj.FileSizeCompressedBytes,
                DecompressedFilePath=dl_method_obj.FilePathDecompressed,
            )

            all_results.Results.append(currDlRes)

            for conv_method_obj in dl_method_obj.ConventionalCompressions:

                currConvCompressed = load_image(conv_method_obj.FilePathDecompressed)
                m = calculate_metrics(
                    reference_img=reference_img,
                    compressed_img=currConvCompressed,
                    device=device,
                )

                currConvRes = MetricResultRow(
                    CompressionMethod=conv_method_obj.CompressMethod,
                    DeepLearningModel=dl_method_obj.CompressMethod,
                    CompressedFilePath=conv_method_obj.FilePathCompressed,
                    ReferenceFilePath=reference_image_obj.OriginalFilePath,
                    Metrics=m,
                    FileSizeOriginal=reference_image_obj.FileSizeByptes,
                    FileSizeCompressed=conv_method_obj.FileSizeCompressedBytes,
                    DecompressedFilePath=conv_method_obj.FilePathDecompressed,
                )

                all_results.Results.append(currConvRes)

    r = all_results.to_dict()["Results"]
    df = pd.DataFrame.from_dict({i: d for i, d in enumerate(r)}, orient="index")
    pd.concat([df, df["Metrics"].apply(pd.Series)], axis=1).to_csv(
        "./tmp/last_run_metrics.csv"
    )
