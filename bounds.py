# -*- coding: utf-8 -*-
"""
Functions to work with bounding boxes in Inkscape extensions. This
is largely based upon the src/helper/geom.cpp file from the
Inkscape source code.

The code in geom.cpp is Copyright (C) 2008 Johan Engelen and is
available under the GPL.

Copyright (C) 2010 Blair Bonnett, blair.bonnett@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import gettext
_ = gettext.gettext

import inkex
import simpletransform
import simplepath


class BoundingBox:
    """A class which represents a bounding box. Has four attributes
    (left, right, bottom and top) defining the edges of the box, and
    a number of functions to work with the box.

    """

    def __init__(self, x0, x1, y0, y1):
        """Create a new bounding box. The arguments are the two
        x-points followed by the two y-points defining the edges of
        the box.

        """
        self.left = min(x0, x1)
        self.right = max(x0, x1)
        self.bottom = min(y0, y1)
        self.top = max(y0, y1)

    def contains(self, point):
        """Check if the given point, specified as a pair (x, y), is
        contained within this bounding box.

        """
        if point[0] < self.left or point[0] > self.right:
            return False
        if point[1] < self.bottom or point[1] > self.top:
            return False
        return True

    def contains_x(self, x):
        """Check if the given x-value is within the range of x-values
        encompassed by the box.

        """
        if x < self.left or x > self.right:
            return False
        return True

    def contains_y(self, y):
        """Check if the given y-value is within the range of y-values
        encompassed by the box.

        """
        if y < self.bottom or y > self.top:
            return False
        return True

    def union(self, box):
        """Extend this box to include the area of the other box.

        """
        self.left = min(self.left, box.left)
        self.right = max(self.right, box.right)
        self.bottom = min(self.bottom, box.bottom)
        self.top = max(self.top, box.top)

    def extend(self, point):
        """Extend the box to include the given point which should be
        a pair of floating point numbers (x,y).

        """
        self.left = min(self.left, point[0])
        self.right = max(self.right, point[0])
        self.bottom = min(self.bottom, point[1])
        self.top = max(self.top, point[1])

    def extend_x(self, x):
        """Extend the box to include the given x point.

        """
        self.left = min(self.left, x)
        self.right = max(self.right, x)

    def extend_y(self, y):
        """Extend the box to include the given y point.

        """
        self.bottom = min(self.bottom, y)
        self.top = max(self.top, y)

def path_bounding_box(path, box=None):
    """Compute the bounding box for a path. If an existing bounding box is
    given in the box parameter, it is extended to encompass the path and
    returned. Otherwise, a new bounding box is created and returned.

    Currently, this function returns loose (but encompassing) bounds for
    cubic and quadratic Bézier curves, and incorrect bounds for elliptical
    arcs.

    """

    # Get the transform
    transform = simpletransform.parseTransform(path.get('transform', ''))

    # Parse the path details.
    # Note that when parsing all path segments are converted to absolute
    # coordinates. It also converts H and V segments to L, S segments to C and
    # T segments to Q.
    parsed = simplepath.parsePath(path.get('d'))

    # Starting point
    current = parsed[0][1]
    objbox = BoundingBox(current[0], current[0], current[1], current[1])

    # Loop through each segment.
    for type,params in parsed[1:]:
        # End of path
        if type == 'Z':
            break

        # Line or move to
        elif type == 'L' or type == 'M':
            objbox.extend(params)
            current = params

        # Cubic Bézier curve
        # This is a loose bound using the fact that the curve is contained
        # within the convex hull of the four points defining it.
        elif type == 'C':
            objbox.extend(params[0:2])
            objbox.extend(params[2:4])
            objbox.extend(params[4:6])
            current = params[4:6]

        # Quadratic Bézier curve
        # This is a loose bound using the fact that the curve is contained
        # within the convex hull of the three points defining it.
        elif type == 'Q':
            objbox.extend(params[0:2])
            objbox.extend(params[2:4])
            current = params[2:4]

        # Elliptical arc
        # Currently not handled properly - just ensures the endpoints are in
        # the box.
        elif type == 'A':
            objbox.extend(params[5:7])
            current = params[5:7]

        # Unknown segment type
        else:
            raise Exception(_('Unknown path segment type %s.' % type))

    # Returnt the appropriate box
    if box is None:
        return objbox
    else:
        return box.union(objbox)

def get_bounding_box(obj, box=None):
    """Get the bounding box of the given object. If an existing box
    is given in the box parameter, it is extended to encompass the
    object and returned. If no box is given, a new one is created
    and returned.

    """

    if obj.tag == 'path' or obj.tag == inkex.addNS('path', 'svg'):
        objbox = path_bounding_box(obj)
    else:
        objbox = BoundingBox(0, 0, 0, 0)

    if box is None:
        return objbox
    else:
        return box.union(objbox)

def draw_bounding_box(obj, style=None, replace=False):
    """Draws the bounding box of the given object.

    The required argument is the object to draw the bounding box of.
    Two optional arguments can be given; the first, style, sets the
    style to draw the bounding box with. If not given, it defaults to
    the style of the object. The second, replace, is used to set
    whether the bounding box replaces the object in the drawing or if
    it is added to the drawing. It defaults to False.

    """

    # Default to the style of the given object
    if style is None:
        style = obj.get('style')

    # Get the bounding box
    box = get_bounding_box(obj)

    # Convert the bounding box to path data
    points = (box.left, box.bottom, box.right, box.bottom,
              box.right, box.top, box.left, box.top)
    d = 'M%f %f %f %f %f %f %f %f z' % points

    # Create the new node
    boxobj = inkex.etree.Element('path')
    boxobj.set('style', style)
    boxobj.set('d', d)

    # Get the parent of the object
    parent = obj.getparent()

    # Insert the box outline
    parent.insert(parent.index(obj) + 1, boxobj)

    # Remove the object if desired
    if replace:
       parent.remove(node)
