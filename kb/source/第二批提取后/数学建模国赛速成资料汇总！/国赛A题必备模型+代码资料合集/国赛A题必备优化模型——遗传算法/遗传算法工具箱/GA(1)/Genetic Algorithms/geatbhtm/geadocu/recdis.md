GEATbx: Function recdis

# Documentation of recdis

Index of Functions of GEA Toolbox for Matlab

## Function Synopsis

NewChrom = recdis(OldChrom, XOVR);

## Help text

 RECombination DIScrete

 This function performs discrete recombination between pairs of individuals

 and returns the new individuals after mating.

 Syntax:  NewChrom = recdis(OldChrom, XOVR)

 Input parameters:

    OldChrom  - Matrix containing the chromosomes of the old

                population. Each line corresponds to one individual

                (in any form, not necessarily real values).

    XOVR      - Probability of recombination ocurring between pairs

                of individuals. (not used, only for compatibility)

 Output parameter:

    NewChrom  - Matrix containing the chromosomes of the population

                after mating, ready to be mutated and/or evaluated,

                in the same format as OldChrom.

 See also: recombin, recint, reclin, recmut, xovsp, xovdp, xovsh

## Cross-Reference Information

This function is called by

- dgagraf

- dganew

- gatbxini

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
