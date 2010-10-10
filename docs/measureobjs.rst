Measuring SVG objects
=====================

The following functions calculate the bounding boxes of various SVG objects.
All bounding boxes returned by these functions are axis-aligned bounding boxes
(AABBs), i.e., the top and bottom of the boxes are parallel to the x-axis of
the image, and the left and right edges are parallel to its y-axis.

Any object
----------

.. autofunction:: bounds.object_bounding_box

Path
----

.. autofunction:: bounds.path_bounding_box
