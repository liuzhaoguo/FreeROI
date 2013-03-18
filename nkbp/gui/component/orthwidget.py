# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""A viewer (part of Qt model-view-delegate classes) for image display 
in orthographic style.

"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from imagelabel import (SagittalImageLabel, AxialImageLabel, CoronalImageLabel)

class OrthView(QScrollArea):
    """
    Implementation a widget for image display in a orthographic style.

    """
    xyz_updated = pyqtSignal(list)
    
    def __init__(self, model=None, draw_settings=None, parent=None):
        """
        Initialize the widget.

        """
        super(OrthView, self).__init__(parent)

        self._model = model
        self._model.scale_changed.connect(self.resize_item)
        self.set_draw_settings(draw_settings)
        
        self._saglabel = SagittalImageLabel(model, draw_settings, self)
        self._axilabel = AxialImageLabel(model, draw_settings, self)
        self._corlabel = CoronalImageLabel(model, draw_settings, self)
        # current position of cursor
        self._current_pos = self._model.get_current_pos()

        # set label layout
        layout = QGridLayout()
        layout.setSpacing(5)
        layout.addWidget(self._corlabel, 0, 0)
        layout.addWidget(self._saglabel, 0, 1)
        layout.addWidget(self._axilabel, 1, 0)

        # add display widget
        view_widget = QWidget()
        view_widget.setLayout(layout)
        #self.setLayout(layout)
        self.setWidget(view_widget)
        self.setBackgroundRole(QPalette.Dark)

        self._type = 'orth'

        # -- temporary
        self.layout = layout
        # --

        # variable for drawing
        self.voxels = set()

        self.set_label_mouse_tracking(True)

    def display_type(self):
        return self._type

    def set_display_type(self, type):
        self._type = type

    def set_label_mouse_tracking(self, t=False):
        self._saglabel.setMouseTracking(t)
        self._axilabel.setMouseTracking(t)
        self._corlabel.setMouseTracking(t)

    def resize_item(self):
        """
        Resize label -- remove label from layout first, and re-fill it

        """
        self.repaint()

    def setModel(self, model):
        """
        Set model.

        """
        self._model = model

    def set_draw_settings(self, draw_settings):
        """
        Set scale factor.

        """
        self._draw_settings = draw_settings

    def get_coord(self):
        """
        Get current cursor coordinates.

        """
        return self._current_pos

    def set_coord(self, new_coord):
        """
        Set current coordinate as a new value.

        """
        self._current_pos = new_coord
        self._model.set_current_pos(new_coord)
        self.repaint()
        #print '------------------------------------'
        #print new_coord

    def repaint(self):
        """
        repaint.

        """
        self._saglabel.update_image(self._current_pos)
        self._axilabel.update_image(self._current_pos)
        self._corlabel.update_image(self._current_pos)

    def reset_view(self):
        """
        Reset view.

        """
        self._saglabel.pic_src_point = None
        self._axilabel.pic_src_point = None
        self._corlabel.pic_src_point = None
        self.repaint()
