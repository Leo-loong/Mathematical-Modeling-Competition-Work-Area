GEATbx: Function objlinq2

# Documentation of objlinq2

Index of Functions of GEA Toolbox for Matlab

## Function Synopsis

[ObjVal, t, x] = objlinq2(Chrom, option, TSTART, TEND);

## Help text

 OBJective function for LINear Quadratic problem 2

 This function implements the continuous LINear Quadratic problem.

 Syntax:  ObjVal = objlinq2(Chrom, option, TSTART, TEND)

 Input parameters:

    Chrom     - Matrix containing the chromosomes of the current

                population. Each row corresponds to one individual's

                string representation.

                if Chrom == [], then special values will be returned

    option    - if Chrom == [] and

                option == 1 (or []) return boundaries

                option == 2 return title

                option == 3 return value of global minimum

                if Chrom ~[], method of simulation

    TSTART    - (optional) start time

    TEND      - (optional) end time

 Output parameters:

    ObjVal    - Column vector containing the objective values of the

                individuals in the current population.

                if called with Chrom == [], then ObjVal contains

                option == 1, matrix with the boundaries of the function

                option == 2, text for the title of the graphic output

                option == 3, value of global minimum

    t         - time vector of last simulation

    x         - matrix containing state values of last simulation

 See also: simlinq1, simlinq2, objlinq, objdopi, objharv, objpush

## Cross-Reference Information

This function calls

- rep

- simlinq1

- simlinq2

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
