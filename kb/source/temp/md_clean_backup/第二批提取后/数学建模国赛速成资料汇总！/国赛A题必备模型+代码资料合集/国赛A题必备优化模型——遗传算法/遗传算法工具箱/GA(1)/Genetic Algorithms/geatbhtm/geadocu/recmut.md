GEATbx: Function recmut




# Documentation of recmut


Index of Functions of GEA Toolbox for Matlab




## Function Synopsis

NewChrom = recmut(OldChrom, FieldDR, MutOpt);


## Help text


 line RECombination with MUTation features

 This function performs line recombination with mutation features between
 pairs of individuals and returns the new individuals after mating.

 This function uses the same calling syntax as the real value
 mutation functions (mutate, mutbga). The result is similar to reclin.

 Syntax:  NewChrom = recmut(OldChrom, FieldDR, MutOpt)

 Input parameters:
    OldChrom  - Matrix containing the chromosomes of the old
                population. Each line corresponds to one individual
    FieldDR   - Matrix describing the boundaries of each variable.
    MutOpt    - (optional) Vector containing recombination rate and shrink value
                MutOpt(1): MutR - number containing the recombination rate -
                           probability for recombine a pair of parents
                           if omitted or NaN, MutOpt(1) = 1 is assumed
                MutOpt(2): MutShrink - (optional) number for shrinking the
                           recombination range in the range [0 1], possibility to
                           shrink the range of the recombination depending on,
                           for instance actual generation.
                           if omitted or NaN, MutOpt(2) = 1 is assumed

 Output parameter:
    NewChrom - Matrix containing the chromosomes of the population
               after mating, ready to be mutated and/or evaluated,
               in the same format as OldChrom.

 See also: mutate, mutbga, recombin, recdis, recint, reclin



## Cross-Reference Information



This function calls
This function is called by




- rep




- gatbxini

- recombin






GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions





   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).


   The Genetic and Evolutionary Algorithm Toolbox is not public domain.


   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,
      (pohlheim@systemtechnik.tu-ilmenau.de).
