GEATbx: Function expandm




# Documentation of expandm


Index of Functions of GEA Toolbox for Matlab




## Function Synopsis

MatOut = expandm(MatIn, EXPN)


## Help text


 EXPAND a Matrix, utility function

 This function expands a matrix MatIn in both dimensions.
 In the output matrix MatOut each element of MatIn is
 repeated as often as defined in EXPN. The size of MatOut is
 [EXPN(1)*size(MatIn,1), EXPN(2)*size(MatIn,2)].
 This function is used in the GEA Toolbox.

 Input parameters:
    MatIn     - Input Matrix (before expanding)
    EXPN      - Vector of 2 numbers, how often expand in each
                   dimensiom
                EXPN(1): replicate vertically
                EXPN(2): replicate horizontally

 Output parameter:
    MatOut    - Output Matrix (after expanding)

 Example:
    MatIn = [1 2 3
             4 5 6]

    EXPN = [1 2] => MatOut = [1 1 2 2 3 3;
                              4 4 5 5 6 6]

    EXPN = [2 1] => MatOut = [1 2 3;
                              1 2 3;
                              4 5 6;
                              4 5 6]

    EXPN = [3 2] => MatOut = [1 1 2 2 3 3;
                              1 1 2 2 3 3;
                              1 1 2 2 3 3;
                              4 4 5 5 6 6;
                              4 4 5 5 6 6;
                              4 4 5 5 6 6]

 See also: rep



## Cross-Reference Information




This function is called by




- inteul

- intrk4

- objdopi

- objfun11

- scrgtx02






GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions





   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).


   The Genetic and Evolutionary Algorithm Toolbox is not public domain.


   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,
      (pohlheim@systemtechnik.tu-ilmenau.de).
