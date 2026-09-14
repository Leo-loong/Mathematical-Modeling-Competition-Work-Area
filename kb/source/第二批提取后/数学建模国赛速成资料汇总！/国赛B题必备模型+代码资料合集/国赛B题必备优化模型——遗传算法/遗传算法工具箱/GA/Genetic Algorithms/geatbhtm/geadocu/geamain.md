GEATbx: Function geamain

# Documentation of geamain

Index of Functions of GEA Toolbox for Matlab

## Function Synopsis

[xnew, GOPTIONS] = geamain(OBJ_F, GOPTIONS, VLB, VUB, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10);

## Help text

 high level entry function for GENetic ALGorithm toolbox for matlab

 This function is the main driver for the GA Toolbox.

 Here all the parameters are resolved and the appropriate

 functions are called. Additionally, result functions and

 plot functions are called.

 Syntax:  [xnew, GOPTIONS] = geamain(OBJ_F, GOPTIONS, VLB, VUB, P1, P2, P3, P4, P5, P6, P7, P7, P8, P9, P10)

 Input parameter:

    OBJ_F     - Name of m-file containing the objective function or

                matlab-expression of objective function

                The function 'OBJ_F' should return the values of the objectives, ObjV.

                ObjV = OBJ_F(X).

    GOPTIONS  - vector of parameters, see ckekgopt for details or documentation

    VLB       - vector containing lower bounds of domain of objectives

    VUB       - vector containing upper bounds of domain of objectives

    P1-P10    - (optional) parameters, passed through to OBJ_F

 Output parameter:

    xnew      - best objective values of OBJ_F, obtained during all generations.

    GOPTIONS  - same as input parameter, returns parameter set, see fgoption for details

 See also: tbxmpga, tbxdbga, tbxloga, dgagraf

## Cross-Reference Information

This function calls

This function is called by

- bin2int

- bin2real

- compdiv

- gatbxini

- initbp

- initrp

- migrate

- mutate

- ranking

- recombin

- reins

- reinsloc

- rep

- resplot

- select

- sellocal

- tbxdbga

- tbxdbin

- tbxes1

- tbxloga

- tbxmpga

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
