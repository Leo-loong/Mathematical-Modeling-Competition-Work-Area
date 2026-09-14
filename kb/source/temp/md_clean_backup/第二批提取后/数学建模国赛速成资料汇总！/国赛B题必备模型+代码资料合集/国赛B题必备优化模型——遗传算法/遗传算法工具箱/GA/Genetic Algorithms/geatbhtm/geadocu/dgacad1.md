GEATbx: Function dgacad1




# Documentation of dgacad1


Index of Functions of GEA Toolbox for Matlab




## Function Synopsis

dgacad1();


## Help text


 Demo of GA toolbox - CAD 1

 This function displays a number of figures. Select a number of these 
 figures with the mouse by click in the area of the shape. These 
 figure are the parents for the next generation. The offspring are
 created by recombination and mutation. The user is the selector. 

 The shape of the figures is defined by Points X- and Y-values each.
 These points are ploted by patch(), each figure in a rectangle.
 The X- and Y-values are the variables of an individual.

 Aim of this demo is to &quot;construct (CAD)&quot; a special figure, e.g. a square 
 or a star or ..., imagine, what you want and choose/click appropriate.

 Parameters inside function for changing:
    Num       -  Number of figures (4, 9, 16, 25, ...)
    Points    -  Number of Points per figure (3, 4, 5...), 5 recommended 
    MAXGEN    -  Number of generations (more than 30 recommended)

 Syntax:  dgacad1;

 Input parameters:
    no input parameter
 Output parameter:
    no output parameter

 See also: dgagraf, geamain



## Cross-Reference Information



This function calls





- mutbga

- recint

- recombin

- rep






GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions





   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).


   The Genetic and Evolutionary Algorithm Toolbox is not public domain.


   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,
      (pohlheim@systemtechnik.tu-ilmenau.de).
