GEATbx: Function migrate

# Documentation of migrate

Index of Functions of GEA Toolbox for Matlab

## Function Synopsis

[Chrom, ObjV] = migrate(Chrom, SUBPOP, MigOpt, ObjV);

## Help text

 MIGRATion of individuals between subpopulations

 This function performs migration of individuals.

 Syntax:  [Chrom, ObjV] = migrate(Chrom, SUBPOP, MigOpt, ObjV)

 Input parameters:

    Chrom     - Matrix containing the individuals of the current

                population. Each row corresponds to one individual.

    SUBPOP    - Number of subpopulations

    MigOpt    - (optional) Vector containing migration paremeters

                MigOpt(1): MIGR - Rate of individuals to be migrated per

                           subpopulation (% of subpopulation)

                           if omitted or NaN, 0.2 (20%) is assumed

                MigOpt(2): Select - number indicating the selection method

                           of replacing individuals

                           0 - uniform selection

                           1 - fitness-based selection (replace worst individuals)

                           if omitted or NaN, 0 is assumed

                MigOpt(3): Structure - number indicating the structure

                           of the subpopulations for migration

                           0 - net structure (unconstrained migration)

                           1 - neighbourhood structure

                           2 - ring structure

                           if omitted or NaN, 0 is assumed

    ObjV      - (optional) Column vector containing the objective values

                of the individuals in the current population, needed for

                fitness-based migration,

                saves recalculation of objective values for population

 Output parameters:

    Chrom     - Matrix containing the individuals of the current

                population after migration.

    ObjV      - if ObjV is input parameter, than column vector containing

                the objective values of the individuals of the current

                generation after migration.

 See also: geamain, mutate, recombin, select

## Cross-Reference Information

This function is called by

- dgampga

- geamain

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
