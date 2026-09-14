GEATbx: Function tbxmpga

# Documentation of tbxmpga

Index of Functions of GEA Toolbox for Matlab

## Function Synopsis

[xnew, GOPTIONS] = tbxmpga(FUN, GOPTIONSIN, VLB, VUB, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10);

## Help text

 ToolBoX Multi Population Genetic Algorithm

 This function implements the multi population genetic algorithm.

 Syntax:  [xnew, GOPTIONS] = tbxmpga(FUN, GOPTIONSIN, VLB, VUB, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10)

 Input parameter:

    FUN       - Name of m-file containing the objective function or

                matlab-expression of objective function

                The function 'FUN' should return the values of the

                objectives, ObjV = FUN(X).

    GOPTIONSIN- matrix of parameters, see chekgopt for details

    VLB       - vector containing lower bounds of domain of objectives

    VUB       - vector containing upper bounds of domain of objectives

    P1-P10    - (optional) parameters, passed through to FUN

 Output parameter:

    xnew      - best objective values of FUN, obtained during all generations.

    GOPTIONS  - same as input parameter, returns parameter set,

                see chekgopt for details

 See also: geamain, scrgtx01, tbxdbga, tbxdbin, tbxloga, chekgopt

## Cross-Reference Information

This function calls

This function is called by

- chekgopt

- geamain

- scrfun1

- scrfun1A

- scrgtx01

- scrgtx02

- scrrastr

- scrsim1

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
