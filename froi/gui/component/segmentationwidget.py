# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from growdialog_liu import GrowDialog
from watersheddialog import WatershedDialog
from clusterdialog import ClusterDialog
from froi.gui.base.utils import *


class SegmentationWidget(QDialog):
    """
    Model for tools tabwidget.

    """

    def __init__(self, model, main_win, parent=None):
        super(SegmentationWidget, self).__init__(parent)
        self._icon_dir = get_icon_dir()
        self._init_gui()
        self._create_actions()
        self._main_win = main_win
        self._model = model

    def _init_gui(self):
        """
        Initialize GUI.
        """
        self.grow_button = QPushButton()
        self.grow_button.setFocusPolicy(Qt.NoFocus)
        #self.grow_button.resize(100,100)
        self.grow_button.setIcon(QIcon(os.path.join(self._icon_dir,
                                                    'grow.png')))
        self.grow_button.setEnabled(True)
        self.grow_button.setToolTip("region growing")

        self.watershed_button = QPushButton()
        self.watershed_button.setFocusPolicy(Qt.NoFocus)
        self.watershed_button.setIcon(QIcon(os.path.join(self._icon_dir,
                                                         'watershed.png')))
        self.watershed_button.setEnabled(True)
        self.watershed_button.setToolTip("Watershed")

        self.cluster_button = QPushButton()
        self.cluster_button.setFocusPolicy(Qt.NoFocus)
        self.cluster_button.setIcon(QIcon(os.path.join(self._icon_dir,
                                                         'merging.png')))
        self.cluster_button.setEnabled(True)
        self.cluster_button.setToolTip("Cluster")

        gridlayout = QGridLayout(self)
        gridlayout.addWidget(self.grow_button, 1, 0)
        gridlayout.addWidget(self.watershed_button, 1, 1)
        gridlayout.addWidget(self.cluster_button, 2, 0)

    def _create_actions(self):
        """
        Create actions about the toobar

        """
        self.grow_button.clicked.connect(self._grow_clicked)
        self.watershed_button.clicked.connect(self._watershed_clicked)
        self.cluster_button.clicked.connect(self._cluster_clicked)

    def _grow_clicked(self):
        """
        region growing clicked

        """
        if self.grow_button.isEnabled():
            new_dialog = GrowDialog(self._model, self._main_win)
            new_dialog.exec_()

    def _watershed_clicked(self):
        """
        watershed clicked

        """
        if self.watershed_button.isEnabled():
            new_dialog = WatershedDialog(self._model, self)
            new_dialog.exec_()

    def _cluster_clicked(self):
        """
        Run cluster labeling.

        """
        new_dialog = ClusterDialog(self._model)
        new_dialog.exec_()

