# deep_learning_compression

Folder with additional information: [GoogleDrive](https://drive.google.com/drive/folders/169hvlZwRuLNFSC1VJuDmnXZuatHHbEax?usp=sharing)



## Installation

One should consider the usage of an virtual environment. Please see [Creating virtual environments](https://docs.python.org/3/library/venv.html#creating-virtual-environments) for more information.


 To install the dependencies run:

```bash
$ python -m pip install -r requirements.txt
```

For Development purposes, one should also install the project locally with:
```bash
$ python -m pip install -e .
```

## Image Quality Metrics
We use full- and no-reference image quality metrics to assess the quality of the used compression techniques.

### Full-Reference Metrics

MSE - Mean Squared Error  
PSNR - Peak Signal-To-Noise Ratio  
MSSIM - Multi-scale Structural Similarity

Use `./image_metrics/calculate_metrics.py` for evaluation.
The program can handle a pair of images consisting of an uncompressed vs an compressed image.
```bash
$ python calculate_metrics.py birb.jpg  birb_compressed.jpg
using two images for comparison
Reference image vs compressed image: mse: 1.46 | psnr: 46.49 | mssim: 0.98
```
Furthermore, two folders, consisting of either compressed and uncompressed images can be compared and their results averaged.
```bash
$ python calculate_metrics.py reference_images/ compressed_images/
using two directories with images for comparison
processed 1 file pair/s
References image vs compressed images: avg_mse: 1.46 | avg_psnr: 46.49 | avg_mssim: 0.98
```



### No-Reference Metrics

BRISQUE - Blind/Referenceless Image Spatial Quality Evaluator  
NIQE - Natural Image Quality Evaluator  
PIQE - Perception-based Image Quality Evaluator  

For those metrics, we use the [NRVQA](https://github.com/buyizhiyou/NRVQA]) repo.

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






