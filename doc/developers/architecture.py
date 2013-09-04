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

* The *model* consists of neuroimage data, rules for image display and the 
  functions to read/modify datasets in the application. The *model* is
  implemented as the the module *froi.gui.component.datamodel*, and the
  base dataset is packaged in the module *froi.gui.base.bpdataset*.

* 


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
