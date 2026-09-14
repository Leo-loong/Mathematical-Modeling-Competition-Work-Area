GEATbx: Function objfun12

# Documentation of objfun12

Index of Functions of GEA Toolbox for Matlab

## Function Synopsis

ObjVal = objfun12(Chrom, option);

## Help text

 OBJective function for michalewicz's function 12

 This function implements the MICHALEWICZ function 12.

 Syntax:  ObjVal = objfun12(Chrom, option)

 Input parameters:

    Chrom     - Matrix containing the chromosomes of the current

                population. Each row corresponds to one individual's

                string representation.

                if Chrom == [], then special values will be returned

    option    - if Chrom == [] and

                option == 1 (or []) return boundaries

                option == 2 return title

                option == 3 return value of global minimum

                if Chrom is not empty, option can optionally contain

                the parameter m, which defines the stepness of the edges

 Output parameters:

    ObjVal    - Column vector containing the objective values of the

                individuals in the current population.

                if called with Chrom == [], then ObjVal contains

                option == 1, matrix with the boundaries of the function

                option == 2, text for the title of the graphic output

                option == 3, value of global minimum

 See also: objfun1a, objfun1b, objfun2, objfun6, objfun7, objfun8, objfun9, objfun10, initfun1

 Examples:

    ObjVal = objfun12(Chrom);

    ObjVal = objfun12(Chrom, 10);

 Reference:

## Cross-Reference Information

This function calls

- rep

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
