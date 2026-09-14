Genetic and Evolutionary Algorithm Toolbox: Parameter Settings
 
 
 

 
 
 
 
 
# Parameter settings for structure GOPTIONS

 
 
 oriented on and compared to structure OPTIONS used in Optimization
 Toolbox
 
 The goptions structure contains parameters used
 in the optimization routines. If, on the first call to an optimization
 routine, the goptions structure is empty, a set
 of default parameters is generated. If goptions
 is present and has less than all elements, the remaining elements
 assume their default values.
 
 Some of the goptions parameters are calculated
 using factors based on the problem size (e.g., number of variables).
 Other parameters are dependent on specific routines and are documented
 in the Reference Guide. The parameters
 in the goptions structure are shown in the following
 table.
 
 The check of consistency for these parameters is done in chekgopt
 
 (In the function row the old (Optimization Toolbox) meaning
 is written in parenthesis.)
 
 
 No.Function
 DefaultDescription and Possible Values
 
 
 1 Display
 0Controls amount of output during the optimization.
 

 0: displays no output

 1: displays tabular output

 2: displays tabular and graphical output

 3: displays graphical output (resplot)
 
 
 2Terminate for x1e-4Termination criteria, that is a measure of the worst case precision required of the independent variables, x. The optimization does not terminate until all termination criteria have been met. (not implemented yet)
 
 
 3Terminate for f1e-4Termination criteria, that is a measure of the precision required of the objective function, f, at the solution. (not implemented yet)
 
 
 4Terminate for g1e-7Termination criteria used by constrained optimization routines that is a measure of the worst case constraint violation that is acceptable. (not implemented yet)
 
 
 5Selection Algorithm (Main)0
 Selection algorithm selection.

 0: Stochastic universal sampling selsus

 1: Roulette wheel selection selrws

 2: Local selection sellocal

 3: Truncation selection seltrunc

 4: Truncation selection seltour
 
 
 6 Mutation Algorithm (SD)
 0Mutation algorithm selection.
 

 0: Real mutation mutbga

 1: Binary mutation mutbint

 2: Integer mutation mutbint

 11: Real mutation mutbga4

 12: Real mutation mutbga8

 13: Real mutation mutbga24

 21: Evolutionary strategy mutevo1

 99: No mutation
 
 
 7 Recombination Algorithm (Search)
 0Recombination algorithm selection.

 0: Discrete recombination recdis

 1: Intermediate recombination recint

 2: Line recombination reclin

 3: Extended line recombination recmut

 10: Double-point crossover xovdp

 11: Double-point reduced surrogate crossover xovdprs

 12: Single-point crossover xovsp

 13: Single-point reduced surrogate crossover xovsprs

 14: Shuffle crossover xovsh

 15: Shuffle reduced surrogate crossover xovshrs

 99: No recombination
 
 
 8Best Objective Value (Function)
 returnBest value of the objective function during optimization.
 
 
 9(Gradient Check)not used
 
 
 10Function CountreturnObjective function evaluation counter
 
 
 11(Gradient Count)not used
 
 
 12(Constraint Count)not used
 
 
 13Equality Constraints0Number of equality constraints. Equality constraints are placed in the first elements of the variable g. (used by multiobjective optimization) (not implemented yet)
 
 
 14Max Generations (Iterations)200 sqrt(n)
 Maximum number of generations. This value is set to 200 times sqrt(n), where n is the number of independent variables.
 
 
 15Objectives Used0Number of objectives to be as near as possible to the goals. (used by multiobjective optimization) (not implemented yet)
 
 
 16(Min Perturb)not used
 
 
 17(Max Perturb)not used
 
 
 18(Step-size)not used
 
 
 19Format of objective variable values
 0Format of objective variable values and internal representation. Depending on the setting a conversion between internal representation and the representation of the objective values is done.

 This parameter corresponds with GOPTIONS(6) and GOPTIONS(7).
 

 0: Real values (the GA works on real values)

 1: Real values (converts real values to binary, the GA works on binary values)

 2: Binary/Integer values (no conversion, the GA works on binary/integer values)

 3: Integer values (converts integer values to binary, the GA works on binary values)
 
 
 20Number of Individuals
 20+n/10Number of individuals (per subpopulation).

 This value is set to 20 plus n divided by 10 where n is the number of independent variables.

 The setting of this parameter corresponds to GOPTIONS(21).

 The number of all individuals in a population is GOPTIONS(20) times GOPTIONS(21).
 
 
 21Number of Subpopulation
 2 sqrt(n)Number of subpopulation. This value is set to 2 times sqrt(n), where n is the number of independent variables.

 The setting of this parameter corresponds to GOPTIONS(20).

 The number of all individuals in a population is GOPTIONS(20) times GOPTIONS(21).
 
 
 22Generation Gap1.0Fraction of the population to be reproduced every generation.

 If Generation Gap is smaller than 1.0, less offspring than individuals in population are produced, thus, some individuals of the population survive. This is identical to elitist selection.

 If Generation Gap is greater than 1.0 more offspring than individuals in population are produced. Not all offspring are inserted in the population.
 
 
 23Selection Pressure2Value of selection pressure. Used by ranking algorithm. Value of selection pressure determines the ranking algorithm.

 1 - 2: Linear ranking algorithm

 >2 - (Nind-2): Nonlinear ranking algorithm (Nind: number of individuals per subpopulation as defined in GOPTIONS(20)
 
 
 24Selection Structure (of local selection)
 0Determines the structure of selection in local selection (sellocal).
 

 0: linear, full

 1: linear, half

 2: torus, full star

 3: torus, half star
 
 
 25Selection ???(not used yet)
 
 
 26Migration Rate (MigRate)0.2
 The migration rate specifies the fraction of a subpopulation to be migrated every 20 generations in the range [0,1). (migrate)
 
 
 27Migration Structure (MigStruct)
 0Migration structure determines the topology of migration.

 0: complete net structure

 1: neighbourhood structure

 2: ring structure
 
 
 28Results/output to file (Save2File)
 0Determines writing of results/output to file.

 0: no output to file

 >=1: write output to file every 'Save2File' generation

 The name of the file for saving the output is taken from/must be defined in gatbxini.
 
 
 29Init function0Determines using an application specific initialization function.

 0: don't use a special init function

 1: use a special init function

 The name of the special init function is taken from/must be defined in gatbxini.

 A special init function gives the chance of incorporating application specific knowledge. The init function will be used for initialization of the population at the begin of the optimization (instead of initbp/initrp). For an example see initfun1.
 
 
 30State plot0Determines plotting of intermediate results using an application specific function.
 

 0: no specific result plotting

 >=1: application specific result plotting

 If the parameter is greater 1, only every 'state plot' generation specific results are plotted.

 The name of the application specific plot function is taken from/must be defined in gatbxini.
 
 
 
 
 
 This table is very near the OPTIONS table of the Optimization
 Toolbox page 1-13/1-14. Additional parameters are added at the
 end of the table/list.
 
 
 
## Examples of parameter setting

 
 
 As an example, commands that change the first and fifth parameter
 are shown below.
 
 
 Changing the Default Settings
 
 
 
 >> goptions(1,1) = 1;   % Display intermediate results
 >> goptions(5,1) = 3;   % Use truncation selection
 >> [x, gopt] = tbxmpga('objfun1', goptions);
 
 
 
 
 Display of results during optimization

 (first line: name of used objective function; first row: number of generation, second row: number of objective function calls, third row: best objective value in generation, fourth row (optional): rank of subpopulations)
 
 
 
 
 Objective function:  objfun1
 Generation   f-Count      Function
     1.           160        740203
     2.           304        577926
     3.           448        577926
     4.           592        577926
     5.           736        573184
    ...  % display of most generations removed
    50.          7216       20419.3  
   100.         14416       1611.08  
   600.         86416   0.000146002
   800.        115216  0.0000808368
 
 
 
 
 Results best individual and objective value (after 800 generations and several minutes)
 
 
 
 
 >> x            % best individual (20 variables)
 x =
     0.0010    0.0019    0.0028   -0.0006    0.0021
     0.0029    0.0015    0.0001   -0.0029   -0.0024
    -0.0020    0.0021   -0.0025    0.0008   -0.0012
    -0.0024    0.0008    0.0023   -0.0031    0.0000
 
 >> bestobjvalue = gopt(8)
 bestobjvalue =
    8.0837e-005
 
 
 
 
 
 
 
 On-line help for goptions is available by typing
 help chekgopt or type chekgopt.
 The command chekgopt, when used without right-hand
 arguments, returns the set of default parameters.
 
 
 Returning the Default Settings
 
 
 
 >> goptions = chekgopt
 
 goptions =
          0
     0.0001
     0.0001
     0.0000
          0
          0
          0
          0
          0
          0
          0
          0
          0
   600.0000
          0
          0
          0
          0
          0
    20.0000
     6.0000
     1.0000
     2.0000
          0
          0
     0.2000
          0
          0
          0
          0
 
 
 
 
 
 
 
 
 
## Using predefined evolutionary algorithms

 
 
 The GA Toolbox includes a number of predefined Genetic Algorithms
 called tbx*.m (ToolBoX functions). An example is the
 often used tbxmpga. These functions
 define some of the parameters in the structure GOPTIONS and define
 thus a special algorithm. The ToolBoX functions can be used as
 a starting point for own predefined Genetic Algorithms.
 
 

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions





   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).


   The Genetic and Evolutionary Algorithm Toolbox is not public domain.


   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,
      (pohlheim@systemtechnik.tu-ilmenau.de).
