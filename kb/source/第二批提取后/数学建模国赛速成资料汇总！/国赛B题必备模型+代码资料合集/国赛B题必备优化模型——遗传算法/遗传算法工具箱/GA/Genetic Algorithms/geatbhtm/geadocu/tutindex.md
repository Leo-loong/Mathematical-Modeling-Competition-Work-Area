GEATbx: Tutorial

#

 Genetic and Evolutionary Algorithm Toolbox for use with MATLAB

 - Tutorial

## Contents

- 1 Quick Start

- 2 Variable representation

- 3 Writing Objective Functions

- 3.1 Parametric optimization functions

- 3.2 Optimization of dynamic systems

- 4 Calling Tree of functions

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

- 5 Naming conventions

- 6 Data structures

- 6.1 Chromosomes

- 6.2 Phenotypes

- 6.3 Objective function values

- 6.4 Fitness values

- 6.5 Multiple subpopulations

 This Tutorial provides an introduction to the Genetic and

 Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

 The first steps for a quick start

 are described and some examples are shown.

 When using the Genetic and Evolutionary Algorithm Toolbox

 for use with Matlab one needs to consider the format of the variable representation

 and how to write an objective function

 implementing a problem. These tasks are explained in detail.

 The structure of the toolbox is described by explaining the calling tree

 of the functions. Thus, the user gets a quick overview about the

 interconnection between the functions.

 At the end the naming conventions

 and the data structures of the GA

 Toolbox are documented.

 All the direct algorithm documentation is done inside the Matlab

 m-files (help name_of_m_file).

 An extensive help option is provided explaining the purpose and

 syntax of each function with illustrative examples. The M-function index

 contains all this information.

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
