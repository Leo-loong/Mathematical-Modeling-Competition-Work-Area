GEATbx: Function rep

# Documentation of rep

Index of Functions of GEA Toolbox for Matlab

## Function Synopsis

MatOut = rep(MatIn, REPN)

## Help text

 REPlicate a matrix, utility function

 This function repeats a matrix MatIn in both dimensions.

 In the output matrix MatOut the input matrix MatIn is

 repeated as often as defined in REPN. The size of MatOut is

 [REPN(1)*size(MatIn,1), REPN(2)*size(MatIn,2)].

 This function is widely used in the GEA Toolbox.

 Syntax:  MatOut = rep(MatIn, REPN);

 Input parameters:

    MatIn     - Input Matrix (befor replicating)

    REPN      - Vector of 2 numbers, how often replicate in each

                   dimensiom

                REPN(1): replicate vertically

                REPN(2): replicate horizontally

 Output parameter:

    MatOut    - Output Matrix (after replicating)

 Example:

    MatIn = [1 2 3;

             4 5 6]

    REPN = [1 2] => MatOut = [1 2 3 1 2 3;

                              4 5 6 4 5 6]

    REPN = [2 1] => MatOut = [1 2 3;

                              4 5 6;

                              1 2 3;

                              4 5 6]

    REPN = [3 2] => MatOut = [1 2 3 1 2 3;

                              4 5 6 4 5 6;

                              1 2 3 1 2 3;

                              4 5 6 4 5 6;

                              1 2 3 1 2 3;

                              4 5 6 4 5 6]

 See also: expandm

## Cross-Reference Information

This function is called by

- bindecod

- chekgopt

- compdiv

- dgacad1

- dgamesh

- dgampga

- geamain

- initdopi

- initfun1

- initrp

- mutate

- mutbga

- mutevo1

- objdopi

- objfun1

- objfun10

- objfun11

- objfun12

- objfun1a

- objfun1b

- objfun1c

- objfun2

- objfun6

- objfun7

- objfun8

- objfun9

- objharv

- objint1

- objlinq

- objlinq2

- objone1

- objpush

- recmut

- recombin

- reinsloc

- scrgtx02

- select

- sellocal

- selrws

- selsus

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
