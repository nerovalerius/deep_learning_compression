"""
Image Metrics - Application of Full-Reference and No-Reference Image Metrics
"""

import numpy as np
import argparse
import os
import sys
from skimage import io
from skimage.metrics import mean_squared_error, peak_signal_noise_ratio, structural_similarity

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

# Average Full-Reference metrics in case we compare 2 folders with images
avg_mse = 0
avg_psnr = 0
avg_mssim = 0

# compare 2 images
if use_files:
    # read images
    reference_img = io.imread(reference_path)
    compressed_img = io.imread(compressed_path)

    # Full Reference Metrics
    # The mean-squared error (MSE)
    mse = mean_squared_error(reference_img, compressed_img)
    # The peak signal to noise ratio (PSNR)
    psnr = peak_signal_noise_ratio(reference_img, compressed_img)
    # The mean structural similarity index
    mssim = structural_similarity(reference_img, compressed_img, channel_axis=2)

    print("Reference image vs compressed image: mse: %.2f | psnr: %.2f | mssim: %.2f" % (mse, psnr, mssim))

# compare 2 directories with images and take the mean value
elif use_dirs:

    files = os.listdir(reference_path)
    # iterate over N files in reference - if #images in folder compressed is >N the remaining images are ignored
    i = 1 # counter
    for f in files:
        reference_img = io.imread(os.path.join(reference_path, f))
        compressed_img = io.imread(os.path.join(compressed_path, f[:len(f) - 4] + "_compressed.jpg"))
        # The mean-squared error (MSE)
        mse = mean_squared_error(reference_img, compressed_img)
        # The peak signal to noise ratio (PSNR)
        psnr = peak_signal_noise_ratio(reference_img, compressed_img)
        # The mean structural similarity index
        mssim = structural_similarity(reference_img, compressed_img, channel_axis=2)

        # add up
        avg_mse += mse
        avg_psnr += psnr
        avg_mssim += mssim

    # divide by N to get mean
    avg_mse /= i
    avg_psnr /= i
    avg_mssim /= i

    print("processed %i file pair/s" % i)

    # raise counter
    i +=1

    print("References image vs compressed images: avg_mse: %.2f | avg_psnr: %.2f | avg_mssim: %.2f"
          % (avg_mse, avg_psnr, avg_mssim))

