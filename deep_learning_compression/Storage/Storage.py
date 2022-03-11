import logging
from dataclasses import dataclass
from pathlib import Path
from tokenize import Name
from typing import List

from deep_learning_compression.Storage.StorageDataSet import StorageDataSet

logging.basicConfig(level=logging.INFO)


@dataclass
class DataSetInfo:
    Name: str
    Url: str
    NrImages: int


@dataclass
class ImageInfo:

    Filepath: Path


class Storage:
    def __init__(self):
        pass

    def _getAllDatasets(self):
        """Get Pointers to all datasets. They are not instantiated.

        This searches for all classes that are subclass to 'StorageDataSet'.
        They need to be imported somewhere! Be careful - this attempt to make plugins
        is therefore limited!

        """
        # All subclasses of StorageDataset Contain Datset implementations
        a = StorageDataSet.__subclasses__()

        return a

    def DownloadAndPrepareAllDatasets(self):
        """Download and prepare all datasets."""

        allSets = self._getAllDatasets()

        logging.info(f"Found total {len(allSets)} datasets that will be downloaded.")

        for set in allSets:

            setInstance = set()  # make instance
            setInstance.prepareDataForUsage()

    def GetAllDataSetInformation(self) -> List[DataSetInfo]:
        """Get Information about all available datasets."""
        a = self._getAllDatasets()

        ret = []
        for i in a:
            d = DataSetInfo(Name=i.NAME, Url=i.URL, NrImages=0)
            ret.append(d)

        return ret

    def GetAllFileInformationOfASingleDataSet(self, setName: str) -> List[ImageInfo]:

        allSets = self._getAllDatasets()

        foundSet = None
        foundSets = [s for s in allSets if s.NAME == setName]

        if len(foundSets) == 0 or len(foundSets) > 1:
            raise Exception(f"The dataset {setName} was not found.")
        else:
            foundSet = foundSets[0]()  # make instance

        return [ImageInfo(Filepath=a) for a in foundSet.get_all_filepaths()]
