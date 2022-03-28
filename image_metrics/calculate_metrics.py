"""
Image Metrics - Application of Full-Reference and No-Reference Image Metrics
Credits of no-reference metrics: https://github.com/buyizhiyou/NRVQA
"""

import argparse
import os
import sys
import pandas as pd
import cv2
from joblib import load
import sewar.full_ref as full_ref
from no_ref import brisque, niqe, piqe

# Parse input arguments - either you compare two images or you compare two folders each with images
# Compare reference image vs compressed image
parser = argparse.ArgumentParser(description='Calculate Quality Metrics of Images.')
parser.add_argument('reference', help='specify single reference image or directory')
parser.add_argument('compressed', help='specify single compressed image or directory')
args = parser.parse_args()

# save the two paths - either 2 files or 2 folders
reference_path = args.reference
compressed_path = args.compressed

# Are we comparing two images or two folders with images
use_dirs = os.path.isdir(reference_path) and os.path.isdir(compressed_path)
use_files = not os.path.isdir(reference_path) and not os.path.isdir(compressed_path)

# check if the user specifies two folders or two files
if use_dirs:
    print('using two directories with images for comparison')
elif use_files:
    print('using two images for comparison')
else:
    print('cannot compare single image with folder of images')
    sys.exit()

# create a dataframe for later storage as csv
df = pd.DataFrame(columns=['image','rmse', 'psnr', 'rmse_sw', 'uqi',
                           'ssim', 'ergas', 'scc', 'rase', 'sam',
                           'msssim', 'vifp', 'psnrb', 'piqe', 'niqe', 'brisque'])

# Average Full-Reference metrics in case we compare 2 folders with images

# compare 2 images
if use_files:
    # read images
    reference_img = cv2.imread(reference_path)
    compressed_img = cv2.imread(compressed_path)

    # Full Reference Metrics
    mse =  full_ref.mse(reference_img, compressed_img)           # Mean Squared Error (MSE)
    rmse = full_ref.rmse(reference_img, compressed_img)         # Root Mean Sqaured Error (RMSE)
    psnr = full_ref.psnr(reference_img, compressed_img)         # Peak Signal-to-Noise Ratio (PSNR)
    rmse_sw = full_ref.rmse_sw(reference_img, compressed_img)   # Structural Similarity Index (SSIM)
    uqi = full_ref.uqi(reference_img, compressed_img)           # Universal Quality Image Index (UQI)
    ssim = full_ref.ssim(reference_img, compressed_img)         # Multi-scale Structural Similarity Index (MS-SSIM)
    ergas = full_ref.ergas(reference_img, compressed_img)       # Erreur Relative Globale Adimensionnelle de Synthèse (ERGAS)
    scc = full_ref.scc(reference_img, compressed_img)           # Spatial Correlation Coefficient (SCC)
    rase = full_ref.rase(reference_img, compressed_img)         # Relative Average Spectral Error (RASE)
    sam = full_ref.sam(reference_img, compressed_img)           # Spectral Angle Mapper (SAM)
    msssim = full_ref.msssim(reference_img, compressed_img)     # Structural Similarity Index (SSIM)
    vifp = full_ref.vifp(reference_img, compressed_img)         # Visual Information Fidelity (VIF)
    psnrb = full_ref.psnrb(reference_img, compressed_img)       # Block Sensitive - Peak Signal-to-Noise Ratio (PSNR-B)

    # No Reference Metrics
    piqe_score, _, _, _ = piqe.piqe(compressed_img)     # Perception-based Image Quality Evaluator (PIQE)
    niqe_score = niqe.niqe(compressed_img)              # Natural Image Quality Evaluator (NIQE)
    #feature = brisque.brisque(compressed_img)           # Blind/Referenceless Image Spatial Quality Evaluator (BRISQUE)
    #feature = feature.reshape(1, -1)
    #clf = load('./no_ref/svr_brisque.joblib')
    brisque_score = 0.0 # clf.predict(feature)[0]

    new_row = {'image': reference_path,
               'mse': mse,
               'rmse': rmse,
               'psnr': psnr,
               'rmse_sw': rmse_sw[0],
               'uqi': uqi,
               'ssim': ssim,
               'ergas': ergas,
               'scc': scc,
               'rase': rase,
               'sam': sam,
               'msssim': msssim,
               'vifp': vifp,
               'psnrb': psnrb,
               'piqe': piqe_score,
               'niqe': niqe_score,
               'brisque': brisque_score
               }

    df = df.append(new_row, ignore_index=True)

# compare 2 directories with images and take the mean value
elif use_dirs:

    files = os.listdir(reference_path)
    # iterate over N files in reference - if #images in folder compressed is >N the remaining images are ignored

    for file in files:
        reference_img = cv2.imread(os.path.join(reference_path, file))
        compressed_img = cv2.imread(os.path.join(compressed_path, file[:len(file) - 4] + "_compressed.jpg"))

    # Full Reference Metrics
    mse = full_ref.mse(reference_img, compressed_img)           # Mean Squared Error (MSE)
    rmse = full_ref.rmse(reference_img, compressed_img)         # Root Mean Sqaured Error (RMSE)
    psnr = full_ref.psnr(reference_img, compressed_img)         # Peak Signal-to-Noise Ratio (PSNR)
    rmse_sw = full_ref.rmse_sw(reference_img, compressed_img)   # Structural Similarity Index (SSIM)
    uqi = full_ref.uqi(reference_img, compressed_img)           # Universal Quality Image Index (UQI)
    ssim = full_ref.ssim(reference_img, compressed_img)         # Multi-scale Structural Similarity Index (MS-SSIM)
    ergas = full_ref.ergas(reference_img, compressed_img)       # Erreur Relative Globale Adimensionnelle de Synthèse (ERGAS)
    scc = full_ref.scc(reference_img, compressed_img)           # Spatial Correlation Coefficient (SCC)
    rase = full_ref.rase(reference_img, compressed_img)         # Relative Average Spectral Error (RASE)
    sam = full_ref.sam(reference_img, compressed_img)           # Spectral Angle Mapper (SAM)
    msssim = full_ref.msssim(reference_img, compressed_img)     # Structural Similarity Index (SSIM)
    vifp = full_ref.vifp(reference_img, compressed_img)         # Visual Information Fidelity (VIF)
    psnrb = full_ref.psnrb(reference_img, compressed_img)       # Block Sensitive - Peak Signal-to-Noise Ratio (PSNR-B)

    # No Reference Metrics
    piqe_score, _, _, _ = piqe.piqe(compressed_img)     # Perception-based Image Quality Evaluator (PIQE)
    niqe_score = niqe.niqe(compressed_img)              # Natural Image Quality Evaluator (NIQE)
    #feature = brisque.brisque(compressed_img)           # Blind/Referenceless Image Spatial Quality Evaluator (BRISQUE)
    #feature = feature.reshape(1, -1)
    #clf = load('./no_ref/svr_brisque.joblib')
    brisque_score = 0.0 # clf.predict(feature)[0]

    new_row = {'image': reference_path,
               'mse': mse,
               'rmse': rmse,
               'psnr': psnr,
               'rmse_sw': rmse_sw[0],
               'uqi': uqi,
               'ssim': ssim,
               'ergas': ergas,
               'scc': scc,
               'rase': rase,
               'sam': sam,
               'msssim': msssim,
               'vifp': vifp,
               'psnrb': psnrb,
               'piqe': piqe_score,
               'niqe': niqe_score,
               'brisque': brisque_score
               }

    df = df.append(new_row, ignore_index=True)


df.to_csv("out.csv", index=False, sep=";")