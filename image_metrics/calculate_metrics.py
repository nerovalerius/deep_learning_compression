"""
Image Metrics - Application of Full-Reference and No-Reference Image Metrics
Credits of no-reference metrics: https://github.com/buyizhiyou/NRVQA
"""

import argparse
import os
import sys
import pandas as pd
import cv2
import torch
from piq import vsi, brisque
import sewar.full_ref as full_ref
from no_ref import niqe, piqe

# check cuda availability
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

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
df = pd.DataFrame(columns=['image', 'uqi', 'vifp', 'vsi', 'piqe', 'niqe', 'brisque'])

# Average Full-Reference metrics in case we compare 2 folders with images

# compare 2 images
if use_files:
    # read images
    reference_img = cv2.imread(reference_path)
    compressed_img = cv2.imread(compressed_path)

    # Full Reference Metrics
    vsi = vsi(torch.tensor(reference_img).to(device).permute(2, 0, 1)[None, ...] / 255.,
                           torch.tensor(compressed_img).to(device).permute(2, 0, 1)[None, ...] / 255.,
                           data_range=1.)                   # Visual Saliency-induced Index
    uqi = full_ref.uqi(reference_img, compressed_img)       # Universal Quality Image Index (UQI)
    vifp = full_ref.vifp(reference_img, compressed_img)     # Visual Information Fidelity (VIF)

    # No Reference Metrics
    piqe_score, _, _, _ = piqe.piqe(compressed_img)         # Perception-based Image Quality Evaluator (PIQE)
    niqe_score = niqe.niqe(compressed_img)                  # Natural Image Quality Evaluator (NIQE)
    brisque = brisque(torch.tensor(compressed_img).permute(2, 0, 1)[None, ...] / 255.,
                      data_range=1., reduction='none')      # Blind/Referenceless Image Spatial Quality Evaluator (BRISQUE)

    new_row = {'image': reference_path,
               'uqi': uqi,
               'vifp': vifp,
               'vsi': vsi.item(),
               'piqe': piqe_score,
               'niqe': niqe_score,
               'brisque': brisque.item()
               }
    print("finished image metrics for: " + str(compressed_path))
    df = df.append(new_row, ignore_index=True)

# compare 2 directories with images and take the mean value
elif use_dirs:

    files = os.listdir(reference_path)
    # iterate over N files in reference - if #images in folder compressed is >N the remaining images are ignored

    for file in files:

        reference_img = cv2.imread(os.path.join(reference_path, file))
        compressed_img = cv2.imread(os.path.join(compressed_path, file[:len(file) - 4] + "_compressed.jpg"))

        # Full Reference Metrics
        vsi = vsi(torch.tensor(reference_img).to(device).permute(2, 0, 1)[None, ...] / 255.,
                  torch.tensor(compressed_img).to(device).permute(2, 0, 1)[None, ...] / 255.,
                  data_range=1.)  # Visual Saliency-induced Index
        uqi = full_ref.uqi(reference_img, compressed_img)  # Universal Quality Image Index (UQI)
        vifp = full_ref.vifp(reference_img, compressed_img)  # Visual Information Fidelity (VIF)

        # No Reference Metrics
        piqe_score, _, _, _ = piqe.piqe(compressed_img)     # Perception-based Image Quality Evaluator (PIQE)
        niqe_score = niqe.niqe(compressed_img)              # Natural Image Quality Evaluator (NIQE)
        brisque = brisque(torch.tensor(compressed_img).permute(2, 0, 1)[None, ...] / 255.,
                      data_range=1., reduction='none')      # Blind/Referenceless Image Spatial Quality Evaluator (BRISQUE)

        new_row = {'image': reference_path,
                   'uqi': uqi,
                   'vifp': vifp,
                   'vsi': vsi.item(),
                   'piqe': piqe_score,
                   'niqe': niqe_score,
                   'brisque': brisque.item()
                   }
        print("finished image metrics for: " + str(file))
        df = df.append(new_row, ignore_index=True)


df.to_csv("out.csv", index=False, sep=";")