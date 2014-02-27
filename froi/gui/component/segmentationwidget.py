# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import os
import froi

from growdialog_liu import GrowDialog
from watersheddialog import WatershedDialog


class SegmentationWidget(QDialog):
    """
    Model for tools tabwidget.

    """

    def __init__(self, model,main_win, parent=None):
        super(SegmentationWidget, self).__init__(parent)

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

        self.grow_button = QPushButton()
        #self.grow_button.setFlat(True)
        #self.grow_button.setFocusPolicy(Qt.NoFocus)
        self.grow_button.resize(100,100)
        self.grow_button.setIcon(QIcon(os.path.join(self._icon_dir,'grow.png')))
        self.grow_button.setEnabled(True)
        self.grow_button.setToolTip("region growing")

        self.watershed_button = QPushButton()
        #self.watershed_button.setFlat(True)
        #self.watershed_button.setFocusPolicy(Qt.NoFocus)
        self.watershed_button.setIcon(QIcon(os.path.join(self._icon_dir,'watershed.png')))
        self.watershed_button.setEnabled(True)
        self.watershed_button.setToolTip("Watershed")

        gridlayout = QGridLayout(self)
        gridlayout.addWidget(self.grow_button,1,0)
        gridlayout.addWidget(self.watershed_button,1,1)


    def _create_actions(self):
        """
        Create actions about the toobar
        """
        # self.brush_pushbutton.clicked.connect(self._mainwindow._brush_enable)
        # self.roibrush_pushbutton.clicked.connect(self._mainwindow._roibrush_enable)
        self.grow_button.clicked.connect(self._grow_clicked)
        self.watershed_button.clicked.connect(self._watershed_clicked)


    def _grow_clicked(self):
        '''
        region growing clicked
        '''
        if self.grow_button.isEnabled():
            new_dialog = GrowDialog(self._model, self._main_win)
            new_dialog.exec_()

    def _watershed_clicked(self):
        '''
        watershed clicked
        '''
        if self.watershed_button.isEnabled():
            new_dialog = WatershedDialog(self._model, self)
            new_dialog.exec_()









