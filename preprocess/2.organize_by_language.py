#!/bin/env python

import matplotlib.pylab as plt
import pickle
import sys
import numpy

# Let's generate a structure of image files that organize script snippets based
# on language, to help others do machine learning.

extensions = ["txt","js","py","json","java","csv","html","xml","cpp","map",
               "c","m","css","dat","f90","cc","go","md","R","cxx","cs","h"]


################################################################################

# Step 0: Reorganize data

from helpers.load import ( recursive_find, load_all, load_by_extension )
import cv2
import os

data_base = '/tmp/data'
data_reorg_base = '/tmp/data1'
data_reorg = '%s/data' %data_reorg_base

if not os.path.exists(data_reorg):
    os.mkdir(data_reorg)

# Create output directories
for ext in extensions:
    outdir = os.path.join(data_reorg, ext.lower())
    if not os.path.exists(outdir):
        os.mkdir(outdir)

count = 0
for image_pkl in recursive_find(data_base, 'images_*.pkl'):

    # Save images to folder based on extension
    try:
        images = load_by_extension(image_pkl)
    except:
         count+=1
         print('Error loading %s!' %image_pkl)
         continue

    # We will save images based on zenodo id
    zenodo_id = image_pkl.split('_')[-1].replace('.pkl', '')

    print('Processing count %s, %s' %(count, zenodo_id))

    # If we are including the extension, save it
    for ext, imageset in images.items():
        if ext.lower() in extensions:
            # Put zenodo id in subfolder, so it's somewhat manageable
            image_base = os.path.join(data_reorg, ext.lower(), zenodo_id)
            if not os.path.exists(image_base):
                os.mkdir(image_base)
            # Using cv2 seemed to be a good way to save a single channel image,
            # and retain the original values
            for i in range(len(imageset)):
                image = imageset[i]
                #if image.shape != (80,80):
                #    print(image.shape)
                image_path = "%s/%s_%s.png" %(image_base, zenodo_id, i)
                cv2.imwrite(image_path, image)

    count+=1


# Step 1. Create archives (see 2.create_archives.sh)

# This is to provide data to Kaggle
here = os.getcwd()
os.chdir(data_reorg)
if not os.path.exists('ARCHIVE'):
    os.mkdir('ARCHIVE')

os.system('/bin/bash %s/2.create_archives.sh' % here)
