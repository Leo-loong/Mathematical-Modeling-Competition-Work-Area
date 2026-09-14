GEATbx: Function reinsloc

# Documentation of reinsloc

Index of Functions of GEA Toolbox for Matlab

## Function Synopsis

[Chrom, ObjVCh] = reinsloc(Chrom, SelCh, SUBPOP, InsOpt, ObjVCh, ObjVSel, RankCh, RankSel, SelIx);

## Help text

 RE-INSertion of offspring in population replacing parents LOCal

 This function performs local insertion of offspring into the current

 population, replacing parents with offspring and returning the

 resulting population. If sellocal was used for selection, reinsloc

 must be used for reinsertion. This is the only chance to

 keep the local neighbourhood unchanged.

 The offspring are contained in the matrix SelCh and the parents

 in the matrix Chrom. Each row in Chrom and Selch corresponds

 to one individual.

 If the objective values of the population (ObjVCh) and the

 offspring (ObjVSel) are input parameter and ObjVCh is output

 parameter the objective values are copied, according to the

 insertion of offspring, saving the recomputation of the objective

 values for the whole population. The function can handle multiple

 objective values per individual.

 For fitness-based reinsertion the fitness values/ranking of the

 population (RankCh) is needed. If omitted or empty single objective

 scaling using the first column of ObjVCh is assumed.

 If the number of offspring is greater than the number of offspring

 to reinsert the fitness values/ranking of the offspring (RankSel)

 is needed. If omitted or empty single objective scaling using the

 first column of ObjVSel is assumed.

 Syntax:  [Chrom, ObjVCh] = reinsloc(Chrom, SelCh, SUBPOP, InsOpt, ObjVCh, ObjVSel, RankCh, RankSel, SelIx)

 Input parameters:

    Chrom     - Matrix containing the individuals (parents) of the current

                population. Each row corresponds to one individual.

    SelCh     - Matrix containing the offspring of the current

                population. Each row corresponds to one individual.

    SUBPOP    - (optional) Number of subpopulations

                if omitted or NaN, 1 subpopulation is assumed

    InsOpt    - (optional) Vector containing the insertion method parameters

                InsOpt(1): SELKIND - number indicating kind of insertion

                           0 - every offspring replace randomly

                           1 - every offspring replace weakest

                           2 - fitter than weakest replace weakest

                           3 - fitter than weakest replace parents

                           4 - fitter than weakest replace randomly

                           5 - fitter than parent replace parent

                           if omitted or NaN, 1 is assumed

                InsOpt(2): SELSTRUCT - Structure of neighbourhood

                           identical to neighbourhood in local selection

                           0 - linear, full

                           1 - linear, half;

                           2 - torus, full star

                           3 - torus, half star

                           if omitted or NaN, 0 is assumed

    ObjVCh    - (optional) Column vector containing the objective values

                of the individuals (parents - Chrom) in the current population,

                needed for fitness-based insertion

                saves recalculation of objective values for population

    ObjVSel   - (optional) Column vector containing the objective values

                of the offspring (SelCh) in the current population, needed for

                partial insertion of offspring,

                saves recalculation of objective values for population

    RankCh    - (optional) Column vector containing the fitness values (obtained

                by ranking) of the individuals (parents - Chrom) in the current

                population, best individual has highest value,

                if omitted or empty, single objective scaling using ObjVCh is assumed

    RankSel   - (optional) Column vector containing the fitness values (obtained

                by ranking) of the offspring (SelCh) in the current

                population, best offspring has highest value

                if omitted or empty, single objective scaling using ObjVSel is assumed

    SelIx     - Matrix containing indices of selected parents in Chrom, output parameter

                of select/sellocal

 Output parameters:

    Chrom     - Matrix containing the individuals of the current

                population after reinsertion.

    ObjVCh    - if ObjVCh and ObjVSel are input parameter, than column vector containing

                the objective values of the individuals of the current

                generation after reinsertion.

 See also: reins, sellocal, select, ranking

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
