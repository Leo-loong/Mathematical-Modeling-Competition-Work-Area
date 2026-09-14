Evolutionary Algorithms: Principles, Methods and Algorithms

 1 Introduction

 Contents3 Selection

## 2 Overview

 Evolutionary algorithms are stochastic search methods that mimic

 the metaphor of natural biological evolution. Evolutionary algorithms

 operate on a population of potential solutions applying the principle

 of survival of the fittest to produce better and better approximations

 to a solution. At each generation, a new set of approximations

 is created by the process of selecting individuals according to

 their level of fitness in the problem domain an d breeding them

 together using operators borrowed from natural genetics. This

 process leads to the evolution of populations of individuals that

 are better suited to their environment than the individuals that

 they were created from, just as in natural adaptation.

 Evolutionary algorithms model natural processes, such as selection,

 recombination, mutation, migration, locality and neighbourhood.

 Figure 1 shows the structure

 of a simple genetic algorithm. Evolutionary algorithms work on

 populations of individuals instead of single solutions. In this

 way the search is performed in a parallel manner.

 Fig 1: Structure of a single

 population evolutionary algorithm

 At the beginning of the computation a number of individuals (the

 population) are randomly initialised. The objective function is

 then evaluated for these individuals. The first/initial generation

 is produced.

 If the optimization criteria are not met the creation of a new

 generation starts. Individuals are selected according to their

 fitness for the production of offspring. Parents are recombined

 to produce offspring. All offspring will be mutated with a certain

 probability. The fitness of the offspring is then computed. The

 offspring are inserted into the population replacing the parents,

 producing a new generation. This cycle is performed until the

 optimization criteria are reached.

 Such a single population evolutionary algorithm is powerful and

 performs well on a broad class of problems. However, better results

 can be obtained by introducing many populations, called subpopulations.

 Every subpopulation evolves for a few generations isolated (like

 the single population evolutionary algorithm) before one or more

 individuals are exchanged between the subpopulations. The Multipopulation

 evolutionary algorithm models the evolution of a species in a

 way more similar to nature than the single population evolutionary

 algorithm.

 From the above discussion, it can be seen that evolutionary algorithms

 differ substantially from more traditional search and optimization

 methods. The most significant differences are:

- Evolutionary algorithms search a population of points in parallel,

 not a single point.

- Evolutionary algorithms do not require derivative information

 or other auxiliary knowledge; only the objective function and

 corresponding fitness levels influence the directions of search.

- Evolutionary algorithms use probabilistic transition rules,

 not deterministic ones.

- Evolutionary algorithms are generally more straightforward

 to apply

- Evolutionary algorithms can provide a number of potential

 solutions to a given problem. The final choice is left to the

 user. (Thus, in cases where the particular problem does not have

 one individual solution, for example a family of pareto-optimal

 solutions, as in the case of multiobjective optimization and scheduling

 problems, then the evolutionary algorithm is potentially useful

 for identifying these alternative solutions simultaneously.)

### 2.1 Selection

 Selection determines, which individuals are chosen for mating

 (recombination) and how many offspring each selected individual

 produces. The first step is fitness assignment by:

- proportional fitness assignment [Gol89]

 or

- rank-based fitness assignment

 [Bak85].

 The actual selection is performed in the next step. Parents are

 selected according to their fitness by means of one of the following

 algorithms:

- roulette-wheel selection

 [Bak87],

- stochastic universal sampling

 [Bak87],

- local selection

 [GS91],

 [VSB92],

- truncation selection

 [MSV93b]

 or

- tournament selection

 [BT95].

### 2.2 Recombination

 Recombination produces new individuals in combining the information

 contained in the parents (parents - mating population). Depending

 on the representation of the variables of the individuals the

 following algorithms can be applied:

- Real valued recombination:

- discrete recombination

 [MSV93a],

- intermediate recombination

 [MSV93a],

- line recombination

 [MSV93a],

- extended line recombination

 [M&uuml;h94].

- Binary valued recombination:

- single-point crossover,

- multi-point crossover,

- uniform crossover

 [Sys89]

- shuffle crossover

 [CES89]

- crossover with reduced surrogate

 [Boo87].

### 2.3 Mutation

 After recombination every offspring undergoes mutation. Offspring

 variables are mutated by small perturbations (size of the mutation

 step), with low probability. The representation of the variables

 determines the used algorithm. Two operators are explained:

- mutation for binary valued variables,

- mutation operator of the breeder genetic algorithm [MSV93a]

 for real valued variables.

### 2.4 Reinsertion

 If less offspring are produced than the size of the original population

 the offspring have to be reinserted into the old population. Similarly,

 if not all offspring are to be used at each generation or if more

 offspring are generated than needed a reinsertion scheme must

 be used to determine which individuals should be inserted into

 the new population.

 The used selection algorithm determines the reinsertion scheme:

- global reinsertion for all population based selection algorithm

 (roulette-wheel selection, stochastic universal sampling, truncation

 selection),

- local reinsertion for local selection.

### 2.5 Parallel implementation of evolutionary algorithms

 Parallel genetic algorithms were developed to speed up the computation

 by harnessing the power of parallel computers. Three different

 models for parallel genetic algorithms exist:

- migration model,

- global model,

- diffusion model.

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
