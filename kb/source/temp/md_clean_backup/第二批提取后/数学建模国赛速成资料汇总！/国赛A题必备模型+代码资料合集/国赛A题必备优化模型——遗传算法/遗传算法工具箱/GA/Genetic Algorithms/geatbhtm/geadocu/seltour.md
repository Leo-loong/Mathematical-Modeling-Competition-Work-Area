GEATbx: Function seltour




# Documentation of seltour


Index of Functions of GEA Toolbox for Matlab




## Function Synopsis

NewChrIx = seltour(FitnV, Nsel, Dummy);


## Help text


 SELection by TOURnament

 This function performs SELection by TOURnament.

 Syntax:  NewChrIx = seltour(FitnV, Nsel)

 Input parameters:
    FitnV     - Column vector containing the fitness values of the
                individuals in the population.
    Nsel      - Number of individuals to be selected

 Output parameters:
    NewChrIx  - Column vector containing the indexes of the selected
                individuals relative to the original population, shuffeld.
                The new population, ready for mating, can be obtained
                by calculating OldChrom(NewChrIx,:).

 The tournament size Tour is determined from the highest
 fitness value ceil(max(FitnV)). If ranking was used, this
 means ceil(SP);
    FitnV = [1.0; 1.1; 1.9;  0.5; 1.3]; ==> Tour = 2;
    FitnV = [1.6; 2.1; 3.05; 1.0; 0.4]; ==> Tour = 4;
 The tournament size should be in [1, Nind]. If not, Tour is set
 to one of these values and a message is displayed.
 For Tour==1 tournament selection is identical to random selection
 (no selective pressure). 

 See also: select, selsus, selrws, seltrunc, sellocal

 Example:
    % define fitness vector
       FitnV = [.1; .9; 1.6; 2.0; 0.4; 1.3; 1.7; 0.7; 0.2];
    % selects 6 indices from FitnV, Tour = 2;
       NewChrIx = seltour(FitnV, 6);
    % possible result
       NewChrIx = [4; 7; 6; 7; 6; 5];
    % Get selected individuals from population Chrom
       SelChrom = Chrom(NewChrIx, :)



## Cross-Reference Information




This function is called by




- gatbxini






GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions





   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).


   The Genetic and Evolutionary Algorithm Toolbox is not public domain.


   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,
      (pohlheim@systemtechnik.tu-ilmenau.de).
