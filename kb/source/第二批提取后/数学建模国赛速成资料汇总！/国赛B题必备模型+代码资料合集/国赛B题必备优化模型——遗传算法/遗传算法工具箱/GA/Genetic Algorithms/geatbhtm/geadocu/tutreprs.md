GEATbx: Tutorial

 1 Quick Start

 Tutorial - Contents

 3 Writing Objective Functions

## 2 Variable representation

 The first step in deciding which genetic algorithm to use is a

 close look to the format/representation of your variables. The

 second step is the direct decision on which format the genetic

 algorithm should work. The representation determines the overall

 algorithm, that means, the used genetic operators.

 In the GA Toolbox 3 different representations are supported:

- real value representation

- binary value representation

- integer value representation

 When working with different representations, the toolbox provides

 functions for conversion between these representations where necessary:

- binary to integer (bin2int)

- binary to real (bin2real)

 Let's give an example: The variables of the objective function

 are in real value representation. Now it could be chosen between

 binary and real value representation for the genetic algorithm.

 The real value representation (tbxmpga)

 is recommended. It works much quicker than the binary one. However,

 if the decision comes to using the binary values inside the genetic

 algorithm, the population is initialized as if the variables would

 be binary (initbp), the genetic operators

 (mutbint and, for instance, xovsp)

 are applied and before the evaluation of the objective function

 the binary values are converted to real values (bin2real).

 One more example. In this case the variables are in integer representation.

 The genetic algorithm can work on integer values (mutbint

 and recdis), however, there are no

 more or really specialized operators for integer variable representation.

 Thus, the best decision would be to work with binary values and

 convert them to integer (bin2int)

 before evaluation of the objective function.

 The use of a representation and necessary conversion is controlled

 by parameter GOPTIONS(19)

 of the options structure.

 Table 1: Combinations of variable representation and conversion

 genetic algorithm works onvariable representation

 conversion

 realreal-

 integerinteger-

 binaryrealbin2real

 binaryintegerbin2int

 binarybinary-

 At the end it could be stated:

- If the variables of the objective function are real

 use the real value presentation for the genetic

 algorithm as well.

- If the variables of the objective function are binary

 use the binary value presentation for the genetic

 algorithm as well.

- If the variables of the objective function are integer

 use the binary value presentation for the genetic

 algorithm and convert for evaluation.

 Matlab Examples:

 Real --- Real:

 tbxmpga('objfun1',[],[-5,-5,-5],[5,5,5])

 objfun1 is an objective function

 using real representation

 all the examples from quick start

 apply as well.

 Binary --- Binary

 tbxdbin('objone1',[],rep[0,[1

 100]],rep[1,[1 100]])

 objone1 is an objective function

 using binary representation

 Real --- Binary

 opt(19)=1; tbxloga('objfun1',opt,[-5,-5,-5],[5,5,5])

 objfun1 is an objective function

 using real representation

 opt(19)=1 determines working on binary representation and convert

 binary to real before evaluation.

 Integer --- Binary

 opt(19)=3; tbxdbin('objint2,opt,[0,0,0],[511,1023,255])

 objint2 is an objective function

 using integer representation

 opt(19)=3 determines working on binary representation and convert

 binary to integer before evaluation.

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
