GEATbx: Function reins




# Documentation of reins


Index of Functions of GEA Toolbox for Matlab




## Function Synopsis

[Chrom, ObjVCh] = reins(Chrom, SelCh, SUBPOP, InsOpt, ObjVCh, ObjVSel, RankCh, RankSel, Dummy);


## Help text


 RE-INSertion of offspring in population replacing parents

 This function performs insertion of offspring into the current 
 population, replacing parents with offspring and returning the
 resulting population.
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

 Syntax:  [Chrom, ObjVCh] = reins(Chrom, SelCh, SUBPOP, InsOpt, ObjVCh, ObjVSel, RankCh, RankSel)

 Input parameters:
    Chrom     - Matrix containing the individuals (parents) of the current
                population. Each row corresponds to one individual.
    SelCh     - Matrix containing the offspring of the current
                population. Each row corresponds to one individual.
    SUBPOP    - (optional) Number of subpopulations
                if omitted or NaN, 1 subpopulation is assumed
    InsOpt    - (optional) Vector containing the insertion method parameters
                InsOpt(1): Select - number indicating kind of insertion
                           0 - uniform insertion
                           1 - fitness-based insertion
                           if omitted or NaN, 0 is assumed
                InsOpt(2): INSR - Rate of offspring to be inserted per
                           subpopulation (% of subpopulation)
                           if omitted or NaN, 1.0 (100%) is assumed
    ObjVCh    - (optional) Column vector or matrix containing the objective values
                of the individuals (parents - Chrom) in the current population,
                needed for fitness-based insertion
                saves recalculation of objective values for population
    ObjVSel   - (optional) Column vector or matrix containing the objective values
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

 Output parameters:
    Chrom     - Matrix containing the individuals of the current
                population after reinsertion.
    ObjVCh    - if ObjVCh and ObjVSel are input parameter, than column vector containing
                the objective values of the individuals of the current
                generation after reinsertion.

 See also: reinsloc, select, ranking



## Cross-Reference Information




This function is called by




- dgampga

- geamain






GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions





   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).


   The Genetic and Evolutionary Algorithm Toolbox is not public domain.


   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,
      (pohlheim@systemtechnik.tu-ilmenau.de).
