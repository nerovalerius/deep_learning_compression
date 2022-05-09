from pathlib import Path


class CompressStorage(object):
    def __init__(self, path="./tmp/compressed_datasets"):

        if not isinstance(path, Path):
            path = Path(path)

        self.__ensure_exists(path)

        self.path: Path = path

    def __ensure_exists(self, path):

        path.mkdir(exist_ok=True, parents=True)

    def CreateAndPrepareCompressedPathDL(self, dataSetName, modelName, filePath: Path):

        currPath = self.path / dataSetName / modelName / "compressed"

        self.__ensure_exists(currPath)

        currPath = currPath / Path(filePath).stem
        currPath = currPath.with_suffix(".tfci")
        return currPath

    def CreateAndPrepareDecompressedPathDL(self, dataSetName, modelName, filePath):

        currPath = self.path / dataSetName / modelName / "decompressed"

        self.__ensure_exists(currPath)

        currPath = currPath / Path(filePath).stem
        currPath = currPath.with_suffix(".png")
        return currPath

    def CreateAndPrepareCompressedPathConventional(
        self, dataSetName, DLmodelName, methodName, filePath: Path
    ):

        currPath = self.path / dataSetName / DLmodelName / "compressed" / methodName

        self.__ensure_exists(currPath)

        currPath = currPath / Path(filePath).stem
        currPath = currPath.with_suffix(".compress")

        return currPath

    def CreateAndPrepareDeCompressedPathConventional(
        self, dataSetName, DLmodelName, methodName, filePath: Path
    ):

        currPath = self.path / dataSetName / DLmodelName / "decompressed" / methodName

        self.__ensure_exists(currPath)

        currPath = currPath / Path(filePath).stem
        currPath = currPath.with_suffix(".decompress")
        return currPath
