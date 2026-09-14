GEATbx: Function ranking




# Documentation of ranking


Index of Functions of GEA Toolbox for Matlab




## Function Synopsis

FitnV = ranking(ObjV, RFun, SUBPOP);


## Help text


 RANK-based fitness assignment, linear and nonlinear

 This function performs linear and nonlinear ranking of individuals.

 Syntax:  FitnV = ranking(ObjV, RFun, SUBPOP)

 This function ranks individuals represented by their associated
 cost, to be *minimized*, and returns a column vector FitnV
 containing the corresponding individual fitnesses. For multiple
 subpopulations the ranking is performed separately for each
 subpopulation. Different size of every subpopulation is supported.

 Input parameters:
    ObjV      - Column vector/matrix containing the objective values of the
                individuals in the current population (cost values).
                if a matrix, multiobjective ranking assumed (at the moment
                only singleobjective ranking - however, this is transparent)
                each row corresponds to the objective value/s of one individual
    RFun      - (optional) If RFun is a scalar in [1, 2] linear ranking is
                assumed and the scalar indicates the selective pressure.
                If RFun is a 2 element vector:
                RFun(1): SP - scalar indicating the selective pressure
                RFun(2): RM - ranking method
                         RM = 0: linear ranking
                         RM = 1: non-linear ranking
                If RFun is a vector with length(Rfun) > 2 it containes
                the fitness to be assigned to each rank. Then it should have
                the same length as ObjV. Usually RFun is monotonously
                decreasing. Rank 1 is the best individual!
                If RFun is omitted or NaN, linear ranking and a selective
                pressure of 2 are assumed.
    SUBPOP    - (optional) Vector/scalar containing number of individuals
                per subpopulation/number of subpopulations
                if omitted or NaN, 1 subpopulation is assumed

 Output parameters:
    FitnV     - Column vector containing the fitness values of the
                individuals in the current population.
                
 See also: select, compdiv



## Cross-Reference Information



This function calls
This function is called by




- compdiv




- compdiv

- dgampga

- geamain






GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions





   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).


   The Genetic and Evolutionary Algorithm Toolbox is not public domain.


   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,
      (pohlheim@systemtechnik.tu-ilmenau.de).
