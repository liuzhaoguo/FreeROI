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
    sliceIndexData = Int(50)
    test = Int(50)
    colormap = Str('black-white')
    displayCutplaneFlag = Bool(False)

    _listXYZ = List()

    scene = Instance(MlabSceneModel, ())

    # def __init__(self,**traits):
    #     HasTraits.__init__(self,**traits)

    def __init__(self,**traits):
        HasTraits.__init__(self,**traits)

        tmp_dir = os.path.dirname(src_pkg.__file__)
        template_dir = os.path.join(tmp_dir, 'data', 'standard','MNI152_T1_2mm_brain.nii.gz')
        img = nib.load(template_dir)
        self.data = img.get_data()

    view = View(Item('scene', editor=SceneEditor(scene_class=Scene), show_label=False),resizable=True)
                # menubar=MenuBar(fileMenu,aboutMenu),handler=MenuDemoHandler())

    @on_trait_change('scene.activated')
    def update_plot(self):
        src = mlab.pipeline.scalar_field(self.data)
        src.spacing = [1, 1, 1.2]
        src.update_image_data = True

        fig = mlab.gcf()
        fig.scene.background = (0.,0.,0.)

        blur = mlab.pipeline.user_defined(src, filter='ImageGaussianSmooth')
        extract_data= mlab.pipeline.extract_grid(blur)

        mlab.clf(fig)
        self.ipwX = mlab.pipeline.image_plane_widget(src,plane_orientation='x_axes',colormap=self.colormap,slice_index=50)
        self.ipwX.ipw.restrict_plane_to_volume=False
        self.ipwY = mlab.pipeline.image_plane_widget(src,plane_orientation='y_axes',colormap='black-white',slice_index=50)
        self.ipwY.ipw.restrict_plane_to_volume=False
        self.ipwZ = mlab.pipeline.image_plane_widget(src,plane_orientation='z_axes',colormap='black-white',slice_index=50)
        self.ipwZ.ipw.restrict_plane_to_volume=False

        # self.scalarCutPlane=mlab.pipeline.scalar_cut_plane(src,plane_orientation='z_axes',colormap='hot')
        # self.ipwX.ipw.on_trait_change(self.ipw_index_changed)
        # self.ipwY.ipw.on_trait_change(self.ipw_index_changed)
        # self.ipwZ.ipw.on_trait_change(self.ipw_index_changed)


















