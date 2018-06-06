#!/usr/bin/env python

# This script has functions that can be used to load a particular pickle file

import pickle
import numpy


def load_all(image_pkl, 
             pad_images=True,
             length_cutoff=30,
             padding_length=80,
             script_name=None):

    '''load all data from repository, ignoring extensions, etc.
       Images that are under 2 lines will be filtered out,
       those between 2 and 80 will have padding added.

       Parameters
       ==========
       image_pkl: full path to the image pickle to load
       pad_images: if True, run add_padding function based on padding params
       length_cutoff: images with fewer than length_cutoff lines discarded
       padding_length: add padding so length == this value (# lines)
       script_name: if defined, load only scripts with this name included.

    '''

    images = pickle.load(open(image_pkl,"rb"))

    # Create a final list of images
    final = []

    for filename,subset in images.items():

        # Skip script if doesn't match name, if user wants this
        if script_name is not None:
            if script_name.lower() not in filename:
                continue

        # Are we adding padding / filtering?
        if pad_images is True:
            subset = add_padding(subset, length_cutoff, padding_length)
        final.append(subset)

    return final


def load_by_extension(image_pkl, 
                      pad_images=True,
                      length_cutoff=30,
                      padding_length=80):

    '''load data based on file extensions. The single pickle provided
       for a repository will be returned with a vector of extensions
       matching it. Images that are under 2 lines will be filtered out,
       those between 2 and 80 will have padding added.

       Parameters
       ==========
       image_pkl: full path to the image pickle to load
       pad_images: if True, run add_padding function based on padding params
       length_cutoff: images with fewer than length_cutoff lines discarded
       padding_length: add padding so length == this value (# lines)

    '''

    images = pickle.load(open(image_pkl,"rb"))

    # Create a dictionary lookup
    lookup = dict()

    for filename,subset in images.items():

        # Are we adding padding / filtering?
        if pad_images is True:
            subset = add_padding(subset, length_cutoff, padding_length)

        ext = filename.split('/')[-1].split('.')[-1]
        if ext in lookup:
            lookup[ext].append(subset)
        else:
            lookup[ext] = [subset]  

    return lookup


def add_padding(images, 
                length_cutoff=30, 
                padding_length=80):

    '''Add padding to an images array.

       Parameters
       ==========
       images: an NxN array of images
       length_cutoff: images with fewer than length_cutoff lines discarded
       padding_length: add padding so length == this value (# lines)

    '''
    padded = []

    # iterate through the list of 80x80 images
    for idx in range(len(images)):
        current = images[idx]
        updated = []

        # Only consider if greater than the length cutoff
        if current.shape[0] > length_cutoff:

            # Image needs padding, pad and append
            if current.shape[0] < padding_length:
                updated.append(pad_image(current))

            # Doesn't need padding, just append
            else:
                updated.append(current)

        # Only add to the padded list if we had any matching
        if len(updated) > 0:
            padded.append(updated)
 
    return padded


def pad_image(image, size=(80,80), const=32):
    '''Pad an array to a certain size with constant value (ordinal value of 32
       corresponds to a space).

       Parameters
       ==========
       image: an NxM numpy array
       size: a tuple of dimensions for the image
       const: the constant value to use for the padding (ordinal 32 is space)

    '''
    # check for equivalent dimensions (2)
    assert len(size) == len(image.shape)

    # Check that each dimension is within upper boundary
    for i in range(len(size)):
        assert image.shape[i] <= size[i]
        
    padded = numpy.ones(size) * const
    padded[:image.shape[0], :image.shape[1]] = image
    return padded
