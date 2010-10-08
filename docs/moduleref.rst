Module reference
================

The bounds module is designed to be used in Inkscape extensions, and provides
the ability to calculate the bounding boxes of SVG objects.

Version
-------

Version information is stored as module attributes in the same manner as the
Python ``sys`` module. This can be used to check which version of the module is
being used.

.. attribute:: bounds.version

   Module version information in a human-readable string, for example
   ``'0.9.0 alpha 1'``.

.. attribute:: bounds.version_info

   A tuple of module version information in the format
   (major_version, minor_version, revision, releaselevel, serial). All of these
   parameters are integers except for releaselevel which will be one of
   'alpha', 'beta', 'candidate', or 'final'. For example, ``(0, 9, 0, 'alpha', 1)``.

.. attribute:: bounds.hexversion

   Module version information encoded as a four-byte hexadecimal number. The
   most significant byte will be the major version, the next byte minor version,
   the third byte the revision, the first half of the final byte the release
   level ('a', 'b', 'c', or 'f') and the final half-byte the serial. For
   example, ``0x000900a1``.

BoundingBox
-----------

.. autoclass:: bounds.BoundingBox
   :members:

   .. attribute:: left

      The left-hand edge of the bounding box.

   .. attribute:: right

      The right-hand edge of the bounding box.

   .. attribute:: bottom

      The bottom edge of the bounding box.

   .. attribute:: top

      The top edge of the bounding box.

Measurement functions
---------------------

Any object
++++++++++

.. autofunction:: bounds.object_bounding_box

Path
++++

.. autofunction:: bounds.path_bounding_box

Bézier curves
+++++++++++++

.. autofunction:: bounds.quadratic_bounding_box
.. autofunction:: bounds.cubic_bounding_box

Helper functions
----------------

.. autofunction:: bounds.draw_bounding_box
