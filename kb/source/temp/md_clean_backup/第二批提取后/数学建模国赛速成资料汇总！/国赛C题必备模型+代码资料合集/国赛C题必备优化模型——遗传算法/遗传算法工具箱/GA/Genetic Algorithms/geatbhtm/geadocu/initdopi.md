GEATbx: Function initdopi




# Documentation of initdopi


Index of Functions of GEA Toolbox for Matlab




## Function Synopsis

[Chrom, VLUB] = initdopi(Nind, VLUB, method, TSTART, TEND);


## Help text


 INITialzation function for DOuble Integrator objdopi

 This function initializes the Double Integrator.

 Syntax:  [Chrom, VLUB] = initdopi(Nind, VLUB, method, TSTART, TEND)

 Input parameters:
    Nind      - Number of individuals
    VLUB      - Matrix containing the boundaries of the variables
    method    - (optional) method of simulation
    TSTART    - (optional) start time
    TEND      - (optional) end time

 Output parameters:
    Chrom     - Matrix containing the chromosomes of the current
                population. Each row corresponds to one individual's
                string representation.
    VLUB      - (optional) Matrix containing the new boundaries
                of the variables
                
 See also: objdopi, initfun1



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
