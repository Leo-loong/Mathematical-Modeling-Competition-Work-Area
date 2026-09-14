GEATbx: Function mutbga




# Documentation of mutbga


Index of Functions of GEA Toolbox for Matlab




## Function Synopsis

NewChrom = mutbga(OldChrom, FieldDR, MutOpt);


## Help text


 real value MUTation like Breeder Genetic Algorithm

 This function takes a matrix OldChrom containing the real
 representation of the individuals in the current population,
 mutates the individuals with probability MutR and returns
 the resulting population.

 This function implements the mutation operator of the Breeder Genetic
 Algorithm. (Muehlenbein et. al.)

 Syntax:  NewChrom = mutbga(OldChrom, FieldDR, MutOpt)

 Input parameter:
    OldChrom  - Matrix containing the chromosomes of the old
                population. Each line corresponds to one individual.
    FieldDR   - Matrix describing the boundaries of each variable.
    MutOpt    - (optional) Vector containing mutation rate and shrink value
                MutOpt(1): MutR - number containing the mutation rate -
                           probability for mutation of a variable
                           if omitted or NaN, MutR = 1/variables per individual
                           is assumed
                MutOpt(2): MutShrink - (optional) number for shrinking the
                           mutation range in the range [0 1], possibility to
                           shrink the range of the mutation depending on,
                           for instance actual generation.
                           if omitted or NaN, MutShrink = 1 is assumed
                MutOpt(3): MutPreci - (optional) precision of mutation steps
                           if omitted or NaN, MutPreci = 16 is assumed

 Output parameter:
    NewChrom  - Matrix containing the chromosomes of the population
                after mutation in the same format as OldChrom.

 See also: mutate, mutbint



## Cross-Reference Information



This function calls
This function is called by




- rep




- dgacad1

- dgagraf

- dganew

- gatbxini

- mutbga24

- mutbga4

- mutbga8






GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions





   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).


   The Genetic and Evolutionary Algorithm Toolbox is not public domain.


   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,
      (pohlheim@systemtechnik.tu-ilmenau.de).
