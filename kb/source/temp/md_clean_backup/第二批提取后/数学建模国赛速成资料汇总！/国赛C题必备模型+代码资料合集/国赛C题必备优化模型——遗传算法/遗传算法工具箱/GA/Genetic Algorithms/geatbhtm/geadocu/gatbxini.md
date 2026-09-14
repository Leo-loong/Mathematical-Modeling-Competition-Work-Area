GEATbx: Function gatbxini




# Documentation of gatbxini


Index of Functions of GEA Toolbox for Matlab




## Function Synopsis

[FileName, ParaOutOne] = gatbxini(ParaName, OBJ_F, Para);


## Help text


 Genetic Algorithm ToolBoX function/file name INItialization

 Syntax:  FileName = gatbxini(ParaName, OBJ_F, Para)

 Input parameter:
    ParaName  - String containing the name of the parameter the function
                name/file name is needed for 
    OBJ_F     - String containing Name of objective function for user 
                defined function/file names
    Para      - (optional) Scalar or vector containing number of 
                defined function (selection, recombination, mutation)

 Output parameter:
    FileName  - String or String-Matrix containing the function/file name
                corresponding with the input parameters
    ParaOutOne- (optional) used for additional parameters
                ParaName == 'mutation':
                   number of additional parameter sets for step sizes

 See also: chekgopt, geamain



## Cross-Reference Information



This function calls
This function is called by




- initdopi

- initfun1

- mutbga

- mutbga24

- mutbga4

- mutbga8

- mutbint

- mutevo1

- objdopi

- objfun1

- plotdopi

- recdis

- recint

- reclin

- recmut

- sellocal

- selrws

- selsus

- seltour

- seltrunc

- xovdp

- xovdprs

- xovsh

- xovshrs

- xovsp

- xovsprs




- chekgopt

- geamain






GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions





   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).


   The Genetic and Evolutionary Algorithm Toolbox is not public domain.


   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,
      (pohlheim@systemtechnik.tu-ilmenau.de).
