GEATbx: Function chekgopt




# Documentation of chekgopt


Index of Functions of GEA Toolbox for Matlab




## Function Synopsis

GOPTIONS = chekgopt(GOPTIN, GOPTDEF, NVAR);


## Help text


 CHEcK parameter structure GOPTions

 Syntax:  GOPTIONS = chekgopt(GOPTIN, GOPTDEF, NVAR)

 Input parameter:
    GOPTIN    - Structure of parameters for Genetic Algorithm Toolbox, provided set
    GOPTDEF   - (optional) Structure of parameters for Genetic Algorithm Toolbox, default set
    NVAR      - (optional) Number of variables/objectives,
                used for defining number of generations, individuals and subpopulations
                if empty or omitted, NVAR = 10 is assumed

 Output parameter:
    GOPTIONS  - same as input, merged with GOPTIN, GOPTDEF and missing values added/defined

 See also: geamain, tbxmpga, tbxdbga, tbxdbin, tbxloga, gatbxini



## Cross-Reference Information



This function calls
This function is called by




- gatbxini

- rep




- tbxdbga

- tbxdbin

- tbxes1

- tbxloga

- tbxmpga






GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions





   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).


   The Genetic and Evolutionary Algorithm Toolbox is not public domain.


   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,
      (pohlheim@systemtechnik.tu-ilmenau.de).
