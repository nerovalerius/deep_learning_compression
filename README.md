# deep_learning_compression

Folder with additional information: [GoogleDrive](https://drive.google.com/drive/folders/169hvlZwRuLNFSC1VJuDmnXZuatHHbEax?usp=sharing)



## Installation

One should consider the usage of an virtual environment. Please see [Creating virtual environments](https://docs.python.org/3/library/venv.html#creating-virtual-environments) for more information.


 To install the dependencies run:

```bash
$ python -m pip install -r requirements.txt

$ git submodules init && git submodule update
```

For Development purposes, one should also install the project locally with:
```bash
$ python -m pip install -e .
```

The following dependencies are required to use Compression.py:
- nconvert - download, build and install from https://www.xnview.com/en/xnconvert/#downloads
- openjpeg - download an build and install from https://github.com/uclouvain/openjpeg/blob/master/INSTALL.md


## Datasets

To evaluate performance of the compression techniques, different datasets can be used. They will be located in the `./datasets` folder.

Available Datasets:
- ImageCompressionBenchmark8BitRGB

To make the data available locally, a script was created. This downloads all different datasets.

```bash
$ python Scripts/PrepareData.py

Found following datasets:
	- ImageCompressionBenchmark8BitRGB


INFO:root:Found total 1 datasets that will be downloaded.
INFO:root:Dataset ImageCompressionBenchmark8BitRGB was already downloaded.
INFO:root:Dataset ImageCompressionBenchmark8BitRGB was already prepared!

```

To use the data of a specific dataset, you can use the storage interface:

```python
from deep_learning_compression.Storage.Storage import Storage

s = Storage()  # Make an instance

s.GetAllFileInformationOfASingleDataSet(setName="ImageCompressionBenchmark8BitRGB")

```

## Compression

To run the compression over all methods, you can run following script.
(Currently, the values are hard coded, but this can easily be extended to make variable options!)


```bash
$ python ./Scripts/RunCompression.py

```



