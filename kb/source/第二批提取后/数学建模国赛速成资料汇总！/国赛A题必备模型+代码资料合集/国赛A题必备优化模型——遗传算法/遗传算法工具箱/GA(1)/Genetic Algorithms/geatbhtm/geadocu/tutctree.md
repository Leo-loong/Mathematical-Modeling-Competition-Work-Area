GEATbx: Tutorial

 3 Writing Objective Functions

 Tutorial - Contents

 5 Naming conventions

## 4 Calling Tree of functions

### Contents

- 4.1 Startup script

- 4.2 Predefined Algorithms

- 4.3 Genetic Algorithm - Main function

- 4.3.1 Ranking

- 4.3.2 Selection

- 4.3.3 Recombination/Crossover

- 4.3.4 Mutation

- 4.3.5 Evaluation

- 4.3.6 Reinsertion

- 4.3.7 Migration

- 4.3.8 Visualization

- 4.4 Utility functions

### 4.1 Startup script

 At the beginning there is a high level script for defining

 some parameters and the application specific details. These scripts

 are called &quot;scr*.m&quot;.

 scrgtx01 (example script)

 scrbin1 (example script for binary

 variables)

 scrdopi (example script for optimization

 of dynamic systems)

### 4.2 Predefined Algorithms

 These scripts call toolbox functions defining a genetic algorithm.

 These functions are called &quot;tbx*.m&quot;.

 tbxdbga (implements the Distributed

 Breeder Genetic Algorithm)

 tbxdbin (implements the Distributed

 Binary Genetic Algorithm)

 tbxloga (implements the Local Genetic

 Algorithm)

 tbxmpga (implements the Multi Population

 Genetic Algorithm)

 By using one of these functions all appropriate parameters are

 defined. The remaining parameters are set to default values by

 chekgopt, checking the correct values

 at the same time.

### 4.3 Genetic Algorithm - Main

 function

 The tbx-functions call the working horse of the GA Toolbox:

 geamain (genetic algorithm 1)

 Here all the administrative work is done: resolve parameter values,

 map parameter values to function names (gatbxini),

 initialize population, run the genetic algorithm and display and

 save results.

 The initialization is done by:

 initbp (initializes a population

 using binary/integer values)

 initrp (initializes a population using

 real values)

 an application specific init function (for instance initdopi)

 When the population of individuals is initialized and evaluated,

 the genetic algorithm starts. For as many generations as necessary/defined,

 new populations are produced and evaluated. All functions of the

 genetic algorithm are called via high level functions, thus supporting

 the multi-population (distributed) concept.

- Ranking (ranking)

- Selection (select)

- Recombination/Crossover

 (recombin)

- Mutation (mutate)

- Evaluation (obj*.m)

- Reinsertion (reins)

- Migration (migrate)

- Visualization (resplot)

 Inside the high level functions the appropriate functions are

 called.

#### 4.3.1 Ranking

 For ranking the toolbox provides 1 function, no low level

 functions are used.

 ranking (linear and non-linear

 ranking)

#### 4.3.2 Selection

 For selection a high level function is provided.

 select (high level selection function)

 By parameter a low level selection functions can be chosen,

 that will be called for every subpopulation inside the high level

 function.

 selsus (selection by stochastic

 universal sampling)

 selrws (roulette wheel selection)

 seltrunc (truncation selection)

 seltour (tournament selection)

 sellocal (local selection)

#### 4.3.3 Recombination/Crossover

 For recombination/crossover a high level function is provided.

 recombin (high level recombination/crossover

 function)

 By parameter a low level recombination/crossover functions can

 be chosen, that will be called for every subpopulation inside

 the high level function. The term recombination is used for real

 valued variables, crossover for binary valued variables (historical

 reasons).

 Recombination

 recdis (discrete recombination)

 recint (intermediate recombination)

 reclin (line recombination)

 recmut (line recombination with mutation

 features)

 Crossover

 xovsp (single point crossover)

 xovdp (double point crossover)

 xovsh (shuffle point crossover)

 xovsprs (single point crossover with

 reduced surrogate)

 xovdprs (double point crossover with

 reduced surrogate)

 xovshrs (shuffle point crossover with

 reduced surrogate)

 All crossover functions call the lowest level function xovmp

 (multi point crossover), that does all the functionality provide.

 Currently, for integer valued variables the function recdis

 must be used.

#### 4.3.4 Mutation

 For mutation a high level function is provided.

 mutate (high level mutation function)

 Depending on the variable representation one of the low-level

 mutation functions will be called for every subpopulation:

 Real values:

 mutbga (mutation operator of the

 Breeder Genetic Algorithm)

 Binary/Integer values:

 mutbint (mutation operator for

 binary/integer values)

#### 4.3.5 Evaluation

 The toolbox provides many examples for objective functions. These

 functions are called &quot;obj*.m&quot;. All functions use the

 same calling syntax.

 Standard genetic algorithm test functions with a free definable

 dimension using the real value representation are provided in:

 objfun1 (DE JONG's function 1)-

 objfun12 (MICHALEWICZ's function)

 Binary value representation is used in:

 objone1 (ONEMAX function).

 Dynamic optimization is implemented in:

 objdopi (double integrator)

 objlinq2 (Linear quadratic problem)

 Standard optimization test function with 2 independent variables

 (dimension = 2) are provided in:

 objbran (BRANIN's rcos function)

 objeaso (EASOM's function)

 objgold (GOLDSTEIN-PRICE function)

 objsixh (six hump camelback function)

 See Reference of GA Toolbox Matlab functions - Index

 for all functions or Examples of objective functions

 for a mathematical description.

 It is possible to pass up to 10 parameters to every objective

 function.

 Instead of writing an objective function file and passing the

 name of the function the objective function can be passed directly

 in a string to the Genetic Algorithm Toolbox as well. However,

 it is recommended to use one of the provided objective functions

 as a template and pass over only the file name.

#### 4.3.6 Reinsertion

 For reinsertion the toolbox provides 2 functions, no low level

 functions are used.

 reins (reinsertion of offspring

 into population)

 reinsloc (local reinsertion of offspring

 into population)

#### 4.3.7 Migration

 For migration the toolbox provides 1 function, no low level

 functions are used.

 migrate (migration of individuals

 between subpopulation)

#### 4.3.8 Visualization

 The visualization of the results is implemented on 3 different

 levels:

 tabular output of results of genetic algorithm

 graphical output of results of genetic algorithm (resplot)

 problem specific output (specific m-file, for instance plotdopi

 for objdopi)

### 4.4 Utility functions

 Throughout the toolbox low level utility functions are used.

 They will be useful for everyday work as well:

 rep (repeat a matrix)

 expandm (expand a matrix)

 compdiv (compute diverse things)

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
