# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""A viewer (part of Qt model-view-delegate classes) for layer selection 
and parameters alternating.

"""

import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from nkbp.algorithm..array2qimage import idx2rgb
from drawsettings import DrawSettings
from ..base.labelconfig import LabelConfig
from labelconfigcenter import *

class LayerView(QWidget):
    """
    Implementation a widget for layer selection and parameters alternating.

    Inherits QWidget.

    """
    current_changed = pyqtSignal()

    builtin_colormap = ['gray', 'red2yellow', 'blue2cyanblue', 'red', 'green', 'blue', 'rainbow', 'single ROI']

    def __init__(self, label_config_center,parent=None):
        """
        Initialize the widget.

        """
        super(LayerView, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
#add by dxb 
        self.setMaximumWidth(230)
        # Get module path
        module_path = os.path.dirname(os.path.join(os.getcwd(), __file__))
        temp = module_path.split('/')
        temp.pop()
        temp.append('icon')
        self._icon_dir = '/'.join(temp)
        self.label_config_center = label_config_center

        # initialize the model
        self._model = None
        self._init_gui()

    def _init_gui(self):
        """
        Initialize a GUI designation.

        """
        # initialize QListView
        self._list_view = QListView()
        # initialize up/down push button
#add by dxb      
        button_size=QSize(12,12)

        self._up_button = QPushButton()
        self._up_button.setIcon(QIcon(os.path.join(
                            self._icon_dir, 'arrow_up.png'))) 
        self._up_button.setIconSize(button_size)
        self._down_button = QPushButton()
        self._down_button.setIcon(QIcon(os.path.join(
                            self._icon_dir, 'arrow_down.png')))
        self._down_button.setIconSize(button_size)
     
        # layout config for list_view panel
        button_layout = QHBoxLayout()


       # button_layout.addWidget(self._up_button)
       # button_layout.addWidget(self._down_button)
        
        # initialize parameter selection widgets
        visibility_label = QLabel('Visibility')
        self._visibility = QSlider(Qt.Horizontal)
        self._visibility.setMinimum(0)
        self._visibility.setMaximum(100)
        self._visibility.setSingleStep(5)

        button_layout.addWidget(visibility_label)    
        button_layout.addWidget(self._visibility)

        button_layout.addWidget(self._up_button)
        button_layout.addWidget(self._down_button)

        max_label = QLabel('Max:')
        self._view_max = QLineEdit()
        min_label = QLabel('Min:')
        self._view_min = QLineEdit()
        colormap_label = QLabel('Colormap:')
        self._colormap = QComboBox()
        colormaps = self.builtin_colormap + self.label_config_center.get_all_labelconfig_names()
        self._colormap.addItems(colormaps)

        # initialize parameter selection panel
        grid_layout = QGridLayout()
        grid_layout.addWidget(colormap_label, 1, 0)
        grid_layout.addWidget(self._colormap, 1, 1, 1, 3)


        para_layout = QHBoxLayout()
        para_layout.addWidget(min_label)
        para_layout.addWidget(self._view_min)
        para_layout.addWidget(max_label)
        para_layout.addWidget(self._view_max)
        


        list_view_layout = QVBoxLayout()
        list_view_layout.addWidget(self._list_view)
        list_view_layout.addLayout(button_layout)
        list_view_layout.addLayout(para_layout) 
        list_view_layout.addLayout(grid_layout)

        #label config center
        labcon_panel=self.label_config_center
        # initialize cursor coord&value widgets
        xyz_layout=QHBoxLayout()
        coord_x_label = QLabel('x: ')
        self._coord_x = QLineEdit()
        self._coord_x.setReadOnly(True)
        coord_y_label = QLabel('y: ')
        self._coord_y = QLineEdit()
        self._coord_y.setReadOnly(True)
        coord_z_label = QLabel('z: ')
        self._coord_z = QLineEdit()
        self._coord_z.setReadOnly(True)
        xyz_layout.addWidget(coord_x_label)
        xyz_layout.addWidget(self._coord_x)
        xyz_layout.addWidget(coord_y_label)
        xyz_layout.addWidget(self._coord_y)
        xyz_layout.addWidget(coord_z_label)
        xyz_layout.addWidget(self._coord_z)

        
        coord_value_label = QLabel('value:')
        self._coord_value = QLineEdit()
        self._coord_value.setReadOnly(True)
        coord_label_label = QLabel('label:')
        self._coord_label = QLineEdit()
        self._coord_label.setReadOnly(True)
        
        glayout = QGridLayout()
        glayout.addLayout(xyz_layout,0,0,1,6)    
        glayout.addWidget(coord_value_label,1,0)
        glayout.addWidget(self._coord_value,1,1,1,5)
        glayout.addWidget(coord_label_label,2,0)
        glayout.addWidget(self._coord_label,2,1,1,5)
       
        self._cursor_info_panel = QGroupBox('Cursor')
        self._cursor_info_panel.setLayout(glayout)

        # layout config of whole widget
        self.setLayout(QVBoxLayout())
        self.layout().addLayout(list_view_layout)
        self.layout().addWidget(labcon_panel)
        self.layout().addWidget(self._cursor_info_panel)

    def setModel(self, model):
        """
        Set model of the viewer.

        """
        if isinstance(model, QAbstractListModel):
            self._model = model
            self._list_view.setModel(model)
            self._create_actions()
        else:
            raise ValueError('Input must be a ListModel!')

    def _create_actions(self):
        """
        Create several necessay actions.

        """
        # When select one item, display specific parameters
        self._list_view.selectionModel().currentChanged.connect(
                                            self._disp_current_para)
        # When select one item, display its undo/redo settings
        self._list_view.selectionModel().currentChanged.connect(
                self.current_changed)
        

        # When dataset changed, refresh display.
        self._model.dataChanged.connect(self._disp_current_para)

        # When add new item, refresh display.
        self._model.rowsInserted.connect(self._disp_current_para)
        
        # When remove new item, refresh display.
        self._model.rowsRemoved.connect(self._disp_current_para)

        # When layout changed, refresh display.
        self._model.layoutChanged.connect(self._disp_current_para)

        # Config setting actions
        self._view_min.editingFinished.connect(self._set_view_min)
        self._view_max.editingFinished.connect(self._set_view_max)
        self._colormap.currentIndexChanged.connect(self._set_colormap)
        self._visibility.sliderReleased.connect(self._set_alpha)
        self._up_button.clicked.connect(self._up_action)
        self._down_button.clicked.connect(self._down_action)

    def _disp_current_para(self):
        """
        Display current model's parameters.

        """
        index = self._list_view.currentIndex()

        if index.row() != -1:
            # set up status of up/down button
            if index.row() == 0:
                self._up_button.setEnabled(False)
            else:
                self._up_button.setEnabled(True)
            if index.row() == (self._model.rowCount() - 1):
                self._down_button.setEnabled(False)
            else:
                self._down_button.setEnabled(True)

            # min/max value
            self._view_min.setText(str(self._model.data(index, Qt.UserRole)))
            self._view_max.setText(str(
                self._model.data(index, Qt.UserRole + 1)))
        
            # colormap combo box setting
            cur_colormap = self._model.data(index, Qt.UserRole + 3)
            if isinstance(cur_colormap, LabelConfig):
                cur_colormap = cur_colormap.get_name()
            idx = self._colormap.findText(cur_colormap)
            self._colormap.setCurrentIndex(idx)
        
            # alpha slider setting
            current_alpha = self._model.data(index, Qt.UserRole + 2) * \
                    100 / 255
            self._visibility.setValue(current_alpha)
        
            self._list_view.setFocus()

            # Set current index
            self._model.setCurrentIndex(self._list_view.currentIndex())
            self._model.setSelectedIndexes()
        
    def _set_view_min(self):
        """
        Set current selected item's view_min value.

        """
        index = self._list_view.currentIndex()
        value = self._view_min.text()
        if value == '':
            self._view_min.setText(str(self._model.data(index, Qt.UserRole)))
        else:
            self._model.setData(index, value, role=Qt.UserRole)

    def _set_view_max(self):
        """
        Set current selected item's view_max value.

        """
        index = self._list_view.currentIndex()
        value = self._view_max.text()
        if value == '':
            self._view_max.setText(str(self._model.data(index, Qt.UserRole+1)))
        else:
            self._model.setData(index, value, role=Qt.UserRole + 1)

    def _set_colormap(self):
        """
        Set colormap of current selected item.

        """
        index = self._list_view.currentIndex()
        value = self._colormap.currentText()
        builtin_len = len(self.builtin_colormap)
        row = self._colormap.currentIndex()
        if row >= builtin_len:
            value = self.label_config_center.get_label_config(row - builtin_len)
        self._model.setData(index, value, role=Qt.UserRole + 3)

    def _set_alpha(self):
        """
        Set alpha value of current selected item.

        """
        index = self._list_view.currentIndex()
        value = self._visibility.value() * 255 / 100
        self._model.setData(index, value, role=Qt.UserRole + 2)

    def _up_action(self):
        """
        Move selected item up for one step.

        """
        index = self._list_view.currentIndex()
        self._model.moveUp(index.row())
        index = self._list_view.currentIndex()
        if index.row() == 0:
            self._up_button.setEnabled(False)
        else:
            self._up_button.setEnabled(True)
        if index.row() == (self._model.rowCount() - 1):
            self._down_button.setEnabled(False)
        else:
            self._down_button.setEnabled(True)
        self._list_view.setFocus()

    def _down_action(self):
        """
        Move selected item down for one step.

        """
        index = self._list_view.currentIndex()
        self._model.moveDown(index.row())
        index = self._list_view.currentIndex()
        if index.row() == 0:
            self._up_button.setEnabled(False)
        else:
            self._up_button.setEnabled(True)
        if index.row() == (self._model.rowCount() - 1):
            self._down_button.setEnabled(False)
        else:
            self._down_button.setEnabled(True)
        self._list_view.setFocus()

    def currentRow(self):
        """
        Return the row of current selected item.

        """
        return self._list_view.currentIndex().row()

    def setCurrentIndex(self, index):
        """
        Set selected item.

        """
        self._list_view.setCurrentIndex(index)

    def update_xyzvl(self, xyzvl):
        self._coord_x.setText(xyzvl['x'])
        self._coord_y.setText(str(108 - int(xyzvl['y'])))
        self._coord_z.setText(xyzvl['z'])
        self._coord_value.setText(xyzvl['value'])
        self._coord_label.setText(xyzvl['label'])
