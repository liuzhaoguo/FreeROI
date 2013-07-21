# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""A viewer (part of Qt model-view-delegate classes) for image display 
in orthographic style.

"""

import numpy as np
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from imagelabel import (SagittalImageLabel, AxialImageLabel, CoronalImageLabel)
from mayaviwidget import *

class ThreeDWidget(QWidget):
    """
    Implementation a widget for image display in a 3D volume.

    """

    def __init__(self, model=None, draw_settings=None, parent=None):
        """
        Initialize the widget.

        """
        super(ThreeDWidget, self).__init__(parent)

        self._model = model
        # self._saglabel = SagittalImageLabel(model, draw_settings, self)

        self._mayaviwidget = Visualization().edit_traits().control
        layout = QGridLayout()
        layout.addWidget(self._mayaviwidget)
        # add display widget
        self.setLayout(layout)

    def get_expanding_factor(self):
        return self._expanding_factor

    def display_type(self):
        return self._type

    def set_display_type(self, type):
        self._type = type


    def setModel(self, model):
        """
        Set model.

        """
        self._model = model



