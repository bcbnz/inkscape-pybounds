# -*- coding: utf-8 -*-
"""
Functions to calculate and work with bounding boxes in Inkscape extensions.

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
from math import sqrt, sin, cos, tan, radians, atan2, pi

import inkex
import simpletransform
import simplepath


# Module version information as per the sys module
version = '0.9.0 alpha 1'
version_info = (0, 9, 0, 'alpha', 1)
hexversion = 0x000900a1

class BoundingBox:
    """A class which represents a bounding box. It has four attributes
    (left, right, bottom and top) which define the edges of the box, and
    a number of functions to work with the box.

    """

    def __init__(self, x0, x1, y0, y1):
        """
        :param x1: The x-value representing one vertical edge of the box.
        :param x2: The x-value representing the other vertical edge.
        :param y1: The y-value representing one horizontal edge of the box.
        :param y2: The y-value representing the other horizontal edge.

        When creating the box, the constructor will automatically choose the
        lower of the two x-values for the left edge and the higher for the
        right. Similarly, the lower y-value is used for the bottom of the box
        and the higher for the top of the box.

        """
        self.left = min(x0, x1)
        self.right = max(x0, x1)
        self.bottom = min(y0, y1)
        self.top = max(y0, y1)

    def contains(self, point):
        """Check if the given point is contained with this box.

        :param point: The point to check specified as a pair of numbers (x,y).
        :return: True or False.

        """
        if point[0] < self.left or point[0] > self.right:
            return False
        if point[1] < self.bottom or point[1] > self.top:
            return False
        return True

    def contains_x(self, x):
        """Check if the given x value is within the range of x values
        encompassed by the box.

        :param x: The x value to check.
        :return: True or False

        """
        if x < self.left or x > self.right:
            return False
        return True

    def contains_y(self, y):
        """Check if the given y value is within the range of y values
        encompassed by the box.

        :param y: The y value to check.
        :return: True or False

        """
        if y < self.bottom or y > self.top:
            return False
        return True

    def combine(self, box):
        """Combines this box with another bounding box. This extends the edges
        of this box as necessary to encompass the contents of the other box.

        :param box: The other box.

        """
        self.left = min(self.left, box.left)
        self.right = max(self.right, box.right)
        self.bottom = min(self.bottom, box.bottom)
        self.top = max(self.top, box.top)

    def extend(self, point):
        """Extend the box as necessary to encompass the given point.

        :param point: The point specified as a pair of numbers (x,y).

        """
        self.left = min(self.left, point[0])
        self.right = max(self.right, point[0])
        self.bottom = min(self.bottom, point[1])
        self.top = max(self.top, point[1])

    def extend_x(self, x):
        """Extend the width of the box as necessary to include the given x
        point.

        :param x: The x point to include.

        """
        self.left = min(self.left, x)
        self.right = max(self.right, x)

    def extend_y(self, y):
        """Extend the height of the box as necessary to include the given y
        point.

        :param y: The y point to include.

        """
        self.bottom = min(self.bottom, y)
        self.top = max(self.top, y)

def quadratic_bounding_box(p0, p1, p2, box=None):
    """Calculate the bounding box of a quadratic Bézier curve.

    :param p0: The start point of the curve.
    :param p1: The control point of the curve.
    :param p2: The end point of the curve.
    :param box: The current bounding box if available.
    :return: A :class:`bounds.BoundingBox` encompassing the curve.

    The three points defining the curve must be given as pairs of numbers
    ``(x,y)``.

    If an existing BoundingBox is given in the ``box`` argument, it is extended
    as necessary to encompass the curve and then returned. If no box is given,
    a new one encompassing the curve is created and returned.

    See the :ref:`bezier` page in the accompanying documentation for further
    details on how Bézier curves are defined, and how their bounding boxes are
    calculated.

    """

    # Make sure the box encompasses the endpoints
    if box is None:
        box = BoundingBox(p0[0], p2[0], p0[1], p2[1])
    else:
        box.extend(p0)
        box.extend(p2)

    # All the points of a cubic Bézier curve lie in the convex hull of the
    # three points. So if the box already includes p1, it contains the entire
    # curve.
    contains_x = box.contains_x(p1[0])
    contains_y = box.contains_y(p1[1])

    # If not already encompassed, find the extrema in the x direction
    if not contains_x:
        q0 = p1[0] - p0[0]
        q1 = p2[0] - p1[0]
        t = q0 / (q0 - q1)

        if t > 0.0 and t < 1.0:
            x = p0[0]*(1 - t)**2 + p1[0]*2*(1-t)*t + p2[0]*t**2
            box.extend_x(x)

    # If not already encompassed, find the extrema in the y direction
    if not contains_y:
        q0 = p1[1] - p0[1]
        q1 = p2[1] - p1[1]
        t = q0 / (q0 - q1)

        if t > 0.0 and t < 1.0:
            y = p0[1]*(1 - t)**2 + p1[1]*2*(1-t)*t + p2[1]*t**2
            box.extend_y(y)

    # And done
    return box

def cubic_bounding_box(p0, p1, p2, p3, box=None):
    """Calculate the bounding box of a cubic Bézier curve.

    :param p0: The start point of the curve.
    :param p1: The first control point of the curve.
    :param p2: The second control point of the curve.
    :param p3: The end point of the curve.
    :param box: The current bounding box if available.
    :return: A :class:`bounds.BoundingBox` encompassing the curve.

    The four points defining the curve must be given as pairs of numbers
    ``(x,y)``.

    If an existing BoundingBox is given in the ``box`` argument, it is extended
    as necessary to encompass the curve and then returned. If no box is given,
    a new one encompassing the curve is created and returned.

    See the :ref:`bezier` page in the accompanying documentation for further
    details on how Bézier curves are defined, and how their bounding boxes are
    calculated.

    """

    # Make sure the box encompasses the endpoints
    if box is None:
        box = BoundingBox(p0[0], p3[0], p0[1], p3[1])
    else:
        box.extend(p0)
        box.extend(p3)

    # All the points of a cubic Bézier curve lie in the convex hull of the
    # four points. So if the box already includes p1 and p2, it contains the
    # entire curve, and thus we can avoid calculating the extrema.
    contains_x = box.contains_x(p1[0]) and box.contains_x(p2[0])
    contains_y = box.contains_y(p1[1]) and box.contains_y(p2[1])

    # Helper function to calculate the extrema values for the given points.
    # Used since identical logic is required to calculate both x and y extrema.
    def extrema_values(p0, p1, p2, p3):
        # Values for the quadratic formula
        # Note a is actually 2a - it is always used as 2a or 4a so this reduces
        # the number of computations.
        a = 6*(p1-p0) - 12*(p2-p1) + 6*(p3-p2)
        b = -6*(p1-p0) + 6*(p2-p1)
        c = 3*(p1-p0)

        # Check the discriminant - solutions must be real
        discriminant = b**2 - (2*a*c)
        if discriminant < 0:
            return []

        # Lambda function to calculate value from location
        bezier = lambda t: p0*(1-t)**3 + 3*p1*t*(1-t)**2 + 3*p2*(1-t)*t**2 + p3*t**3

        # Value of -b/2a is used repeatedly
        ba = -b / a

        # Single (repeated) real value
        if discriminant == 0:
            t = ba
            if t > 0.0 and t < 1.0:
                return [bezier(t)]
            else:
                return []

        # Pair of values
        vals = []
        discriminant = sqrt(discriminant) / a
        t = ba + discriminant
        if t > 0.0 and t < 1.0:
            vals.append(bezier(t))
        t = ba - discriminant
        if t > 0.0 and t < 1.0:
            vals.append(bezier(t))
        return vals

    # Calculate the extent of the curve in the x-direction
    if not contains_x:
        vals = extrema_values(p0[0], p1[0], p2[0], p3[0])
        for x in vals:
            box.extend_x(x)

    # Calculate the extent of the curve in the y-direction
    if not contains_y:
        vals = extrema_values(p0[1], p1[1], p2[1], p3[1])
        for y in vals:
            box.extend_y(y)

    # And done
    return box

def elliptical_arc_bounding_box(start, rx, ry, rotation, large_arc, sweep, end,
                                box=None):
    """Compute the bounding box for an SVG elliptical arc.

    :param start: The start point of the arc.
    :param rx: The semi-major (x) radius of the arc.
    :param ry: The semi-minor (y) radius of the arc.
    :param rotation: The angle at which the x-axis of the arc is rotated from
                     the x-axis of the image.
    :param large_arc: If the angle swept by the arc is greater than 180 degrees.
    :param sweep: Which direction the arc is swept in.
    :param end: The end point of the arc.
    :param box: The current bounding box if available.
    :return: A :class:`bounds.BoundingBox` encompassing the arc.

    One of the types of segments available for use in an SVG path is the
    elliptical arc. This is largely defined from the start and end points, and
    the semi-major and semi-minor radii. This gives four possible arcs; the
    ``large_arc`` and ``sweep`` flags set which arc is used. If ``sweep`` is
    zero, the arg is swept through decreasing angles; otherwise it is swept
    through increasing angles. If ``large_arc`` is zero, the arc will span 180
    degrees or less; otherwise, it will be greater than 180 degrees. Finally,
    the x-axis of the arc can be rotated from the x-axis of the image; the
    angle it is rotated at (in degrees) is given by the ``rotation`` parameter.

    This function calculates the bounding box necessary to contain an
    elliptical arc. If an existing BoundingBox is given in the ``box``
    argument, it is extended as necessary to encompass the arc and then
    returned. If no box is given, a new one encompassing the arc is created and
    returned.

    As per the SVG 1.1 specification, out-of-range parameters are handled as
    follows:

    * If the start and end points are the same, the arc is not drawn. In this
      case, the value of the ``box`` parameter (an existing bounding box or
      ``None``) is returned.
    * If either ``rx`` or ``ry`` is zero, the arc is treated as a straight line
      segment.
    * If either ``rx`` or ``ry`` are negative, the absolute value is used as
      the corresponding radius.
    * If ``rx``, ``ry`` and ``rotation`` are such that the ellipse is not big
      enough to reach from the start to the end, the ellipse is scaled
      uniformly until it can reach.
    * Any non-zero value for either ``large_arc`` or ``sweep`` is treated as if
      the value ``1`` was given.

    See the :ref:`elliptarc` page in the accompanying documentation for further
    details on how elliptical arcs are defined, and how their bounding boxes
    are calculated.

    """

    # If the endpoints are the same, the elliptical arc will not be drawn.
    if start == end:
        return box

    # Ensure the endpoints are in the box.
    if box is None:
        box = BoundingBox(start[0], end[0], start[1], end[1])
    else:
        box.extend(start)
        box.extend(end)

    # If either radius is zero, it is treated as a straight line. As we already
    # added the endpoints, our work here is done.
    if rx == 0 or ry == 0:
        return box

    # Make sure the radii are positive.
    if rx < 0:
        rx = -rx
    if ry < 0:
        ry = -ry

    # Ensure the flags to boolean values. As per the SVG 1.1 specification,
    # non-zero values for large_arc or sweep are treated as true.
    if large_arc != 0:
        large_arc = True
    if sweep != 0:
        sweep = True

    # Convert rotation angle to radians as this is what the Python
    # trigonometric functions work with. Also pre-compute the sine and cosine
    # of the angle.
    rotation = radians(rotation)
    sin_rotation = sin(rotation)
    cos_rotation = cos(rotation)

    # Unpack the start and end points.
    x1, y1 = start
    x2, y2 = end

    # Transform the origin to the midpoint of the line joining the start and
    # end points.
    xm =  (cos_rotation * (x1 - x2)/2.0) + (sin_rotation * (y1 - y2)/2.0)
    ym = -(sin_rotation * (x1 - x2)/2.0) + (cos_rotation * (y1 - y2)/2.0)

    # Pre-square some values.
    rx2 = rx**2
    ry2 = ry**2
    xm2 = xm**2
    ym2 = ym**2

    # Numerator of the root used to calculated the transformed centre.
    numerator = rx2*ry2 - rx2*ym2 - ry2*xm2

    # If the numerator is negative, there are no solutions for the centre point
    # (i.e., the radii are not large enough to join the start and end). Per the
    # SVG 1.1 specification, we increase the radii to obtain a solution.
    if numerator < 0.0:
        s = sqrt(1.0 - numerator/(rx2*ry2))
        rx = rx * s
        ry = ry * s
        rx2 = rx**2
        ry2 = ry**2
        root = 0.0

    # Radii were large enough
    else:
        if large_arc == sweep:
            root = -1 * sqrt(numerator/(rx2*ym2 + ry2*xm2))
        else:
            root = sqrt(numerator/(rx2*ym2 + ry2*xm2))

    # Calculate the transformed centre
    cxprime =  (root * rx * ym)/ry
    cyprime = -(root * ry * xm)/rx

    # Calculate the centre
    cx = (cos_rotation * cxprime) - (sin_rotation * cyprime) + (x1 + x2)/2.0
    cy = (sin_rotation * cxprime) + (cos_rotation * cyprime) + (y1 + y2)/2.0

    # Function to calculate the angle between two vectors mod 360 degrees.
    def angle_between_vectors(a, b):
        atana = atan2(a[1], a[0])
        atanb = atan2(b[1], b[0])
        if atanb >= atana:
            return atanb - atana;
        return (2 * pi) - (atana - atanb);

    # Calculate the start angle and angle the arc sweeps through
    theta1 = angle_between_vectors((1.0, 0.0), ((xm - cxprime)/rx, (ym - cyprime)/ry))
    dtheta = angle_between_vectors(((xm - cxprime)/rx,  (ym - cyprime)/ry),
                                  ((-xm - cxprime)/rx, (-ym - cyprime)/ry))

    # Make sure the sweep angle is in the correct range based upon the sweep
    # flag.
    if not sweep and dtheta > 0:
        dtheta = dtheta - (2.0 * pi);
    elif sweep and dtheta < 0:
        dtheta = dtheta + (2.0 * pi);

    # Convert to start and end angles in the range [-pi, pi] as this is the
    # region atan2 will return extrema locations in.
    if theta1 > pi:
        start_angle = theta1 - (2*pi)
    else:
        start_angle = theta1
    theta2 = start_angle + dtheta
    if theta2 > pi:
        end_angle = theta2 - (2*pi)
    elif theta2 < -pi:
        end_angle = theta2 + (2*pi)
    else:
        end_angle = theta2

    # Helper function to check if the arc sweeps over the given angle.
    def contains_angle(t):
        if sweep:
            if start_angle < end_angle:
                return not (t < start_angle or t > end_angle)
            else:
                return not (t < start_angle and t > end_angle)
        else:
            if start_angle > end_angle:
                return not (t > start_angle or t < end_angle)
            else:
                return not (t > start_angle and t < end_angle)

    # Calculate the angle of the first maximas
    thetax = atan2(-ry * tan(rotation), rx)
    thetay = atan2(ry, rx * tan(rotation))

    # The second maximas will be pi radians away
    if thetax < 0:
        xangles = [thetax, thetax + pi]
    else:
        xangles = [thetax, thetax - pi]
    if thetay < 0:
        yangles = [thetay, thetay + pi]
    else:
        yangles = [thetay, thetay - pi]

    # Lambda functions to get the x or y value of the arc at a given angle
    fx = lambda t: cx + (rx * cos(t) * cos_rotation) - (ry * sin(t) * sin_rotation)
    fy = lambda t: cy + (rx * cos(t) * sin_rotation) + (ry * sin(t) * cos_rotation)

    # Extend the box to include any extrema swept by the arc
    for t in xangles:
        if contains_angle(t):
            box.extend_x(fx(t))
    for t in yangles:
        if contains_angle(t):
            box.extend_y(fy(t))

    # And done
    return box

def path_bounding_box(path, box=None):
    """Compute the bounding box for an SVG path.

    :param path: The XML node defining the path.
    :param box: The existing :class:`bounds.BoundingBox` if available.
    :return: A :class:`bounds.BoundingBox` encompassing the path.

    SVG paths are a collection of various types of segments:

    * Straight lines
    * Quadratic Bézier curves
    * Cubic Bézier curves
    * Elliptical arcs

    This function splits the path into its segments, calculates the bounding
    box for each segment and combines them to get the bounding box of the path.
    If an existing bounding box is given in the ``box`` parameter, it is
    extended to encompass the path and returned. Otherwise, a new bounding box
    is created and returned.

    """

    # Get the transform
    transform = path.get('transform', None)
    if transform:
        transform = simpletransform.parseTransform(transform)

    # Parse the path details.
    # Note that when parsing all path segments are converted to absolute
    # coordinates. It also converts H and V segments to L, S segments to C and
    # T segments to Q.
    parsed = simplepath.parsePath(path.get('d'))

    # Starting point
    current = parsed[0][1]
    if transform:
        simpletransform.applyTransformToPoint(transform, current)
    objbox = BoundingBox(current[0], current[0], current[1], current[1])

    # Loop through each segment.
    for type,params in parsed[1:]:
        # End of path
        if type == 'Z':
            break

        # Line or move to
        elif type == 'L' or type == 'M':
            point = params
            if transform:
                simpletransform.applyTransformToPoint(transform, point)
            objbox.extend(point)
            current = point

        # Cubic Bézier curve
        elif type == 'C':
            p1 = params[0:2]
            p2 = params[2:4]
            p3 = params[4:6]
            if transform:
                simpletransform.applyTransformToPoint(transform, p1)
                simpletransform.applyTransformToPoint(transform, p2)
                simpletransform.applyTransformToPoint(transform, p3)
            objbox = cubic_bounding_box(current, p1, p2, p3, objbox)
            current = p3

        # Quadratic Bézier curve
        elif type == 'Q':
            p1 = params[0:2]
            p2 = params[2:4]
            if transform:
                simpletransform.applyTransformToPoint(transform, p1)
                simpletransform.applyTransformToPoint(transform, p2)
            objbox = quadratic_bounding_box(current, p1, p2, objbox)
            current = p2

        # Elliptical arc
        elif type == 'A':
            rx, ry, rotation, large_arc, sweep = params[0:5]
            end = params[5:7]
            if transform:
                simpletransform.applyTransformToPoint(transform, end)
            objbox = elliptical_arc_bounding_box(current, rx, ry, rotation,
                                                 large_arc, sweep, end, objbox)
            current = end

        # Unknown segment type
        else:
            raise Exception(_('Unknown path segment type %s.' % type))

    # Returnt the appropriate box
    if box is None:
        return objbox
    else:
        return box.combine(objbox)

def object_bounding_box(obj, box=None):
    """Get the bounding box of an SVG object.

    :param obj: The XML node defining the object.
    :param box: The existing :class:`bounds.BoundingBox` if available.
    :return: A :class:`bounds.BoundingBox` encompassing the object.

    SVG images are constructed of a number of primitive objects (paths,
    rectangles, circles, groups etc.). This function takes an arbitrary object,
    determines what type of object is, and calculates the bounding box
    correspondingly.

    If an existing bounding box is given in the ``box`` parameter, it is
    extended to encompass the object and returned. Otherwise, a new bounding
    box is created and returned.

    Currently, this function can only handle ``path`` objects.

    """

    if obj.tag == 'path' or obj.tag == inkex.addNS('path', 'svg'):
        objbox = path_bounding_box(obj)
    else:
        objbox = BoundingBox(0, 0, 0, 0)

    if box is None:
        return objbox
    else:
        return box.combine(objbox)

def draw_bounding_box(obj, style=None, replace=False):
    """Draws the bounding box of the given object.

    :param obj: The XML node representing the object.
    :param style: The SVG style to draw the bounding box with.
    :param replace: Whether to replace the object with its bounding box.

    This function draws the bounding box around the given object. If no style
    is specified, the style of the object is used to draw the bounding box. If
    ``replace`` is ``True``, the object is removed from the image and is
    replaced by its bounding box. If it is ``False``, the bounding box is drawn
    on top of the object.

    """

    # Default to the style of the given object
    if style is None:
        style = obj.get('style')

    # Get the bounding box
    box = object_bounding_box(obj)

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
