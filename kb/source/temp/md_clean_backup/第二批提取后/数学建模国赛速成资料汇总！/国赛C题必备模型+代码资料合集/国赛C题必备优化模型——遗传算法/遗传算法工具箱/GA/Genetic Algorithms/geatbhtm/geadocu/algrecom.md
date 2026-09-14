Evolutionary Algorithms: Principles, Methods and Algorithms
 
 
 

 
 
 
 
 
 
 
 
 
 
 
 
 
 3 Selection
 Contents5 Mutation
 
 
 
 
 
 
 
 
 
## 4 Recombination

 
 
### Contents

 
 
 
- 4.1 Real valued recombination
 
 
- 4.1.1 Discrete recombination
 
- 4.1.2 Intermediate recombination
 
- 4.1.3 Line recombination
 
- 4.1.4 Extended line recombination
 
 
 
- 4.2 Binary valued recombination (crossover)
 
 
- 4.2.1 Single-point crossover
 
- 4.2.2 Multi-point crossover
 
- 4.2.3 Uniform crossover
 
- 4.2.4 Shuffle crossover
 
- 4.2.5 Crossover with reduced surrogate
 
 
 
 
 
 
 
### 4.1 Real valued recombination
 

 
 
 
 
#### 4.1.1 Discrete recombination
 

 
 
 Discrete recombination [MSV93a]
 performs an exchange of variable values between the individuals.
 Consider the following two individuals with 3 variables each (3
 dimensions), which will also be used to illustrate the other types
 of recombination:
 
 individual 1      12     25      5
 individual 2     123      4     34
 
 
 
 For each variable the parent who contributes its variable to the
 offspring is chosen randomly with equal probability.
 
 
 
 sample 1           2      2      1
 sample 2           1      2      1
 
 
 
 After recombination the new individuals are created:
 
 offspring 1      123      4      5
 offspring 2       12      4      5
 
 
 
 Fig. 1: Possible positions of
 the offspring after discrete recombination
 
 
 
 Discrete recombination generates corners of the hypercube defined
 by the parents. Figure 1 shows
 the geometric effect of discrete recombination.
 
 Discrete recombination can be used with any kind of variables
 (binary, real or symbols).
 
 
 
#### 4.1.2 Intermediate
 recombination

 
 
 Intermediate recombination [MSV93a]
 is a method only applicable to real variables (and not binary
 variables). Here the variable values of the offspring are chosen
 somewhere around and between the variable values of the parents.
 
 Offspring are produced according to the rule:
 offspring = parent 1 + Alpha (parent 2 - parent 1),
 
 
 
 where Alpha is a scaling factor chosen uniformly at random over
 an interval [-d, 1 + d]. In intermediate
 recombination d = 0, for extended intermediate recombination
 d > 0. A good choice is d = 0.25. Each variable
 in the offspring is the result of combining the variables according
 to the above expression with a new Alpha chosen for each
 variable.
 
 See figure 2 for a picture of
 the area of the variable range of the offspring defined by the
 variables of the parents.
 
 Fig. 2: Area for variable value
 of offspring compared to parents in intermediate recombination
 
 
 
 Consider the following two individuals with 3 variables each:
 
 individual 1      12     25      5
 individual 2     123      4     34
 
 
 
 The chosen Alpha for this example are:
 
 sample 1         0.5    1.1   -0.1
 sample 2         0.1    0.8    0.5
 
 
 
 The new individuals are calculated as:
 
 offspring 1     67.5    1.9    2.1
 offspring 2     23.1    8.2   19.5
 
 
 
 Intermediate recombination is capable of producing any point within
 a hypercube slightly larger than that defined by the parents.
 Figure 3 shows the possible
 area of offspring after intermediate recombination.
 
 Fig. 3: Possible area of the
 offspring after intermediate recombination
 
 
 
 
 
#### 4.1.3 Line recombination
 

 
 
 Line recombination [MSV93a]
 is similar to intermediate recombination, except that only one
 value of Alpha for all variables is used:
 
 individual 1      12     25      5
 individual 2     123      4     34
 
 
 
 The chosen Alpha for this example are:
 
 sample 1         0.5
 sample 2         0.1
 
 
 
 The new individuals are calculated as:
 
 offspring 1     67.5   14.5   19.5
 offspring 2     23.1   22.9    7.9
 
 
 
 Line recombination can generate any point on the line defined
 by the parents. Figure 4 shows
 the possible positions of the offspring after line recombination.
 
 Fig. 4: Possible positions of the
 offspring after line recombination
 
 
 
 
 
#### 4.1.4 Extended line
 recombination

 
 
 Extended line recombination [M&uuml;h94]
 generates offspring in a direction defined by the parents (line
 recombination). It tests more often outside the area defined by
 the parents and in the direction of parent 1. The point for the
 offspring is defined by features of the mutation operator of the
 Breeder Genetic Algorithm (Real valued mutation).
 The probability of small step sizes is greater than that of bigger
 steps (see figure ).
 Extended line recombination is only applicable to real variables
 (and not binary or integer variables).
 
 Offspring are produced according to the following rule:
 
 
- offspring 1 = parent 1 + RecMx&#183;range&#183;delta&#183;diff,
 

 offspring 2 = parent 2 + RecMx&#183;range&#183;delta&#183;(-diff).
 
- RecMx =  1 (- with probability 0.9),
 
- range = 0.5&#183;domain of variable (search interval),
 
- delta = sum(a(i)&#183; 2^-i),
 a(i) = 1 with probability 1/m,
 else a(i) = 0; m = 20; i=0:(m-1),
 
- diff = (parent 1 - parent 2)/parent 1 - parent
 2
 
 
 
 Consider the following two individuals with 3 variables each:
 
 individual 1      12     25      5
 individual 2     123      4     34
 
 
 
 The chosen variables for this example are:
 
 RecMx     -1
 range             50     50     50
 delta     0.015625
 diff           -0.95   0.18  -0.25
 
 
 
 The new individuals are calculated as:
 
 offspring 1     12.7   24.8   5.19
 offspring 2     11.2   25.1   4.80
 
 
 
 
 
### 4.2 Binary valued recombination
 (crossover)

 
 
 
 
#### 4.2.1 Single-point crossover
 

 
 
 In single-point crossover one crossover position k[1,2,...,Nvar-1],
 Nvar: number of variables of an individual, is selected
 uniformly at random and the variables exchanged between the individuals
 about this point, then two new offspring are produced. Figure
 6 illustrates this process.
 
 Consider the following two individuals with 11 binary variables
 each:
 
 individual 1     0  1  1  1  0  0  1  1  0  1  0
 individual 2     1  0  1  0  1  1  0  0  1  0  1
 
 
 
 The chosen crossover position is:
 
 crossover position            5
 
 
 
 After crossover the new individuals are created:
 
 offspring 1      0  1  1  1  0| 1  0  0  1  0  1
 offspring 2      1  0  1  0  1| 0  1  1  0  1  0
 
 
 
 Fig. 6: Single-point crossover
 
 
 
 
 
#### 4.2.2 Multi-point crossover
 

 
 
 For multi-point crossover, m crossover positions ki[1,2,...,Nvar-1],
 i=1:m, Nvar: number of variables
 of an individual, are chosen at random with no duplicates and
 sorted in ascending order. Then, the variables between successive
 crossover points are exchanged between the two parents to produce
 two new offspring. The section between the first variable and
 the first crossover point is not exchanged between individuals.
 Figure 7 illustrates this
 process.
 
 Consider the following two individuals with 11 binary variables
 each:
 
 individual 1     0  1  1  1  0  0  1  1  0  1  0
 individual 2     1  0  1  0  1  1  0  0  1  0  1
 
 
 
 The chosen crossover positions are:
 
 cross pos. (m=3)     2           6          10
 
 
 
 After crossover the new individuals are created:
 
 offspring 1      0  1| 1  0  1  1| 0  1  1  1| 1
 offspring 2      1  0| 1  1  0  0| 0  0  1  0| 0
 
 
 
 Fig. 7: Multi-point crossover
 
 
 
 The idea behind multi-point, and indeed many of the variations
 on the crossover operator, is that parts of the chromosome representation
 that contribute to the most to the performance of a particular
 individual may not necessarily be contained in adjacent substrings
 [Boo87].
 Further, the disruptive nature of multi-point crossover appears
 to encourage the exploration of the search space, rather than
 favouring the convergence to highly fit individuals early in the
 search, thus making the search more robust [SDJ91b].
 
 
 
#### 4.2.3 Uniform crossover
 

 
 
 Single and multi-point crossover define cross points as places
 between loci where a individual can be split. Uniform crossover
 [Sys89]
 generalizes this scheme to make every locus a potential crossover
 point. A crossover mask, the same length as the individual structure
 is created at random and the parity of the bits in the mask indicate
 which parent will supply the offspring with which bits.
 
 Consider the following two individuals with 11 binary variables
 each:
 
 individual 1     0  1  1  1  0  0  1  1  0  1  0
 individual 2     1  0  1  0  1  1  0  0  1  0  1
 
 
 
 For each variable the parent who contributes its variable to the
 offspring is chosen randomly with equal probability. Here, the
 offspring 1 is produced by taking the bit from parent 1 if the
 corresponding mask bit is 1 or the bit from parent 2 if the corresponding
 mask bit is 0. Offspring 2 is created using the inverse of the
 mask, usually.
 
 sample 1         0  1  1  0  0  0  1  1  0  1  0
 sample 2         1  0  0  1  1  1  0  0  1  0  1
 
 
 
 After crossover the new individuals are created:
 
 offspring 1      1  1  1  0  1  1  1  1  1  1  1
 offspring 2      0  0  1  1  0  0  0  0  0  0  0
 
 
 
 Uniform crossover, like multi-point crossover, has been claimed
 to reduce the bias associated with the length of the binary representation
 used and the particular coding for a given parameter set. This
 helps to overcome the bias in single-point crossover towards short
 substrings without requiring precise understanding of the significance
 of the individual bits in the individuals representation. Spears
 and De Jong [SDJ91a]
 have demonstrated how uniform crossover may be parameterised by
 applying a probability to the swapping of bits. This extra parameter
 can be used to control the amount of disruption during recombination
 without introducing a bias towards the length of the representation
 used.
 
 The algorithm of uniform crossover is identical to discrete recombination.
 
 
 
#### 4.2.4 Shuffle crossover
 

 
 
 Shuffle crossover [CES89]
 is related to uniform crossover. A single crossover position (as
 in single-point crossover) is selected. But before the variables
 are exchanged, they are randomly shuffled in both parents. After
 recombination, the variables in the offspring are unshuffled.
 This removes positional bias as the variables are randomly reassigned
 each time crossover is performed.
 
 
 
#### 4.2.5 Crossover with
 reduced surrogate

 
 
 The reduced surrogate operator [Boo87]
 constrains crossover to always produce new individuals wherever
 possible. This is implemented by restricting the location of crossover
 points such that crossover points only occur where gene values
 differ.
 
 

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions





   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).


   The Genetic and Evolutionary Algorithm Toolbox is not public domain.


   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,
      (pohlheim@systemtechnik.tu-ilmenau.de).
