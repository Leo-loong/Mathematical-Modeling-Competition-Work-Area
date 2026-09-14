GEATbx: Function recombin

# Documentation of recombin

Index of Functions of GEA Toolbox for Matlab

## Function Synopsis

NewChrom = recombin(REC_F, Chrom, RecOpt, SUBPOP, VLUB);

## Help text

 high level RECOMBINation function

 This function performs recombination between pairs of individuals

 and returns the new individuals after mating. The function handles

 multiple populations and calls the low level recombination function

 for the actual recombination process.

 Syntax:  NewChrom = recombin(REC_F, OldChrom, RecOpt, SUBPOP, VLUB)

 Input parameters:

    REC_F     - String containing the name of the recombination or

                crossover function

    Chrom     - Matrix containing the chromosomes of the old

                population. Each line corresponds to one individual

    RecOpt    - (optional) Scalar containing the probability of

                recombination/crossover ocurring between pairs

                of individuals.

                if omitted or NaN, 1 is assumed

    SUBPOP    - (optional) Number of subpopulations

                if omitted or NaN, 1 subpopulation is assumed

    VLUB      - (optional) matrix containing lower and upper

                bounds of all variables, only for 'recmut' needed

 Output parameter:

    NewChrom  - Matrix containing the chromosomes of the population

                after recombination in the same format as OldChrom.

 See also: recdis, recint, reclin, recmut, xovsp, xovdp, xovsh, migrate, mutate, select

## Cross-Reference Information

This function calls

This function is called by

- recmut

- rep

- dgacad1

- dgampga

- geamain

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
