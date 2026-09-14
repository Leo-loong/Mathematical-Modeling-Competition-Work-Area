# Genetic Algorithm Optimization Toolbox (GAOT)

The following files are in the distribution:

Main interface

 ga.m                   The Genetic Algorithm  
 initialize.m           Initialization function Used by ga.m   

Operators used during simulated evolution

 Crossover Operators
  heuristicXover.m       Operator for the Algorithm Used by ga.m 
  arithXover.m           Operator for the Algorithm Used by ga.m 
  simpleXover.m          Operator for the Algorithm Used by ga.m 

 Mutation Operators
  binaryMutation.m       Operator for the Algorithm Used by ga.m 
  boundaryMutation.m     Operator for the Algorithm Used by ga.m 
  multiNonUnifMutation.m Operator for the Algorithm Used by ga.m 
  nonUnifMutation.m      Operator for the Algorithm Used by ga.m 
  unifMutation.m         Operator for the Algorithm Used by ga.m

 Selection Functions
  normGeomSelect.m       Selection function Used by ga.m
  roulette.m             Selection function Used by ga.m
  tournSelect.m          Selection function Used by ga.m

 Termination Functions
  maxGenTerm.m           Termination function Used by ga.m
  optMaxGenTerm.m        Termination function Used by ga.m

Functions used for binary representation
  calcbits.m             Binary precision function used by ga.m
  f2b.m                  Float to Binary conversion used by ga.m
  b2f.m                  Binary to Float conversion used by ga.m

Utility functions
  parse.m                Parse blank separated names used by ga.m
  delta.m                Used by nonUnifMutation.m and mult...m

Demonstrations
  gademo1.m              Introductory demo of GAOT
  gademo2.m              Multi-dimensional demo of GAOT
  gademo3.m              Reference for GAOT

 Functions used in Demonstrations
  gademo1eval1.m         Example eval function used by gademo1.m
  coranaEval.m           Calculate Corana functions used by gademo2.m
  coranaMin.m            Calculate negative of Corana used by gademo2.m
  gaEval.m               Calculation of Corana used for testing
  gaGradEval.m           Evaluation Used for Testing      
  gaGradGrad.m           Gradient used for SQP during Testing

Jeff Joines (jjoine@eos.ncsu.edu)

Last modified: Wed Feb  7 10:21:44 1996
