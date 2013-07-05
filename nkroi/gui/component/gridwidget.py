# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""A viewer (part of Qt model-view-delegate classes) for image display 
in a grid style.

"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from imagelabel import ImageLabel

class GridView(QScrollArea):
    """
    Implementation a widget for image display in a grid style.

    """
    # number of slice each row
    _row_count = 7
    # define new signal
    xyz_updated = pyqtSignal(list)

    def __init__(self, model=None, draw_settings=None, 
                 vertical_srollbar_position=0, parent=None):
        """
        Initialize the widget.

        """
        super(GridView, self).__init__(parent)

        # set scroll bar position
        #self._horizontal_scrollbar_position = horizontal_scrollbar_position
        self._vertical_scrollbar_position = vertical_srollbar_position

        # model settings
        self.setModel(model)
        self._model.scale_changed.connect(self.resize_item)
        self.set_draw_settings(draw_settings)

        # current cursor position
        self._current_pos = self._model.get_current_pos()

        #self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # imagelabel instances
        self.image_labels = [ImageLabel(model, draw_settings, n_slice, self) for
                             n_slice in xrange(model.getZ())]
        self.update_row_count()
        self.update_layout()
        self.set_label_mouse_tracking(True)

        self._type = 'grid'
        
        #if self._horizontal_scrollbar_position and \
           #self._horizontal_scrollbar_position <= \
                #self.horizontalScrollBar().maximum():
            #self.horizontalScrollBar().setValue(
                    #self._horizontal_scrollbar_position)
        #if self._vertical_scrollbar_position and \
           #self._vertical_scrollbar_position <= \
                #self.verticalScrollBar().maximum():
            #self.verticalScrollBar().setValue(
                    #self._vertical_scrollbar_position)

    def update_layout(self):
        layout = QGridLayout()
        layout.setSpacing(5)
        for slice, image in enumerate(self.image_labels):
            row, col = slice / self._row_count, slice % self._row_count
            layout.addWidget(image, row, col)
        view_widget = QWidget()
        view_widget.setLayout(layout)
        self.setWidget(view_widget)
        self.setBackgroundRole(QPalette.Dark)
        self.layout = layout
        if self._vertical_scrollbar_position and \
           self._vertical_scrollbar_position <= \
                self.verticalScrollBar().maximum():
            self.verticalScrollBar().setValue(
                    self._vertical_scrollbar_position)
        
    def display_type(self):
        return self._type

    def set_display_type(self, type):
        self._type = type

    #def get_horizontal_scrollbar_position(self):
        #return self.horizontalScrollBar().value()

    def get_vertical_srollbar_position(self):
        return self.verticalScrollBar().value()

    def set_label_mouse_tracking(self, t=False):
        """
        Set mouse tracking status.

        """
        for label in self.image_labels:
            label.setMouseTracking(t)

    def update_row_count(self, twidth=None):
        if twidth is None:
            twidth = self.size().width()
        img_label_width = self.image_labels[0].size().width()
        row_count = twidth // (img_label_width+7)
        if row_count <= 0:
            row_count=1
        self._row_count = row_count

    def resize_item(self):
        """
        Resize images function.

        """
        for image in self.image_labels:
            self.layout.removeWidget(image)
        self.update_row_count(self.size().width())
        self.update_layout()
        #for image in self.image_labels:
            #self.layout.addWidget(image)
        #view_widget = QWidget()
        #view_widget.setLayout(self.layout)
        #self.setWidget(view_widget)

    def resizeEvent(self, e):
        self.update_row_count(e.size().width())
        self.update_layout()
        
    def setModel(self, model):
        """
        Set model of the viewer.

        """
        self._model = model

    def set_draw_settings(self, draw_settings):
        """
        Set scale factor.

        """
        self._draw_settings = draw_settings

    def get_coord(self):
        """
        Get current curosr coordinate.

        """
        return self._current_pos

    def set_coord(self, new_coord):
        """
        Set current coordinate as a new value.

        """
        old_slice = self._current_pos[2]
        self._current_pos = new_coord
        self._model.set_current_pos(new_coord)
        self.image_labels[old_slice].repaint()
        self.image_labels[self.get_coord()[2]].repaint()

