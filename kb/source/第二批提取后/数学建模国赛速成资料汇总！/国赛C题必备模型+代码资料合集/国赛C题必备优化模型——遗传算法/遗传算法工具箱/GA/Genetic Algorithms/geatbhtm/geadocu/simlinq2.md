GEATbx: Function simlinq2

# Documentation of simlinq2

Index of Functions of GEA Toolbox for Matlab

## Function Synopsis

[sys, x0] = simlinq2(t, x, u, flag);

## Help text

 Modell of Linear Quadratic Problem, s-function

 This function implements the modell of the Linear Quadratic Problem.

 Syntax:  [sys, x0] = simlinq2(t, x, u, flag)

 Input parameters:

    t         - given time point

    x         - current state vector

                1 column for every individual

    u         - input vector

                1 column for every individual

    flag      - flags

 Output parameters:

    sys       - Vector containing the new state derivatives

                1 column for every individual

    x0        - initial value

 See also: objlinq2, objlinq, simdopiv, simdopi1

## Cross-Reference Information

This function is called by

- objlinq2

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
