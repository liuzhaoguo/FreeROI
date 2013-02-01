""" Test pybp.cluster.base

Author: Yangzetian @ BNU/BUAA
"""

import numpy as np
import scipy.ndimage as ndimage
import nibabel as nib

import pybp.cluster.base as base
from pybp.algorithm import region_grow

"""
    Testing 
    -------
    ClustersImage
        ClustersImgae(image, mask=None)
        get_clusters_volumes(ithr=0, sthr=0, cluster_conn=26)
        is_homo(img2)
        write_roi(voxels, algorithm='sphere', raduis=0, conn=26,
                  save_as='ROI.nii.gz')
        
    ClustersVolume
        ClustersVolume(img_data, img_hdr, mask=None, ithr=0, sthr=0,
                       clusters_conn=26)
        get_clusters_lmax(lmax_conn=26, dthr=0, border=True)
        get_clusters_stat()
        get_clusters_areas(atlas, area_idx) save_clusters()
        save_clusters(path='.')
"""

"""
   Test Case 1
   ----------
   fvo_prob.nii.gz : 3D
   ithr = 0
   sthr = 0
   cluster_conn = 26 : single cluster
   lmax_conn = 26, 6, 18
   dthr = 10, 50, 100, 200, 300
   
   Test Case 2
   ----------
   fvo_prob.nii.gz : 3D
   ithr = 0.05
   sthr = 0, 100
   cluster_conn = 26 : two cluster, one thresholded
   lmax_conn = 26, 6, 18
   dthr = 10, 50, 100, 200, 300

   Test Case 3
   fvo_prob.nii.gz : 3D
   ithr = 0.1
   sthr = 0, 100
   cluster_conn = 26 : two cluster, one thresholded
   lmax_conn = 26, 6, 18
   dthr = 10, 50, 100, 200, 300

   Test Case 4
   ----------
   fvo_prob.nii.gz : 3D
   ithr = 0.0
   mask = cluster1.nii.gz
   sthr = 0, 100
   cluster_conn = 26 : one cluster 
   lmax_conn = 26, 6, 18
   dthr = 10, 50, 100, 200, 300

   Test Case 5
   ----------
   prob.nii.gz : 4D
   ithr = 0.1
   sthr = 0, 100
   cluster_conn = 26 : two cluster, one thresholded
   lmax_conn = 26, 6, 18
   dthr = 10, 50, 100, 200, 300
"""

datadd = '/nfs/t3/workingshop/yangzetian/project/svn/neospearman/toolbox/pybp/trunk/pybp/tests/data/'
#np.seterr(invalid='raise')
#img = base.BpVolume(datadd+'zstat1.nii.gz', datadd+'cluster_mask_zstat1.nii.gz')
#clusters = img.get_clusters_volumes()

img = base.BpVolume(datadd+'4D_example.nii.gz')
clusters = img.get_clusters_volumes()
#clusters100 = img.get_clusters_volumes(ithr=0.1, sthr=100)

"""
try:
    clusters10 = img.get_clusters_volumes(ithr=0.05, cluster_conn=10)
except KeyError:
    print 'catch cluster_conn'
"""

# 3D is also treated as 4D
clusters = clusters[0]

"""Local maxima"""
lmax = clusters.get_clusters_lmax()
lmax6 = clusters.get_clusters_lmax(dthr=6)
lmax10 = clusters.get_clusters_lmax(dthr=10)

img.segment(vox_markers=lmax[0], save_as='segment.nii.gz')
img.segment(vox_markers=lmax6[0], save_as='segment6.nii.gz')
img.segment(vox_markers=lmax10[0], save_as='segment10.nii.gz')


#lmax = clusters_dthr50_lmax[0]
#img.write_roi(lmax, 'sphere', save_as=datadd+'lmax_plain.nii.gz')
#img.write_roi(lmax, 'sphere', 20, save_as=datadd+'lmax_sphere.nii.gz')
#img.write_roi(lmax, 'region_grow', 20, 6, datadd+'lmax_region_grow.nii.gz')



"""Clusters statistics"""
#clusters_stat = clusters.get_clusters_stat() 

"""Area information"""
#atlas = nib.load(datadd+'HarvardOxford-cort-maxprob-thr25-2mm.nii.gz')
#atlas_bug = nib.load(datadd+'HarvardOxford-cort-maxprob-thr25-1mm.nii.gz')

#if not img.ishomo(atlas):
#    raise ValueError

#clusters_areas = clusters.get_clusters_areas(atlas, [1, 40])
#voxel_area = [c.get_area(atlas) for c in clusters_lmax[0]]

"""Save clusters"""
#clusters.save_clusters(datadd)

