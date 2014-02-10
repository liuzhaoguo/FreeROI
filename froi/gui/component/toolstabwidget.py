# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import os
import froi

from edgedetectiondialog import Edge_detectionDialog
from localmaxdialog import LocalMaxDialog


class ToolsTabWidget(QDialog):
    """
    Model for tools tabwidget.

    """

    def __init__(self, model,main_win, parent=None):
        super(ToolsTabWidget, self).__init__(parent)

        froi_dir = os.path.dirname(froi.__file__)
        self._icon_dir = os.path.join(froi_dir,'gui/icon/')

        self._init_gui()
        self._create_actions()
        self._main_win=main_win
        self._model = model


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

        self.detection_button = QPushButton()
        self.detection_button.setFlat(True)
        self.detection_button.setFocusPolicy(Qt.NoFocus)
        self.detection_button.setIcon(QIcon(os.path.join(self._icon_dir,'edge_detection.png')))
        self.detection_button.setEnabled(True)
        self.detection_button.setToolTip("edge detection")

        self.localmax_button = QPushButton()
        self.localmax_button.setFlat(True)
        self.localmax_button.setFocusPolicy(Qt.NoFocus)
        self.localmax_button.setIcon(QIcon(os.path.join(self._icon_dir,'localmax.png')))
        self.localmax_button.setEnabled(True)
        self.localmax_button.setToolTip("Local Max")

        gridlayout = QGridLayout(self)
        gridlayout.addWidget(self.brush_pushbutton,0,0)
        gridlayout.addWidget(self.roibrush_pushbutton,0,1)
        gridlayout.addWidget(self.localmax_button,1,0)
        gridlayout.addWidget(self.detection_button,1,1)


    def _create_actions(self):
        """
        Create actions about the toobar
        """
        # self.brush_pushbutton.clicked.connect(self._mainwindow._brush_enable)
        # self.roibrush_pushbutton.clicked.connect(self._mainwindow._roibrush_enable)
        self.brush_pushbutton.clicked.connect(self._brush_clicked)
        self.roibrush_pushbutton.clicked.connect(self._roibrush_clicked)
        self.detection_button.clicked.connect(self._edge_detection_clicked)
        self.localmax_button.clicked.connect(self._local_max_clicked)


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

    def _edge_detection_clicked(self):
        '''
        edge detection clicked
        '''
        if self.detection_button.isEnabled():
            new_dialog = Edge_detectionDialog(self._model, self)
            new_dialog.exec_()

    def _local_max_clicked(self):
        '''
        local max clicked
        '''
        if self.localmax_button.isEnabled():
            new_dialog = LocalMaxDialog(self._model, self)
            new_dialog.exec_()

