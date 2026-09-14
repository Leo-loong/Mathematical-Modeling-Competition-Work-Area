Evolutionary Algorithms: Principles, Methods and Algorithms

 6 Reinsertion

 Contents

## 7 Parallel implementations

### Contents

- 7.1 Migration

- 7.2 Global model - worker/farmer

- 7.3 Diffusion model

### 7.1 Migration

 The migration model divides the population in multiple subpopulations.

 These subpopulations evolve independently from each other for

 a certain number of generations (isolation time). After the isolation

 time a number of individuals is distributed between the subpopulations

 (migration). The number of exchanged individuals (migration rate),

 the selection method of the individuals for migration and the

 scheme of migration determines how much genetic diversity can

 occur in the subpopulations and the exchange of information between

 subpopulations.

 The parallel implementation of the migration model showed not

 only a speedup in computation time, but it also needed less objective

 function evaluations when compared to a single population algorithm.

 So, even for a single processor computer, implementing the parallel

 algorithm in a serial manner (pseudo-parallel) delivers better

 results (the algorithm finds the global optimum more often or

 with less function evaluations).

 The selection of the individuals for migration can take place:

- uniform at random (pick individuals for migration in a random

 manner),

- fitness-based (select the best individuals for migration).

 Many possibilities exist for the structure of the migration of

 individuals between subpopulations. For example, migration may

 take place:

- between all subpopulations (complete net topology - unrestricted),

 see figure 1,

- in a ring topology, see figure 3,

- in a neighbourhood topology, see figure 4.

 Fig. 1: Unrestricted migration topology

 (Complete net topology)

 The most general migration strategy is that of unrestricted migration

 (complete net topology). Here, individuals may migrate from any

 subpopulation to another. For each subpopulation, a pool of potential

 immigrants is constructed from the other subpopulations. The individual

 migrants are then uniformly at random determined from this pool.

 Figure 2 gives a detailed description

 for the unrestricted migration scheme for 4 subpopulations with

 fitness-based selection. Subpopulations 2, 3 and 4 construct a

 pool of their best individuals (fitness-based migration). 1 individual

 is uniformly at random chosen from this pool and replaces the

 worst individual in subpopulation 1. This cycle is performed for

 every subpopulation. Thus, it is ensured that no subpopulation

 will receive individuals from itself.

 Fig. 2: Scheme for migration

 of individuals between subpopulations

 The most basic migration scheme is the ring topology. Here individuals

 are transferred between directionally adjacent subpopulations.

 For example, individuals from subpopulation 6 migrate only to

 subpopulation 1 and individuals from subpopulation 1 only migrate

 to subpopulation 2.

 Fig. 3: Ring migration topology

 A similar strategy to the ring topology is the neighbourhood migration

 of figure 4. Like the ring topology,

 migration is made only between nearest neighbours. However, migration

 may occur in either direction between subpopulations. For each

 subpopulation, the possible immigrants are determined, according

 to the desired selection method, from adjacent subpopulations

 and a final selection is made from this pool of individuals (similar

 to figure 2).

 Fig. 4: Neighbourhood migration

 topology (2-D implementation)

 Figure 4 shows a possible scheme

 for a 2-D implementation of the neighbourhood topology. Sometimes

 this structure is called a torus.

 With the Multipopulation genetic algorithm, for every function

 tested better results were obtained than for a single population

 algorithm with proportionally more individuals. Similar results

 are reported in [Loh91],

 [MSB91],

 [Rud91],

 [SWM91],

 [Tan89],

 [VBS91]

 and [VSB92].

### 7.2 Global model - worker/farmer

 The global model employs the inherent parallelism of genetic algorithms

 (population of individuals). The Worker/Farmer algorithm is a

 possible implementation.

 Fig. 5: Worker/Farmer genetic

 algorithm

### 7.3 Diffusion model

 The diffusion model handles every individual separately and selects

 the mating partner in a local neighbourhood similar to local selection.

 Thus, a diffusion of information through the population takes

 place. During the search virtual islands, see figure 6

 will evolve.

 Fig. 6: Diffusion genetic algorithm

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
