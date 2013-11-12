# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""Graphic User Interface.

"""

import sys
import os
import ConfigParser
import glob
import froi as src_pkg

from froi.version import __version__

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
from component.regularroidialog import RegularROIDialog
from component.intersectdialog import IntersectDialog
#from component.growdialog import GrowDialog
from component.growdialog_liu import GrowDialog
from component.edgedetectiondialog import Edge_detectionDialog
from component.autolabeldialog import AutoLabelDialog
from component.opendialog import OpenDialog
from component.localmaxdialog import LocalMaxDialog
from component.labelconfigcenter import LabelConfigCenter
from component.roifilterdialog import ROIFilterDialog
from component.roilabeldialog import ROILabelDialog
from component.roieraserdialog import ROIEraserDialog
from component.roimergedialog import ROIMergeDialog
from component.roidialog import ROIDialog
from component.binaryzationdialog import BinaryzationDialog
from component.binaryerosiondialog import BinaryerosionDialog
from component.binarydilationdialog import BinarydilationDialog
from component.greydilationdialog import GreydilationDialog
from component.greyerosiondialog import GreyerosionDialog
from component.voxeltimepointcurvedialog import VoxelTimePointCurveDialog

class BpMainWindow(QMainWindow):
    """Class BpMainWindow provides UI interface of FreeROI.

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

    def __init__(self, parent=None):
        """
        Initialize an instance of BpMainWindow.
        
        """
        # Inherited from QMainWindow
        if sys.platform == 'darwin':
            # Workaround for Qt issue on OS X that causes QMainWindow to
            # hide when adding QToolBar, see
            # https://bugreports.qt-project.org/browse/QTBUG-4300
            super(BpMainWindow, self).__init__(parent, Qt.MacWindowToolBarButtonHint)
        else:
            super(BpMainWindow, self).__init__(parent)

        # temporary variable
        self._temp_dir = None

        # pre-define a model variable
        self.model = None

    def config_extra_settings(self, data_dir, icon_dir):
        """
        Set data directory and update some configurations.

        """
        # load data directory configuration
        self.label_path = data_dir
        self.label_config_dir = os.path.join(self.label_path, 'labelconfig')
        self.label_config_suffix = 'lbl'

        # set icon configuration
        self._icon_dir = icon_dir

        # set window title
        self.setWindowTitle('FreeROI')
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
        self._actions['add_template'].setEnabled(True)

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
        self._actions['new_image'].triggered.connect(self.__new_image)
        self._actions['new_image'].setEnabled(False)

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

        # dwhether display the cross hover
        self._actions['cross_hover_view'] = QAction(QIcon(os.path.join(
                                                    self._icon_dir,
                                                   'cross_hover_enable.png')),
                                                 self.tr("Disable cross hover"), self)
        self._actions['cross_hover_view'].triggered.connect(self._display_cross_hover)
        self._actions['cross_hover_view'].setEnabled(False)

        #-- generated by zgf
        # Binaryzation view action
        self._actions['binaryzation'] = QAction(QIcon(os.path.join(
                                            self._icon_dir, 'binaryzation.png')),
                                            self.tr("Binaryzation"), self)
        self._actions['binaryzation'].triggered.connect(self._binaryzation)
        self._actions['binaryzation'].setEnabled(False)

        # Binary_erosion view action
        self._actions['binaryerosion'] = QAction(QIcon(os.path.join(
                                            self._icon_dir, 'binary_erosion.png')),
                                            self.tr("Binaryerosion"), self)
        self._actions['binaryerosion'].triggered.connect(self._binaryerosion)
        self._actions['binaryerosion'].setEnabled(False)

        # Binary_dilation view action
        self._actions['binarydilation'] = QAction(QIcon(os.path.join(
                                            self._icon_dir, 'binary_dilation.png')),
                                            self.tr("Binarydilation"), self)
        self._actions['binarydilation'].triggered.connect(self._binarydilation)
        self._actions['binarydilation'].setEnabled(False)

        # grey_erosion view action
        self._actions['greyerosion'] = QAction(QIcon(os.path.join(
                                            self._icon_dir, 'grey_erosion.png')),
                                            self.tr("Greyerosion"), self)
        self._actions['greyerosion'].triggered.connect(self._greyerosion)
        self._actions['greyerosion'].setEnabled(False)

        # grey_dilation view action
        self._actions['greydilation'] = QAction(QIcon(os.path.join(
                                            self._icon_dir, 'grey_dilation.png')),
                                            self.tr("Greydilation"), self)
        self._actions['greydilation'].triggered.connect(self._greydilation)
        self._actions['greydilation'].setEnabled(False)

        # voxel time point curve view action
        self._actions['voxeltimepointcurve'] = QAction(QIcon(os.path.join(
            self._icon_dir, 'voxel_time_point_curve.png')),
                                                self.tr("Voxeltimepointcurve"), self)
        self._actions['voxeltimepointcurve'].triggered.connect(self._voxeltimepointcurve)
        self._actions['voxeltimepointcurve'].setEnabled(True)
        #-- generated by zgf


        # About software
        self._actions['about_pybp'] = QAction(self.tr("About FreeROI"), self)
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
        
        # sphere and cube roi
        self._actions['regular_roi'] = QAction(QIcon(os.path.join(
                                    self._icon_dir, 'sphere_and_cube.png')),
                                    self.tr("Regular ROI"), self)
        self._actions['regular_roi'].triggered.connect(self._regular_roi)
        self._actions['regular_roi'].setEnabled(False)

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

        # Edge Detection
        self._actions['edge_detection'] = QAction(QIcon(os.path.join(
            self._icon_dir, 'edge_detection.png')),
                                                  self.tr("Multi Label Edge Detection"), self)
        self._actions['edge_detection'].triggered.connect(self._edge_detection)
        self._actions['edge_detection'].setEnabled(False)

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
        #self._toolbar = QToolBar()
        self._toolbar = self.addToolBar("Tools")
      
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
        self._toolbar.addAction(self._actions['cross_hover_view'])
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
        self._toolbar.addAction(self._actions['regular_roi'])
        self._toolbar.addAction(self._actions['intersect'])
        self._toolbar.addAction(self._actions['open'])
        self._toolbar.addAction(self._actions['lmax'])
        self._toolbar.addAction(self._actions['grow'])
        self._toolbar.addAction(self._actions['edge_detection'])
        self._toolbar.addAction(self._actions['watershed'])
        self._toolbar.addAction(self._actions['roifilter'])
        self._toolbar.addAction(self._actions['roimerge'])
        self._toolbar.addAction(self._actions['roidialog'])

        self._toolbar.addSeparator() 
        self._toolbar.addWidget(self._spinbox)

        #self.addToolBar(self._toolbar)

    def _set_scale_factor(self, value):
        """
        Set scale factor.

        """
        value = float(value) / 100
        self.model.set_scale_factor(value, self.image_view.display_type())

    def _add_template(self):
        """
        Open a dialog window and select a template file.

        """
        template_dir = os.path.join(self.label_path, 'standard', 
                                    'MNI152_T1_2mm_brain.nii.gz')
        template_name = QFileDialog.getOpenFileName(
                                        self,
                                        'Open standard file',
                                        template_dir,
                                        'Nifti files (*.nii.gz *.nii)')
        if not template_name.isEmpty():
            template_path = str(template_name)
<<<<<<< HEAD
            self._add_template_img(template_path)

    def _add_template_img(self, source, name=None, header=None, view_min=None, 
                          view_max=None, alpha=255, colormap='gray'):
        """
        Add template image.

        """
        if not self._actions['remove_image'].isEnabled():
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
            self.list_view = LayerView(self._label_config_center, self)
            self.list_view.setModel(self.model)
            self.image_view = GridView(self.model, self.painter_status)

            # initialize display layout
            central_widget = QWidget()
            layout = QHBoxLayout()
            central_widget.setLayout(layout)
            central_widget.layout().addWidget(self.list_view)
            central_widget.layout().addWidget(self.image_view)
            self._init_data_select()
            self.setCentralWidget(central_widget)

            # add a toolbar
            self._add_toolbar()

            # change button status
            self._actions['add_template'].setEnabled(False)
            self._actions['add_image'].setEnabled(True)
            self._actions['save_image'].setEnabled(True)
            self._actions['ld_lbl'].setEnabled(True)
            self._actions['ld_glbl'].setEnabled(True)
            self._actions['new_image'].setEnabled(True)
            self._actions['close'].setEnabled(True)
            self._actions['orth_view'].setEnabled(True)
            self._actions['original_view'].setEnabled(True)
            self._actions['watershed'].setEnabled(True)
            self._actions['grow'].setEnabled(True)
            self._actions['edge_detection'].setEnabled(True)
            self._actions['binaryzation'].setEnabled(True)
            self._actions['binarydilation'].setEnabled(True)
            self._actions['binaryerosion'].setEnabled(True)
            self._actions['greydilation'].setEnabled(True)
            self._actions['greyerosion'].setEnabled(True)

            self._actions['undo'].setEnabled(False)
            self._actions['redo'].setEnabled(False)
            self.list_view.current_changed.connect(self._update_undo)
            self.list_view.current_changed.connect(self._update_redo)
            self.list_view.input_changed.connect(self._inputUpdate)
            self.list_view.volume_index_spinbox.valueChanged.connect(self._volume_index_changed)
            
            self.list_view.current_changed.connect(self._current_layer_xyzvl_changed)

            self.model.undo_stack_changed.connect(self._update_undo)
            self.model.redo_stack_changed.connect(self._update_redo)

            self._actions['watershed'].setEnabled(True)
            self._actions['grow'].setEnabled(True)
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

    #generate by zgf
    def _inputUpdate(self):
         """
        Display the image via changing the value of the spinbox...
        """
         new_coord = [self.list_view._coord_x.value(),self.list_view._coord_y.value(),self.list_view._coord_z.value()]
         self.image_view.set_coord(new_coord)
    #generate by zgf

=======
            self._add_img(template_path)
>>>>>>> eeee50717d4242be3212165ca7bc620df089e650

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
        Add image.

        """
        # If model is NULL, then re-initialize it.
        if not self.model:
            self._init_label_config_center()
            self.model = VolumeListModel([], self._label_config_center)
            self.model.set_scale_factor(self.default_grid_scale_factor, 'grid')
            self.model.set_scale_factor(self.default_orth_scale_factor, 'orth')
            self.painter_status = PainterStatus(ViewSettings())

        # Save previous opened directory (except `standard` directory)
        file_path = str(source)
        temp_dir = os.path.dirname(file_path)
        if not os.path.samefile(temp_dir, os.path.join(self.label_path, 'standard')): 
            self._temp_dir = temp_dir

        if self.model.addItem(file_path, None, name, header, view_min,
                              view_max, alpha, colormap):
<<<<<<< HEAD
            self._actions['remove_image'].setEnabled(True)
            self._actions['intersect'].setEnabled(True)
            self._actions['auto_label'].setEnabled(True)
            self._actions['grow'].setEnabled(True)
            self._actions['edge_detection'].setEnabled(True)
            self._actions['open'].setEnabled(True)
            self._actions['regular_roi'].setEnabled(True)
            self._actions['lmax'].setEnabled(True)
            self._actions['roifilter'].setEnabled(True)
            self._actions['roimerge'].setEnabled(True)

            if self._actions['add_template'].isEnabled():
               # initialize views and model
               self.list_view = LayerView(self._label_config_center, self)
               self.list_view.setModel(self.model)
               self.image_view = GridView(self.model, self.painter_status)

               # initialize display layout
               central_widget = QWidget()
               layout = QHBoxLayout()
               central_widget.setLayout(layout)
               central_widget.layout().addWidget(self.list_view)
               central_widget.layout().addWidget(self.image_view)
               self._init_data_select()
               self.setCentralWidget(central_widget)

               # add a toolbar
               self._add_toolbar()

               # change button status
               self._actions['add_image'].setEnabled(True)
               self._actions['save_image'].setEnabled(True)
               self._actions['ld_lbl'].setEnabled(True)
               self._actions['ld_glbl'].setEnabled(True)
               self._actions['new_image'].setEnabled(True)
               self._actions['close'].setEnabled(True)
               self._actions['orth_view'].setEnabled(True)
               self._actions['original_view'].setEnabled(True)
               self._actions['watershed'].setEnabled(True)
               self._actions['grow'].setEnabled(True)
               self._actions['edge_detection'].setEnabled(True)
               self._actions['binaryzation'].setEnabled(True)
               self._actions['binarydilation'].setEnabled(True)
               self._actions['binaryerosion'].setEnabled(True)
               self._actions['greydilation'].setEnabled(True)
               self._actions['greyerosion'].setEnabled(True)

               self._actions['undo'].setEnabled(False)
               self._actions['redo'].setEnabled(False)
               self.list_view.current_changed.connect(self._update_undo)
               self.list_view.current_changed.connect(self._update_redo)
               self.list_view.input_changed.connect(self._inputUpdate)
               self.list_view.volume_index_spinbox.valueChanged.connect(self._volume_index_changed)

               self.list_view.current_changed.connect(self._current_layer_xyzvl_changed)

               self.model.undo_stack_changed.connect(self._update_undo)
               self.model.redo_stack_changed.connect(self._update_redo)

               self._actions['watershed'].setEnabled(True)
               self._actions['grow'].setEnabled(True)
               self.list_view.setCurrentIndex(self.model.index(0))

               # update_xyzvl when necessarily
               self.image_view.xyz_updated.connect(self._update_xyzvl)
               self.image_view.xyz_updated.emit([self.model.get_current_pos()[1],
                                                self.model.get_current_pos()[0],
                                                self.model.get_current_pos()[2]])
            self.list_view.setCurrentIndex(self.model.index(0))
            self._init_data_select()
=======
            # Take different acions in different case.
            # If only one data in VolumeList, then initialize views.
            if self.model.rowCount() == 1:
                # initialize views
                self.list_view = LayerView(self._label_config_center, self)
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
                #self.setUnifiedTitleAndToolBarOnMac(True)
                # change button status
                self._actions['save_image'].setEnabled(True)
                self._actions['ld_lbl'].setEnabled(True)
                self._actions['ld_glbl'].setEnabled(True)
                self._actions['new_image'].setEnabled(True)
                self._actions['close'].setEnabled(True)
                self._actions['orth_view'].setEnabled(True)
                self._actions['cross_hover_view'].setEnabled(True)
                self._actions['original_view'].setEnabled(True)
                self._actions['open'].setEnabled(True)
                self._actions['regular_roi'].setEnabled(True)
                self._actions['lmax'].setEnabled(True)
                self._actions['watershed'].setEnabled(True)
                self._actions['grow'].setEnabled(True)
                self._actions['binaryzation'].setEnabled(True)
                self._actions['binarydilation'].setEnabled(True)
                self._actions['binaryerosion'].setEnabled(True)
                self._actions['greydilation'].setEnabled(True)
                self._actions['greyerosion'].setEnabled(True)
                self._actions['undo'].setEnabled(False)
                self._actions['redo'].setEnabled(False)
                # connect signals with slots
                self.list_view.current_changed.connect(self._update_undo)
                self.list_view.current_changed.connect(self._update_redo)
                # self.list_view._list_view.selectionModel().currentChanged.connect(self._voxeltimepointcurve)
                self.model.undo_stack_changed.connect(self._update_undo)
                self.model.redo_stack_changed.connect(self._update_redo)
                # set current volume index
                self.list_view.setCurrentIndex(self.model.index(0))
                # set crosshair as the center of the data
                self.model.set_cross_pos([self.model.getY()/2,
                                          self.model.getX()/2,
                                          self.model.getZ()/2])
                ## Enable cursor tracking
                # self.list_view._list_view.selectionModel().currentChanged.connect(
                #                self._switch_cursor_status)
            elif self.model.rowCount() > 1:
                self._actions['remove_image'].setEnabled(True)
                self._actions['intersect'].setEnabled(True)
                self._actions['auto_label'].setEnabled(True)
                self._actions['roifilter'].setEnabled(True)
                self._actions['roimerge'].setEnabled(True)
                # set current volume index
                self.list_view.setCurrentIndex(self.model.index(0))
>>>>>>> eeee50717d4242be3212165ca7bc620df089e650
        else:
            QMessageBox.information(self,'FreeROI', 'Cannot load ' + file_name + '.')

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
        self._actions['regular_roi'].setEnabled(True)
        self._actions['grow'].setEnabled(True)
        self._actions['edge_detection'].setEnabled(True)
        self._actions['auto_label'].setEnabled(True)
        self._actions['open'].setEnabled(True)
        self._actions['lmax'].setEnabled(True)
        self._actions['roifilter'].setEnabled(True)
        self._actions['roimerge'].setEnabled(True)
        
    def new_image_action(self):
        self._actions['remove_image'].setEnabled(True)
        self._actions['intersect'].setEnabled(True)
        self._actions['grow'].setEnabled(True)
        self._actions['edge_detection'].setEnabled(True)
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
            self._actions['regular_roi'].setEnabled(False)
            self._actions['grow'].setEnabled(False)
            self._actions['edge_detection'].setEnabled(False)
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
        self.model = None
        self._actions['add_template'].setEnabled(True)
        self._actions['add_image'].setEnabled(True)
        self._actions['remove_image'].setEnabled(False)
        self._actions['new_image'].setEnabled(False)
        self._actions['save_image'].setEnabled(False)
        self._actions['ld_glbl'].setEnabled(False)
        self._actions['ld_lbl'].setEnabled(False)
        self._actions['close'].setEnabled(False)
        self._actions['intersect'].setEnabled(False)
        self._actions['regular_roi'].setEnabled(False)
        self._actions['grow'].setEnabled(False)
        self._actions['edge_detection'].setEnabled(False)
        self._actions['auto_label'].setEnabled(False)
        self._actions['watershed'].setEnabled(False)
        self._actions['open'].setEnabled(False)
        self._actions['lmax'].setEnabled(False)
        self._actions['grid_view'].setEnabled(False)
        self._actions['orth_view'].setEnabled(False)
        self._actions['original_view'].setEnabled(False)
        self._actions['roifilter'].setEnabled(False)
        self._actions['roimerge'].setEnabled(False)
        self._actions['binaryzation'].setEnabled(False)
        self._actions['binarydilation'].setEnabled(False)
        self._actions['binaryerosion'].setEnabled(False)
        self._actions['greydilation'].setEnabled(False)
        self._actions['greyerosion'].setEnabled(False)

    def _about_pybp(self):
        """
        About software.

        """
        QMessageBox.about(self,
                          self.tr("About FreeROI"),
                          self.tr("<p>the <b>FreeROI</b> could make ROI manually"
                                  "and automatically.</p>"
                                  "<p>Version: " + __version__ + "</p>"))

    def _create_menus(self):
        """Create menus."""
        self.file_menu = self.menuBar().addMenu(self.tr("File"))
        self.file_menu.addAction(self._actions['add_image'])
        self.file_menu.addAction(self._actions['add_template'])
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
        self.view_menu.addAction(self._actions['cross_hover_view'])

        self.tool_menu = self.menuBar().addMenu(self.tr("Tools"))
        self.tool_menu.addAction(self._actions['regular_roi'])
        self.tool_menu.addAction(self._actions['intersect'])
        self.tool_menu.addAction(self._actions['grow'])
        self.tool_menu.addAction(self._actions['edge_detection'])
        self.tool_menu.addAction(self._actions['auto_label'])
        self.tool_menu.addAction(self._actions['watershed'])
        self.tool_menu.addAction(self._actions['open'])
        self.tool_menu.addAction(self._actions['lmax'])
        self.tool_menu.addAction(self._actions['binaryzation'])
        self.tool_menu.addAction(self._actions['binarydilation'])
        self.tool_menu.addAction(self._actions['binaryerosion'])
        self.tool_menu.addAction(self._actions['greydilation'])
        self.tool_menu.addAction(self._actions['greyerosion'])
        self.tool_menu.addAction(self._actions['roifilter'])
        self.tool_menu.addAction(self._actions['roimerge'])
        self.tool_menu.addAction(self._actions['voxeltimepointcurve'])

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

    def _regular_roi(self):
        regular_roi_dialog = RegularROIDialog(self.model, self)
        regular_roi_dialog.exec_()


    #def _repaint_slices(self):
    #    self.model.update_current_rgba()

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
   
    #def _current_layer_xyzvl_changed(self):
    #    """
    #      modified by dxb, need rethink the code. 
    #    """
    #    self.image_view.xyz_updated.connect(self._update_xyzvl)
    #    self.image_view.xyz_updated.emit([self.model.get_current_pos()[1],
    #                                      self.model.get_current_pos()[0],
    #                                      self.model.get_current_pos()[2]])
        
    #def _update_xyzvl(self, xyz):
    #    xyzvl = dict(zip(['y', 'x', 'z'], map(str, xyz)))
    #    value = self.model.get_current_value(xyz)
    #    xyzvl['value'] = str(value)
    #    xyzvl['label'] = self.model.get_current_value_label(int(value))
    #    self.list_view.update_xyzvl(xyzvl)

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

    def _edge_detection(self):
        new_dialog = Edge_detectionDialog(self.model)
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
        self.model.scale_changed.disconnect()
        self.model.repaint_slices.disconnect()
        self.model.cross_pos_changed.disconnect(self.image_view.update_cross_pos)
        self.image_view.deleteLater()
        self._spinbox.setValue(100 * self.model.get_scale_factor('grid'))
        self.image_view = GridView(self.model, self.painter_status,
                self._gridview_vertical_scrollbar_position)
        self.centralWidget().layout().addWidget(self.image_view)

    def _orth_view(self):
        """
        Orth view option.
        """


        self._actions['orth_view'].setEnabled(False)
        self._actions['grid_view'].setEnabled(True)
        self._actions['hand'].setEnabled(True)
        self._actions['cursor'].trigger()

        self._gridview_vertical_scrollbar_position = \
            self.image_view.get_vertical_srollbar_position()
        self.centralWidget().layout().removeWidget(self.image_view)
        self.image_view.set_display_type('orth')
        self.model.scale_changed.disconnect()
        self.model.repaint_slices.disconnect()
        self.model.cross_pos_changed.disconnect(self.image_view.update_cross_pos)
        self.image_view.deleteLater()
        self._spinbox.setValue(100 * self.model.get_scale_factor('orth'))
        self.image_view = OrthView(self.model, self.painter_status)
        self.centralWidget().layout().addWidget(self.image_view)

    def _display_cross_hover(self):
        if self.model._display_cross:
            self.model.set_cross_status(False)
            self._actions['cross_hover_view'].setText('Enable cross hover')
            self._actions['cross_hover_view'].setIcon(QIcon(os.path.join(self._icon_dir,'cross_hover_disable.png')))
        else:
            self.model.set_cross_status(True)
            self._actions['cross_hover_view'].setText('Disable cross hover')
            self._actions['cross_hover_view'].setIcon(QIcon(os.path.join(self._icon_dir,'cross_hover_enable.png')))

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

    def _binaryzation(self):
        binaryzation_dialog = BinaryzationDialog(self.model)
        binaryzation_dialog.exec_()

    def _binaryerosion(self):
        binaryerosion_dialog = BinaryerosionDialog(self.model)
        binaryerosion_dialog.exec_()

    def _binarydilation(self):
        binarydilation_dialog = BinarydilationDialog(self.model)
        binarydilation_dialog.exec_()

    def _greyerosion(self):
        greyerosiondialog = GreyerosionDialog(self.model)
        greyerosiondialog.exec_()

    def _voxeltimepointcurve(self):
        self.voxeltimepointcurve = VoxelTimePointCurveDialog(self.model)
        self.voxeltimepointcurve.setModal(False)
        self.voxeltimepointcurve.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.voxeltimepointcurve.show()
        self.list_view.current_changed.connect(self.voxeltimepointcurve._plot)

    def _greydilation(self):
        greydilation_dialog = GreydilationDialog(self.model)
        greydilation_dialog.exec_()

