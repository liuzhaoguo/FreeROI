# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

from PyQt4.QtCore import *

from froi.algorithm import imtool

def inverse_image(model):
    """
    Inverse current selected image by multiplying with -1.

    """
    # get data and name from current selected image
    current_row = model.currentIndex().row()
    source_vol = model.data(model.index(current_row), Qt.UserRole + 6)
    source_name = model.data(model.index(current_row), Qt.DisplayRole)
    # inverse process
    inversed_vol =  imtool.inverse_transformation(source_vol)
    inversed_vol_name = 'inverse_' + source_name
    # save result as a new image
    model.addItem(inversed_vol, None, inversed_vol_name, 
                  model._data[0].get_header())
    return 


