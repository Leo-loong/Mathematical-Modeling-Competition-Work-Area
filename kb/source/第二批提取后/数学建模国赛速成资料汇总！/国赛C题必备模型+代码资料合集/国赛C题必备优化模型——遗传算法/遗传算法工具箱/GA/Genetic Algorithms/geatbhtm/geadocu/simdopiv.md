GEATbx: Function simdopiv

# Documentation of simdopiv

Index of Functions of GEA Toolbox for Matlab

## Function Synopsis

[sys, x0] = simdopiv(t, x, u, flag);

## Help text

 SIMulation Modell of DOPpelIntegrator, s-function, Vectorized

 This function implements the modell of the double integrator.

 Syntax:  [sys, x0] = simdopiv(t, x, u, flag)

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

 See also: objdopi, simdopi1, simlinq2

## Cross-Reference Information

This function is called by

- objdopi

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
