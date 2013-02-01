"""Segmentation module

Author: Yangzetian@BUAA 
"""

import numpy as np
import scipy.ndimage as ndimage
import skimage.morphology as skmorph
from skimage.filter import threshold_otsu
from skimage.util import img_as_uint
#import pymorph
#import mahotas


def normalize(data):
    """Negative values are set to zeros"""
    data[data<0] = 0
    m = data.max()
    data *= 255/m
    return data

class Segmenter(object):
    def segment(self):
        raise NotImplementedError('segment')


class Watersheder(Segmenter):
    def segment(self, *args, **kargs):
        return self.watershed(*args, **kargs)     # what a hard bug to find!

    def watershed(self):
        raise NotImplementedError('watershed')

class Watersheder_Scipy(Watersheder):
    def watershed(self, data, markers):
        data = normaliza(data)
        result = ndimage.watershed_ift(data.astype(np.uint8), markers)
        return result
        
class Watersheder_Scikit(Watersheder):
    def watershed(self, data, thr=None, 
                  dist_filter=False, sigma=3, reg_max=False):

        """Referenced from the Scikits watershed example"""
        if thr is None:
            thr = threshold_otsu(data)
        print "otsu threshold:", thr
        data = data > thr
        dist = ndimage.distance_transform_edt(data)
        if dist_filter:
            dist = ndimage.gaussian_filter(dist, sigma)
        if reg_max:
            seeds = pymorph.regmax(img_as_uint(dist))
        else:
            seeds = skmorph.is_local_maximum(dist, data, 
                            ndimage.generate_binary_structure(3, 3))
        markers = ndimage.label(seeds)[0]
        labels = skmorph.watershed(-dist, markers, mask=data)
        return labels

class Watersheder_Scikit_Invimage(Watersheder):
    def watershed(self, data, thr=None,
                  inv_filter=False, sigma=3):
        if thr is None:
            thr = 0.1
        data[data <= thr] = 0
        data_mask = data > thr
        if inv_filter:
            data = ndimage.gaussian_filter(data, sigma)
        seeds = skmorph.is_local_maximum(data, data_mask, 
                        ndimage.generate_binary_structure(3,3))
        markers = ndimage.label(seeds)[0]
        labels = skmorph.watershed(-data, markers, data_mask)
        return labels

class Watersheder_Scikit_Gradimage(Watersheder):
    def watershed(self, data, thr=None,
                  grad_filter=False, sigma=3):
        pass

class Watersheder_Pymorph(Watersheder):
    def watershed(self, data, thr=None):
        """Referenced from pythonvision.org/basic-tutorial"""
        if thr is None:
            thr = mahotas.thresholding.otsu(data)
        rmax = pymorph.regmax(data)
        seeds = ndimage.label(rmax)[0]
        dist = ndimage.distance_transform_edt(data > thr)
        dist = dist.max() - dist
        dist -= dist.min()
        dist = dist/float(dist.ptp()) * 255
        dist = dist.astype(np.uint8)
        result = mahotas.cwatershed(dist, seeds)
        return result

def sk_watershed_dist(data, thr=None, 
                      dist_filter=False, sigma=3, reg_max=False):
    if thr is None:
        thr = 0.1
    data = data > thr
    dist = ndimage.distance_transform_edt(data)
    if dist_filter:
        dist = ndimage.gaussian_filter(dist, sigma)
    if reg_max:
        seeds = pymorph.regmax(img_as_uint(dist))
    else:
        seeds = skmorph.is_local_maximum(dist, data, 
                        ndimage.generate_binary_structure(3, 3))
    markers = ndimage.label(seeds)[0]
    labels = skmorph.watershed(-dist, markers, mask=data)
    return labels, markers, -dist
    
def sk_watershed_invimage(data, thr=None,
                          inv_filter=False, sigma=3):
    if thr is None:
        thr = 0.1
    data[data <= thr] = 0
    data_mask = data > thr
    if inv_filter:
        data = ndimage.gaussian_filter(data, sigma)
    seeds = skmorph.is_local_maximum(data, data_mask, 
                    ndimage.generate_binary_structure(3,3))
    markers = ndimage.label(seeds)[0]
    labels = skmorph.watershed(-data, markers, data_mask)
    return labels, markers, -data

def scipy_watershed(data, markers):
    data = normalize(data)
    result = ndimage.watershed_ift(data.astype(np.uint8), markers)
    return result

def scikit_watershed(data, thr=None):
    """Referenced from the Scikits watershed example"""
    if thr is None:
        thr = threshold_otsu(data)
    data = data > thr
    dist = ndimage.distance_transform_edt(data)
    local_max = skmorph.is_local_maximum(dist, data, 
                                 ndimage.generate_binary_structure(3, 3))
    markers = ndimage.label(local_max)[0]
    labels = skmorph.watershed(-dist, markers, mask=data)
    return labels

def pymorph_watershed(data, thr=None):
    """Referenced from pythonvision.org/basic-tutorial"""
    if thr is None:
        thr = mahotas.thresholding.otsu(data)
    rmax = pymorph.regmax(data)
    seeds = ndimage.label(rmax)[0]
    dist = ndimage.distance_transform_edt(data > thr)
    dist = dist.max() - dist
    dist -= dist.min()
    dist = dist/float(dist.ptp()) * 255
    dist = dist.astype(np.uint8)
    result = mahotas.cwatershed(dist, seeds)
    return result
