GEATbx: Function xovsp




# Documentation of xovsp


Index of Functions of GEA Toolbox for Matlab




## Function Synopsis

NewChrom = xovsp(OldChrom, XOVR);


## Help text


 CROSSOVer Single Point

 This function performs single point crossover between pairs of 
 individuals and returns the current generation after mating.

 Syntax:  NewChrom = xovsp(OldChrom, XOVR)

 Input parameters:
    OldChrom  - Matrix containing the chromosomes of the old
                population. Each line corresponds to one individual
                (in binary form).
    XOVR      - Probability of recombination ocurring between pairs
                of individuals.

 Output parameter:
    NewChrom  - Matrix containing the chromosomes of the population
                after mating, ready to be mutated and/or evaluated,
                in the same format as OldChrom.

 See also: recombin, xovsprs, xovdp, xovsh, xovmp



## Cross-Reference Information



This function calls
This function is called by




- xovmp




- dgagraf

- gatbxini






GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions





   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).


   The Genetic and Evolutionary Algorithm Toolbox is not public domain.


   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,
      (pohlheim@systemtechnik.tu-ilmenau.de).
