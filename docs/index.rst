=================
inkscape-pybounds
=================

The open source vector graphics editor `Inkscape <http://inkscape.org/>`_
allows extensions to be written in the `Python <http://www.python.org/>`_
scripting language. It comes with a number of modules to make it easier to
write these extensions. One of them, ``simpletransform``, has some basic
functions to calculate the bounding box of SVG objects. The main issue with
this is that it cannot provide tight bounding boxes (that is, boxes which fit
the objects with no overlap). Additionally, in an ideal world the code to work
with SVG transforms and the code to calculate bounding boxes would live in
separate modules.

This project provides a Python module, ``bounds``, which defines a
:class:`bounds.BoundingBox` class to represent a bounding box, and a number of
functions to calculate the bounding boxes of the various SVG objects. These
bounding boxes should all be tight bounds.

**Note: This module is currently under initial development (hence the alpha tag
in the version). Bounding boxes cannot yet be calculated for a number of SVG
objects, and the API is liable to change without notice.**

Module reference
================

.. toctree::
   :maxdepth: 2

   moduleinfo
   boundingbox
   measureobjs
   measuresegs
   helperfuncs

Implementation notes
====================

.. toctree::
   :maxdepth: 1

   transformations
   bezier
   elliptarc

Licenses
========

.. toctree::
   :maxdepth: 1

   codelicense
   doclicense

:ref:`genindex`
===============

:ref:`search`
=============
