# deep_learning_compression

Folder with additional information: [GoogleDrive](https://drive.google.com/drive/folders/169hvlZwRuLNFSC1VJuDmnXZuatHHbEax?usp=sharing)


## Howto

The main part of this project is the evaluation of the compression methods. The evaluation is located in a jupyter notebook in `./Notebooks/Evaluation.ipynb`. To generate the data needed for this you have to run some scripts in the following order:

```bash

$ python ./Scripts/PrepareData.py
$ python ./Scripts/ResizeImagesInDataset.py
$ python ./Scripts/RunCompression.py
$ python ./Scripts/RunMetricEvaluation.py

``` 

The creates a file `./tmp/last_run_metrics.csv` that needs to be imported into the evaluation jupyter notebook.


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
## Image Quality Metrics
We use full- and no-reference image quality metrics to assess the quality of the used compression techniques.

### Full-Reference Metrics

Mean Squared Error (MSE)
Root Mean Sqaured Error (RMSE)
Peak Signal-to-Noise Ratio (PSNR)
Structural Similarity Index (SSIM)
Universal Quality Image Index (UQI)
Multi-scale Structural Similarity Index (MS-SSIM)
Erreur Relative Globale Adimensionnelle de Synthèse (ERGAS)
Spatial Correlation Coefficient (SCC)
Relative Average Spectral Error (RASE)
Spectral Angle Mapper (SAM)
Spectral Distortion Index (D_lambda)
Spatial Distortion Index (D_S)
Quality with No Reference (QNR)
Visual Information Fidelity (VIF)
Block Sensitive - Peak Signal-to-Noise Ratio (PSNR-B)

### No-Reference Metrics

Blind/Referenceless Image Spatial Quality Evaluator (BRISQUE)
Natural Image Quality Evaluator (NIQE)
Perception-based Image Quality Evaluator (PIQE)

For those metrics, we use the [NRVQA](https://github.com/buyizhiyou/NRVQA]) repo.


Use `./image_metrics/calculate_metrics.py` to calculate metrics.
The program can handle a pair of images consisting of an uncompressed vs an compressed image.
```bash
$ python calculate_metrics.py birb.jpg  birb_compressed.jpg
using two images for comparison
```
Furthermore, two folders, consisting of either compressed and uncompressed images can be compared and their results averaged.
```bash
$ python calculate_metrics.py reference_images/ compressed_images/
using two directories with images for comparison
```

The output is a CSV file:
```bash
csv.out
```

With the following formatting:

|image_name|rmse|psnr|rmse_sw|uqi|ssim|ergas|scc|rase|sam|msssim|vifp|psnrb|niqe|brisque|
|-----|----|----|-------|---|----|-----|---|----|---|------|----|-----|----|-------|
|0.0|0.0|0.0|0.0|0.0|0.0|0.0|0.0|0.0|0.0|0.0|0.0|0.0|0.0|0.0|
