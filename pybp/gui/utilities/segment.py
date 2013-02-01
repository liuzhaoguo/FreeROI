# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import numpy as np
import scipy.ndimage as ndimage
import skimage.morphology as skmorph


def distance_transformation(data):
    dist = ndimage.distance_transform_edt(data)
    return -dist

def gradient_transformation(data):
    gx = ndimage.sobel(data, 0)
    gy = ndimage.sobel(data, 1)
    gz = ndimage.sobel(data, 2)
    grad = np.sqrt(gx**2 + gy**2 + gz**2)
    return grad

def inverse_transformation(data):
    return -data

def watershed(data, sigma, thresh, seeds=None, sfx=inverse_transformation):
    thresh = thresh > 0 and thresh
    if thresh == 0:
        mask = data > thresh 
    else:
        mask = data >= thresh
    data = ndimage.gaussian_filter(data, sigma)
    if seeds is None:
        # using unmasked data to get local maximum
        seeds = skmorph.is_local_maximum(data)
    # mask out those smaller than threshold
    seeds[~mask] = 0

    se = ndimage.generate_binary_structure(3, 3)
    markers = ndimage.label(seeds, se)[0]
    if sfx == distance_transformation:
        seg_input = sfx(mask)
    else:
        seg_input = sfx(data)
    result = skmorph.watershed(seg_input, markers, mask=mask)
    return markers, seg_input, result
