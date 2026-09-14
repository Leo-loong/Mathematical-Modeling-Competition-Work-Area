GEATbx: Function selsus

# Documentation of selsus

Index of Functions of GEA Toolbox for Matlab

## Function Synopsis

NewChromIx = selsus(FitnV, Nsel, Dummy);

## Help text

 SELection by Stochastic Universal Sampling

 This function performs selection with stochastic universal sampling.

 This function selects a given number of individuals Nsel from a

 population. FitnV is a column vector containing the fitness

 values of the individuals in the population.

 Syntax:  NewChrIx = selsus(FitnV, Nsel)

 Input parameters:

    FitnV     - Column vector containing the fitness values of the

                individuals in the population.

    Nsel      - Number of individuals to be selected

 Output parameters:

    NewChromIx- Column vector containing the indexes of the selected

                individuals relative to the original population, shuffeld.

                The new population, ready for mating, can be obtained

                by calculating OldChrom(NewChromIx,:).

 See also: select, selrws, sellocal, seltrunc, seltour

## Cross-Reference Information

This function calls

This function is called by

- rep

- dgagraf

- dganew

- gatbxini

- sellocal

- seltrunc

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
