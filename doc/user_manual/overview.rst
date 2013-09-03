Introduction
============

FreeROI is a versatile image processing software developed for neuroimaging data.
It's goal is to provide a user-friendly user-interface for neuroimaging researchers to visualize and analyze their data.

Features
---------

As its name revealed, FreeROI is focused on the `region of interest <http://en.wikipedia.org/wiki/Region_of_interest>`_ data analysis method.
It has:

* Powerful ROI labeling and generating methods and toolset, which could be used to reliabily and efficiently creating ROIs specifically for multi-modal neuroimaging analysis (eg. fMRI, Resting, DTI...), see :ref:`ROI Analysis <roi-anlaysis>`

* Three modes to view and explore neuroimage data, including a sigle-orientation slicing viewer, a three-orientation slicing viewer and a 3D volume viewer, see :ref:`Data Viewing <data-viewing>`
  
* A bunch of data processing tools to manipulate and analyzing neuroimage data, see :ref:`Data Analysis Toolset <data-analysis-toolkit>`

* Support for both 3D and 4D neuroimage data, which is very useful for batch processing, see :ref:`Data format <data-format>`

FreeROI is currently under active developing and maintaning by a group of experienced neuroimage data analysists, the following are some upcoming features:

* more ROI statistical analysis functions
* more automatic ROI generating functions based on machine learning strategies
* support for surface neuroimaging data format

Idea
----

The key idea behind the design of FreeROI is that neuroimaging data should be analyzed *reliabily* and *efficiently*. 
Here *reliability* means every two times of data analysis should get the same result. 
In addition, as time is extremely valuable resource for researchers, data analyzing software should provide 
