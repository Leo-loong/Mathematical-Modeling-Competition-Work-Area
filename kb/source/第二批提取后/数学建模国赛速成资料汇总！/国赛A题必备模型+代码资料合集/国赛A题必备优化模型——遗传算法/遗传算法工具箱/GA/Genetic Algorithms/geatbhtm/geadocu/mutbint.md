GEATbx: Function mutbint

# Documentation of mutbint

Index of Functions of GEA Toolbox for Matlab

## Function Synopsis

NewChrom = mutbint(Chrom, VLUB, MutRate)

## Help text

 MUTation for BINary representation

 This function takes the binary representation of the current

 population, mutates each element with given probability and

 returns the resulting population.

 Syntax:  NewChrom = mutbint(Chrom, VLUB, MutRate)

 Input parameters:

    Chrom     - A matrix containing the chromosomes of the

                current population. Each row corresponds to

                an individuals string representation.

    VLUB      - Matrix containing the boundaries of each variable.

                not used here, necessary for compatibility with

                real valued mutation

    MutRate   - Scalar containing the mutation rate / probability.

                if omitted or NaN MutRate = 0.7/size(Chrom,2) is

                assumed.

 Output parameter:

    NewChrom  - Matrix containing a mutated version of Chrom.

 See also: mutate, mutbmd, mutbmc, initbp

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
