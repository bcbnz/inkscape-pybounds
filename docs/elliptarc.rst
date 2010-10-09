.. _elliptarc:

Elliptical arcs
===============

Parameters
----------

SVG defines an elliptical arc with the following parameters:

* :math:`(x_1,y_1)` - The starting point of the arc, taken from the end point
  of the previous segment.
* :math:`r_x` - The semimajor (x) radius.
* :math:`r_y` - The semiminor (y) radius.
* :math:`\varphi` - The rotation of the x-axis of the ellipse from the x-axis
  of the image.
* :math:`f_A` - The large arc flag. If it is set to 0, an arc spanning 180
  degrees or less is chosen. If it is 1, the arc is greater than 180 degrees.
* :math:`f_S` - The sweep flag. If it is set to 0, the arc sweeps through
  decreasing angles. If it is 1, the arc sweeps through increasing angles.
* :math:`(x_2,y_2)` - The end point of the arc.

Centre point
------------

The centre point :math:`(c_x,c_y)` is calculated in three steps. Firstly, the
midpoint of the line joining the start and end points is calculated:

.. math::

   x_m &= \frac{x_1-x_2}{2}\cos(\varphi) + \frac{y_1-y_2}{2}\sin(\varphi) \\
   y_m &= -\frac{x_1-x_2}{2}\sin(\varphi) + \frac{y_1-y_2}{2}\cos(\varphi)

An intermediate value of the centre points are then calculated with the
equations

.. math::

   c_x' &= \pm\sqrt{\frac{r_x^2r_y^2 - r_x^2y_m^2 - r_y^2x_m^2}{r_x^2y_m^2 + r_y^2x_m^2}}\times\frac{r_xy_m}{r_y} \\
   c_y' &= \pm\sqrt{\frac{r_x^2r_y^2 - r_x^2y_m^2 - r_y^2x_m^2}{r_x^2y_m^2 + r_y^2x_m^2}}\times-\frac{r_yx_m}{r_x}

where the + sign is chosen if the two flags are different (:math:`f_A \neq f_S`)
and the - sign is chosen if the flags are the same (:math:`f_A = f_S`). Finally,
the centre point is calculated:

.. math::

   c_x &= \cos(\varphi)c_x' - \sin(\varphi)c_y' + \frac{x_1 + x_2}{2} \\
   c_y &= \sin(\varphi)c_x' + \cos(\varphi)c_y' + \frac{y_1 + y_2}{2}

Starting and sweep angles
-------------------------

The angle between two vectors :math:`\vec{a}` and :math:`\vec{b}` is given by

.. math::

   \Theta(\vec{a}, \vec{b}) = \mathrm{atan2}(b_y, b_x) - \mathrm{atan2}(a_y, a_x)

The :math:`\mathrm{atan2}(y,x)` function is provided by most math libraries. It
returns the arctangent of :math:`\frac{y}{x}`, using the signs of the inputs to
get the correct quadrant for the angle. See the `Python math library
documentation <http://docs.python.org/library/math.html#trigonometric-functions>`_
for further information on :math:`\mathrm{atan2}`.

The starting angle of the arc is calculated as follows:

.. math::

    \vec{a} &= (1, 0) \\
    \vec{b} &= \left(\frac{x_m - c_x'}{r_x}, \frac{y_m - c_y}{r_y}\right) \\
   \theta_1 &= \Theta(\vec{a}, \vec{b})

The angle that the arc sweeps over is calculated as:

.. math::

        \vec{c} &= \left(\frac{-x_m - c_x'}{r_x}, \frac{-y_m - c_y}{r_y}\right) \\
   \Delta\theta &= \Theta(\vec{b}, \vec{c}) \mod 360^\circ

:math:`\Delta\theta` is adjusted by adding or subtracting 360 degrees as
necessary to meet the conditions

.. math::

   &\Delta\theta < 0 \qquad f_S = 0 \\
   &\Delta\theta > 0 \qquad \mathrm{otherwise}

Extrema
-------

The point :math:`(x,y)` at an angle :math:`\theta` from the centre is given by
the equations

.. math::
   :label: arcpos

   x(\theta) &= c_x + r_x\cos(\theta)\cos(\varphi) - r_y\sin(\theta)\sin(\varphi) \\
   y(\theta) &= c_y + r_x\cos(\theta)\sin(\varphi) + r_y\sin(\theta)\cos(\varphi)

To find the angles at which any extrema are located, we differentiate these
functions and solve for :math:`\theta` when the derivative is zero. Remembering
that :math:`\varphi` and hence :math:`\cos(\varphi)` and :math:`\sin(\varphi)`
are constants, the derivatives of these functions are:

.. math::

   \frac{\mathrm{d}x(\theta)}{\mathrm{d}\theta} &= -r_x\sin(\theta)\cos(\varphi) - r_y\cos(\theta)\sin(\varphi) \\
   \frac{\mathrm{d}y(\theta)}{\mathrm{d}\theta} &= -r_x\sin(\theta)\sin(\varphi) + r_y\cos(\theta)\cos(\varphi)

Setting these to zero and solving for :math:`\theta` gives the angles at which
extrema occur as

.. math::

   \theta_x &= \arctan\left(-\frac{r_y}{r_x}\tan(\varphi)\right) \\
   \theta_y &= \arctan\left(\frac{r_y}{r_x}\cot(\varphi)\right)

Due to the periodic nature of the trigonometric functions, these will give
multiple solutions. We restrict the values to those that are swept by the arc,
and then find the values of the extrema by evaluating :eq:`arcpos` at these
locations. Along with the start and end points of the arc, these extrema are
then used to generate the bounding box of the arc.

External links
--------------

* `Arc implementation notes <http://www.w3.org/TR/SVG11/implnote.html#ArcImplementationNotes>`_
