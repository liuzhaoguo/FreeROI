# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""Some basic functions for image construction

"""

import sys as _sys
import numpy as _np
from PyQt4 import QtGui as _qt

from qimageview import qimageview as _qimageview

if _sys.byteorder == 'little':
    _bgra = (0, 1, 2, 3)
else:
    _bgra = (3, 2, 1, 0)

bgra_dtype = _np.dtype({'b': (_np.uint8, _bgra[0], 'blue'),
                        'g': (_np.uint8, _bgra[1], 'green'),
                        'r': (_np.uint8, _bgra[2], 'red'),
                        'a': (_np.uint8, _bgra[3], 'alpha')})

# Define a rainbow colormap
RAINBOW = {0: [0, 0, 0],
           1: [182, 147, 205],
           2: [185, 109, 81],
           3: [156, 87, 38],
           4: [161, 231, 187],
           5: [4, 69, 50],
           6: [209, 13, 113],
           7: [110, 244, 96],
           8: [127, 47, 199],
           9: [127, 77, 122],
           10: [204, 57, 49],
           11: [23, 41, 182],
           12: [155, 1, 125],
           13: [90, 193, 25],
           14: [44, 235, 71],
           15: [54, 246, 122],
           16: [6, 15, 164],
           17: [133, 222, 82],
           18: [22, 188, 214],
           19: [126, 118, 179],
           20: [198, 157, 251],
           21: [188, 133, 21],
           22: [107, 118, 42],
           23: [108, 157, 54],
           24: [114, 144, 142],
           25: [165, 61, 35],
           26: [94, 234, 131],
           27: [3, 62, 239],
           28: [183, 223, 13],
           29: [28, 211, 154],
           30: [240, 5, 103],
           31: [26, 211, 15],
           32: [97, 23, 49],
           33: [12, 165, 109],
           34: [230, 12, 162],
           35: [88, 246, 29],
           36: [157, 70, 248],
           37: [2, 232, 180],
           38: [119, 146, 34],
           39: [119, 69, 166],
           40: [248, 158, 111],
           41: [203, 58, 136],
           42: [117, 76, 214],
           43: [93, 29, 224],
           44: [86, 25, 85],
           45: [164, 222, 51],
           46: [231, 227, 17],
           47: [145, 180, 111],
           48: [121, 231, 98],
           49: [198, 112, 251],
           50: [230, 36, 125],
           51: [164, 203, 141],
           52: [249, 178, 175],
           53: [197, 58, 62],
           54: [252, 92, 24],
           55: [30, 74, 84],
           56: [237, 57, 9],
           57: [142, 215, 225],
           58: [110, 207, 125],
           59: [187, 12, 233],
           60: [245, 105, 109],
           61: [151, 58, 78],
           62: [16, 193, 171],
           63: [90, 157, 205],
           64: [139, 164, 142],
           65: [65, 249, 100],
           66: [3, 126, 141],
           67: [104, 19, 45],
           68: [51, 206, 148],
           69: [237, 132, 96],
           70: [207, 203, 216],
           71: [165, 209, 226],
           72: [69, 63, 244],
           73: [130, 156, 54],
           74: [199, 1, 153],
           75: [90, 107, 242],
           76: [216, 110, 37],
           77: [67, 31, 212],
           78: [62, 179, 98],
           79: [153, 126, 84],
           80: [243, 38, 227],
           81: [212, 113, 166],
           82: [138, 218, 56],
           83: [55, 136, 126],
           84: [117, 130, 43],
           85: [45, 118, 235],
           86: [244, 57, 81],
           87: [120, 218, 91],
           88: [142, 141, 118],
           89: [227, 227, 127],
           90: [80, 228, 112],
           91: [139, 37, 184],
           92: [30, 72, 84],
           93: [121, 250, 243],
           94: [126, 251, 202],
           95: [116, 10, 109],
           96: [222, 17, 158],
           97: [239, 114, 83],
           98: [28, 110, 58],
           99: [1, 222, 84],
           100: [76, 212, 193],
           101: [166, 20, 208],
           102: [32, 139, 45],
           103: [60, 137, 175],
           104: [217, 113, 137],
           105: [162, 129, 150],
           106: [93, 37, 82],
           107: [231, 216, 242],
           108: [233, 71, 20],
           109: [241, 177, 13],
           110: [72, 128, 224],
           111: [189, 85, 104],
           112: [225, 153, 151],
           113: [118, 41, 50],
           114: [196, 240, 37],
           115: [23, 24, 53],
           116: [241, 69, 56],
           117: [193, 112, 21],
           118: [48, 68, 185],
           119: [72, 23, 108],
           120: [144, 208, 83],
           121: [147, 208, 36],
           122: [222, 24, 246],
           123: [28, 5, 15],
           124: [144, 144, 89],
           125: [106, 121, 120],
           126: [84, 119, 29],
           127: [59, 249, 145],
           128: [163, 129, 48],
           129: [116, 94, 245],
           130: [223, 108, 39],
           131: [178, 38, 140],
           132: [150, 81, 32],
           133: [163, 87, 246],
           134: [109, 86, 157],
           135: [146, 50, 241],
           136: [115, 242, 109],
           137: [205, 13, 191],
           138: [235, 24, 99],
           139: [97, 11, 235],
           140: [75, 233, 7],
           141: [135, 232, 109],
           142: [206, 99, 84],
           143: [46, 226, 85],
           144: [130, 198, 162],
           145: [141, 212, 58],
           146: [115, 185, 128],
           147: [147, 211, 77],
           148: [18, 154, 251],
           149: [177, 57, 37],
           150: [75, 26, 107],
           151: [78, 78, 88],
           152: [200, 160, 166],
           153: [58, 220, 160],
           154: [116, 234, 100],
           155: [243, 174, 40],
           156: [132, 173, 248],
           157: [192, 152, 158],
           158: [141, 111, 50],
           159: [37, 87, 9],
           160: [136, 138, 117],
           161: [175, 172, 118],
           162: [16, 106, 197],
           163: [144, 106, 244],
           164: [66, 30, 22],
           165: [224, 198, 13],
           166: [85, 63, 150],
           167: [124, 166, 199],
           168: [234, 38, 237],
           169: [123, 83, 55],
           170: [241, 110, 86],
           171: [156, 230, 153],
           172: [230, 91, 235],
           173: [64, 197, 162],
           174: [20, 162, 153],
           175: [238, 153, 167],
           176: [133, 189, 43],
           177: [194, 202, 203],
           178: [55, 70, 97],
           179: [169, 87, 155],
           180: [232, 107, 68],
           181: [194, 134, 115],
           182: [112, 173, 62],
           183: [200, 14, 73],
           184: [125, 157, 217],
           185: [63, 15, 152],
           186: [166, 192, 215],
           187: [117, 71, 243],
           188: [121, 152, 21],
           189: [224, 21, 142],
           190: [19, 171, 237],
           191: [111, 168, 9],
           192: [30, 100, 78],
           193: [205, 217, 244],
           194: [83, 200, 1],
           195: [15, 35, 100],
           196: [92, 237, 136],
           197: [99, 108, 229],
           198: [107, 239, 69],
           199: [1, 148, 175],
           200: [148, 109, 59],
           201: [20, 80, 75],
           202: [192, 29, 79],
           203: [140, 64, 105],
           204: [65, 60, 98],
           205: [77, 245, 189],
           206: [174, 124, 38],
           207: [170, 245, 194],
           208: [97, 3, 234],
           209: [183, 10, 238],
           210: [29, 189, 220],
           211: [12, 72, 153],
           212: [188, 103, 191],
           213: [93, 50, 157],
           214: [207, 214, 234],
           215: [131, 24, 13],
           216: [158, 92, 2],
           217: [216, 234, 232],
           218: [203, 124, 97],
           219: [23, 11, 112],
           220: [196, 150, 227],
           221: [217, 2, 185]
           }

def gray(array, alpha):
    """
    Return a rgba array which color ranges from black to white.
    
    """
    h, w = array.shape
    new_array = _np.zeros((h, w, 4), dtype=_np.uint8)
    array[array<=0] = 0
    array[array>255] = 255
    new_array[..., 0] = array
    new_array[..., 1] = array
    new_array[..., 2] = array
    new_array[..., 3] = alpha * array.clip(0,1)
    
    return new_array

def red2yellow(array, alpha):
    """
    Return a rgba array which color ranges from red to yellow.
    
    """
    h, w = array.shape
    new_array = _np.zeros((h, w, 4), dtype=_np.uint8)
    array[array<=0] = 0
    array[array>255] = 255
    new_array[..., 0] = 255 * array.clip(0, 1)
    new_array[..., 1] = array
    new_array[..., 2] = 0
    new_array[..., 3] = alpha * array.clip(0, 1)
    
    return new_array

def blue2cyanblue(array, alpha):
    """
    Return a rgba array which color ranges from blue to cyanblue.
    
    """
    h, w = array.shape
    new_array = _np.zeros((h, w, 4), dtype=_np.uint8)
    array[array<=0] = 0
    array[array>255] = 255
    new_array[..., 0] = 0
    new_array[..., 1] = array
    new_array[..., 2] = 255 * array.clip(0, 1)
    new_array[..., 3] = alpha * array.clip(0, 1)

    return new_array

def red(array, alpha):
    """
    Return a whole red rgba array.
    
    """
    h, w = array.shape
    new_array = _np.zeros((h, w, 4), dtype=_np.uint8)
    new_array[..., 0] = 255 * array.clip(0, 1)
    new_array[..., 1] = 0
    new_array[..., 2] = 0
    new_array[..., 3] = alpha * array.clip(0, 1)
    
    return new_array

def green(array, alpha):
    """
    Return a whole green rgba array.
    
    """
    h, w = array.shape
    new_array = _np.zeros((h, w, 4), dtype=_np.uint8)
    new_array[..., 0] = 0
    new_array[..., 1] = 255 * array.clip(0, 1)
    new_array[..., 2] = 0
    new_array[..., 3] = alpha * array.clip(0, 1)

    return new_array

def blue(array, alpha):
    """
    Return a whole blue rgba array.
    
    """
    h, w = array.shape
    new_array = _np.zeros((h, w, 4), dtype=_np.uint8)
    new_array[..., 0] = 0
    new_array[..., 1] = 0
    new_array[..., 2] = 255 * array.clip(0, 1)
    new_array[..., 3] = alpha * array.clip(0, 1)
    
    return new_array

def single_roi(array, alpha, roi):
    """
    Return a single roi view array.

    """
    color = (70, 70, 70)
    h, w = array.shape
    new_array = _np.zeros((h, w, 4), dtype=_np.uint8)
    if roi is None or roi == 0:
        return new_array
    mask = array == roi
    new_array[mask, 0] = color[0]
    new_array[mask, 1] = color[1]
    new_array[mask, 2] = color[2]
    new_array[mask, 3] = alpha 
    return new_array

def _normalize255(array, normalize, scale_length=255.0):
    if not normalize:
        return array

    if normalize is True:
        normalize = array.min(), array.max()
    elif _np.isscalar(normalize):
        normalize = (0, normalize)
    elif isinstance(normalize, tuple) and (normalize[0] == normalize[1]):
        normalize = array.min(), array.max()
    nmin, nmax = normalize

    if nmin:
        array = array - nmin

    scale =  scale_length / (nmax - nmin)
    if scale != 1.0:
        array = array * scale

    return _np.round(array)

def gray2qimage(array, normalize=False):
    """Convert a 2D numpy array 'array' into a 8-bit, indexed QImage with
    a specific colormap. The first dimension represents the vertical image
    axis.

    The parameter 'normalize' can be used to normalize an image's value range
    to 0 ~ 255:

        normalize = (nmin, nmax):
         scale & clip image values from nmin..nmax to 0..255

        normalize = nmax:
         lets nmin default to zero, i.e. scale & clip the range 0..nmax to
         0..255

        normalize = True:
         scale image values to 0..255 (same as passing (array.min(), 
         array.max()))

    If the source array 'array' contains masked values, the result will have 
    only 255 shades of gray, and one color map entry will be used to make the
    corresponding pixels transparent.


    """
    if _np.ndim(array) != 2:
        raise ValueError("gray2qimage can only convert 2D arrays")

    h, w = array.shape
    result = _qt.QImage(w, h, _qt.QImage.Format_Indexed8)

    array = _normalize255(array, normalize)

    for i in range(256):
        result.setColor(i, _qt.qRgb(i, i, i))

    _qimageview(result)[:] = array.clip(0, 255)

    return result

def byte_view(qimage, byteorder = 'little'):
    raw = _qimageview(qimage)
    result = raw.view(_np.uint8).reshape(raw.shape + (-1, ))
    if byteorder and byteorder != _sys.byteorder:
        result = result[...,::-1]
    return result

def rgb_view(qimage, byteorder='big'):
    if byteorder is None:
        byteorder = _sys.byteorder
    bytes = byte_view(qimage, byteorder)
    if bytes.shape[2] != 4:
        raise ValueError, "For rgb_view, the image must have 32 bit pixel" + \
                " size (use RGB32, ARGB32, or ARGB32_Premultiplied)"

    if byteorder == 'little':
        return bytes[..., :3]
    else:
        return bytes[..., 1:]

def alpha_view(qimage):
    bytes = byte_view(qimage, byteorder = None)
    if bytes.shape[2] != 4:
        raise ValueError, "For alpha_view, the image must have 32 bit pixel" + \
                        " size (use RGB32, ARGB32, or ARGB32_Premultiplied)"
    return bytes[..., _bgra[3]]

def idx2rgb(value, colormap, normalize):
    """
    Convert a index to a RGB value based on the colormap.

    """
    if colormap != 'rainbow':
        if normalize[0] == normalize[1]:
            new_value = 0
        else:
            scale = 255. / (normalize[1] - normalize[0])
            new_value = value - normalize[0]
            new_value = int(new_value * scale)
            if new_value < 0:
                new_value = 0
            elif new_value > 255:
                new_value = 255

        if colormap == 'gray':
            return _qt.QColor(new_value, new_value, new_value)
        elif colormap == 'red2yelloe':
            return _qt.QColor(255, new_value, 0)
        elif colormap == 'blue2cyanblue':
            return _qt.QColor(0, new_value, 255)
        elif colormap == 'red':
            return _qt.QColor(255, 0, 0)
        elif colromap == 'green':
            return _qt.QColor(0, 255, 0)
        elif colormap == 'blue':
            return _qt.QColor(0, 0, 255)
    else:
        color = RAINBOW[value]
        return _qt.QColor(color[0], color[1], color[2])

def array2qrgba(array, alpha, colormap, normalize=False, roi=None):
    """Convert a 2D-array into a 3D-array containing rgba value."""
    if _np.ndim(array) != 2:
        raise ValueError("array2qrgb can only convert 2D array")

    if isinstance(colormap, str):
        if colormap != 'rainbow':
            if colormap != 'single ROI':
                array = _normalize255(array, normalize)
                if colormap == 'gray':
                    new_array = gray(array, alpha)
                elif colormap == 'red2yellow':
                    new_array = red2yellow(array, alpha)
                elif colormap == 'blue2cyanblue':
                    new_array = blue2cyanblue(array, alpha)
                elif colormap == 'red':
                    new_array = red(array, alpha)
                elif colormap == 'green':
                    new_array = green(array, alpha)
                elif colormap == 'blue':
                    new_array = blue(array, alpha)
            else:
                new_array = single_roi(array, alpha, roi)
        else:
            if _np.isscalar(normalize):
                new_array = array.clip(0, array.max())
                new_array[array < 0] = 0
                new_array[array > normalize] = 0
            elif isinstance(normalize, tuple):
                new_array = array.clip(0, array.max())
                new_array[array < normalize[0]] = 0
                new_array[array > normalize[1]] = 0
            else:
                new_array = array.clip(0, array.max())
                new_array[array < 0] = 0
            #values = RAINBOW.keys()
            h, w = new_array.shape
            R, G, B = 41, 61, 83
            fst_norm = 100000.0
            new_array_raw = _normalize255(new_array, normalize, scale_length=fst_norm)
            #print 'hahahhaha', new_array_raw.max(), new_array_raw.min()
            new_array_R = _normalize255(new_array_raw % R, (0, R), scale_length=254.0)
            new_array_G = _normalize255(new_array_raw % G, (0, G), scale_length=254.0)
            new_array_B = _normalize255(new_array_raw % B, (0, B), scale_length=254.0)
            new_array2 = _np.zeros((h, w, 4), dtype=_np.uint8)
            #for item in values:
            #    new_array2[new_array==item] = [RAINBOW[item][0],
            #                                   RAINBOW[item][1],
            #                                   RAINBOW[item][2], 
            #                                   0]
            add_ = new_array.clip(0, 1)
            new_array2[..., 0] = new_array_R + add_ 
            new_array2[..., 1] = new_array_G + add_
            new_array2[..., 2] = new_array_B + add_
            new_array2[..., 3] = alpha * _np.sum(new_array2, 2).clip(0, 1)
            #_np.set_printoptions(threshold=1000000)
            #print new_array2
            new_array = new_array2
    else:
        if _np.isscalar(normalize):
            new_array = array.clip(0, array.max())
            new_array[array < 0] = 0
            new_array[array > normalize] = 0
        elif isinstance(normalize, tuple):
            new_array = array.clip(0, array.max())
            new_array[array < normalize[0]] = 0
            new_array[array > normalize[1]] = 0
        else:
            new_array = array.clip(0, array.max())
            new_array[array < 0] = 0
        values = colormap.keys()
        values = [int(item) for item in values]
        h, w = new_array.shape
        new_array2 = _np.zeros((h, w, 4), dtype=_np.uint8)
        for item in values:
            new_array2[new_array==item] = [colormap[item][0],
                                           colormap[item][1],
                                           colormap[item][2],
                                           0]
        new_array2[..., 3] = alpha * _np.sum(new_array2, 2).clip(0, 1)
        new_array = new_array2

    return new_array

def qcomposition(array_list):
    """Composite several qrgba arrays into one."""
    if not len(array_list):
        raise ValueError('Input array list cannot be empty.')
    if _np.ndim(array_list[0]) != 3:
        raise ValueError('RGBA array must be 3D.')

    h, w, channel = array_list[0].shape
    result = _np.array(array_list[0][..., :3], dtype=_np.int64)
    for index in range(1, len(array_list)):
        item = _np.array(array_list[index], dtype=_np.int64)
        alpha_array = _np.tile(item[..., -1].reshape((-1, 1)), (1, 1, 3))
        alpha_array = alpha_array.reshape((h, w, 3))
        result = item[..., :3] * alpha_array + result * \
                (255 - alpha_array)
        result = result / 255
    result = _np.array(result, dtype=_np.uint8)
    return result

def composition(dest, source):
    """Save result in place
    
    Note
    ----
    The dest is a rgb image, while the source is a rgba image
    """
    alpha = source[...,3].reshape(source.shape[0], source.shape[1], 1).astype(_np.float)
    alpha /= 255
    source_rgb = source[...,:3].astype(_np.float)
    dest[:] = _np.uint8(source_rgb * alpha + dest.astype(_np.float) * (1 - alpha))
    return dest

def qrgba2qimage(array):
    """Convert the input array into a image."""
    if _np.ndim(array) != 3:
        raise ValueError("RGBA array must be 3D.")

    h, w, channel = array.shape
    fmt = _qt.QImage.Format_ARGB32
    result = _qt.QImage(w, h, fmt)
    rgb_view(result)[:] = array[..., :3]
    alpha = alpha_view(result)
    alpha[:] = 255
    return result

def null_image(h, w):
    """return a whole black rgba array"""
    new_array = _np.zeros((h, w, 4), dtype=_np.uint8)
    new_array[..., 3] = 255
    return new_array
