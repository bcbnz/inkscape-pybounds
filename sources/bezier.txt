.. _bezier:

Bézier curves
=============

The Bézier curve is a parametric curve commonly used in graphics applications
as they are smooth and scalable. They were first developed in 1959 by Paul de
Casteljau, and were widely publicised by Pierre Bézier. The Bézier curve of
degree :math:`n` is defined as

.. math::

   B_n(t) = \sum_{i=0}^n b_{i,n}(t)P_i \qquad t \in [0,1]

where the polynomials

.. math::

   b_{i,n}(t) = \frac{n!(1-t)^{n-1}t^i}{i!(n-i)!} \qquad i=0,1,\ldots,n

are known as the Bernstein basis polynomials, and the points
:math:`P_0,P_1,\ldots,P_n` are the control points. The curve begins at :math:`P_0`
and ends at :math:`P_n`.

The derivative of a Bézier curve is given by

.. math::

   B_n'(t) = \sum_{i=0}^{n-1} b_{i,n-1}(t)Q_i

where :math:`Q_i = n(P_{i+1} - P_i)`, i.e., the derivative is itself a Bézier
curve of degree :math:`n-1`.

SVG (and thus Inkscape) uses both quadratic (:math:`n=2`) and cubic (:math:`n=3`)
Bézier curves. Hence we need to be able to calculate the bounding box of a Bézier
curve.

Loose bounds
------------

The convex hull of the control points :math:`P_0,P_1,\ldots,P_n` contains the
entire curve. Hence, a bounding box which encompasses all the control points is
guaranteed to encompass the curve. However, unless all the control points are
colinear (i.e., the curve actually describes a straight line), this will not be
a tight bounding box.

Tight bounds
------------

The curve is guaranteed to pass through the start and end points (:math:`P_0`
and :math:`P_n`) so the initial bounding box is one that encompasses these two
points. We then need to extend it so it includes the maxima and minima of the
curve. To find the locations of these extrema, we set the derivative of the
curve to zero and solve for :math:`t`. The extrema themselves can then be found
by evaluating the curve at these locations.

If we have an existing bounding box (e.g, if this curve is not the first path
segment we are getting a box for), we can check if all the control points
already fit inside this box. If so, there is no need to continue as the
existing box already encompasses the entire curve.

Quadratic Bézier curve
++++++++++++++++++++++

A quadratic Bézier curve requires three control points, and is defined by the
formula

.. math::

   B_2(t) = (1 - t)^2P_0 + 2(1 - t)tP_1 + t^2P_2

Its derivative is

.. math::

   B_2'(t) = 2(1 - t)Q_0 + 2tQ_1

Setting this to zero and solving for :math:`t` gives

.. math::

   t = \frac{Q_0}{Q_0 - Q_1}

As we need to find the extrema in both the x and y dimensions, we need to split
this into two:

.. math::

   t_x &= \frac{Q_{0,x}}{Q_{0,x} - Q_{1,x}} \\
   t_y &= \frac{Q_{0,y}}{Q_{0,y} - Q_{1,y}}

If :math:`0 < t_x < 1` then this is the location of an extrema in the x
dimension, and hence we extend the bounding box to encompass the x value of
:math:`B_2(t_x)`. Similarly, if :math:`0 < t_y < 1` we have an extrema in the
y direction, and hence extend the bounding box to encompass the y value of
:math:`B_2(t_y)`. We now have a tight bounding box for the curve.

Cubic Bézier curve
++++++++++++++++++

A cubic Bézier curve require four control points, and is defined by the
function

.. math::

   B_3(t) = (1 - t)^3P_0 + 3(1 - t)^2tP_1 + 3(1 - t)t^2P_2 + t^3P_3

Its derivative is the quadratic Bézier curve

.. math::

   B_3'(t) = 3(1 - t)^2Q_0 + 6(1 - t)tQ_1 + 3t^2Q_2

Setting this to zero and expanding and collecting terms gives the quadratic
equation

.. math::

   \left(3Q_0 - 6Q_1 + 3Q_2\right)t^2 + \left(-6Q_0 + 6Q_1\right)t + 3Q_0 = 0

Applying the quadratic formula gives

.. math::

   t = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}

where

.. math::

   a &= 3Q_0 - 6Q_1 + 3Q_2 \\
   b &= -6Q_0 + 6Q_1 \\
   c &= 3Q_0

As with the quadratic Bézier curve, we need to split this into the x and y
components to find the extrema in both dimensions. Either one or two possible
solutions will be found by the quadratic formula in each dimension. To be
valid, a solution must be real and meet the criteria :math:`0 < t < 1`. If this
is the case, :math:`B_3(t)` is evaluated at this point and the bounding box is
extended appropriately. Once this has been completed for all solutions in both
dimensions, we have a tight bounding box for the curve.

External links
--------------

* `Bézier curve <http://en.wikipedia.org/wiki/B%C3%A9zier_curve>`_ at Wikipedia
* `Derivatives of a Bézier curve <http://www.cs.mtu.edu/~shene/COURSES/cs3621/NOTES/spline/Bezier/bezier-der.html>`_
