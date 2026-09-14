GEATbx: Function recint




# Documentation of recint


Index of Functions of GEA Toolbox for Matlab




## Function Synopsis

NewChrom = recint(OldChrom, XOVR);


## Help text


 RECombination extended INTermediate

 This function performs extended intermediate recombination between
 pairs of individuals and returns the new individuals after mating.

 Syntax:  NewChrom = recint(OldChrom, XOVR)

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

 See also: recombine, recdis, reclin, recmut, xovsp, xovdp, xovsh



## Cross-Reference Information




This function is called by




- dgacad1

- dgagraf

- gatbxini






GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions





   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).


   The Genetic and Evolutionary Algorithm Toolbox is not public domain.


   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,
      (pohlheim@systemtechnik.tu-ilmenau.de).
