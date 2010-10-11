Transformations
===============

SVG allows objects to be transformed using affine transformations. An affine
transformation is composed of one or more of the following:

* Translation
* Rotation
* Scaling
* Skew (also known as shear)

Matrix representation
---------------------

An affine transformation can be represented as a 3 by 3 matrix. This is the
format used to specify transformations in SVG. The SVG specification also
defines a number of shortcut notations (e.g., ``rotate(angle)``) which are then
mapped to the corresponding matrix.

The general form of the matrix is

.. math::

   \begin{bmatrix}
   a & c & e \\
   b & d & f \\
   0 & 0 & 1
   \end{bmatrix}

The final row is really only there to give the matrix symmetry. For this reason,
most SVG libraries don't require it to be explicitly given, instead representing
transformations either as a 2 by 3 matrix or a vector :math:`[a\ b\ c\ d\ e\ f]`.

Translation
+++++++++++

A translation by vector :math:`(t_x, t_y)` is represented by the matrix

.. math::

   \begin{bmatrix}
   1 & 0 & t_x \\
   0 & 1 & t_y \\
   0 & 0 & 1
   \end{bmatrix}

Rotation
++++++++

A rotation by angle :math:`\theta` is represented by the matrix

.. math::

   \begin{bmatrix}
   \cos\theta & -\sin\theta & 0 \\
   \sin\theta &  \cos\theta & 0 \\
        0     &      0      & 1
   \end{bmatrix}

Scaling
+++++++

Scaling by factors of :math:`s_x` in the x-dimension and :math:`s_y` in the
y-dimension corresponds to the matrix

.. math::

   \begin{bmatrix}
   s_x &  0  & 0 \\
    0  & s_y & 0 \\
    0  &  0  & 1
   \end{bmatrix}


Skew
++++

A skew transformation of angle :math:`\theta` along the x-axis results in the
matrix

.. math::

   \begin{bmatrix}
    1 &  \tan\theta & 0 \\
    0 &      1      & 0 \\
    0 &      0      & 1
   \end{bmatrix}

while a skew transformation of angle :math:`\theta` along the y-axis corresponds
to

.. math::

   \begin{bmatrix}
         1     & 0 & 0 \\
    \tan\theta & 1 & 0 \\
         0     & 0 & 1
   \end{bmatrix}

Combining transformations
-------------------------

Multiple transformations can be combined into one via `matrix multiplication
<http://en.wikipedia.org/wiki/Matrix_multiplication>` in the order they are to
be applied. For example, if a translation (represented by matrix :math:`\mathbf{T}`)
is to be followed by a scale (:math:`\mathbf{S}`), the resulting matrix is
given by

.. math::

   \mathbf{M} = \mathbf{T}\times\mathbf{S}

Applying transformations
------------------------

Applying the transformation representing by the matrix to a point is simply a
case of performing matrix multiplication:

.. math::

   \begin{pmatrix}x_t\\y_t\\1\end{pmatrix}
   =
   \begin{bmatrix}
   a & c & e \\
   b & d & f \\
   0 & 0 & 1
   \end{bmatrix}
   \begin{pmatrix}x\\y\\1\end{pmatrix}

This can be broken down into the following equations:

.. math::

   x_t &= ax + cy + e \\
   y_t &= bx + dy + f
