GEATbx: Function reclin

# Documentation of reclin

Index of Functions of GEA Toolbox for Matlab

## Function Synopsis

NewChrom = reclin(OldChrom, XOVR);

## Help text

 RECombination extended LINe

 This function performs extended line recombination between

 pairs of individuals and returns the new individuals after mating.

 Syntax:  NewChrom = reclin(OldChrom, XOVR)

 Input parameters:

    OldChrom  - Matrix containing the chromosomes of the old

                population. Each line corresponds to one

                individual

    XOVR      - Probability of crossover ocurring between pairs

                of individuals. (not used, only for compatibility)

 Output parameter:

    NewChrom - Matrix containing the chromosomes of the population

               after mating, ready to be mutated and/or evaluated,

               in the same format as OldChrom.

 See also: recombine, recdis, recint, recmut, xovsp, xovdp, xovsh

## Cross-Reference Information

This function is called by

- dgagraf

- gatbxini

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
