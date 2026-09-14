GEATbx: Function dgamesh

# Documentation of dgamesh

Index of Functions of GEA Toolbox for Matlab

## Function Synopsis

dgamesh(OBJ_F, Bounds, Points)

## Help text

 Demo GeA toolbox MESH Plot of objective functions

 This function takes the name of an objective function and produces

 a mesh plot using the first 2 dimensions. This gives a first impression

 of the objective function and is particular useful in demos.

 Syntax:  dgamesh(OBJ_F, Bounds, Points)

 Input:

    OBJ_F     - string with function name of objective function

                if omitted, 'objfun1' is assumed

    Bounds    - Matrix containing the boundaries of the objective

                function for mesh plotting, same format as in

                objective function.

                Bounds=[lower_bound_x1, lower_bound_x2;

                        upper_bound_x1, upper_bound_x2]

    Points    - Scalar/vector containing number of mesh grid points.

                If 2 scalars are provided, the first is used for

                points in x1 and the second for points in x2.

                If 1 scalar is provided it is used for points in x1 and x2

                if ommitted, 50 points in both directions are assumed

 Output:

   no output

 See also: dgagraf

 Examples:

    % plot with default parameters

       dgamesh('objfun1');

    % use default boundaries, use 20 grid point in both dimensions

       dgamesh('objfun1', [], 20);

    % same boundaries for both dimensions, use 100 grid points per dimension

       dgamesh('objfun1', [-10; 10], 100);

    % define everything

       dgamesh('objfun1', [-10, -5; 10, 5], [40, 30]);

## Cross-Reference Information

This function calls

This function is called by

- objfun1

- plotstd

- rep

- dgagraf

- scrfun1

- scrgtx02

- scrrastr

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
