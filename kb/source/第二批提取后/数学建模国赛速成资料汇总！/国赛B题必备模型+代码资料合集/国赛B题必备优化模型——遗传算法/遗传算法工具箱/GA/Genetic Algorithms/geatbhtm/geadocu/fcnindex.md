GEATbx: Examples of Objective Functions

# GEA Toolbox - Examples of Objective Functions

 This document describes a number of test functions implemented

 for use with the Genetic and Evolutionary Algorithm Toolbox

 for Matlab (GEATbx). These functions are drawn from the literature

 on genetic algorithms, evolutionary strategies and global optimization.

 The first Section describes a set of common parametric test problems

 implemented as Matlab m-files. The second Section presents

 a number of dynamic systems, implemented in Simulink,

 as s-files and m-files as appropriate.

 1 Parametric Optimization

 Table 1: Set of described

 parametric functions

 No.

 function name

 description

 1.objfun11.1 De Jong's function 1

 2.objfun1a

 1.2 Axis parallel hyper-ellipsoid function

 3.objfun1b

 1.3 Rotated hyper-ellipsoid function

 4.objfun21.4 Rosenbrock's valley (De Jong's function 2)

 5.objfun61.5 Rastrigin's function 6

 6.objfun71.6 Schwefel's function 7

 7.objfun81.7 Griewangk's function 8

 8.objfun91.8 Sum of different power function 9

 9.objfun10

 1.9 Ackley's Path function 10

 10.objfun11

 1.10 Langermann's function 11

 11.objfun12

 1.11 Michalewicz's function 12

 12.objbran1.12 Branins's rcos function

 13.objeaso1.13 Easom's function

 14.objgold1.14 Goldstein-Price's function

 15.objsixh1.15 Six-hump camel back function

 2 Optimization of dynamic

 systems

 Dynamic control problems are complex and difficult to solve. The

 use of dynamic-optimization specific methods, such as Hamiltonian,

 is complicated and problematic. The application of specific methods

 requires a large amount of mathematical support even for systems

 of moderate size, and only the most trivial systems can be solved

 analytically.

 In the following example problems, each individual in the evolutionary

 algorithm corresponds to a (discrete) control vector. Each variable

 in an individual is associated with the control input at a time

 step of the dynamic optimization problem. In this section, x

 is the state vector and u the control vector of a system.

 Table 2: Set of described dynamic

 systems

 No.

 function name

 description

 1.objdopi2.1 Double integrator

 2.objlinq2.2 Linear-quadratic system

 3.objharv2.3 Harvest system

 4.objpush2.4 Push-cart system

 All of the test function implementations are scaleable, i.e. the

 functions can be called with as many dimensions as necessary and

 the default dimension of the test functions is adjustable via

 a single parameter value inside the function.

 For writing own objective functions see Writing objective functions .

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
