# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""Graphic User Interface.

"""

import os
import ConfigParser
import glob
import nkbp as src_pkg

from nkbp.version import __version__

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from base.labelconfig import LabelConfig
from component.listwidget import LayerView
from component.gridwidget import GridView
from component.orthwidget import OrthView
from component.datamodel import VolumeListModel
from component.imagelabel import ImageLabel
from component.drawsettings import PainterStatus, ViewSettings, MoveSettings
from component.labeldialog import LabelDialog
from component.eraserdialog import EraserDialog
from component.watersheddialog import WatershedDialog
from component.intersectdialog import IntersectDialog
from component.growdialog import GrowDialog
from component.autolabeldialog import AutoLabelDialog
from component.opendialog import OpenDialog
from component.localmaxdialog import LocalMaxDialog
from component.labelconfigcenter import LabelConfigCenter
from component.roifilterdialog import ROIFilterDialog
from component.roilabeldialog import ROILabelDialog
from component.roieraserdialog import ROIEraserDialog
from component.roimergedialog import ROIMergeDialog
from component.roidialog import ROIDialog

class BpMainWindow(QMainWindow):
    """Class BpMainWindow provides UI interface of PyBP.

    Example:
    --------

    >>> from PyQt4.QtGui import QApplication
    >>> import main
    >>> app = QApplication([])
    >>> win = main.BpMainWindow()
    ......
    >>> win.show()
    >>> app.exec_()

    """
    temp_path = os.path.dirname(os.path.join(os.getcwd(), __file__))
    temp_path = temp_path.split('/')
    temp_path.pop()
    temp_path.append('data')
    label_path = '/'.join(temp_path)
    label_config_dir = os.path.join(label_path, 'labelconfig')
    label_config_suffix = 'lbl'
    config_file = 'pybpconfig.lbl'

    def __init__(self, parent=None):
        """
        Initialize an instance of BpMainWindow.
        
        """
        # Inherited from QMainWindow
        super(BpMainWindow, self).__init__(parent)

        # Get module path
        module_path = os.path.dirname(os.path.join(os.getcwd(), __file__))
        self._icon_dir = os.path.join(module_path, 'icon')
        
        # set window title
        self.setWindowTitle('PyBP')
        #self.resize(1280, 1000)
        self.center()
        # set window icon
        self.setWindowIcon(QIcon(os.path.join(self._icon_dir, 'icon.png')))

        self._init_configuration()
        self._init_label_config_center()
        # create actions
        self._create_actions()
        # create menus
        self._create_menus()

        # temporary variable
        self._temp_dir = None

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _init_configuration(self):
        config_file = os.path.expanduser('~/.pybp.conf')
        if os.path.exists(config_file):
            config = ConfigParser.RawConfigParser()
            config.read(config_file)
            self.window_width = config.getint('width', 'int')
            self.window_height = config.getint('height', 'int')
            self.orth_scale_factor = config.getint('orth_scale', 'int')
            self.grid_scale_factor = config.getint('grid_scale', 'int')
            self.window_xpos = config.getint('xpos', 'int')
            self.window_ypos = config.getint('ypos', 'int')

            self.resize(self.window_width, self.window_height)
            self.move(self.window_xpos, self.window_ypos)
            self.default_orth_scale_factor = float(self.orth_scale_factor) / 100
            self.default_grid_scale_factor = float(self.grid_scale_factor) / 100
        else:
            self.setWindowState(Qt.WindowMaximized)
            self.default_orth_scale_factor = 1.0
            self.default_grid_scale_factor = 2.0

    def _save_configuration(self):
        config_file = os.path.expanduser('~/.pybp.conf')

        config = ConfigParser.RawConfigParser()
        config.add_section('width')
        config.add_section('height')
        config.add_section('orth_scale')
        config.add_section('grid_scale')
        config.add_section('xpos')
        config.add_section('ypos')
        config.set('width', 'int', self.width())
        config.set('height', 'int', self.height())
        config.set('xpos', 'int', self.x())
        config.set('ypos', 'int', self.y())
        if hasattr(self, 'model'):
            config.set('orth_scale', 'int', int(self.model.get_scale_factor('orth')*100))
            config.set('grid_scale', 'int', int(self.model.get_scale_factor('grid')*100))
        else:
            config.set('orth_scale', 'int', int(self.default_orth_scale_factor * 100))
            config.set('grid_scale', 'int', int(self.default_grid_scale_factor * 100))

        with open(config_file, 'wb') as conf:
            config.write(conf)

    def closeEvent(self, e):
        self._save_configuration()
        e.accept()

    def _create_actions(self):
        """
        Create actions.

        """
        # create a dictionary to store actions info
        self._actions = {}
        
        # Open template action
        self._actions['add_template'] = QAction(QIcon(os.path.join(
                                            self._icon_dir, 'open.png')),
                                            self.tr("&Open standard volume"), 
                                            self)
        self._actions['add_template'].setShortcut(self.tr("Ctrl+O"))
        self._actions['add_template'].triggered.connect(self._add_template)

        # Add a new image action
        self._actions['add_image'] = QAction(QIcon(os.path.join(
                                                self._icon_dir,'add.png')),
                                             self.tr("&Add volume"), self)
        self._actions['add_image'].setShortcut(self.tr("Ctrl+A"))
        self._actions['add_image'].triggered.connect(self._add_image)
        self._actions['add_image'].setEnabled(True)

        # Remove an image
        self._actions['remove_image'] = QAction(QIcon(os.path.join(
                                                self._icon_dir, 'remove.png')),
                                                self.tr("&Remove volume"), 
                                                self)
        self._actions['remove_image'].setShortcut(self.tr("Ctrl+R"))
        self._actions['remove_image'].triggered.connect(self._remove_image)
        self._actions['remove_image'].setEnabled(False)

        # New image
        self._actions['new_image'] = QAction(QIcon(os.path.join(
                                                self._icon_dir, 'create.png')),
                                             self.tr("&New volume"), self)
        self._actions['new_image'].setShortcut(self.tr("Ctrl+N"))
        self._actions['new_image'].setEnabled(False)
        self._actions['new_image'].triggered.connect(self.__new_image)

        # Save image
        self._actions['save_image'] = QAction(QIcon(os.path.join(
                                                self._icon_dir, 'save.png')),
                                              self.tr("&Save volume as..."), 
                                              self)
        self._actions['save_image'].setShortcut(self.tr("Ctrl+S"))
        self._actions['save_image'].triggered.connect(self._save_image)
        self._actions['save_image'].setEnabled(False)

        # Load Label Config
        self._actions['ld_lbl'] = QAction('Load Label', self)
        self._actions['ld_lbl'].triggered.connect(self._ld_lbl)
        self._actions['ld_lbl'].setEnabled(False)

        # Load Global Label Config
        self._actions['ld_glbl'] = QAction('Load Global Label', self)
        self._actions['ld_glbl'].triggered.connect(self._ld_glbl)
        self._actions['ld_glbl'].setEnabled(False)

        # Close display
        self._actions['close'] = QAction(self.tr("Close"), self)
        #self._actions['close'].setShortcut(self.tr("Ctrl+W"))
        self._actions['close'].triggered.connect(self._close_display)
        self._actions['close'].setEnabled(False)

        # Quit action
        self._actions['quit'] = QAction(QIcon(os.path.join(
                                            self._icon_dir, 'quit.png')),
                                        self.tr("&Quit"), self)
        self._actions['quit'].setShortcut(self.tr("Ctrl+Q"))
        self._actions['quit'].triggered.connect(self.close)

        # Grid view action
        self._actions['grid_view'] = QAction(QIcon(os.path.join(
                                               self._icon_dir, 'gridview.png')),
                                             self.tr("Lightbox"), self)
        self._actions['grid_view'].triggered.connect(self._grid_view)
        self._actions['grid_view'].setEnabled(False)

        # Orth view action
        self._actions['orth_view'] = QAction(QIcon(os.path.join(
                                               self._icon_dir, 'orthview.png')),
                                             self.tr("Orthographic"), self)
        self._actions['orth_view'].triggered.connect(self._orth_view)
        self._actions['orth_view'].setEnabled(False)

        # return original size
        self._actions['original_view'] = QAction(QIcon(os.path.join(
                                                self._icon_dir, 
                                                'original_size.png')),
                                             self.tr("Reset view"), self)
        self._actions['original_view'].triggered.connect(self._reset_view)
        self._actions['original_view'].setEnabled(False)

        # About PyBP
        self._actions['about_pybp'] = QAction(self.tr("About PyBP"), self)
        self._actions['about_pybp'].triggered.connect(self._about_pybp)

        # About Qt
        self._actions['about_qt'] = QAction(QIcon(os.path.join(
                                                self._icon_dir, 'qt.png')),
                                            self.tr("About Qt"), self)
        self._actions['about_qt'].triggered.connect(qApp.aboutQt)
        
        # Hand
        self._actions['hand'] = QAction(QIcon(os.path.join(self._icon_dir,
                                                           'hand.png')),
                                              self.tr("Hand"), self)
        self._actions['hand'].triggered.connect(self._hand_enable)
        self._actions['hand'].setCheckable(True)
        self._actions['hand'].setChecked(False)
        self._actions['hand'].setEnabled(False)

        # Cursor
        self._actions['cursor'] = QAction(QIcon(os.path.join(
                                            self._icon_dir, 'cursor.png')),
                                          self.tr("Cursor"), self)
        self._actions['cursor'].triggered.connect(self._cursor_enable)
        self._actions['cursor'].setCheckable(True)
        self._actions['cursor'].setChecked(True)
        self._actions['cursor'].setEnabled(True)
        
        # Brush
        self._actions['brush'] = QAction(QIcon(os.path.join(
                                            self._icon_dir, 'brush.png')),
                                         self.tr("Voxel Edit"), self)
        self._actions['brush'].triggered.connect(self._brush_enable)
        self._actions['brush'].setCheckable(True)
        self._actions['brush'].setChecked(False)

        # ROI Brush
        self._actions['roibrush'] = QAction(QIcon(os.path.join(
                                            self._icon_dir, 'roibrush.png')),
                                            self.tr("ROI Edictor"), self)
        self._actions['roibrush'].triggered.connect(self._roibrush_enable)
        self._actions['roibrush'].setCheckable(True)
        self._actions['roibrush'].setChecked(False)

        self._update_brush()

        self._actions['roidialog'] = QAction(QIcon(os.path.join(
                                             self._icon_dir,'roitool.png')),
                                             self.tr("ROI Toolset"), self)
        self._actions['roidialog'].setCheckable(True)
        self._actions['roidialog'].triggered.connect(self._roidialog_enable)

        # Undo
        self._actions['undo'] = QAction(QIcon(os.path.join(
                                            self._icon_dir, 'undo.png')),
                                        self.tr("Undo"), self)
        self._actions['undo'].triggered.connect(self._undo)

        # Redo
        self._actions['redo'] = QAction(QIcon(os.path.join(
                                            self._icon_dir, 'redo.png')),
                                        self.tr("Redo"), self)
        self._actions['redo'].triggered.connect(self._redo)
        
        # Intersect
        self._actions['intersect'] = QAction(QIcon(os.path.join(
                                             self._icon_dir, 'intersect.png')),
                                             self.tr("Intersection"), self)
        self._actions['intersect'].triggered.connect(self._intersect)
        self._actions['intersect'].setEnabled(False)

        # Watershed
        self._actions['watershed'] = QAction(QIcon(os.path.join(
                                             self._icon_dir, 'watershed.png')),
                                             self.tr("Watershed"), self)
        self._actions['watershed'].setEnabled(False)
        self._actions['watershed'].triggered.connect(self._watershed)
        self._actions['watershed'].setShortcut(self.tr("Ctrl+W"))

        # Region Grow
        self._actions['grow'] = QAction(QIcon(os.path.join(
                                            self._icon_dir, 'grow.png')),
                                        self.tr("Region Grow"), self)
        self._actions['grow'].triggered.connect(self._grow)
        self._actions['grow'].setEnabled(False)
        
        # Auto Labeling
        self._actions['auto_label'] = QAction(QIcon(os.path.join(
                                        self._icon_dir, 'auto_labeling.png')),
                                    self.tr("Auto Labeling"), self)
        self._actions['auto_label'].triggered.connect(self._auto_label)
        self._actions['auto_label'].setEnabled(False)

        # Open
        self._actions['open'] = QAction(QIcon(os.path.join(
                                        self._icon_dir, 'opening.png')),
                                        self.tr("Opening"), self)
        self._actions['open'].setShortcut("Ctrl+P")
        self._actions['open'].triggered.connect(self._open)
        self._actions['open'].setEnabled(False)

        # Local Max
        self._actions['lmax'] = QAction(QIcon(os.path.join(
                                        self._icon_dir, 'localmax.png')),
                                        self.tr("Local Max"), self)
        self._actions['lmax'].setShortcut("Ctrl+L")
        self._actions['lmax'].triggered.connect(self._lmax)
        self._actions['lmax'].setEnabled(False)

        # ROI filter
        self._actions['roifilter'] = QAction(QIcon(os.path.join(
                                        self._icon_dir, 'filtering.png')),self.tr("ROI Filtering"), self)
        self._actions['roifilter'].setShortcut("Ctrl+F")
        self._actions['roifilter'].triggered.connect(self._roifilter)
        self._actions['roifilter'].setEnabled(False)

        # ROI merge
        self._actions['roimerge'] = QAction(QIcon(os.path.join(
                                        self._icon_dir, 'merging.png')),
                                        self.tr("ROI Merging"), self)
        self._actions['roimerge'].setShortcut("Ctrl+M")
        self._actions['roimerge'].triggered.connect(self._roimerge)
        self._actions['roimerge'].setEnabled(False)

    def _add_toolbar(self):
        """
        Add toolbar.

        """
        # Initialize a spinbox for zoom-scale selection
        self._spinbox = QSpinBox()
        self._spinbox.setMaximum(500)
        self._spinbox.setMinimum(50)
        self._spinbox.setSuffix('%')
        self._spinbox.setSingleStep(10)
        self._spinbox.setValue(self.default_grid_scale_factor * 100)
        self._spinbox.valueChanged.connect(self._set_scale_factor)

        # Add a toolbar
        self._toolbar = QToolBar()
        #self._toolbar.addWidget(self._spinbox)
      
        # Add file actions
        self._toolbar.addAction(self._actions['add_image'])
        self._toolbar.addAction(self._actions['remove_image'])
        self._toolbar.addAction(self._actions['new_image'])
        self._toolbar.addAction(self._actions['save_image'])
        # Add view actions
        self._toolbar.addSeparator()
        self._toolbar.addAction(self._actions['grid_view'])
        self._toolbar.addAction(self._actions['orth_view'])
        self._toolbar.addAction(self._actions['original_view'])
        # Add draw tools
        self._toolbar.addSeparator()
        self._toolbar.addAction(self._actions['hand'])
        self._toolbar.addAction(self._actions['cursor'])
        self._toolbar.addAction(self._actions['brush'])
        self._toolbar.addAction(self._actions['roibrush'])
        # Add undo redo
        self._toolbar.addSeparator()
        self._toolbar.addAction(self._actions['undo'])
        self._toolbar.addAction(self._actions['redo'])
        # Add automatic tools
        self._toolbar.addSeparator()
        self._toolbar.addAction(self._actions['intersect'])
        self._toolbar.addAction(self._actions['open'])
        self._toolbar.addAction(self._actions['lmax'])
        self._toolbar.addAction(self._actions['watershed'])
        self._toolbar.addAction(self._actions['roifilter'])
        self._toolbar.addAction(self._actions['roimerge'])
        self._toolbar.addAction(self._actions['roidialog'])
        

        self._toolbar.addSeparator() 
        self._toolbar.addWidget(self._spinbox)

#add by dang begin 
        # initialize cursor coord&value widgets
       
        self._toolbar.addSeparator()
        coord_x_label = QLabel('x: ')
        self._coord_x = QLineEdit()
        self._coord_x.setFixedWidth(30)
        self._coord_x.setReadOnly(True)
        coord_y_label = QLabel('y: ')
        self._coord_y = QLineEdit()
        self._coord_y.setFixedWidth(30)
        self._coord_y.setReadOnly(True)
        coord_z_label = QLabel('z: ')
        self._coord_z = QLineEdit()
        self._coord_z.setFixedWidth(30)
        self._coord_z.setReadOnly(True)
        
        coord_value_label = QLabel('value:')
        self._coord_value = QLineEdit()
        self._coord_value.setFixedWidth(50)
        self._coord_value.setReadOnly(True)
        coord_label_label = QLabel('label:')
        self._coord_label = QLineEdit()
        self._coord_label.setFixedWidth(80)
        self._coord_label.setReadOnly(True)
        
        self._toolbar.addWidget(coord_label_label)
        self._toolbar.addWidget(self._coord_label)
        self._toolbar.addWidget(coord_value_label)
        self._toolbar.addWidget(self._coord_value)
        
        self._toolbar.addSeparator()
        self._toolbar.addWidget(coord_x_label)
        self._toolbar.addWidget(self._coord_x)
        self._toolbar.addWidget(coord_y_label)
        self._toolbar.addWidget(self._coord_y)
        self._toolbar.addWidget(coord_z_label)
        self._toolbar.addWidget(self._coord_z)
        
        self._toolbar.addSeparator()
        
#end
        self.addToolBar(self._toolbar)

    def _update_xyzvl_toolbar(self, xyzvl):
        self._coord_x.setText(xyzvl['x'])
        self._coord_y.setText(str(108 - int(xyzvl['y'])))
        self._coord_z.setText(xyzvl['z'])
        self._coord_value.setText(xyzvl['value'])
        self._coord_label.setText(xyzvl['label'])

    def _set_scale_factor(self, value):
        """
        Set scale factor.

        """
        value = float(value) / 100
        self.model.set_scale_factor(value, self.image_view.display_type())
        #print self.model.get_scale_factor(self.image_view.display_type())

    def _add_template(self):
        """
        Open a dialog window and select a template file.

        """
        tmp_dir = os.path.dirname(src_pkg.__file__)
        template_dir = os.path.join(tmp_dir, 'data', 'standard', 
                                    'MNI152_T1_2mm_brain.nii.gz')
        template_name = QFileDialog.getOpenFileName(
                                        self,
                                        'Open standard file',
                                        template_dir,
                                        'Nifti files (*.nii.gz *.nii)')
        if not template_name.isEmpty():
            template_path = str(template_name)
            self._add_template_img(template_path)

    def _add_template_img(self, source, name=None, header=None, view_min=None, 
                          view_max=None, alpha=255, colormap='gray'):
        """
        Add template image.

        """
        self._init_label_config_center()

        self.model = VolumeListModel([], self._label_config_center)
        self.model.set_scale_factor(self.default_grid_scale_factor, 'grid')
        self.model.set_scale_factor(self.default_orth_scale_factor, 'orth')
        self.painter_status = PainterStatus(ViewSettings())

        template_path = str(source)
        #label_config = self._get_label_config(template_path)
        if self.model.addItem(template_path, None, name, header,
                              view_min, view_max, alpha, colormap):
            # initialize views and model
            self.list_view = LayerView(self._label_config_center)
            self.list_view.setModel(self.model)
            self.image_view = GridView(self.model, self.painter_status)

            # initialize display layout
            central_widget = QWidget()
            layout = QHBoxLayout()
            central_widget.setLayout(layout)
            central_widget.layout().addWidget(self.list_view)
            central_widget.layout().addWidget(self.image_view)
            self.setCentralWidget(central_widget)

            # add a toolbar
            self._add_toolbar()

            # change button status
            self._actions['add_template'].setEnabled(False)
            #self._actions['add_image'].setEnabled(True)
            self._actions['save_image'].setEnabled(True)
            self._actions['ld_lbl'].setEnabled(True)
            self._actions['ld_glbl'].setEnabled(True)
            self._actions['new_image'].setEnabled(True)
            self._actions['close'].setEnabled(True)
            self._actions['orth_view'].setEnabled(True)
            self._actions['original_view'].setEnabled(True)

            self._actions['undo'].setEnabled(False)
            self._actions['redo'].setEnabled(False)
            self.list_view.current_changed.connect(self._update_undo)
            self.list_view.current_changed.connect(self._update_redo)
            
            self.list_view.current_changed.connect(self._current_layer_xyzvl_changed)

            self.model.undo_stack_changed.connect(self._update_undo)
            self.model.redo_stack_changed.connect(self._update_redo)

            self._actions['watershed'].setEnabled(True)
            self.list_view.setCurrentIndex(self.model.index(0))

            # update_xyzvl when necessarily
            self.image_view.xyz_updated.connect(self._update_xyzvl)
            self.image_view.xyz_updated.emit([self.model.get_current_pos()[1],
                                              self.model.get_current_pos()[0],
                                              self.model.get_current_pos()[2]])
            # Enable cursor tracking
            #self.list_view._list_view.selectionModel().currentChanged.connect(
            #                                    self._switch_cursor_status)
        else:
            QMessageBox.information(self, 'PyBP', 
                    'Cannot load ' + template_name + '.')

    def _add_image(self):
        """
        Add new item.

        """
        if self._temp_dir == None:
            temp_dir = QDir.currentPath()
        else:
            temp_dir = self._temp_dir
        file_name = QFileDialog.getOpenFileName(self,
                                                'Add new file',
                                                temp_dir,
                                                'Nifti files (*.nii.gz *.nii)')
        if not file_name.isEmpty():
            file_path = str(file_name)
            self._add_img(file_path)

    def _add_img(self, source, name=None, header=None, view_min=None,
                 view_max=None, alpha=255, colormap='gray'):
        """
        Add extra image.

        """
        file_path = str(source)
        self._temp_dir = os.path.dirname(file_path)
        if self.model.addItem(file_path, None, name, header, view_min,
                              view_max, alpha, colormap):
            self._actions['remove_image'].setEnabled(True)
            self._actions['intersect'].setEnabled(True)
            self._actions['auto_label'].setEnabled(True)
            self._actions['grow'].setEnabled(True)
            self._actions['open'].setEnabled(True)
            self._actions['lmax'].setEnabled(True)
            self._actions['roifilter'].setEnabled(True)
            self._actions['roimerge'].setEnabled(True)
            self.list_view.setCurrentIndex(self.model.index(0))
        else:
            QMessageBox.information(self,'PyBP', 'Cannot load '+file_name + '.')

    def __new_image(self):
        self._new_image()

    def _new_image(self, data=None, name=None, colormap=None):
        """
        Create a new volume for brain parcellation.

        """
        if colormap is None:
            colormap = self._label_config_center.get_first_label_config()
        self.model.new_image(data, name, None, colormap)
        self.list_view.setCurrentIndex(self.model.index(0))

        # change button status
        self._actions['remove_image'].setEnabled(True)
        self._actions['intersect'].setEnabled(True)
        self._actions['grow'].setEnabled(True)
        self._actions['auto_label'].setEnabled(True)
        self._actions['open'].setEnabled(True)
        self._actions['lmax'].setEnabled(True)
        self._actions['roifilter'].setEnabled(True)
        self._actions['roimerge'].setEnabled(True)
        
    def new_image_action(self):
        self._actions['remove_image'].setEnabled(True)
        self._actions['intersect'].setEnabled(True)
        self._actions['grow'].setEnabled(True)
        self._actions['auto_label'].setEnabled(True)
        self._actions['open'].setEnabled(True)
        self._actions['lmax'].setEnabled(True)
        self._actions['roifilter'].setEnabled(True)
        self._actions['roimerge'].setEnabled(True)

    def _remove_image(self):
        """
        Remove current image.

        """
        row = self.list_view.currentRow()
        self.model.delItem(row)
        if self.model.rowCount() == 1:
            self._actions['remove_image'].setEnabled(False)
            self._actions['intersect'].setEnabled(False)
            self._actions['grow'].setEnabled(False)
            self._actions['auto_label'].setEnabled(False)
            self._actions['open'].setEnabled(False)
            self._actions['lmax'].setEnabled(False)
            self._actions['roifilter'].setEnabled(False)
            self._actions['roimerge'].setEnabled(False)

    def _save_image(self):
        """
        Save image as a nifti file.

        """
        index = self.model.currentIndex()
        if self._temp_dir == None:
            temp_dir = str(QDir.currentPath())
        else:
            temp_dir = self._temp_dir
        file_path = os.path.join(temp_dir, 
                        str(self.model.data(index, Qt.DisplayRole))+'.nii.gz')
        path = QFileDialog.getSaveFileName(
                                self,
                                'Save image as...',
                                file_path,
                                'Nifti files (*.nii.gz *.nii)')
        if not path.isEmpty():
            self._temp_dir = os.path.dirname(str(path))
            self.model._data[index.row()].save2nifti(str(path))

    def _close_display(self):
        """
        Close current display.

        """
        self.setCentralWidget(QWidget())
        self._set_scale_factor(self.default_grid_scale_factor)
        self.removeToolBar(self._toolbar)
        self._actions['add_template'].setEnabled(True)
        #self._actions['add_image'].setEnabled(True)
        self._actions['remove_image'].setEnabled(False)
        self._actions['new_image'].setEnabled(False)
        self._actions['save_image'].setEnabled(False)
        self._actions['ld_glbl'].setEnabled(False)
        self._actions['ld_lbl'].setEnabled(False)
        self._actions['close'].setEnabled(False)
        self._actions['intersect'].setEnabled(False)
        self._actions['grow'].setEnabled(False)
        self._actions['auto_label'].setEnabled(False)
        self._actions['watershed'].setEnabled(False)
        self._actions['open'].setEnabled(False)
        self._actions['lmax'].setEnabled(False)
        self._actions['grid_view'].setEnabled(False)
        self._actions['orth_view'].setEnabled(False)
        self._actions['original_view'].setEnabled(False)
        self._actions['roifilter'].setEnabled(False)
        self._actions['roimerge'].setEnabled(False)

    def _about_pybp(self):
        """
        About PyBP.

        """
        QMessageBox.about(self,
                          self.tr("About PyBP"),
                          self.tr("<p>the <b>PyBP</b> could make ROI manually"
                                  "and automatically.</p>"
                                  "<p>Version: " + __version__ + "</p>"))

    def _create_menus(self):
        """Create menus."""
        self.file_menu = self.menuBar().addMenu(self.tr("File"))
        self.file_menu.addAction(self._actions['add_template'])
        self.file_menu.addAction(self._actions['add_image'])
        self.file_menu.addAction(self._actions['save_image'])
        self.file_menu.addSeparator()
        self.file_menu.addAction(self._actions['ld_lbl'])
        self.file_menu.addAction(self._actions['ld_glbl'])
        self.file_menu.addSeparator()
        self.file_menu.addAction(self._actions['close'])
        self.file_menu.addAction(self._actions['quit'])

        self.volume_menu = self.menuBar().addMenu(self.tr("Volume"))
        self.volume_menu.addAction(self._actions['new_image'])
        self.volume_menu.addAction(self._actions['remove_image'])

        self.view_menu = self.menuBar().addMenu(self.tr("View"))
        self.view_menu.addAction(self._actions['grid_view'])
        self.view_menu.addAction(self._actions['orth_view'])
        self.view_menu.addAction(self._actions['original_view'])

        self.tool_menu = self.menuBar().addMenu(self.tr("Tools"))
        self.tool_menu.addAction(self._actions['intersect'])
        self.tool_menu.addAction(self._actions['grow'])
        self.tool_menu.addAction(self._actions['auto_label'])
        self.tool_menu.addAction(self._actions['watershed'])
        self.tool_menu.addAction(self._actions['open'])
        self.tool_menu.addAction(self._actions['lmax'])
        self.tool_menu.addAction(self._actions['roifilter'])
        self.tool_menu.addAction(self._actions['roimerge'])

        self.help_menu = self.menuBar().addMenu(self.tr("Help"))
        self.help_menu.addAction(self._actions['about_pybp'])
        self.help_menu.addAction(self._actions['about_qt'])

    def _cursor_enable(self):
        """
        Cursor enabled.

        """
        if self._actions['cursor'].isChecked():
            self._actions['brush'].setChecked(False)
            self._actions['roibrush'].setChecked(False)
            self._actions['cursor'].setChecked(True)
            if isinstance(self.image_view, OrthView):
                self._actions['hand'].setChecked(False)

            self.painter_status.set_draw_settings(ViewSettings())

            if hasattr(self, 'roidialog'):
                self._roidialog_disable()

            self.image_view.set_label_mouse_tracking(True)
        else:
            self._actions['cursor'].setChecked(True)

    def _brush_enable(self):
        """
        Brush enabled.

        """
        if self._actions['brush'].isChecked():
            self._actions['cursor'].setChecked(False)
            self._actions['roibrush'].setChecked(False)
            self._actions['brush'].setChecked(True)
            if isinstance(self.image_view, OrthView):
                self._actions['hand'].setChecked(False)

            if hasattr(self, 'roidialog'):
                self._roidialog_disable()

            self._label_config_center.set_is_roi_edit(False)
            self.painter_status.set_draw_settings(self._label_config_center)
            self.image_view.set_label_mouse_tracking(False)

        else:
            self._actions['brush'].setChecked(True)

    def _roibrush_enable(self):
        """
        ROI brush enabled.

        """
        if self._actions['roibrush'].isChecked():
            self._actions['cursor'].setChecked(False)
            self._actions['brush'].setChecked(False)
            self._actions['roibrush'].setChecked(True)

            if hasattr(self, 'roidialog'):
                self._roidialog_disable()

            self._label_config_center.set_is_roi_edit(True)
            self.painter_status.set_draw_settings(self._label_config_center)
            self.image_view.set_label_mouse_tracking(False)
        else:
            self._actions['roibrush'].setChecked(True)

    def _roidialog_enable(self):
        if not hasattr(self, 'roidialog'):
            self._actions['cursor'].setChecked(False)
            self._actions['brush'].setChecked(False)
            self._actions['roibrush'].setChecked(False)

            self._actions['roidialog'].setChecked(True)
            self.roidialog = ROIDialog(self.model)
            self.list_view._list_view.selectionModel().currentChanged.connect(
                self.roidialog.clear_rois)
            self.painter_status.set_draw_settings(self.roidialog)
            self.roidialog.finished.connect(self._roidialog_disable)
            self.roidialog.show()
        self._actions['roidialog'].setChecked(True)

    def _roidialog_disable(self):
        if hasattr(self, 'roidialog'):
            del self.roidialog
        self._actions['roidialog'].setChecked(False)

    def _hand_enable(self):
        """
        Hand enabled.

        """
        if self._actions['hand'].isChecked():
            self._actions['cursor'].setChecked(False)
            self._actions['brush'].setChecked(False)
            #self._actions['eraser'].setChecked(False)
            self._actions['hand'].setChecked(True)

            self.painter_status.set_draw_settings(MoveSettings())

            if hasattr(self, 'label_dialog'):
                self.label_dialog.done(0)
                del self.label_dialog
            if hasattr(self, 'eraser_dialog'):
                self.eraser_dialog.done(0)
                del self.eraser_dialog
            if hasattr(self, 'roilabel_dialog'):
                self.roilabel_dialog.done(0)
                del self.roilabel_dialog
            if hasattr(self, 'roieraser_dialog'):
                self.roieraser_dialog.done(0)
                del self.roieraser_dialog

            self.image_view.set_label_mouse_tracking(True)
        else:
            self._actions['hand'].setChecked(True)

    def _switch_cursor_status(self):
        self._actions['cursor'].setChecked(True)
        self._cursor_enable()

    def _watershed(self):
        watershed_dialog = WatershedDialog(self.model, self)
        watershed_dialog.exec_()

    def _repaint_slices(self):
        self.model.update_current_rgba()

    #def _roieraser_enable(self):
    #    """
    #    ROI Eraser enabled.

    #    """
    #    if self._actions['roieraser'].isChecked():
    #        self._actions['cursor'].setChecked(False)
    #        self._actions['brush'].setChecked(False)
    #        self._actions['eraser'].setChecked(False)
    #        self._actions['roibrush'].setChecked(False)
    #        self._actions['roieraser'].setChecked(True)

    #        if hasattr(self, 'label_dialog'):
    #            self.label_dialog.done(0)
    #            del self.label_dialog
    #        if hasattr(self, 'eraser_dialog'):
    #            self.eraser_dialog.done(0)
    #            del self.eraser_dialog
    #        if hasattr(self, 'roilabel_dialog'):
    #            self.roilabel_dialog.done(0)
    #            del self.roilabel_dialog

    #        self.roieraser_dialog = ROIEraserDialog(self)
    #        self.roieraser_dialog.show()
    #        self.painter_status.set_draw_settings(self.roieraser_dialog)
    #        self.image_view.set_label_mouse_tracking(False)
    #    else:
    #        self._actions['roieraser'].setChecked(True)

    def _switch_cursor_status(self):
        self._actions['cursor'].setChecked(True)
        self._cursor_enable()

    def _watershed(self):
        watershed_dialog = WatershedDialog(self.model, self)
        watershed_dialog.exec_()

    def _repaint_slices(self):
        self.model.update_current_rgba()

    def _update_undo(self):
        if self.model.current_undo_available():
            self._actions['undo'].setEnabled(True)
        else:
            self._actions['undo'].setEnabled(False)

    def _update_redo(self):
        if self.model.current_redo_available():
            self._actions['redo'].setEnabled(True)
        else:
            self._actions['redo'].setEnabled(False)
   
    def _current_layer_xyzvl_changed(self):
        """
          modified by dxb, need rethink the code. 
        """
        self.image_view.xyz_updated.connect(self._update_xyzvl)
        self.image_view.xyz_updated.emit([self.model.get_current_pos()[1],
                                          self.model.get_current_pos()[0],
                                          self.model.get_current_pos()[2]])
        
    def _update_xyzvl(self, xyz):
        xyzvl = dict(zip(['y', 'x', 'z'], map(str, xyz)))
        value = self.model.get_current_value(xyz)
        xyzvl['value'] = str(value)
        xyzvl['label'] = self.model.get_current_value_label(int(value))
        self.list_view.update_xyzvl(xyzvl)
        self._update_xyzvl_toolbar(xyzvl)

    def _init_label_config_center(self):
        lbl_path = os.path.join(self.label_config_dir, 
                                '*.' + self.label_config_suffix)
        label_configs = glob.glob(lbl_path)
        self.label_configs = map(LabelConfig, label_configs)
        self._label_config_center = LabelConfigCenter(self.label_configs)
        # Label Config Changed
        self._label_config_center.label_config_changed_signal().connect(self._update_brush)
        
    def _init_label_config(self):
        label_path = os.path.join(self.label_path, self.config_file)
        if os.path.isfile(label_path):
            cwd_config = label_path
        else:
            cwd = os.getcwd()
            cwd_config = os.path.join(cwd, self.config_file)
            if not os.path.isfile(cwd_config):
                os.mknod(cwd_config)
        self.label_config = LabelConfig(cwd_config)
    
    def _get_label_config(self, file_path):
        """
        Get label config file.

        """
        # Get label config file
        dir = os.path.dirname(file_path)
        file = os.path.basename(file_path)
        split_list = file.split('.')
        nii_index = split_list.index('nii')
        file = ''.join(split_list[:nii_index])
        config_file = os.path.join(file, 'lbl')
        if os.path.isfile(config_file):
            label_config = LabelConfig(config_file, False)
        else:
            label_config = self.label_config
            
        return label_config

    def _undo(self):
        self.model.undo_current_image()

    def _redo(self):
        self.model.redo_current_image()

    def _intersect(self):
        """
        Make a intersection between two layers.

        """
        new_dialog = IntersectDialog(self.model)
        new_dialog.exec_()

    def _grow(self):
        new_dialog = GrowDialog(self.model)
        new_dialog.exec_()

    def _auto_label(self):
        auto_dialog = AutoLabelDialog(self.model)
        auto_dialog.exec_()

    def _open(self):
        new_dialog = OpenDialog(self.model)
        new_dialog.exec_()

    def _lmax(self):
        new_dialog = LocalMaxDialog(self.model)
        new_dialog.exec_()
    
    def _roifilter(self):
        new_dialog = ROIFilterDialog(self.model)
        new_dialog.exec_()

    def _roimerge(self):
        new_dialog = ROIMergeDialog(self.model)
        new_dialog.exec_()

    def _ld_lbl(self):
        file_name = QFileDialog.getOpenFileName(self,
                                                'Load Label File',
                                                QDir.currentPath(),
                                                "Label files (*.lbl)")
        if file_name:
            label_config = LabelConfig(str(file_name), False)
            self.model.set_cur_label(label_config)

    def _ld_glbl(self):
        file_name = QFileDialog.getOpenFileName(self,
                                                'Load Label File',
                                                QDir.currentPath(),
                                                "Label files (*.lbl)")
        if file_name:
            label_config = LabelConfig(str(file_name), True)
            self.model.set_global_label(label_config)

    def _grid_view(self):
        """
        Grid view option.

        """
        self._actions['grid_view'].setEnabled(False)
        self._actions['orth_view'].setEnabled(True)
        self._actions['hand'].setEnabled(False)
        self._actions['cursor'].trigger()

        self.centralWidget().layout().removeWidget(self.image_view)
        self.image_view.set_display_type('grid')
        self.image_view.deleteLater()
        self._spinbox.setValue(100 * self.model.get_scale_factor('grid'))
        self.image_view = GridView(self.model, self.painter_status,
                self._gridview_horizontal_scrollbar_position,
                self._gridview_vertical_scrollbar_position)
        self.centralWidget().layout().addWidget(self.image_view)
        self.image_view.xyz_updated.connect(self._update_xyzvl)

    def _orth_view(self):
        """
        Orth view option.

        """
        self._actions['orth_view'].setEnabled(False)
        self._actions['grid_view'].setEnabled(True)
        self._actions['hand'].setEnabled(True)
        self._actions['cursor'].trigger()

        self._gridview_horizontal_scrollbar_position = \
            self.image_view.get_horizontal_scrollbar_position()
        self._gridview_vertical_scrollbar_position = \
            self.image_view.get_vertical_srollbar_position()
        self.centralWidget().layout().removeWidget(self.image_view)
        self.image_view.set_display_type('orth')
        self.image_view.deleteLater()
        self._spinbox.setValue(100 * self.model.get_scale_factor('orth'))
        self.image_view = OrthView(self.model, self.painter_status)
        self.centralWidget().layout().addWidget(self.image_view)
        self.image_view.xyz_updated.connect(self._update_xyzvl)

    def _reset_view(self):
        """
        Reset view parameters.

        """
        if self.image_view.display_type() == 'orth':
            if not self.model.get_scale_factor('orth') == \
                self.default_orth_scale_factor:
                self._spinbox.setValue(100 * self.default_orth_scale_factor)
            self.image_view.reset_view()
        elif self.image_view.display_type() == 'grid':
            if not self.model.get_scale_factor('grid') == \
                self.default_grid_scale_factor:
                self._spinbox.setValue(100 * self.default_grid_scale_factor)

    def _update_brush(self):
        if self._label_config_center.is_drawing_valid():
            self._actions['brush'].setEnabled(True)
            self._actions['roibrush'].setEnabled(True)
        else:
            self._actions['brush'].setEnabled(False)
            self._actions['roibrush'].setEnabled(False)
