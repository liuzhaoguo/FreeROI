.. _data-analysis-toolkit:

Image Processing Toolkit
=====================

As an integrated software suite for neuroimaging data processing, FreeROI 
not only provides the user-friendly pipeline for defining ROI, but also many
related tools for image processing, such as smoothing, binarization, and 
image segmentation.

Common Tools
------------

In FreeROI, the images could be smoothed, binarized, or masked by another image
by a few clicks, liberating users from complex command lines.

1. Smoothing

#. Intersection

#. Local Maxima Detection

#. Binarization

#. Image Dilation

#. Image Erosion


Image Segmentation
------------------

As the initial step for defining ROI semi-automatically, an image could be 
divided into several subregions each with a specific label using image
segmentation algorithm. In FreeROI, three segmentation methods could be used,
including *cluster detection*, *watershed*, and *region grow*.

1. Cluster Detection

   After a voxel-wise analysis, researchers usually only concern the regions
   which show a significant effect of experiment manipulation. Thus, after 
   a threshold processing, the image would consist of many separated clusters
   which defined by a set of continous voxels. With the *cluster detection*
   approach, each cluster could be extracted out and labeled with a 
   distinguishable number.

#. Watershed

   *Watershed* algorithm could divide an image following the topographical
   information in the image. This algorithm finds local maxima and "grow"
   regions around these maxima by incorporating neighboring voxels in
   decreasing order of voxel intensity. 


#. Region Grow


ROI Related Tools
-----------------------

1. Merging

#. Edge Detection

#. Filter

#. Statistics


Morphology Tools
-----------------

