GEATbx: Function resplot




# Documentation of resplot


Index of Functions of GEA Toolbox for Matlab




## Function Synopsis

resplot(FigName, Chrom, IndAll, ObjV, Best, gen, FitDist, fdcc);


## Help text


 RESult PLOTing of ga toolbox optimization

 This function plots some of the results of the genetic
 algorithm during computation.

 Syntax:  resplot(FigName, Chrom, IndAll, ObjV, Best, gen)

 Input parameters:
    FigName   - String containing name for plot figure
    Chrom     - Matrix containing the chromosomes of the current
                population. Each line corresponds to one individual.
    IndAll    - Matrix containing the best individual (variables) of each
                generation. Each line corresponds to one individual.
    ObjV      - Vector containing objective values of the current
                generation
    Best      - Matrix containing the best and average Objective values of each
                generation, [best value per generation, average value per generation]
    gen       - Scalar containing the number of the current generation

 Output parameter:
    no output parameter

 See also: geamain



## Cross-Reference Information



This function calls
This function is called by




- compdiv




- dgampga

- geamain






GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions





   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).


   The Genetic and Evolutionary Algorithm Toolbox is not public domain.


   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,
      (pohlheim@systemtechnik.tu-ilmenau.de).
