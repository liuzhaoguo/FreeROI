# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from intersectdialog import IntersectDialog
from localmaxdialog import LocalMaxDialog
from opendialog import OpenDialog
from froi.gui.base.utils import *
from no_gui_tools import inverse_image

class BasicWidget(QDialog):
    """
    Model for tools tabwidget.

    """

    def __init__(self, model, main_win, parent=None):
        super(BasicWidget, self).__init__(parent)
        self._icon_dir = get_icon_dir()

        self._init_gui()
        self._create_actions()
        self._main_win = main_win
        self._model = model

    def _init_gui(self):
        """
        Initialize GUI.
        """
        self.localmax_button = QPushButton()
        self.localmax_button.setFocusPolicy(Qt.NoFocus)
        self.localmax_button.setIcon(QIcon(os.path.join(self._icon_dir,
                                                        'localmax.png')))
        self.localmax_button.setEnabled(True)
        self.localmax_button.setToolTip("Local Max")

        self.intersect_button = QPushButton()
        self.intersect_button.setFocusPolicy(Qt.NoFocus)
        self.intersect_button.setIcon(QIcon(os.path.join(self._icon_dir,
                                                         'intersect.png')))
        self.intersect_button.setEnabled(True)
        self.intersect_button.setToolTip("Intersection")

        self.opening_button = QPushButton()
        self.opening_button.setFocusPolicy(Qt.NoFocus)
        self.opening_button.setIcon(QIcon(os.path.join(self._icon_dir,
                                                       'opening.png')))
        self.opening_button.setEnabled(True)
        self.opening_button.setToolTip("Opening")

        self.inverse_button = QPushButton()
        self.inverse_button.setFocusPolicy(Qt.NoFocus)
        self.inverse_button.setIcon(QIcon(os.path.join(self._icon_dir,
                                                       'inverse.icon')))
        self.inverse_button.setEnabled(True)
        self.inverse_button.setToolTip("Inverse")

        gridlayout = QGridLayout(self)
        gridlayout.addWidget(self.localmax_button, 1, 0)
        gridlayout.addWidget(self.intersect_button, 1, 1)
        gridlayout.addWidget(self.opening_button, 2, 0)
        gridlayout.addWidget(self.inverse_button, 2, 1)

    def _create_actions(self):
        """
        Create actions about the toobar
        """
        self.localmax_button.clicked.connect(self._localmax_clicked)
        self.intersect_button.clicked.connect(self._intersect_clicked)
        self.opening_button.clicked.connect(self._opening_clicked)
        self.inverse_button.clicked.connect(self._inverse_clicked)

    def _localmax_clicked(self):
        """
        Localmax button clicked
        """
        new_dialog = LocalMaxDialog(self._model, self._main_win)
        new_dialog.exec_()

    def _intersect_clicked(self):
        """
        Make a intersection between two layers.
        """
        new_dialog = IntersectDialog(self._model)
        new_dialog.exec_()

    def _opening_clicked(self):
        new_dialog = OpenDialog(self._model)
        new_dialog.exec_()

    def _inverse_clicked(self):
        inverse_image(self._model)

