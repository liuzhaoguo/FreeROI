import nibabel as nib
import numpy as np
from mayavi import mlab
from tvtk.api import tvtk

import os
import nkroi as src_pkg

from traits.api import HasTraits, Instance, on_trait_change, Int, Dict, Str, Bool, List
from traitsui.api import View, Item, Group, VGroup, Handler
from traitsui.menu import Action, ActionGroup, Menu, MenuBar
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor
from tvtk.pyface.api import Scene
from mayavi.core.api import PipelineBase, Source

class Visualization(HasTraits):
    scene = Instance(MlabSceneModel, ())
    cord = [0, 0, 0]
    flag = Bool(False)

    def __init__(self,**traits):
        HasTraits.__init__(self, **traits)
        tmp_dir = os.path.dirname(src_pkg.__file__)
        template_dir = os.path.join(tmp_dir, 'data', 'standard','MNI152_T1_2mm_brain.nii.gz')
        img = nib.load(template_dir)
        self.data = img.get_data()


    def picker_callback(self,picker_obj, evt):
        picker_obj = tvtk.to_tvtk(picker_obj)
        picked = picker_obj.actors
        if self.outer.actor.actor._vtk_obj in [o._vtk_obj for o in picked]:
            newPosition = picker_obj.picked_positions.to_array()[0]
            self.cord = [int(newPosition[0]),int(newPosition[1]),int(newPosition[2])]
            self.displayVolume()
            print self.cord,'--------------------------'
            self.flag = True
        else:
            print 'out of the volume!'
            self.flag = False

    def displayVolume(self):
        data_shape = self.data.shape
        xmax = data_shape[0]
        ymax = data_shape[1]
        zmax = data_shape[2]

        # if (data_shape[0]/2-xmin)>(xmax-data_shape[0]/2):
        #     if(data_shape[1]/2-ymin)>(ymax-data_shape[1]/2):
        #         if(data_shape[2]/2-zmin)>(zmax-data_shape[2]/2):
        #             data[0:xmax,0:ymax,0:zmax]=0
        #             cut_plane1.implicit_plane.widget.normal_to_x_axis = True
        #             cut_plane1.implicit_plane.widget.origin = array([ xmax,0.,0.])
        #             cut_plane2.implicit_plane.widget.normal_to_y_axis = True
        #             cut_plane2.implicit_plane.widget.origin = array([ 0.,ymax,0.])
        #             cut_plane3.implicit_plane.widget.normal_to_z_axis = True
        #             cut_plane3.implicit_plane.widget.origin = array([ 0.,0.,zmax])

        if self.flag:
            self.outer.remove()
            tempData = self.data.copy()
            if(self.cord[0] < xmax/2):
                if(self.cord[1] < ymax/2):
                    if(self.cord[2] < zmax/2):
                        print "------8------"
                        tempData[0:tempData.shape[0]/2, 0:tempData.shape[1]/2, 0:tempData.shape[2]/2 ] = 0
                    else:
                        print '------4------'
                        tempData[0:tempData.shape[0]/2, 0:tempData.shape[1]/2, tempData.shape[2]/2:] = 0
                else:
                    if(self.cord[2] < zmax/2):
                        print "------7------"
                        tempData[0:tempData.shape[0]/2, tempData.shape[1]/2:, 0:tempData.shape[2]/2 ] = 0

                    else:
                        print '------3------'
                        tempData[0:tempData.shape[0]/2, tempData.shape[1]/2:, tempData.shape[2]/2: ] = 0
            else:
                if(self.cord[1] < ymax/2):
                    if(self.cord[2] < zmax/2):
                        print "------5------"
                        tempData[tempData.shape[0]/2:, 0:tempData.shape[1]/2, 0:tempData.shape[2]/2 ] = 0
                    else:
                        print '------1------'
                        tempData[tempData.shape[0]/2:, 0:tempData.shape[1]/2, tempData.shape[2]/2: ] = 0
                else:
                    if(self.cord[2] < zmax/2):
                        print "------6------"
                        tempData[tempData.shape[0]/2:, tempData.shape[1]/2:, 0:tempData.shape[2]/2 ] = 0
                    else:
                        print '------2------'
                        tempData[tempData.shape[0]/2:, tempData.shape[1]/2:, tempData.shape[2]/2: ] = 0

            src = mlab.pipeline.scalar_field(tempData)
            self.extract_gridx = mlab.pipeline.extract_grid(src)
            self.outer = mlab.pipeline.iso_surface(self.extract_gridx, colormap='hot')
            self.outer.contour.auto_contours = False
            self.outer.contour.contours[0:1] = [5050]
        else:
            print 'Nothing to do....'


    def picker_callback_left(self, picker_obj):
        picked = tvtk.to_tvtk(picker_obj)
        picked = picker_obj.actors
        print 'Left click!'

    @on_trait_change('scene.activated')
    def update_plot(self):
        self.fig = mlab.gcf()
        self.fig.scene.background = (0.,0.,0.)

        src = mlab.pipeline.scalar_field(self.data)

        self.extract_gridx = mlab.pipeline.extract_grid(src)
        self.outer = mlab.pipeline.iso_surface(self.extract_gridx, colormap='hot')
        self.outer.contour.auto_contours = False
        self.outer.contour.contours[0:1] = [5050]

        self.fig.scene.picker.pointpicker.add_observer('EndPickEvent', self.picker_callback)
        self.fig.on_mouse_pick(self.picker_callback_left,type='point',button='Left')



    view = View(Item('scene', editor=SceneEditor(scene_class=Scene),height=250, width=300, show_label=False),
                resizable=True)


















