GEATbx: Function compdiv

# Documentation of compdiv

Index of Functions of GEA Toolbox for Matlab

## Function Synopsis

[OP1, OP2, OP3, OP4, OP5] = compdiv(What, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10);

## Help text

 COMPute DIVerse things of GEA Toolbox

 This function computes diverse special results for the GEA Toolbox

 during computation used at different points of the toolbox.

 Syntax:  [OP1, OP2, OP3, OP4, OP5] = compdiv(What, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10)

 Input parameters:

    What      - String containing the name of the needed computation

    P1 - P10  - Parameters needed for the specific computations

 Output parameter:

    OP1 - OP5 - Output parameters, specific for every computation

 Possible functions:

    What == 'fitness_distance_correlation' or 'fdc'

       Compute fitness distance correlation

       P1     - Vector containing Fitnesses (objective values for single

                objective functions), corresponds with ChromAll (P2)

       P2     - Matrix containing ChromAll, alle individuals for

                distance computation, every row in ChromAll corresponds

                the same value in Fitnesses(P1)

       P3     - Vector containing best individual or global solution

       OP1    - Scalar containing fitness distance correlation coefficient

       OP2    - Vector containing Fitnesses (same as P1)

       OP3    - Vector containing Distances computed from P2 and P3

    What == 'distance_chrom'

       Compute distance between individuals (used in resplot)

       P1     - Matrix containing individuals, the distance between all

                individuals is computed

       OP1    - Vector containing all distances, similar to upper half

                of distance matrix

    What == 'possubpop'

       Sort/order subpopulations according objective values, return

          position of every subpopulation

       P1     - Matrix/vector containing (objective) values

       P2     - Vector containing number of individuals per subpopulation

       P3     - Vector containing previous filtered order of subpopulations

       OP1    - (row) Vector containing position of every subpopulation

                   subpopulation with best/minimal objective values gets 1,

                   worst subpopulation gets length(SUBPOP)

       OP2    - (row) Vector containing index to best values in every subpopulation,

                   thus, P1(OP2) = values of best individuals of

                   every subpopulation

       OP3    - (row) Vector containing filtered order of subpopulations

    What == 'checksubpop'

       Check variable SUBPOP against number of objective

          values/individuals and set correct values

       P1     - Vector/scalar containing number of individuals per subpopulation

       P2     - Scalar containing number of (objective) values

       OP1    - Vector containing checked number of individuals per subpopulation

 See also: geamain, resplot

## Cross-Reference Information

This function calls

This function is called by

- ranking

- rep

- geamain

- mutate

- ranking

- resplot

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
