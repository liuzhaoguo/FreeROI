# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import os
import froi
from drawsettings import DrawSettings
from orthwidget import OrthView

class ToolsTabWidget(QWidget):
    """
    Model for tools tabwidget.

    """

    def __init__(self,parent=None):
        super(ToolsTabWidget, self).__init__(parent)

        froi_dir = os.path.dirname(froi.__file__)
        self._icon_dir = os.path.join(froi_dir,'gui/icon/')

        self._init_gui()
        self._create_actions()

    def _init_gui(self):
        """
        Initialize GUI.

        """
        self.brush_pushbutton = QPushButton()
        self.brush_pushbutton.setFlat(True)
        self.brush_pushbutton.setFocusPolicy(Qt.NoFocus)
        self.brush_pushbutton.setIcon(QIcon(os.path.join(self._icon_dir,'brush.png')))
        self.brush_pushbutton.setEnabled(False)
        self.roibrush_pushbutton = QPushButton()
        self.roibrush_pushbutton.setFlat(True)
        self.roibrush_pushbutton.setFocusPolicy(Qt.NoFocus)
        self.roibrush_pushbutton.setIcon(QIcon(os.path.join(self._icon_dir,'roibrush.png')))
        self.roibrush_pushbutton.setEnabled(False)

        gridlayout = QGridLayout(self)
        gridlayout.addWidget(self.brush_pushbutton,0,0)
        gridlayout.addWidget(self.roibrush_pushbutton,0,1)

    def _create_actions(self):
        """
        Create actions about the toobar
        """
        # self.brush_pushbutton.clicked.connect(self._mainwindow._brush_enable)
        # self.roibrush_pushbutton.clicked.connect(self._mainwindow._roibrush_enable)
        self.brush_pushbutton.clicked.connect(self._brush_clicked)
        self.roibrush_pushbutton.clicked.connect(self._roibrush_clicked)

    def _brush_clicked(self):
        '''
        brush clicked
        '''
        if self.brush_pushbutton.isEnabled():
            self.roibrush_pushbutton.setEnabled(True)
            self.brush_pushbutton.setEnabled(False)
            # if isinstance(self._mainwindow.image_view, OrthView):
            #     self.hand_pushbutton.setEnabled(False)

    def _roibrush_clicked(self):
        '''
        roibrush clicked
        '''
        if self.roibrush_pushbutton.isEnabled():
            self.brush_pushbutton.setEnabled(True)
            self.roibrush_pushbutton.setEnabled(False)









