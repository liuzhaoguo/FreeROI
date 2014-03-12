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
   A Gaussian filter could be used for image smoothing. The parameter *sigma*
   - standard deviation for Gaussian kernel - should be specified in voxel
   units first.

   A relationship between the *full width at half maximum (FWHM)* and *sigma*
   could be derived as FWHM = 2.3548 * sigma.

#. Inversion
   In fMRI activation image, the negative activation is usually also concerned 
   by reserchers, yet no thresholding process for negative value is implemented
   in FreeROI. To facilitate users extract regions with negative value, the 
   image could be inverted by multiplying with -1 first.

#. Intersection
   An image could be masked by another binary image using intersection tool.

#. Local Maxima Detection
   This tool is used for extract local maxima from an image. The local maxima
   could be used for defining ROIs with regular shape.

#. Binarization
   An image could be binarized with this tool. A threshold should be given, 
   the voxel, which value is not less than threshold, would be assigned as 1,
   otherwise, assigned as 0.

#. Erosion
   Erosion is one of two fundamental operations (the other being dilation) in 
   morohological processing from which all other morphological operations are
   based. The operation could be used to reduce the extent of foreground in the
   image.

#. Dilation
   The effect of dilation is opposite to that of erosion. It would enlarge the
   extent of foreground of the image.

#. Opening
   As the combination of *erosion* and *dilation*, the opening operation is
   usually used as a basic workhorse of morphological noise removal. Opening
   removes small objects from the foreground of an image, placing them in the
   background.

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
   distinguishable marker.

#. Watershed

   *Watershed* algorithm could divide an image following the topographical
   information in the image. Specifically, it treats voxel value as a local
   topography (elevation). The algorithm finds local minima and "grow"
   regions around these minima by incorporating neighboring voxels in
   increasing order of voxel value, until basins attributed to different 
   markers meet on watershed lines. In addition, to segment an fMRI activation
   image, for example, the image should be inverted (multiplied with -1) before
   segmentation. The segmented image consists of several regions each with a 
   activation peak, also an activation cluster which has more than one local
   maxima would be divided into several sub-regions which are separated with
   watershed lines.

#. Region Grow


ROI Related Tools
-----------------------

1. Merging

#. Edge Detection

#. Filter

#. Auto Labeling

#. ROI to Surface

#. Statistics


