GEATbx: Function objint3




# Documentation of objint3


Index of Functions of GEA Toolbox for Matlab




## Function Synopsis

ObjVal = objint3(Chrom, option);


## Help text


 OBJective function for INT function 3

 This function implements x^2 + (y-0.4)^2, where x and y are
 discrete real variables, say x=y=(0.2,0.4,0.6,0.8).

 Syntax:  [ObjVal, Nind, Nvar] = objint3(Chrom, option)

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
                
 See also: objfun1, objone1, objint1, objint2, scrint1



## Cross-Reference Information




This function is called by




- scrint1






GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions





   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).


   The Genetic and Evolutionary Algorithm Toolbox is not public domain.


   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,
      (pohlheim@systemtechnik.tu-ilmenau.de).
