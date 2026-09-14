GEATbx: Function select

# Documentation of select

Index of Functions of GEA Toolbox for Matlab

## Function Synopsis

[SelCh, SelIx] = select(SEL_F, Chrom, FitnV, GGAP, SUBPOP, SelOpt);

## Help text

 high level SELECTion function

 This function is the high level universal selection function. The

 function handles multiple populations and calls the low level

 selection function for the actual selection process.

 Syntax:  [SelCh, SelIx] = select(SEL_F, Chrom, FitnV, GGAP, SUBPOP, SelOpt)

 Input parameters:

    SEL_F     - Name of the selection function

    Chrom     - Matrix containing the individuals (parents) of the current

                population. Each row corresponds to one individual.

    FitnV     - Column vector containing the fitness values of the

                individuals in the population.

    GGAP      - (optional) Rate of individuals to be selected

                if omitted 1.0 is assumed

    SUBPOP    - (optional) Number of subpopulations

                if omitted 1 subpopulation is assumed

    SelOpt    - (optional) Vector containing selection paremeters

                SelOpt(1): Structure - number indicating the structure

                           of the neighbourhood for local selection

                           0: linear, full; 1: linear, half;

                           2: torus, full star; 3: torus, half star;

                           if omitted or NaN, 0 is assumed

 Output parameters:

    SelCh     - Matrix containing the selected individuals.

    SelIx     - (optional) Column vector containing the indices

                of the selected individuals.

 See also: selrws, selsus, sellocal, seltrunc, reins, reinsloc, migrate, mutate, recombin

## Cross-Reference Information

This function calls

This function is called by

- rep

- dgampga

- geamain

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
