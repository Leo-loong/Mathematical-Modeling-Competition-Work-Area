GEATbx: Function xovmp

# Documentation of xovmp

Index of Functions of GEA Toolbox for Matlab

## Function Synopsis

NewChrom = xovmp(OldChrom, Px, Npt, Rs);

## Help text

 CROSSOVer Multi-Point, low level function

 This function takes a matrix OldChrom containing the binary

 representation of the individuals in the current population,

 applies crossover to consecutive pairs of individuals with

 probability Px and returns the resulting population.

 Npt indicates how many crossover points to use (1 or 2, zero

 indicates shuffle crossover).

 Rs indicates whether or not to force the production of

 offspring different from their parents.

 Syntax:  NewChrom = xovmp(OldChrom, Px, Npt, Rs)

 Input parameters:

    OldChrom  - Matrix containing the chromosomes of the old

                population. Each row corresponds to one individual

                (in binary form).

    Px        - Probability of recombination ocurring between pairs

                of individuals.

    Npt       - Scalar indicating the number of crossover points

                1: single point crossover

                2: double point crossover

                0: shuffle point crossover

    Rs        - reduced surrogate

                0: no reduced surrogate

                1: reduced surrogate

 Output parameter:

    NewChrom  - Matrix containing the chromosomes of the population

                after mating, ready to be mutated and/or evaluated,

                in the same format as OldChrom.

 See also: recombin, xovdp, xovsh, xovsp, xovdprs, xovsprs, xovshrs

## Cross-Reference Information

This function is called by

- xovdp

- xovdprs

- xovsh

- xovshrs

- xovsp

- xovsprs

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
