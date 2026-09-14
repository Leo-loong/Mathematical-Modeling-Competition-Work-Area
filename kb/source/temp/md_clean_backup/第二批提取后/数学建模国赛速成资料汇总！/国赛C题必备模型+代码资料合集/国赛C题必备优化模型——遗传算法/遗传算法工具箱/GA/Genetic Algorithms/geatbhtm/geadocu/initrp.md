GEATbx: Function initrp




# Documentation of initrp


Index of Functions of GEA Toolbox for Matlab




## Function Synopsis

Chrom = initrp(Nind, FieldDR);


## Help text


 CReaTe an initial (Real value) Population

 This function creates a population of given size of random real value. 

 Syntax:  Chrom = initrp(Nind, FieldDR);

 Input parameters:
    Nind      - A scalar containing the number of individuals in the new population.
    FieldDR   - A matrix of size 2 by number of variables describing the
                boundaries of each variable. It has the following structure:
                [lower_bound;   (vector with lower bound for each veriable)
                 upper_bound]   (vector with upper bound for each veriable)
                [lower_bound_variable_1  lower_bound_var_2 ... lower_bound_var_Nvar;
                 upper_bound_variable_1  upper_bound_var_2 ... upper_bound_var_Nvar]
                example - each individuals consists of 4 variables:
                FieldDR = [-100 -50 -30 -20;   % lower bound
                            100  50  30  20]   % upper bound
              
 Output parameter:
    Chrom     - A matrix containing the random valued individuals of the
                new population of size Nind by number of variables.

 See also: initbp



## Cross-Reference Information



This function calls
This function is called by




- rep




- dgampga

- geamain






GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions





   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).


   The Genetic and Evolutionary Algorithm Toolbox is not public domain.


   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,
      (pohlheim@systemtechnik.tu-ilmenau.de).
