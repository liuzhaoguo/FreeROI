# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import numpy as np
from scipy import ndimage as nd
from scipy.ndimage import morphology
from skimage import feature as skft
from skimage import morphology as skmorph

def mesh_3d_grid(x, y, z):
    x = np.asarray(x)
    y = np.asarray(y)
    z = np.asarray(z)
    row, col, hei = len(y), len(x), len(z)
    x = x.reshape(1, 1, col)
    y = y.reshape(1, row, 1)
    z = z.reshape(hei, 1, 1)
    X = x.repeat(row, 1)
    X = X.repeat(hei, 0)
    Y = y.repeat(col, 2)
    Y = y.repeat(hei, 0)
    Z = z.repeat(row, 1)
    Z = Z.repeat(col, 2)
    return X, Y, Z

def ball(radius, dtype=np.uint8):
    """Generate a ball structure element"""
    L = np.linspace(-radius, radius, 2*radius+1)
    X, Y, Z = mesh_3d_grid(L, L, L)
    s = X**2 + Y**2 + Z**2
    return np.array(s <= radius * radius, dtype=dtype)

def opening(src, r=2):
    se = ball(r)
    result = nd.grey_opening(src, footprint=se)
    return result

def local_maximum(data, dist=1):
    lmax = np.zeros(data.shape)
    p = skft.peak_local_max(data, dist).T
    p = (np.array(p[0]), np.array(p[1]), np.array(p[2]))
    lmax[p] = 1
    return lmax

def roi_filtering(src, ref):
    mask = ref > 0
    all_roi = np.unique(src[mask])
    result = np.zeros(src.shape)
    for roi in all_roi:
        result[src==roi] = roi
    return result

def sphere_roi(data, x, y, z, radius, value):
    """
    Generate a sphere roi which center in (x, y, z).

    """
    for n_x in range(x - radius, x + radius + 1):
        for n_y in range(y - radius, y + radius + 1):
            for n_z in range(z - radius, z + radius + 1):
                if n_x < 0:
                    n_x = data.shape[0] - n_x
                if n_y < 0:
                    n_y = data.shape[1] - n_y
                if n_z < 0:
                    n_z = data.shape[2] - n_z
                n_coord = np.array((n_x, n_y, n_z))
                coord = np.array((x, y, z))
                if np.linalg.norm(coord - n_coord) <= radius:
                    data[n_x, n_y, n_z] = value
    return data

def cube_roi(data, x, y, z, radius, value):
    """
    Generate a cube roi which center in (x, y, z).

    """
    for n_x in range(x - radius, x + radius + 1):
        for n_y in range(y - radius, y + radius + 1):
            for n_z in range(z - radius, z + radius + 1):
                if n_x >= 0 and n_y >= 0 and n_z >= 0:
                    data[n_x, n_y, n_z] = value
    return data

def nonzero_coord(data):
    """
    Return all non-zero voxels' coordinate.

    """
    x, y, z = np.nonzero(data)
    coord_list = zip(x, y, z)
    value_list = [data[coord] for coord in coord_list]
    return coord_list, value_list

def binaryzation(data,threshold):
    return (data > threshold).astype(int)

def multi_label_edge_detection(data):
    f = nd.generate_binary_structure(len(data.shape), 1)
    # the unwanted thick bounds
    bound = (nd.grey_erosion(data,footprint=f) != \
             nd.grey_dilation(data,footprint=f)) - \
            (nd.binary_dilation(data.astype(np.bool)) - data.astype(np.bool))
    data=bound.astype(data.dtype)
    return data

def inverse_transformation(data):
    """
    Return a inverted image.
    """
    return -data

def cluster_labeling(data, threshold, conn=1):
    """
    Label different clusters in an image.

    """
    temp = data.copy()
    temp[temp <= threshold] = 0
    temp[temp > threshold] = 1
    structure = nd.generate_binary_structure(3, conn)
    labeled_array, num_features = nd.label(temp, structure)
    return labeled_array

def gaussian_smoothing(data, sigma):
    """
    Gaussian smoothing.

    """
    data = nd.gaussian_filter(data, sigma)
    return data

