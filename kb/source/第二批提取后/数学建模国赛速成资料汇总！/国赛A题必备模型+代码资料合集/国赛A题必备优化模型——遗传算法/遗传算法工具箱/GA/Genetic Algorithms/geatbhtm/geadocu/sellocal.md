GEATbx: Function sellocal

# Documentation of sellocal

Index of Functions of GEA Toolbox for Matlab

## Function Synopsis

NewChrIx = sellocal(FitnV, Nsel, SelOpt);

## Help text

 SELection in the LOCAL neighbourhood

 This function performs SELection in the LOCAL neighbourhood.

 Syntax:  NewChrIx = sellocal(FitnV, Nsel, SelOpt)

 Input parameters:

    FitnV     - Column vector containing the fitness values of the

                individuals in the population.

    Nsel      - Number of individuals to be selected

    SelOpt    - (optional) Vector containing selection paremeters

                SelOpt(1): Structure - number indicating the structure

                           of the neighbourhood

                           0: linear, full; 1: linear, half;

                           2: torus, full star; 3: torus, half star;

                           if omitted or NaN, 0 is assumed

 Output parameters:

    NewChrIx  - Column vector containing the indexes of the selected

                individuals relative to the original population, shuffeld.

                The new population, ready for mating, can be obtained

                by calculating OldChrom(NewChrIx,:).

 See also: select, selsus, selrws, seltrunc, reinsloc

## Cross-Reference Information

This function calls

This function is called by

- rep

- selsus

- dgagraf

- dgampga

- gatbxini

- geamain

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
