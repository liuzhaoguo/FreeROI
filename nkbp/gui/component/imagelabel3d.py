# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import numpy as np
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ..utilities.array2qimage import composition, qrgba2qimage
from drawsettings import DrawSettings

"""ImageLabel3d class. It is used to show a slice in a specific orientation."""

class ImageLabel3d(QLabel):
    """
    Class ImageLabel3d provides basic methods for image displaying in three
    different orientation.

    Attention:
    Methods, e.g. painEvent, must be reimplemented.

    """

    # draw voxels signal
    draw_voxels_sig = pyqtSignal()
    
    def __init__(self, model, painter_status, holder, parent=None):
        """
        Initialize an instance.

        """
        super(ImageLabel3d, self).__init__(parent)
        # default setting
        self._expanding_factor = 3
        self._rect_size = 109

        # set background color as black
        palette = self.palette()
        palette.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(palette)
        
        # private attributes
        self.set_model(model)
        self.painter_status = painter_status
        self.background = self.make_background()
        self.image = None
        self.pm = None
        self.pic_src_point = None

        # store parent widget
        self.holder = holder

        # for drawing
        self.drawing = False

        # for moving
        self.old_pos = None
        self.new_pos = None

        # crosshair-displaying setting
        self.display_crosshair = True

    def set_model(self, model):
        """
        Set date model.

        """
        self.model = model
        self.model.repaint_slices.connect(self.update_image)

    def sizeHint(self):
        """
        Size hint configuration.

        """
        return QSize(self._rect_size * self._expanding_factor, 
                     self._rect_size * self._expanding_factor)

    def update_image(self, coord):
        """
        Update image.

        """
        self.repaint()

    def make_background(self):
        """
        Create a whole black background.

        """
        background = np.zeros((self._rect_size * self._expanding_factor,
                               self._rect_size * self._expanding_factor,
                               3),
                              dtype=np.uint8)
        return qrgba2qimage(background)

    def center_src_point(self):
        """
        Return the coordinate of left-up corner.

        """
        x = (self.size().width() - self.pm.size().width()) / 2
        y = (self.size().height() - self.pm.size().height()) / 2
        return (x, y)

    def horizontal_valid_range(self):
        """
        Return the valid range of horizontal axis.

        """
        min_val = self.pic_src_point[0]
        if min_val < 0:
            min_val = 0
        max_val = self.pic_src_point[0] + self.pm.size().width()
        if max_val > self.size().width():
            max_val = self.size().width()
        return (min_val, max_val)

    def vertical_valid_range(self):
        """
        Return the valid range of vertical axis.

        """
        min_val = self.pic_src_point[1]
        if min_val < 0:
            min_val = 0
        max_val = self.pic_src_point[1] + self.pm.size().height()
        if max_val > self.size().height():
            max_val = self.size().height()
        return (min_val, max_val)

    def _mouse_in(self, x, y):
        """
        Check whether current cursor position is in the valid area of the 
        picture.

        """
        return (self.horizontal_valid_range()[0] <= x < self.horizontal_valid_range()[1] and self.vertical_valid_range()[0] <= y < self.vertical_valid_range()[1])

    def mouseReleaseEvent(self, e):
        """
        Reimplement mouseReleaseEvent.

        """
        scale = self.model.get_scale_factor('orth') * self._expanding_factor
        if self.painter_status.is_drawing_valid():
            pix_to_vox = lambda (x, y, z): (int(np.floor(x/scale)), 
                                            int(np.floor(y/scale)), 
                                            int(np.floor(z/scale)))
            voxels = map(pix_to_vox, list(self.holder.voxels))
            if voxels:
                self.model.modify_voxels(voxels,
                        self.painter_status.get_drawing_value())
            self.holder.voxels = set()
        elif self._mouse_in(e.x(), e.y()) and self.painter_status.is_view():
            if isinstance(self, SagittalImageLabel):
                current_pos = [self.holder.get_coord()[0],
                               int((e.x()-self.pic_src_point[0])/scale), 
                               90 - int((e.y() - self.pic_src_point[1])/scale)]
            elif isinstance(self, AxialImageLabel):
                current_pos = [int((e.x() - self.pic_src_point[0])/scale),
                               int((e.y()-self.pic_src_point[1])/scale), 
                               self.holder.get_coord()[2]]
            else:
                current_pos = [int((e.x() - self.pic_src_point[0])/scale),
                               self.holder.get_coord()[1],
                               90 - int((e.y() - self.pic_src_point[1])/scale)]
            self.holder.set_coord(current_pos)
        elif self._mouse_in(e.x(), e.y()) and self.painter_status.is_hand():
            self.setCursor(Qt.OpenHandCursor)

class SagittalImageLabel(ImageLabel3d):
    """
    ImageLabel in sagittal view.

    """
    def paintEvent(self, e):
        """
        Reimplement paintEvent.

        """
        self.voxels_painter = QPainter()
        self.voxels_painter.begin(self)
        
        # composite volume picture
        if not self.image or not self.drawing:
            idx = self.holder.get_coord()[0]
            back_temp = np.zeros((91, 109, 3), dtype=np.uint8)
            blend = reduce(composition, 
                           self.model.sagital_rgba_list(idx),
                           back_temp)
            image = qrgba2qimage(blend)
            self.image = image
        
        # draw black background
        pm = QPixmap.fromImage(self.background)
        self.voxels_painter.drawPixmap(0, 0, pm, 0, 0,
                                       pm.size().width(),
                                       pm.size().height())
        
        # draw volume picture
        pm = QPixmap.fromImage(self.image)
        self.pm = pm.scaled(pm.size() * self.model.get_scale_factor('orth') * 
                            self._expanding_factor)
        if not self.pic_src_point:
            self.pic_src_point = self.center_src_point()
        self.voxels_painter.drawPixmap(self.pic_src_point[0],
                                       self.pic_src_point[1], 
                                       self.pm)

        # draw voxels if necessary
        if self.drawing and self.holder.voxels:
            self.draw_voxels(self.holder.voxels)

        # draw cross line on picture
        if self.display_crosshair:
            scale = self.model.get_scale_factor('orth') * self._expanding_factor
            current_pos = self.holder.get_coord()
            horizon_src = (0, (90-current_pos[2])*scale+self.pic_src_point[1])
            horizon_targ = (self._rect_size * self._expanding_factor,
                            (90-current_pos[2])*scale + self.pic_src_point[1])
            self.voxels_painter.setPen(QColor(0, 255, 0, 255))
            self.voxels_painter.drawLine(horizon_src[0],
                                         horizon_src[1],
                                         horizon_targ[0],
                                         horizon_targ[1])
            vertical_src = (current_pos[1] * scale + self.pic_src_point[0], 0)
            vertical_targ = (current_pos[1] * scale + self.pic_src_point[0],
                             self._rect_size * self._expanding_factor)
            self.voxels_painter.drawLine(vertical_src[0],
                                         vertical_src[1],
                                         vertical_targ[0],
                                         vertical_targ[1])
            
        self.voxels_painter.end()

    def draw_voxels(self, voxels):
        """
        Draw selected voxels.

        """
        self.voxels_painter.setPen(self.painter_status.get_drawing_color())
        scale = self.model.get_scale_factor('orth') * self._expanding_factor
        points = [QPoint(self.pic_src_point[0] + v[1], 
                         self.pic_src_point[1] + 91 * scale - v[2]) 
                  for v in voxels
                  if v[0] == (self.holder.get_coord()[0] * scale)]
        if points:        
            self.voxels_painter.drawPoints(*points)

    def mousePressEvent(self, e):
        """
        Reimplement mousePressEvent.

        """
        if not self._mouse_in(e.x(), e.y()):
            return
        if self.painter_status.is_drawing_valid():
            size = self.painter_status.get_drawing_size()
            X = e.x()
            Y = e.y()
            x_margin = self.pic_src_point[0]
            y_margin = self.pic_src_point[1]
            scale = self.model.get_scale_factor('orth') * self._expanding_factor
            new_voxels = [(self.holder.get_coord()[0] * scale, 
                           x - x_margin, 
                           91 * scale - y + y_margin)
                          for x in xrange(X - size/2, X + size/2 + 1) 
                          for y in xrange(Y - size/2, Y + size/2 + 1)
                          if self._mouse_in(x, y)]
            self.holder.voxels |= set(new_voxels)
            
            # draw voxels
            self.drawing = True
            self.repaint()
            self.drawing = False
        elif self.painter_status.is_view():
            scale = self.model.get_scale_factor('orth') * self._expanding_factor
            x = e.x() - self.pic_src_point[0]
            y = e.y() - self.pic_src_point[1]
            x = int(np.floor(x/scale))
            y = 90 - int(np.floor(y/scale))
            self.holder.xyz_updated.emit([x, self.holder.get_coord()[0], y])
        elif self.painter_status.is_hand():
            self.setCursor(Qt.ClosedHandCursor)
            self.old_pos = (e.x(), e.y())

    def mouseMoveEvent(self, e):
        """
        Reimplement mouseMoveEvent.

        """
        if not self._mouse_in(e.x(), e.y()):
            return
        if self.painter_status.is_drawing_valid():
            self.setCursor(Qt.ArrowCursor)
            size = self.painter_status.get_drawing_size()
            X = e.x()
            Y = e.y()
            x_margin = self.pic_src_point[0]
            y_margin = self.pic_src_point[1]
            scale = self.model.get_scale_factor('orth') * self._expanding_factor
            new_voxels = [(self.holder.get_coord()[0] * scale, 
                           x - x_margin, 
                           91 * scale - y + y_margin)
                          for x in xrange(X - size/2, X + size/2 + 1) 
                          for y in xrange(Y - size/2, Y + size/2 + 1)
                          if self._mouse_in(x, y)]
            self.holder.voxels |= set(new_voxels)
            
            # draw voxels
            self.drawing = True
            self.repaint()
            self.drawing = False
        elif self.painter_status.is_view():
            self.setCursor(Qt.ArrowCursor)
            #scale = self.model.get_scale_factor('orth')*self._expanding_factor
            #x = e.x() - self.pic_src_point[0]
            #y = e.y() - self.pic_src_point[1]
            #x = int(np.floor(x/scale))
            #y = 90 - int(np.floor(y/scale))
            #self.holder.xyz_updated.emit([x, self.holder.get_coord()[0], y])
        elif self.painter_status.is_hand():
            if self.cursor().shape() == Qt.ArrowCursor:
                self.setCursor(Qt.OpenHandCursor)
            if self.cursor().shape() == Qt.ClosedHandCursor:
                self.new_pos = (e.x(), e.y())
                dist = (self.new_pos[0] - self.old_pos[0], 
                        self.new_pos[1] - self.old_pos[1])
                self.old_pos = self.new_pos
                self.pic_src_point = (self.pic_src_point[0] + dist[0],
                                      self.pic_src_point[1] + dist[1])
                self.repaint()
            
class AxialImageLabel(ImageLabel3d):
    """
    ImageLabel in axial view.

    """
    def paintEvent(self, e):
        """
        Reimplement paintEvent.

        """
        self.voxels_painter = QPainter()
        self.voxels_painter.begin(self)

        # composite volume picture
        if not self.image or not self.drawing:
            idx = self.holder.get_coord()[2]
            back_temp = np.zeros((109, 91, 3), dtype=np.uint8)
            blend = reduce(composition, 
                           self.model.axial_rgba_list(idx),
                           back_temp)
            image = qrgba2qimage(blend)
            self.image = image

        # draw black backgroud
        pm = QPixmap.fromImage(self.background)
        self.voxels_painter.drawPixmap(0, 0, pm)

        # draw volume picture
        pm = QPixmap.fromImage(self.image)
        self.pm = pm.scaled(pm.size() * self.model.get_scale_factor('orth') * 
                            self._expanding_factor)
        if not self.pic_src_point:
            self.pic_src_point = self.center_src_point()
        self.voxels_painter.drawPixmap(self.pic_src_point[0],
                                       self.pic_src_point[1],
                                       self.pm)

        # draw voxels if necessary
        if self.drawing and self.holder.voxels:
            self.draw_voxels(self.holder.voxels)

        # draw cross line on picture
        if self.display_crosshair:
            scale = self.model.get_scale_factor('orth') * self._expanding_factor
            current_pos = self.holder.get_coord()
            horizon_src = (0, current_pos[1] * scale + self.pic_src_point[1])
            horizon_targ = (self._rect_size * self._expanding_factor,
                            current_pos[1] * scale + self.pic_src_point[1])
            self.voxels_painter.setPen(QColor(0, 255, 0, 255))
            self.voxels_painter.drawLine(horizon_src[0],
                                         horizon_src[1],
                                         horizon_targ[0],
                                         horizon_targ[1])
            vertical_src = (current_pos[0] * scale + self.pic_src_point[0], 0)
            vertical_targ = (current_pos[0] * scale + self.pic_src_point[0],
                             self._rect_size * self._expanding_factor)
            self.voxels_painter.drawLine(vertical_src[0],
                                         vertical_src[1],
                                         vertical_targ[0],
                                         vertical_targ[1])
        self.voxels_painter.end()
    
    def draw_voxels(self, voxels):
        """
        Draw selected voxels.

        """
        self.voxels_painter.setPen(self.painter_status.get_drawing_color())
        scale = self.model.get_scale_factor('orth') * self._expanding_factor
        points = [QPoint(self.pic_src_point[0] + v[0], 
                         self.pic_src_point[1] + v[1])
                  for v in voxels
                  if v[2] == (self.holder.get_coord()[2] * scale)]
        if points:
            self.voxels_painter.drawPoints(*points)

    def mousePressEvent(self, e):
        """
        Reimplement mousePressEvent.

        """
        if not self._mouse_in(e.x(), e.y()):
            return
        if self.painter_status.is_drawing_valid():
            size = self.painter_status.get_drawing_size()
            X = e.x()
            Y = e.y()
            x_margin = self.pic_src_point[0]
            y_margin = self.pic_src_point[1]
            scale = self.model.get_scale_factor('orth') * self._expanding_factor
            new_voxels = [(x - x_margin, 
                           y - y_margin, 
                           self.holder.get_coord()[2] * scale)
                          for x in xrange(X - size/2, X + size/2 + 1)
                          for y in xrange(Y - size/2, Y + size/2 + 1)
                          if self._mouse_in(x, y)]
            self.holder.voxels |= set(new_voxels)
            # draw voxels
            self.drawing = True
            self.repaint()
            self.drawing = False
        elif self.painter_status.is_view():
            scale = self.model.get_scale_factor('orth') * self._expanding_factor
            x = e.x() - self.pic_src_point[0]
            y = e.y() - self.pic_src_point[1]
            x = int(np.floor(x/scale))
            y = int(np.floor(y/scale))
            self.holder.xyz_updated.emit([y, x, self.holder.get_coord()[2]])
        elif self.painter_status.is_hand():
            self.setCursor(Qt.ClosedHandCursor)
            self.old_pos = (e.x(), e.y())

    def mouseMoveEvent(self, e):
        """
        Reimplement mouseMoveEvent.

        """
        if not self._mouse_in(e.x(), e.y()):
            return
        if self.painter_status.is_drawing_valid():
            self.setCursor(Qt.ArrowCursor)
            size = self.painter_status.get_drawing_size()
            X = e.x()
            Y = e.y()
            x_margin = self.pic_src_point[0]
            y_margin = self.pic_src_point[1]
            scale = self.model.get_scale_factor('orth') * self._expanding_factor
            new_voxels = [(x - x_margin, 
                           y - y_margin, 
                           self.holder.get_coord()[2] * scale)
                          for x in xrange(X - size/2, X + size/2 + 1)
                          for y in xrange(Y - size/2, Y + size/2 + 1)
                          if self._mouse_in(x, y)]
            self.holder.voxels |= set(new_voxels)
            # draw voxels
            self.drawing = True
            self.repaint()
            self.drawing = False
        elif self.painter_status.is_view():
            self.setCursor(Qt.ArrowCursor)
            #scale = self.model.get_scale_factor('orth')* self._expanding_factor
            #x = e.x() - self.pic_src_point[0]
            #y = e.y() - self.pic_src_point[1]
            #x = int(np.floor(x/scale))
            #y = int(np.floor(y/scale))
            #self.holder.xyz_updated.emit([y, x, self.holder.get_coord()[2]])
        elif self.painter_status.is_hand():
            if self.cursor().shape() == Qt.ArrowCursor:
                self.setCursor(Qt.OpenHandCursor)
            if self.cursor().shape() == Qt.ClosedHandCursor:
                self.new_pos = (e.x(), e.y())
                dist = (self.new_pos[0] - self.old_pos[0],
                        self.new_pos[1] - self.old_pos[1])
                self.old_pos = self.new_pos
                self.pic_src_point = (self.pic_src_point[0] + dist[0],
                                      self.pic_src_point[1] + dist[1])
                self.repaint()

class CoronalImageLabel(ImageLabel3d):
    """
    ImageLabel in coronal view.

    """
    def paintEvent(self, e):
        """
        Reimplement paintEvent.

        """
        self.voxels_painter = QPainter()
        self.voxels_painter.begin(self)
        if not self.image or not self.drawing:
            idx = self.holder.get_coord()[1]
            back_temp = np.zeros((91, 91, 3), dtype=np.uint8)
            blend = reduce(composition, 
                           self.model.coronal_rgba_list(idx),
                           back_temp)
            image = qrgba2qimage(blend)
            self.image = image

        # draw black background
        pm = QPixmap.fromImage(self.background)
        self.voxels_painter.drawPixmap(0, 0, pm)

        # draw volume picture
        pm = QPixmap.fromImage(self.image)
        self.pm = pm.scaled(pm.size() * self.model.get_scale_factor('orth') *
                            self._expanding_factor)
        if not self.pic_src_point:
            self.pic_src_point = self.center_src_point()
        self.voxels_painter.drawPixmap(self.pic_src_point[0],
                                       self.pic_src_point[1],
                                       self.pm)

        # draw voxels if necessary
        if self.drawing and self.holder.voxels:
            self.draw_voxels(self.holder.voxels)
            
        # draw cross line on picture
        if self.display_crosshair:
            scale = self.model.get_scale_factor('orth') * self._expanding_factor
            current_pos = self.holder.get_coord()
            horizon_src = (0, (90-current_pos[2])*scale+self.pic_src_point[1])
            horizon_targ = (self._rect_size * self._expanding_factor,
                            (90-current_pos[2]) * scale + self.pic_src_point[1])
            self.voxels_painter.setPen(QColor(0, 255, 0, 255))
            self.voxels_painter.drawLine(horizon_src[0],
                                         horizon_src[1],
                                         horizon_targ[0],
                                         horizon_targ[1])
            vertical_src = (current_pos[0] * scale + self.pic_src_point[0], 0)
            vertical_targ = (current_pos[0] * scale + self.pic_src_point[0],
                             self._rect_size * self._expanding_factor)
            self.voxels_painter.drawLine(vertical_src[0],
                                         vertical_src[1],
                                         vertical_targ[0],
                                         vertical_targ[1])
        self.voxels_painter.end()
    
    def draw_voxels(self, voxels):
        """
        Draw selected voxels.

        """
        self.voxels_painter.setPen(self.painter_status.get_drawing_color())
        scale = self.model.get_scale_factor('orth') * self._expanding_factor
        points = [QPoint(v[0] + self.pic_src_point[0], 
                         91 * scale - v[2] + self.pic_src_point[1]) 
                  for v in voxels
                  if v[1] == (self.holder.get_coord()[1] * scale)]
        if points:
            self.voxels_painter.drawPoints(*points)

    def mousePressEvent(self, e):
        """
        Reimplement mousePressEvent.

        """
        if not self._mouse_in(e.x(), e.y()):
            return
        if self.painter_status.is_drawing_valid():
            size = self.painter_status.get_drawing_size()
            X = e.x()
            Y = e.y()
            x_margin = self.pic_src_point[0]
            y_margin = self.pic_src_point[1]
            scale = self.model.get_scale_factor('orth') * self._expanding_factor
            new_voxels = [(x - x_margin, 
                           self.holder.get_coord()[1] * scale, 
                           91 * scale - y + y_margin)
                          for x in xrange(X - size/2, X + size/2 + 1)
                          for y in xrange(Y - size/2, Y + size/2 + 1)
                          if self._mouse_in(x, y)]
            self.holder.voxels |= set(new_voxels)
            # draw voxels
            self.drawing = True
            self.repaint()
            self.drawing = False
        elif self.painter_status.is_view():
            scale = self.model.get_scale_factor('orth') * self._expanding_factor
            x = e.x() - self.pic_src_point[0]
            y = e.y() - self.pic_src_point[1]
            x = int(np.floor(x/scale))
            y = 90 - int(np.floor(y/scale))
            self.holder.xyz_updated.emit([self.holder.get_coord()[1], x, y])
        elif self.painter_status.is_hand():
            self.setCursor(Qt.ClosedHandCursor)
            self.old_pos = (e.x(), e.y())

    def mouseMoveEvent(self, e):
        """
        Reimplement mouseMoveEvent.

        """
        if not self._mouse_in(e.x(), e.y()):
            return
        if self.painter_status.is_drawing_valid():
            self.setCursor(Qt.ArrowCursor)
            size = self.painter_status.get_drawing_size()
            X = e.x()
            Y = e.y()
            x_margin = self.pic_src_point[0]
            y_margin = self.pic_src_point[1]
            scale = self.model.get_scale_factor('orth') * self._expanding_factor
            new_voxels = [(x - x_margin, 
                           self.holder.get_coord()[1] * scale, 
                           91 * scale - y + y_margin)
                          for x in xrange(X - size/2, X + size/2 + 1)
                          for y in xrange(Y - size/2, Y + size/2 + 1)
                          if self._mouse_in(x, y)]
            self.holder.voxels |= set(new_voxels)
            # draw voxels
            self.drawing = True
            self.repaint()
            self.drawing = False
        elif self.painter_status.is_view():
            self.setCursor(Qt.ArrowCursor)
            #scale = self.model.get_scale_factor('orth')* self._expanding_factor
            #x = e.x() - self.pic_src_point[0]
            #y = e.y() - self.pic_src_point[1]
            #x = int(np.floor(x/scale))
            #y = 90 - int(np.floor(y/scale))
            #self.holder.xyz_updated.emit([self.holder.get_coord()[1], x, y])
        elif self.painter_status.is_hand():
            if self.cursor().shape() == Qt.ArrowCursor:
                self.setCursor(Qt.OpenHandCursor)
            if self.cursor().shape() == Qt.ClosedHandCursor:
                self.new_pos = (e.x(), e.y())
                dist = (self.new_pos[0] - self.old_pos[0],
                        self.new_pos[1] - self.old_pos[1])
                self.old_pos = self.new_pos
                self.pic_src_point = (self.pic_src_point[0] + dist[0],
                                      self.pic_src_point[1] + dist[1])
                self.repaint()
