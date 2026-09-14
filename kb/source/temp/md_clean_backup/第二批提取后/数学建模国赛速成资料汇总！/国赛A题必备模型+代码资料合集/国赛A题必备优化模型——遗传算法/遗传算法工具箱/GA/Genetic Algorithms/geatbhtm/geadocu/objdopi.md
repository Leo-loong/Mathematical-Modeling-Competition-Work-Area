GEATbx: Function objdopi




# Documentation of objdopi


Index of Functions of GEA Toolbox for Matlab




## Function Synopsis

[ObjVal, t, x] = objdopi(Chrom, method, TSTART, TEND);


## Help text


 OBJective function for DOuble Integrator

 This function implements the Double Integrator.

 Syntax:  ObjVal = objdopi(Chrom, method, TSTART, TEND)

 Input parameters:
    Chrom     - Matrix containing the chromosomes of the current
                population. Each row corresponds to one individual's
                string representation.
                if Chrom == [], then special values will be returned
    method    - if Chrom == [] and
                method == 1 (or []) return boundaries
                method == 2 return title
                method == 3 return value of global minimum
                if Chrom ~[], method of simulation
                 1 - sim: simulink model
                 2 - ode: ordinary differential equations
                 3 - con: transfer function to state space,
                          uses Control Toolbox => outcommented (tf2ss, lsim)
                12 - odv: ordinary differential equations vectorized
                if method is omitted or empty 12 is assumed
    TSTART    - (optional) start time, if omitted 0 is assumed
    TEND      - (optional) end time, if omitted 1 is assumed

 Output parameters:
    ObjVal    - Column vector containing the objective values of the
                individuals in the current population.
                if called with Chrom == [], then ObjVal contains
                method == 1, matrix with the boundaries of the function
                method == 2, text for the title of the graphic output
                method == 3, value of global minimum
    t         - time vector of last simulation
    x         - matrix containing state values of last simulation
                
 See also: simdopiv, simdopi1, initdopi, objharv, objlinq, objpush



## Cross-Reference Information



This function calls
This function is called by




- expandm

- intrk4

- rep

- simdopi1

- simdopiv




- gatbxini

- scrdopi

- scrsim1






GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions





   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).


   The Genetic and Evolutionary Algorithm Toolbox is not public domain.


   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,
      (pohlheim@systemtechnik.tu-ilmenau.de).
