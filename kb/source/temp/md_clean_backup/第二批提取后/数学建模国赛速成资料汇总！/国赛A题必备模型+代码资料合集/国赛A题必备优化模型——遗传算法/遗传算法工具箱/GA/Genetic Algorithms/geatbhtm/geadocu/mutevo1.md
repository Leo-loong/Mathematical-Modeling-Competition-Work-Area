GEATbx: Function mutevo1




# Documentation of mutevo1


Index of Functions of GEA Toolbox for Matlab




## Function Synopsis

[NewChromMut] = mutevo1(ChromMut, FieldDR, MutOpt);


## Help text


 MUTation by EVOlutionary strategies 1, derandomized Self Adaption

 This function takes a matrix OldChrom containing the real
 representation of the individuals in the current population,
 mutates the individuals corresponding to OldMutMat and returns
 the offspring, NewChrom and the new mutation step matrix, NewMutMat.

 This function implements the derandomized ES-algorithm with
 individual step sizes.
 Ostermeier, Gawelczyk, Hansen: A Derandomized Approach to
 Self Adaption of Evolution Strategies. Technical Report TR-93-003,
 TU Berlin, 1993.

 Syntax:  [NewChromMut] = mutevo1(ChromMut, FieldDR, MutOpt)

 Input parameter:
    ChromMut  - Matrix containing the chromosomes and the mutation variables
                of the old population. Each row corresponds to one individual.
                First half columns contain the chromosomes, second
                half the individual step sizes.
    FieldDR   - Matrix describing the boundaries of each variable.
    MutOpt    - (optional) Vector containing mutation rate and shrink value
                MutOpt(1): MutRate - number containing the mutation rate -
                           probability for mutation of a variable
                           not used here
                MutOpt(2): MutShrink - (optional) number for shrinking the
                           mutation range in the range [0 1], possibility to
                           shrink the range of the mutation.
                           (used for shrinking the starting step sizes)
                           if omitted or NaN, MutShrink = 1 is assumed
                MutOpt(3): MutNumOff - (optional) Number of offspring to be
                           produced per parent
                           if omitted or NaN, MutNumOff = 1 is assumed
                           at the moment not used, MutNumOff = 1 all the time

 Output parameter:
    NewChromMut-Matrix containing the chromosomes and the mutation variables
                of the new population after mutation, ready to be evaluated,
                in the same format as ChromMut. 
                First half columns contain the chromosomes, second
                half the mutation variables.

 See also: mutevo2, mutevo3, mutate, mutbmd, mutbmc, mutbint



## Cross-Reference Information



This function calls
This function is called by




- rep




- gatbxini






GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions





   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).


   The Genetic and Evolutionary Algorithm Toolbox is not public domain.


   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,
      (pohlheim@systemtechnik.tu-ilmenau.de).
