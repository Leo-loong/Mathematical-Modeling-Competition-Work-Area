GEATbx: Function mutbga4




# Documentation of mutbga4


Index of Functions of GEA Toolbox for Matlab




## Function Synopsis

NewChrom = mutbga4(OldChrom, FieldDR, MutOpt);


## Help text


 real value MUTation like Breeder Genetic Algorithm with precision 4

 This function is a middle level function, that calls mutbga with
 special parameters. For complete explanation and documentation refer
 to mutbga.
 If no mutation precision is provided in MutOpt, mutbga is called 
 with mutation precision 4.

 Syntax:  NewChrom = mutbga4(OldChrom, FieldDR, MutOpt)

 Input parameter:
    same as mutbga

 Output parameter:
    same as mutbga

 See also: mutate, mutbga, mutbint



## Cross-Reference Information



This function calls
This function is called by




- mutbga




- gatbxini






GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions





   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).


   The Genetic and Evolutionary Algorithm Toolbox is not public domain.


   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,
      (pohlheim@systemtechnik.tu-ilmenau.de).
