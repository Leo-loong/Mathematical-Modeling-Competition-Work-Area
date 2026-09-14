GEATbx: Function bindecod




# Documentation of bindecod


Index of Functions of GEA Toolbox for Matlab




## Function Synopsis

Phen = bindecode(Chrom, FieldD, Coding)


## Help text


 BINary DECODing to binary, integer or real numbers

 This function decodes binary chromosomes into vectors of binary,
 integer or real numbers. The chromosomes are seen as the concate-
 nation of binary strings and decoded into binary, integer or real
 numbers in a specified interval using either standard binary or 
 Gray decoding.
 Binary variables can be mixed with integer and real variables. A
 binary variable is an integer/real number decoded with one binary
 value and lower bound 0 and upper bound 1, both bounds included.
 For real numbers the variables are scaled between lower and upper
 bound using either arithmetic or logarithmic scaling. The inclusion
 of lower and upper bound can be defined as well.
 For integer numbers the variables are decoded to direct integer
 numbers and the lower bound is added to this direct decoded numbers.
 A check for upper bound is performed afterwards. Thus, every binary
 string decodes to one and only one integer number and vice versa.
 See examples for more information!


 Syntax:  Phen = bindecod(Chrom, FieldD, Coding)

 Input parameters:
    Chrom     - Matrix containing the chromosomes to decode. Each row
                corresponds to one individual's concatenated binary
                string representation. Leftmost bits are most significant
                and rightmost are least significant.
    FieldD   -  Matrix describing the length and how to decode
                each substring in the chromosome. It has the
                following structure:
                [ NumCols;
                  LowBound;
                  UppBound;
                  BinGray;
                  Scaling;
                  LowIncld;
                  UppIncld ]

                NumCols  - Vector containing number of columns in Chrom
                           decoding to one variable. sum(NumCols)
                           should equal the individual length.
                LowBound - Vector containing lower bound for each variable.
                UppBound - Vector containing upper bound for each variable. 
                BinGray  - Vector indicating coding of binary values.
                           0: standard binary coding
                           1: gray coding
                Scaling  - Vector indicating scaling for decoding of
                           variables.
                           0: arithmetic scaling
                           1: logarithmic scaling
                LowIncld - Vector indicating inclusion of lower bound into
                           the representation range
                           0: exclude lower bound
                           1: include lower bound
                UppIncld - Vector indicating inclusion of upper bound into
                           the representation range
                           0: exclude upper bound
                           1: include upper bound

    Coding   - (optional) Scalar containing decoding method
               0: do not decode, real representation - real variables
               1: decode binary values to real numbers
               2: do not decode, binary representation - binary variables 
               3: decode binary values to integer numbers
               if omitted or NaN, 0 (do not decode) is assumed
               Coding is identical to CODEVARIABLE in geamain

 Output parameter:
    Phen     -  Matrix containing the phenotypes of the individuals
                of Chrom.

 See also: bin2int, bin2real, initbp, initrp



## Cross-Reference Information



This function calls
This function is called by




- rep




- bin2int

- bin2real






GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions





   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).


   The Genetic and Evolutionary Algorithm Toolbox is not public domain.


   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,
      (pohlheim@systemtechnik.tu-ilmenau.de).
