*********************
Software Architecture
*********************

Introduction
============

In order to provide an easy-to-use graphic user interface, with the 
complicated neuroimage datasets and many different image processing methods, 
**FreeROI** is developed following a Model-View-Delegate (MVD) architecture 
pattern (a modified version of 
`Model-View-Controller <http://en.wikipedia.org/wiki/Model-view-controller>`_ 
architecture) under Qt framework.

The software could be divided into three kinds of components, which are 
*model*, *view* and *delegate*. The MVD design define the interaction 
between them.

* The **model** consists of neuroimage data, rules for image display and the 
  functions to read/modify datasets in the application. This component is
  implemented as the the module *froi.gui.component.datamodel*, and the
  base dataset is packaged in the module *froi.gui.base.bpdataset*, which is
  used in *datamodel*.

* The **view** is used to display neuroimage data in different types of
  representation, such as in a slice-wise fashion which implemented in 
  *froi.gui.component.GridView* or display in three orthogonal sections
  implemented in the module *froi.gui.component.OrthView*. The parameters
  configuring display fashion, such as the order of overlapping images, 
  contrast, colormap and transparent, are showed in a list and tabular view
  integrated in the module *froi.gui.component.LayerView*.

* The **delegate** mediates input from the users' operation, converting it
  to commands for the **model** or **view**.

For details about the components, see the following section.

Module Description
==================

Bpdateset
---------

Datamodel
---------

Image Viewer
------------

Parameter Viewer
----------------

Toolsets
--------

Main Window
-----------

A Simple Application
====================
