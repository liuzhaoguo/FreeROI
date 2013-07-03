# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import numpy as np
import scipy.ndimage as ndimage
import scipy.spatial.distance as distance

def intersect(source, mask):
    """
    An intersection action, return a new numpy array. New array will preserve
    the source data value, and mask data will be binaried as a `mask`.

    """
    # binary mask data
    mask[mask > 0] = 1
    temp = source * mask
    temp = np.rot90(temp, 3)
    return temp

def merge(a, b):
    a_mask = a > 0
    b_mask = b > 0
    if len((a_mask & b_mask).nonzero()[0]) > 0:
        raise ValueError, 'Conflicts!'
    c = a + b
    return c

def region_grow(seed, source, labeling=False):
    temp = source.copy()
    labels, n_labels = ndimage.label(seed)
    mask = source > 0
    labels[~mask] = 0
    dilation = ndimage.binary_dilation(labels, iterations=0, mask=mask)
    temp[~dilation] = 0
    if labeling:
        temp = nearest_labeling(seed, temp)
    return temp

def nearest_labeling(src, tar):
    """
    For each temp voxel assigns the value of it's closest seed voxel
    
    """
    srcn = src.nonzero()
    tarn = tar.nonzero()
    srcn_coord = np.column_stack((srcn[0], srcn[1], srcn[2]))
    tarn_coord = np.column_stack((tarn[0], tarn[1], tarn[2]))
    dist = distance.cdist(srcn_coord, tarn_coord)
    min_pos = np.argmin(dist, 0)
    tar[tarn] = src[srcn][min_pos]
    return tar

def cluster_labeling(src, conn=1):
    """
    Label different clusters in a image.
    """
    temp = src.copy()
    temp = temp[temp>=0]
    structure = ndimage.generate_binary_structure(3,conn)
    labeled_array, num_features = label(temp, structure)
    return labeled_array
