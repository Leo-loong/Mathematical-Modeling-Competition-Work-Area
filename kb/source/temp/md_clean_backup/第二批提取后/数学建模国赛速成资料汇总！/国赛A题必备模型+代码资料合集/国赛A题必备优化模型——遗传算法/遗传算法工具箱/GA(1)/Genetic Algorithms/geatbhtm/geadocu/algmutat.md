Evolutionary Algorithms: Principles, Methods and Algorithms
 
 
 

 
 
 
 
 
 
 
 
 
 
 
 
 
 4 Recombination
 Contents6 Reinsertion
 
 
 
 
 
 
 
 
 
## 5 Mutation

 
 
### Contents

 
 
 
- 5.1 Real valued mutation
 
- 5.2 Binary mutation
 
 
 
 
 
 After recombination offspring undergo mutation. Offspring variables
 are mutated by the addition of small random values (size of the
 mutation step), with low probability. The probability of mutating
 a variable is set to be inversely proportional to the number of
 variables (dimensions). The more dimensions one individual has
 as smaller is the mutation probability. See also [MSV93a].
 
 Different papers ([B&auml;c93],
 [MSV93a]) reported
 results for the optimal mutation rate. [MSV93a]
 writes, that a mutation rate of 1/n produced good results
 for a broad class of test function. However, the mutation rate
 was independent of the size of the population. Similar results
 are reported in [B&auml;c93].
 For unimodal functions a mutation rate of 1/n was the
 best choice. An increase of the mutation rate at the beginning
 connected with an decrease of the mutation rate to 1/n
 at the end gave only an insignificant acceleration of the search.
 However, for multimodal functions an self adaptation of the mutation
 rate could be useful.
 
 
 
### 5.1 Real valued mutation
 

 
 
 Figure 1 shows possible mutations
 for an real valued individual in two dimensions.
 
 Fig. 1: Effect of mutation
 
 
 
 The size of the mutation step is usually difficult to choose.
 The optimal step size depends on the problem considered and may
 even vary during the optimization process. Small steps are often
 successful, but sometimes bigger steps are quicker.
 
 In [MSV93a] and [M&uuml;h94]
 such a mutation operator (the mutation operator of the Breeder
 Genetic Algorithm) is proposed:
 
 
- mutated variable = variable &#177; range&#183;delta;
 (+ or - with equal probability)
 
- range = 0.5&#183;domain of variable; (search interval),
 
- delta = sum(a(i) 2^-i),
 a(i) = 1 with probability 1/m,
 else a(i) = 0; m = 20.
 
 
 
 This mutation algorithm is able to generate most points in the
 hypercube defined by the variables of the individual and range
 of the mutation. However, it tests more often near the variable,
 that is, the probability of small step sizes is greater than that
 of bigger steps (see figure 2).
 With m=20, the mutation algorithm is able to locate
 the optimum up to a precision of (range&#183;2^-19)
 .
 
 Fig. 2: Probability and size of
 mutation steps (compared to range)
 
 
 
 
 
### 5.2 Binary mutation

 
 
 For binary valued individuals mutation means flipping of variable
 values. For every individual the variable value to change is chosen
 uniform at random. Table 1
 shows an example of a binary mutation for an individual with 11
 variables, variable 4 is mutated.
 
 Tab 1: Individual before and
 after binary mutation
 
 
 
 
 before mutation
 
 
 
 0
 
 
 
 
 1
 
 
 
 1
 
 
 
 
 1
 
 
 
 
 0
 
 
 
 0
 
 
 
 
 1
 
 
 
 1
 
 
 
 
 0
 
 
 
 1
 
 
 
 
 0
 
 
 
 
 
 after mutation
 
 
 
 0
 
 
 
 
 1
 
 
 
 1
 
 
 
 
 0
 
 
 
 
 0
 
 
 
 0
 
 
 
 
 1
 
 
 
 1
 
 
 
 
 0
 
 
 
 1
 
 
 
 
 0
 
 
 
 
 
 
 Assuming that the above individual decodes an real number in the
 bounds [1, 10], the effect of the mutation depends on the actual
 coding. Table 2 shows the different
 numbers of the individual before and after mutation for binary/gray
 and arithmetic/logarithmic coding.
 
 Tab  2: Result of the binary
 mutation
 
 
 
 
 arithmetic
 
 
 
 logarithmic
 
 
 
 
 
 
 binary
 
 
 
 gray
 
 
 
 
 binary
 
 
 
 gray
 
 
 
 
 
 
 5.0537
 
 
 
 4.2887
 
 
 
 
 2.8211
 
 
 
 2.3196
 
 
 
 
 
 
 4.4910
 
 
 
 3.3346
 
 
 
 
 2.4428
 
 
 
 1.8172
 
 
 
 
 
 
 
 

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions





   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).


   The Genetic and Evolutionary Algorithm Toolbox is not public domain.


   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,
      (pohlheim@systemtechnik.tu-ilmenau.de).
