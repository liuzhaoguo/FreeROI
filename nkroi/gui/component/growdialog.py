# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from nkroi.algorithm import math


class GrowDialog(QDialog):
    """
    A dialog for region grow options.
    
    """

    def __init__(self, model, parent=None):
        super(GrowDialog, self).__init__(parent)

        self._model = model
        self._init_gui()
        self._create_actions()

    def _init_gui(self):
        self.setWindowTitle("Region Grow")

        seed_label = QLabel("Seed")
        self.seed_combo = QComboBox()
        source_label = QLabel("Source")
        self.source_combo = QComboBox()
        vol_list = self._model.getItemList()
        self.seed_combo.addItems(QStringList(vol_list))
        self.source_combo.addItems(QStringList(vol_list))
        lbl_label = QLabel("Label?")
        self.lbl_check = QCheckBox()
        out_label = QLabel("Output")
        self.out_edit = QLineEdit()

        grid_layout = QGridLayout()
        grid_layout.addWidget(seed_label, 0, 0)
        grid_layout.addWidget(self.seed_combo, 0, 1)
        grid_layout.addWidget(source_label, 1, 0)
        grid_layout.addWidget(self.source_combo, 1, 1)
        grid_layout.addWidget(out_label, 2, 0)
        grid_layout.addWidget(self.out_edit, 2, 1)
        grid_layout.addWidget(lbl_label, 3, 0)
        grid_layout.addWidget(self.lbl_check, 3, 1)

        self.run_button = QPushButton("Run")
        self.cancel_button = QPushButton("Cancel")

        hbox_layout = QHBoxLayout()
        hbox_layout.addWidget(self.run_button)
        hbox_layout.addWidget(self.cancel_button)

        vbox_layout = QVBoxLayout()
        vbox_layout.addLayout(grid_layout)
        vbox_layout.addLayout(hbox_layout)

        self.setLayout(vbox_layout)
        
    def _create_actions(self):
        self.run_button.clicked.connect(self._region_grow)
        self.cancel_button.clicked.connect(self.done)

    def _region_grow(self):
        vol_name = str(self.out_edit.text())
        if not vol_name:
            QMessageBox.critical(self, "No output volume name",
                    "Please specify output volume's name")
            return

        seed_row = self.seed_combo.currentIndex()
        source_row = self.source_combo.currentIndex()
        seed_data = self._model.data(self._model.index(seed_row),
                                     Qt.UserRole + 5)
        source_data = self._model.data(self._model.index(source_row),
                                       Qt.UserRole + 5)
        new_vol = math.region_grow(seed_data, source_data,
                                   self.lbl_check.isChecked())
        colormap = self.lbl_check.isChecked() and 'label' or 'gray'
        self._model.addItem((new_vol,
                             self._model._data[source_row].label_config,
                             vol_name,
                             self._model._data[0].get_header(),
                             None, None, 255, colormap))
        self.done(0)

