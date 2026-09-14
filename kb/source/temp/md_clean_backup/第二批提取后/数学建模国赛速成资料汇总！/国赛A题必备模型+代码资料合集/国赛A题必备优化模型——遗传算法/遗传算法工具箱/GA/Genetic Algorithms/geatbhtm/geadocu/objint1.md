GEATbx: Function objint1




# Documentation of objint1


Index of Functions of GEA Toolbox for Matlab




## Function Synopsis

ObjVal = objint1(Chrom, option);


## Help text


 OBJective function for INT function 1

 This function implements the ONEMAX function 1.
 This is an example function. The objective is not
 really useful.

 Syntax:  [ObjVal, Nind, Nvar] = objint1(Chrom, option)

 Input parameters:
    Chrom     - Matrix containing the chromosomes of the current
                population. Each row corresponds to one individual's
                string representation.
                if Chrom == [], then special values will be returned
    option    - if Chrom == [] and
                option == 1 (or []) return boundaries
                option == 2 return title
                option == 3 return value of global minimum

 Output parameters:
    ObjVal    - Column vector containing the objective values of the
                individuals in the current population.
                if called with Chrom == [], then ObjVal contains
                option == 1, matrix with the boundaries of the function
                option == 2, text for the title of the graphic output
                option == 3, value of global minimum
                
 See also: objfun1, objone1



## Cross-Reference Information



This function calls





- bin2int

- rep






GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions





   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).


   The Genetic and Evolutionary Algorithm Toolbox is not public domain.


   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,
      (pohlheim@systemtechnik.tu-ilmenau.de).
