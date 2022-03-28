import logging
import zipfile
from abc import abstractmethod
from pathlib import Path
from typing import List

import requests

logging.basicConfig(level=logging.INFO)


class StorageDataSet:

    STORAGE_PATH = Path("./datasets")
    NAME = ""

    def _IsPrepared(self) -> int:

        p = self.GetStoragePath()

        if p.exists():
            return 0

        else:
            return 1

    def _IsDownloaded(self) -> int:

        p = self.GetDownloadFilePath()

        if p.exists():
            return 0

        else:
            return 1

    def GetStoragePath(self):
        """Path to folder in datasets"""
        return self.STORAGE_PATH / self.NAME

    def GetDownloadFilePath(self):
        """Path to downloaded Zip file"""
        p = self.STORAGE_PATH / (self.NAME + ".zip")

        return p

    @abstractmethod
    def download_data(self):
        """Implement Method to download data from source."""

        pass

    @abstractmethod
    def get_all_filepaths(self) -> List[Path]:

        pass

    @abstractmethod
    def prepareDataForUsage(self):
        raise NotImplementedError


class ImageCompressionBenchmark8BitRGBDataSet(StorageDataSet):

    URL = "https://imagecompression.info/test_images/rgb8bit.zip"
    NAME = "ImageCompressionBenchmark8BitRGB"

    def download_data(self):

        p = self.GetDownloadFilePath()

        r = requests.get(self.URL, stream=True)

        with open(p, "wb") as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)

    def prepareDataForUsage(self):
        """Download data and prepare for usage in project."""

        # Check if already downloaded
        if self._IsDownloaded() == 1:
            logging.info(f"Start downloading data for dataset {self.NAME}")
            self.download_data()
        elif self._IsDownloaded() == 0:
            logging.info(f"Dataset {self.NAME} was already downloaded.")

        if self._IsPrepared() == 0:
            logging.info(f"Dataset {self.NAME} was already prepared!")
        elif self._IsPrepared() == 1:
            # Extract Data
            logging.info(f"Start extracting data of dataset {self.NAME}")
            f = zipfile.ZipFile(self.GetDownloadFilePath())
            f.extractall(self.GetStoragePath())

    def get_all_filepaths(self) -> List[Path]:
        return [p.absolute().as_posix() for p in self.GetStoragePath().glob("*.ppm")]


if __name__ == "__main__":

    s = ImageCompressionBenchmark8BitRGBDataSet()
    s.prepareDataForUsage()

    print(s.get_all_filepaths())
