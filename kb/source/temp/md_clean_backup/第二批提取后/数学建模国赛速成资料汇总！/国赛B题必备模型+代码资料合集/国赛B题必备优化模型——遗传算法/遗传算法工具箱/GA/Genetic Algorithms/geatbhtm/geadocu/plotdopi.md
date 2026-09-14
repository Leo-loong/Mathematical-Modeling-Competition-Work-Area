GEATbx: Function plotdopi




# Documentation of plotdopi


Index of Functions of GEA Toolbox for Matlab




## Function Synopsis

x = plotdopi(OBJ_F, chrom, gen, P1, P2, P3);


## Help text


 PLOTing of DO(Ppel)uble Integration results 

 This function plots some of the results during computation
 of the double integrator.

 Syntax:  plotdopi(OBJ_F, chrom, gen, P1, P2, P3)

 Input parameters:
    OBJ_F     - Vector containing the (name of the) objective function
    chrom     - Vector containing the individual for simulation
    gen       - Scalar containing the number of the current generation
    P1-P3     - additional parameters, see objdopi

 Output parameter:
    x         - Matrix containing the states from answer of objdopi

 See also: objdopi, simdopiv, simdopi1



## Cross-Reference Information




This function is called by




- gatbxini






GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions





   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).


   The Genetic and Evolutionary Algorithm Toolbox is not public domain.


   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,
      (pohlheim@systemtechnik.tu-ilmenau.de).
