GEATbx: Function seltrunc

# Documentation of seltrunc

Index of Functions of GEA Toolbox for Matlab

## Function Synopsis

NewChrIx = seltrunc(FitnV, Nsel, Dummy);

## Help text

 SELection by TRUNCation

 This function performs SELection by TRUNCation.

 Syntax:  NewChrIx = seltrunc(FitnV, Nsel)

 Input parameters:

    FitnV     - Column vector containing the fitness values of the

                individuals in the population.

    Nsel      - Number of individuals to be selected

 Output parameters:

    NewChrIx  - Column vector containing the indexes of the selected

                individuals relative to the original population, shuffeld.

                The new population, ready for mating, can be obtained

                by calculating OldChrom(NewChrIx,:).

 For the truncation threshold the inverse of the selection

 pressure is used (Trunc = 1/SP).

 1/SP is computed from FitnV by mean(FitnV)/max(FitnV)

 See also: select, selsus, selrws, seltour, sellocal

 Example:

    % define fitness vector

       FitnV = [.1; .9; 1.6; 2.0; 0.4; 1.3; 1.7; 0.7; 0.2];

    % selects 6 indices from FitnV, Trunc = 0.5;

       NewChrIx = seltrunc(FitnV, 6);

    % possible result

       NewChrIx = [3; 4; 2; 4; 6; 7];

    % Get selected individuals from population Chrom

       SelChrom = Chrom(NewChrIx, :)

## Cross-Reference Information

This function calls

This function is called by

- selsus

- dgagraf

- gatbxini

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
