GEATbx: Function initfun1

# Documentation of initfun1

Index of Functions of GEA Toolbox for Matlab

## Function Synopsis

[Chrom, VLUB] = initfun1(Nind, VLUB, value);

## Help text

 INITialzation function for de jong's FUNction 1

 This function initializes the DE JONG function 1.

 Syntax:  [Chrom, VLUB] = initfun1(Nind, VLUB, value)

 Input parameters:

    Nind      - Number of individuals

    VLUB      - Matrix containing the boundaries of the variables

    P1 - Px   - Additional parameters

 Output parameters:

    Chrom     - Matrix containing the chromosomes of the current

                population. Each row corresponds to one individual's

                string representation.

    VLUB      - (optional) Matrix containing the new boundaries

                of the variables

 See also: objfun1

## Cross-Reference Information

This function calls

This function is called by

- rep

- gatbxini

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
