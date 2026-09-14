Evolutionary Algorithms: Principles, Methods and Algorithms

 5 Mutation

 Contents7 Parallel implementations

## 6 Reinsertion

### Contents

- 6.1 Global reinsertion

- 6.2 Local reinsertion

 Once the offspring have been produced by selection, recombination

 and mutation of individuals from the old population, the fitness

 of the offspring may be determined. If less offspring are produced

 than the size of the original population then to maintain the

 size of the original population, the offspring have to be reinserted

 into the old population. Similarly, if not all offspring are to

 be used at each generation or if more offspring are generated

 than the size of the old population then a reinsertion scheme

 must be used to determine which individuals are to exist in the

 new population.

 The used selection method determines the reinsertion scheme: local

 reinsertion for local selection and global reinsertion for all

 other selection methods.

### 6.1 Global reinsertion

 Different schemes of global reinsertion exist:

- produce as many offspring as parents and replace all parents

 by the offspring (pure reinsertion).

- produce less offspring than parents and replace parents uniformly

 at random (uniform reinsertion).

- produce less offspring than parents and replace the worst

 parents (elitist reinsertion).

- produce more offspring than needed for reinsertion and reinsert

 only the best offspring (fitness-based reinsertion).

 Pure Reinsertion is the simplest reinsertion scheme. Every individual

 lives one generation only. This scheme is used in the simple genetic

 algorithm. However, it is very likely, that very good individuals

 are replaced without producing better offspring and thus, good

 information is lost.

 The elitist combined with fitness-based reinsertion prevents this

 losing of information and is the recommended method. At each generation,

 a given number of the least fit parents is replaced by the same

 number of the most fit offspring (see figure 1).

 The fitness-based reinsertion scheme implements a truncation selection

 between offspring before inserting them into the population (i.e.

 before they can participate in the reproduction process). On the

 other hand the best individuals can live many generations. However,

 every generation some new individuals are inserted. It is not

 checked whether the parents are replaced by better or worse offspring.

 Fig. 1: Scheme for elitist

 insertion

 Because parents may be replaced by offspring with a lower fitness,

 the average fitness of the population can decrease. However, if

 the inserted offspring are extremely bad, they will be replaced

 with new offspring in the next generation.

### 6.2 Local reinsertion

 In local selection individuals are selected in a bounded neighbourhood.

 (see 3.4 Local selection).

 The reinsertion of offspring takes place in exactly the same neighbourhood.

 Thus, the locality of the information is preserved.

 The used neighbourhood structures are the same as in local selection.

 The parent of an individual is the first selected parent in this

 neighbourhood.

 For the selection of parents to be replaced and for selection

 of offspring to reinsert the following schemes are possible:

- insert every offspring and replace individuals in neighbourhood

 uniform at random,

- insert every offspring and replace weakest individuals in

 neighbourhood,

- insert offspring fitter than weakest individual in neighbourhood

 and replace weakest individuals in neighbourhood,

- insert offspring fitter than weakest individual in neighbourhood

 and replace parent,

- insert offspring fitter than weakest individual in neighbourhood

 and replace individuals in neighbourhood uniform at random,

- insert offspring fitter than parent and replace parent.

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
