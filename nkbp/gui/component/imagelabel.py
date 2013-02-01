# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import numpy as np 
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ..utilities.array2qimage import composition, qrgba2qimage
from drawsettings import DrawSettings

"""ImageLabel class. It is used to show a slice of the 3D image"""

class ImageLabel(QLabel):
    """
    Class ImageLabel provides basic methods for image displaying.

    """

    # resized signal
    resized_signal = pyqtSignal(float, float, int)

    def __init__(self, model, painter_status, n_slice, holder, parent=None):
        """
        Initialize an instance.

        """
        super(ImageLabel, self).__init__(parent)
        # set background color
        palette = self.palette()
        palette.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(palette)
        # model setting
        self.set_model(model)
        self.painter_status = painter_status
        self.n_slice = n_slice
        self.background = np.zeros((model.getX(), model.getY(), 3), 
                                   dtype=np.uint8)
        self.image = None
        self.pm = None

        # for event
        self.holder = holder

        # for drawing
        self.drawing = False
        self.voxels = set() 

        # whether display crosshair
        self.display_crosshair = True

    def sizeHint(self):
        """
        Size hint configuration.

        """
        default_size = QSize(self.background.shape[1],
                             self.background.shape[0])
        scale_factor = self.model.get_scale_factor('grid')
        return default_size * scale_factor

    def set_model(self, model):
        """
        Set data model.

        """
        self.model = model
        self.model.repaint_slices.connect(self.update_image)

    def update_image(self, m_slice):
        """
        Repaint image.

        """
        # -1 for all
        if m_slice == -1 or m_slice == self.n_slice:
            self.repaint()
        self.updateGeometry()

    def is_current_slice(self):
        """
        Return True if cursor select current slice.

        """
        return self.n_slice == self.holder.get_coord()[2]

    def paintEvent(self, e):
        """
        Reimplement repaintEvent.

        """
        self.voxels_painter = QPainter()
        self.voxels_painter.begin(self)
        if not self.image or not self.drawing:
            background = self.background.copy()
            blend = reduce(composition, 
                           self.model.rgba_list(self.n_slice), 
                           background)
            image = qrgba2qimage(blend)
            self.image = image
        pm = QPixmap.fromImage(self.image)
        pm = pm.scaled(pm.size() * self.model.get_scale_factor('grid'))
        self.pm = pm
        self.voxels_painter.drawPixmap(0, 0, pm, 0, 0, 
                                       pm.size().width(), pm.size().height())
        
        # draw voxels if necessary
        if self.drawing and self.voxels:
            self.draw_voxels(self.voxels)

        # draw crosshair on picture
        if self.display_crosshair and self.is_current_slice():
            scale = self.model.get_scale_factor('grid')
            current_pos = self.holder.get_coord()
            horizon_src = (current_pos[0] * scale, 0)
            horizon_targ = (current_pos[0] * scale, self.pm.size().height())
            self.voxels_painter.setPen(QColor(0, 255, 0, 255))
            self.voxels_painter.drawLine(horizon_src[0],
                                         horizon_src[1],
                                         horizon_targ[0],
                                         horizon_targ[1])
            vertical_src = (0, current_pos[1] * scale)
            vertical_targ = (self.pm.size().width(), current_pos[1] * scale)
            self.voxels_painter.drawLine(vertical_src[0],
                                         vertical_src[1],
                                         vertical_targ[0],
                                         vertical_targ[1])

        self.voxels_painter.end()

    def mousePressEvent(self, e):
        if not self._mouse_in(e.x(), e.y()):
            return 
        if self.painter_status.is_drawing_valid():
            if not self.painter_status.is_roi_tool():
                size = self.painter_status.get_drawing_size()
                X = e.x()
                Y = e.y()
                new_voxels = [(x, y, self.n_slice) 
                              for x in xrange(X - size/2, X + size/2 + 1)
                              for y in xrange(Y -size/2, Y + size/2 + 1)
                              if self._mouse_in(x, y)]
                self.voxels |= set(new_voxels)
                self.drawing = True
                self.repaint()
                self.drawing = False
            else:
                scale = self.model.get_scale_factor('grid')
                y = int(np.floor(e.y()/scale))
                x = int(np.floor(e.x()/scale))
                roi_val = self.model.get_current_roi_val(x, y, self.n_slice)
                if roi_val != 0:
                    t_value = self.painter_status.get_drawing_value()
                    self.model.modify_voxels(value=t_value, roi=roi_val)
        else:
            if self.painter_status.is_roi_selection():
                scale = self.model.get_scale_factor('grid')
                y = int(np.floor(e.y()/scale))
                x = int(np.floor(e.x()/scale))
                roi_val = self.model.get_current_roi_val(x, y, self.n_slice)
                if roi_val != 0:
                    self.painter_status.get_draw_settings()._update_roi(roi_val)
            scale = self.model.get_scale_factor('grid')
            y = int(np.floor(e.y()/scale))
            x = int(np.floor(e.x()/scale))
            self.holder.set_coord([x, y, self.n_slice])
            self.holder.xyz_updated.emit([y, x, self.n_slice])
       
    def mouseMoveEvent(self, e):
        if not self._mouse_in(e.x(), e.y()):
            return
        if self.painter_status.is_drawing_valid(): 
            if not self.painter_status.is_roi_tool():
                size = self.painter_status.get_drawing_size()
                X = e.x()
                Y = e.y()
                new_voxels = [(x, y, self.n_slice) 
                              for x in xrange(X - size/2, X + size/2 + 1)
                              for y in xrange(Y - size/2, Y + size/2 + 1)
                              if self._mouse_in(x, y)]
                self.voxels |= set(new_voxels)
                self.drawing = True
                self.repaint()
                self.drawing = False

    def mouseReleaseEvent(self, e):
        if self.painter_status.is_drawing_valid() and (not
           self.painter_status.is_roi_tool()):
            scale = self.model.get_scale_factor('grid')
            pix_to_vox = lambda (x,y,z): (int(np.floor(x/scale)), 
                                          int(np.floor(y/scale)), 
                                          z)
            voxels = map(pix_to_vox, list(self.voxels))
            if voxels:
                self.model.modify_voxels(voxels, 
                    self.painter_status.get_drawing_value())
            self.voxels = set()

    def _mouse_in(self, x, y):
        return (0 <= x < self.size().width() and
                0 <= y < self.size().height())
        
    def draw_voxels(self, voxels):
        self.voxels_painter.setPen(self.painter_status.get_drawing_color())
        points = [QPoint(v[0], v[1]) for v in voxels]
        self.voxels_painter.drawPoints(*points)

    def inrange(self, x=None, y=None):
        if x is None:
            return y >= 0 and y < self.model.getX()
        if y is None:
            return x >= 0 and x < self.model.getY()
        return ((x >= 0 and x < self.model.getY()) and 
                (y >= 0 and y < self.model.getX()))

