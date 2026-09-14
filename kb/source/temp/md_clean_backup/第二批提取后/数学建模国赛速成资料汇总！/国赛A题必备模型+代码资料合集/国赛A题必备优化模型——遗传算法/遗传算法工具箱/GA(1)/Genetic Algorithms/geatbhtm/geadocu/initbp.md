GEATbx: Function initbp




# Documentation of initbp


Index of Functions of GEA Toolbox for Matlab




## Function Synopsis

[Chrom] = initbp(Nind, VarLength)


## Help text


 CReaTe an initial Binary Population

 This function creates a binary population of given size
 and structure.

 Syntax: [Chrom] = initbp(Nind, VarLength)

 Input Parameters:
    Nind      - Scalar containing the number of individuals (of rows)
                to create.
    VarLength - Scalar or vector containing the length of the individuals.
                scalar: length of the whole individual
                vector: length of each variable of individual
                length of the individual will be sum(VarLength)

 Output Parameters:
    Chrom     - A matrix containing the random valued individuals 
                one row per individual.

 See also: initrp, bin2real, bin2int, mutbint



## Cross-Reference Information




This function is called by




- dgampga

- geamain






GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions





   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).


   The Genetic and Evolutionary Algorithm Toolbox is not public domain.


   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,
      (pohlheim@systemtechnik.tu-ilmenau.de).
