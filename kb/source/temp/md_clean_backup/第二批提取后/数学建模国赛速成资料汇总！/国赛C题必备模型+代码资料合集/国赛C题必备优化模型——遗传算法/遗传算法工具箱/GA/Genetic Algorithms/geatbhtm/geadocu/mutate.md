GEATbx: Function mutate




# Documentation of mutate


Index of Functions of GEA Toolbox for Matlab




## Function Synopsis

[NewChrom, SUBPOP] = mutate(MUT_F, Chrom, MutOpt, VLUB, SUBPOP);


## Help text


 high level MUTATion function

 This function takes a matrix Chrom containing the 
 representation of the individuals in the current population,
 mutates the individuals and returns the resulting population.
 The function handles multiple populations and calls the low level
 mutation function for the actual mutation process.
 Different size of every subpopulation is supported.

 Syntax:  [NewChrom, SUBPOP] = mutate(MUT_F, Chrom, MutOpt, VLUB, SUBPOP)

 Input parameter:
    MUT_F     - String containing the name of the mutation function
    Chrom     - Matrix containing the chromosomes of the old
                population. Each row corresponds to one individual.
    MutOpt    - (optional) Vector/matrix containing mutation rate, mutation range
                and mutation ptecision
                multiple sets of options are supported, 1 row per subpopulation
                if omitted or NaN, MutOpt = NaN is assumed
                MutOpt(1): MutR - number containing the mutation rate -
                           probability for mutation of a variable
                           (real, integer and binary mutation)
                MutOpt(2): MutRange - (optional) number for shrinking the
                           mutation range in the range [0, 1], possibility to
                           shrink the range of the mutation depending on,
                           for instance actual generation.
                           (real mutation)
                MutOpt(3): MutPreci - (optional) number for precision of 
                           mutation steps, (mutbm* - real mutation)
                           MutNumOff - (optional) number of mutants per offspring
                           (mutevo* - real mutation)
    VLUB      - Matrix containing the boundaries of each variable (real values)
    SUBPOP    - (optional) Vector/scalar containing number of individuals
                per subpopulation/number of subpopulations
                if omitted or NaN, 1 subpopulation is assumed

 Output parameter:
    NewChrom  - Matrix containing the chromosomes of the population
                after mutation in the same format as Chrom.
    SUBPOP    - (optional) Vector/scalar containing number of individuals
                per subpopulation/number of subpopulations

 See also: mutbmd, mutbmc, mutbint, migrate, recombin, select



## Cross-Reference Information



This function calls
This function is called by




- compdiv

- rep




- dgampga

- geamain






GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions





   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).


   The Genetic and Evolutionary Algorithm Toolbox is not public domain.


   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,
      (pohlheim@systemtechnik.tu-ilmenau.de).
