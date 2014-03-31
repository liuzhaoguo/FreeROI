.. _data-analysis-toolkit:

Image Processing Toolkit
=====================

As an integrated software suite for neuroimaging data processing, FreeROI 
not only provides the user-friendly pipeline for defining ROI, but also many
related tools for image processing, such as smoothing, binarization, and 
image segmentation.

All tools could be classified into several categories based on their
utility.

Basic Tools
-----------

In FreeROI, the images could be binarized, smoothed, or masked by another image
by a few clicks, liberating users from complex command lines.

1. Binarization
   An image could be binarized with this tool. A threshold should be given, 
   the voxel, which value is not less than threshold, would be assigned as 1,
   otherwise, assigned as 0.

#. Smoothing
   A Gaussian filter could be used for image smoothing. The parameter *sigma*
   - standard deviation for Gaussian kernel - should be specified in voxel
   units first.

   The relationship between the *full width at half maximum (FWHM)* and *sigma*
   could be derived as FWHM = 2.3548 * sigma.

#. Inversion
   In fMRI activation image, the negative activation is usually also concerned 
   by reserchers, yet no thresholding process for negative value is implemented
   in FreeROI. To facilitate users extract regions with negative value, the 
   image could be inverted by multiplying with -1 first.

#. Intersection
   An image could be masked by another image using intersection tool.

   The "mask" image is selected as one of the loaded image, and binarized after
   thresholding with the lower-bound value for display.

#. Local Maxima Detection
   This tool is used for extract local maxima from an image. The local maxima
   could be used for defining ROIs with regular shape.

#. Extract mean time course
   After a ROI is defined, this tool could be used to extract mean time course
   of this ROI from an 3D/4D image. 

Image Segmentation
------------------

As the initial step for defining ROI semi-automatically, an image could be 
divided into several subregions each with a specific label using image
segmentation algorithm. In FreeROI, three segmentation methods could be used,
including *cluster detection*, *watershed*, and *region growing*.

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

#. Region Growing

   *Region growing* is a simple voxel(pixel)-based image segmentation method.
   This approach examines neighboring voxels of initial "seed point" and
   determines whether the voxel neighbors should be added to the region. The
   preocess is iterated on, in the same manner as general data clustering
   algorithm.

   The first step in region growing is to select a seed point. The initial
   region begins as the exact location of this seed. The region is then grown
   from the seed point to adjacent points depending on a similarity constraint.
   Also a region size is required from the user. The growing process is
   continued until the region size reach this upper-bound.

Image Editing
-------------

1. Voxel Edit


#. ROI Edit

#. ROI Batch


ROI Tools
-----------------------

This set of tools are designed for ROI generation with regular shape, merging,
edge detection, and several other utility.

1. Merging

#. Edge Detection

#. ROI to Surface

Morphological Processing
------------------------

Morphological image processing is a collection of non-linear operations related
to the shape or morphology of features in an image. According to
`Wikipedia <http://en.wikipedia.org/wiki/Morphological_image_processing>`_ ,
morphological operations rely only on the relative ordering of voxel/pixel
values, not on their numerical values, and therefore are especially suited to
the processing of binary images. Morphological operations can also be applied
to greyscale images such that their light transfer functions are unknown and
therefore their absolute voxel/pixel values are of no or minor interest.

1. Erosion
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

