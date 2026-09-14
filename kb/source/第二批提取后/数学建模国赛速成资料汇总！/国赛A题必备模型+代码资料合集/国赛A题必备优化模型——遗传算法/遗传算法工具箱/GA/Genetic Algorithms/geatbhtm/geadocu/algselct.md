Evolutionary Algorithms: Principles, Methods and Algorithms

 2 Overview

 Contents4 Recombination

## 3 Selection

### Contents

- 3.1 Rank-based fitness assignment

- 3.2 Roulette wheel selection

- 3.3 Stochastic universal sampling

- 3.4 Local selection

- 3.5 Truncation selection

- 3.6 Tournament selection

- 3.7 Comparison of selection schemes

 In selection the individuals producing offspring are chosen. The

 first step is fitness assignment. Each individual in the selection

 pool receives a reproduction probability depending on the own

 objective value and the objective value of all other individuals

 in the selection pool. This fitness is used for the actual selection

 step afterwards.

 Throughout this section some terms are used for comparing the

 different selection schemes. The definition of this terms follows

 [Bak87]

 and [BT95].

 selective pressure:

 probability of the best individual being selected compared

 to the average probability of selection of all individuals

 bias:

 absolute difference between an individual's normalized fitness

 and its expected probability of reproduction

 spread:

 range of possible values for the number of offspring of an

 individual

 loss of diversity:

 proportion of individuals of a population that is not selected

 during the selection phase

 selection intensity:

 expected average fitness value of the population after applying

 a selection method to the normalized Gaussian distribution

 selection variance:

 expected variance of the fitness distribution of the population

 after applying a selection method to the normalized Gaussian distribution

### 3.1 Rank-based fitness assignment

 In rank-based fitness assignment, the population is sorted according

 to the objective values. The fitness assigned to each individual

 depends only on its position in the individuals rank and not on

 the actual objective value.

 Rank-based fitness assignment overcomes the scaling problems of

 the proportional fitness assignment. (Stagnation in the case where

 the selective pressure is too small or premature convergence where

 selection has caused the search to narrow down too quickly.) The

 reproductive range is limited, so that no individuals generate

 an excessive number of offspring. Ranking introduces a uniform

 scaling across the population and provides a simple and effective

 way of controlling selective pressure.

 Rank-based fitness assignment behaves in a more robust manner

 than proportional fitness assignment and, thus, is the method

 of choice. [BH91]

 , [Why89]

 Consider Nind the number of individuals in the population,

 Pos the position of an individual in this population (least

 fit individual has Pos=1, the fittest individual Pos=Nind)

 and SP the selective pressure. The fitness value for

 an individual is calculated as:

 Linear ranking:

 Fitness(Pos) = 2 - SP + 2&#183;(SP

 - 1)&#183;(Pos - 1) / (Nind - 1)

 Linear ranking allows values of selective pressure in [1.0, 2.0].

 A new method for ranking using a non-linear distribution is introduced.

 The use of non-linear ranking permits higher selective pressures

 than the linear ranking method.

 Non-linear ranking:

 Fitness(Pos) = Nind&#183;X^(Pos

 - 1) / sum(X^(i - 1)); i = 1:Nind

 X is computed as the root of the polynomial:

 0 = (SP - 1)&#183;X^(Nind

 - 1) + SP&#183;X^(Nind - 2) +

 ... + SP&#183;X + SP

 Non-linear ranking allows values of selective pressure in [1.0,

 Nind - 2.0].

 Figure 1 compares linear

 and non-linear ranking graphically.

 Fig 1: Fitness assignment

 for linear and non-linear ranking

 The probability of each individual being selected for mating is

 its fitness normalized by the total fitness of the population.

 Table 1 contains the fitness values

 of the individuals for various values of the selective pressure

 assuming a population of 11 individuals and a minimization problem.

 Table 1: Dependency of fitness value

 from selective pressure

 In [BT95] an analysis

 of linear ranking selection can be found.

 Selection intensity:

 SelIntRank(SP) = (SP-1)&#183;(1/sqrt(pi)).

 Loss of diversity:

 LossDivRank(SP) = (SP-1)/4.

 Selection variance:

 SelVarRank(SP) = 1-((SP-1)^2/pi) = 1-SelIntRank(SP)^2.

 Fig 2: Properties of linear

 ranking

### 3.2 Roulette wheel selection

 The simplest selection scheme is roulette-wheel selection, also

 called stochastic sampling with replacement [Bak87].

 This is a stochastic algorithm and involves the following technique:

 The individuals are mapped to contiguous segments of a line, such

 that each individual's segment is equal in size to its fitness.

 A random number is generated and the individual whose segment

 spans the random number is selected. The process is repeated until

 the desired number of individuals is obtained (called mating population).

 This technique is analogous to a roulette wheel with each slice

 proportional in size to the fitness, see figure 3.

 Table 2 shows the selection probability

 for 11 individuals, linear ranking and selective pressure of 2

 together with the fitness value. Individual 1 is the most fit

 individual and occupies the largest interval, whereas individual

 10 as the second least fit individual has the smallest interval

 on the line (see figure 3).

 Individual 11, the least fit interval, has a fitness value of

 0 and get no chance for reproduction

 Table  2: Selection probability and

 fitness value

 Number of individual

 1

 2

 3

 4

 5

 6

 7

 8

 9

 10

 11

 fitness value

 2.0

 1.8

 1.6

 1.4

 1.2

 1.0

 0.8

 0.6

 0.4

 0.2

 0.0

 selection probability

 0.18

 0.16

 0.15

 0.13

 0.11

 0.09

 0.07

 0.06

 0.03

 0.02

 0.0

 For selecting the mating population the appropriate number of

 uniformly distributed random numbers (uniform distributed between

 0.0 and 1.0) is independently generated.

 sample of 6 random numbers:

 0.81, 0.32, 0.96, 0.01, 0.65, 0.42.

 Figure 3 shows the selection

 process of the individuals for the example in table 2

 together with the above sample trials.

 Fig. 3: Roulette-wheel selection

 After selection the mating population consists of the individuals:

 1, 2, 3, 5, 6, 9.

 The roulette-wheel selection algorithm provides a zero bias but

 does not guarantee minimum spread.

### 3.3 Stochastic universal sampling

 Stochastic universal sampling [Bak87]

 provides zero bias and minimum spread. The individuals are mapped

 to contiguous segments of a line, such that each individual's

 segment is equal in size to its fitness exactly as in roulette-wheel

 selection. Here equally spaced pointers are placed over the line

 as many as there are individuals to be selected. Consider NPointer

 the number of individuals to be selected, then the distance between

 the pointers are 1/NPointer and the position of the

 first pointer is given by a randomly generated number in the range

 [0, 1/NPointer].

 For 6 individuals to be selected, the distance between the pointers

 is 1/6=0.167. Figure 4

 shows the selection for the above example.

 sample of 1 random number in the range [0, 0.167]:

 0.1.

 Fig. 4: Stochastic universal

 sampling

 After selection the mating population consists of the individuals:

 1, 2, 3, 4, 6, 8.

 Stochastic universal sampling ensures a selection of offspring

 which is closer to what is deserved then roulette wheel selection.

### 3.4 Local selection

 In local selection every individual resides inside a constrained

 environment called the local neighbourhood. (In the other selection

 methods the whole population or subpopulation is the selection

 pool or neighbourhood.) Individuals interact only with individuals

 inside this region. The neighbourhood is defined by the structure

 in which the population is distributed. The neighbourhood can

 be seen as the group of potential mating partners.

 Fig 5: Linear neighbourhood:

 full and half ring

 The first step is the selection of the first half of the mating

 population uniform at random (or using one of the other mentioned

 selection algorithms, for example, stochastic universal sampling

 or truncation selection). Now a local neighbourhood is defined

 for every selected individual. Inside this neighbourhood the mating

 partner is selected (best, fitness proportional, or uniform at

 random).

 Fig 6: Two-dimensional

 neighbourhood: full and half cross

 The structure of the neighbourhood can be:

- linear

- full ring, half ring (see figure 5)

- two-dimensional

- full cross, half cross (see figure 6)

- full star, half star (see figure 7)

- three-dimensional and more complex with any combination of

 the above structures.

 The distance between possible neighbours together with the structure

 determines the size of the neighbourhood. Table 3

 gives examples for the size of the neighbourhood for the given

 structures and different distance values.

 Fig 7: Two-dimensional

 neighbourhood: full and half star

 Between individuals of a population an 'isolation by distance'

 exists. The smaller the neighbourhood, the bigger the isolation

 distance. However, because of overlapping neighbourhoods, propagation

 of new variants takes place. This assures the exchange of information

 between all individuals.

 Tab. 3: Number of neighbours

 for local selection

 The size of the neighbourhood determines the speed of propagation

 of information between the individuals of a population, thus deciding

 between rapid propagation or maintenance of a high diversity/variability

 in the population. A higher variability is often desired, thus

 preventing problems such as premature convergence to a local minimum.

 Similar results were drawn from simulations in [VSB92].

 Local selection in a small neighbourhood performed better than

 local selection in a bigger neighbourhood. Nevertheless, the interconnection

 of the whole population must still be provided. Two-dimensional

 neighbourhood with structure half star using a distance of 1 is

 recommended for local selection. However, if the population is

 bigger (>100 individuals) a greater distance and/or another

 two-dimensional neighbourhood should be used.

### 3.5 Truncation selection

 Compared to the previous selection methods modelling natural selection

 truncation selection is an artificial selection method. It is

 used by breeders for large populations/mass selection.

 In truncation selection individuals are sorted according to their

 fitness. Only the best individuals are selected for parents. These

 selected parents produce uniform at random offspring. The parameter

 for truncation selection is the truncation threshold Trunc.

 Trunc indicates the proportion of the population to

 be selected as parents and takes values ranging from 50%-10%.

 Individuals below the truncation threshold do not produce offspring.

 The term selection intensity is often used in truncation selection.

 Table 4 shows the relation

 between both.

 Tab. 4: Relation between truncation

 threshold and selection intensity

 truncation threshold

 1%

 10%

 20%

 40%

 50%

 80%

 selection intensity

 2.66

 1.76

 1.2

 0.97

 0.8

 0.34

 In [BT95] an analysis

 of truncation selection can be found. The same results have been

 derived in a different way in [CK70]

 as well.

 Selection intensity:

 SelIntTrunc(Trunc) = 1/Trunc/sqrt(2&#183;pi)&#183;exp(-(fc^2)/2).

 Loss of diversity:

 LossDivTrunc(Trunc) = 1-Trunc.

 Selection variance:

 SelVarTrunc(Trunc) = 1-SelIntTrunc(Trunc)&#183;(SelIntTrunc(Trunc)-fc).

 Fig 8: Properties

 of truncation selection

### 3.6 Tournament selection

 In tournament selection [GD91]

 a number Tour of individuals is chosen randomly from

 the population and the best individual from this group is selected

 as parent. This process is repeated as often as individuals to

 choose. These selected parents produce uniform at random offspring.

 The parameter for tournament selection is the tournament size

 Tour. Tour takes values ranging from 2 -

 Nind (number of individuals in population). Table 5

 and figure 9 show

 the relation between tournament size and selection intensity [BT95].

 Tab. 5: Relation between

 tournament size and selection intensity

 tournament size

 1

 2

 3

 5

 10

 30

 selection intensity

 0

 0.56

 0.85

 1.15

 1.53

 2.04

 In [BT95]

 an analysis of tournament selection can be found.

 Selection intensity:

 SelIntTour(Tour) = sqrt(2&#183;(log(Tour)-log(sqrt(4.14&#183;log(Tour))))),

 (approximation).

 Loss of diversity:

 LossDivTour(Tour) = Tour^-(1/(Tour-1))-Tour^-(Tour/(Tour-1)),

 (About 50% of the population are lost at tournament size Tour=5).

 Selection variance:

 SelVarTour(Tour) = 1-0.096&#183;log(1+7.11&#183;(Tour-1)),

 SelVarTour(2) = 1-1/pi, (approximation)

 Fig 9: Properties

 of tournament selection

### 3.7 Comparison of selection

 schemes

 In [MSV93b]

 an analysis of truncation selection on the ONEMAX function (optima

 for all bit positions 1) can be found. In [BT95]

 this analysis is extended to tournament and linear ranking selection

 as well.

 fraction of 1's in generation gen:

 p(gen) = 0.5&#183;(1+sin(SelInt/sqrt(n)&#183;gen+asin(2&#183;p0-1)))

 (n: dimension of objective function, p0: fraction of

 1's in initial random population) Convergence is characterized

 by p(GenConv) = 1.

 special case: p0 = 0.5:

 GenConv = pi/2&#183;sqrt(n)/SelInt.

 Number of generations to reach convergence:

 ranking selection:

 GenConvRank = sqrt(pi&#183;n)/(2&#183;(SP-1)).

 truncation selection:

 GenConvTrunc = pi/2&#183;sqrt(n)/SelIntTrunc.

 tournament selection:

 GenConvTour = pi/2&#183;sqrt(n/(2&#183;(log(Tour)-log(sqrt(4.14&#183;log(Tour)))))).

 The number of generations to reach convergence with a simple genetic

 algorithm is proportional to sqrt(n)

 and inversely proportional to selection intensity. (The population

 should be large enough to converge to the optimum and the initial

 population should be generated at random.) This would suggest

 a high selection intensity as best selection scheme. However,

 a high selection intensity leads to premature convergence and

 thus a poor quality of the solutions. The genetic algorithm works

 most effectively with the minimal population size N*.

 This is the size where the population still converges to the optimum.

 N* depends

 on the dimension of the objective function and the selection intensity.

 As shown above the three selection methods behave similar assuming

 similar selection intensity. Figure 10

 shows the relation between selection intensity and the appropriate

 parameter of the selection methods (selective pressure, truncation

 threshold and tournament size). It should be stated, that with

 tournament selection only discrete values can be assigned and

 linear ranking selection allows only a smaller range for the selection

 intensity.

 Fig 10: Dependence

 of selection parameter on selection intensity

 However, the behaviour of the selection methods is different.

 Thus, the selection methods will be compared on the parameters

 loss of diversity (figure 11)

 and selections variance (figure 12)

 on the selection intensity.

 Fig 11: Dependence

 of loss of diversity on selection intensity

 Truncation selection leads to a much higher loss of diversity

 for the same selection intensity compared to ranking and tournament

 selection. Truncation selection is more likely to replace less

 fit individuals with fitter offspring, because all individuals

 below a certain fitness threshold don't have a probability to

 be selected. Ranking and tournament selection seem to behave similar.

 However, ranking selection works in an area where tournament selection

 doesn't work because of the discrete character of tournament selection.

 Fig 12: Dependence

 of selection variance on selection intensity

 For the same selection intensity truncation selection leads to

 a much smaller selection variance than ranking or tournament selection.

 As can seen clearly ranking selection behaves similar to tournament

 selection. However, again ranking selection works in an area where

 tournament selection doesn't work because of the discrete character

 of tournament selection. In [BT95]

 was proven, that the fitness distribution for ranking and tournament

 selection for SP=2 and Tour=2 (SelInt=1/sqrt(pi)) is identical.

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
