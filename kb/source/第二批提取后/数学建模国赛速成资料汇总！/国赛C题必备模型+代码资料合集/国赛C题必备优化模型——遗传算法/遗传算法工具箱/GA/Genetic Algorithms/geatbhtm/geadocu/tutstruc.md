GEATbx: Tutorial

 5 Naming conventions

 Tutorial - Contents

## 6 Data structures

### Contents

- 6.1 Chromosomes

- 6.2 Phenotypes

- 6.3 Objective function values

- 6.4 Fitness values

- 6.5 Multiple subpopulations

 Matlab essentially supports only one data type, a rectangular

 matrix of real or complex numeric elements. All data structures

 of the GA Toolbox should be mapped to this 2-D matrix structure.

 The main data structures in the Genetic Algorithm Toolbox:

- Chromosomes (individuals)

- Phenotype (decision variables)

- Objective function values (objective values

- Fitness values

### 6.1 Chromosomes

 The chromosome data structure stores an entire population in a

 single matrix of size Nind&#183;Lind,

 where Nind is the

 number of individuals in the population and Lind

 is the length of the genotypic representation of those individuals.

 Each row corresponds to an individual's genotype, consisting of

 binary, integer or real values.

 An example of the chromosome structure

            g1,1     g1,2     g1,3    ...  g1,Lind        individual 1

            g2,1     g2,2     g2,3    ...  g2,Lind        individual 2

    Chrom = g3,1     g3,2     g3,3    ...  g3,Lind        individual 3

             .       .       .     ...   .

            gNind,1   gNind,2   gNind,3   ...  gNind,Lind     individual Nind

 This data representation does not force a structure on the chromosome

 structure, only requiring that all chromosomes are of equal length.

 Thus, structured populations or populations with varying genotypic

 bases may be used in the Genetic Algorithm Toolbox provided that

 a suitable decoding function, mapping chromosomes onto phenotypes,

 is employed.

### 6.2 Phenotypes

 The decision variables, or phenotypes, in the genetic algorithm

 are obtained by applying some mapping from the chromosome representation

 into the decision variable space. Here, each string contained

 in the chromosome structure decodes to a row vector of order Nvar,

 according to the number of dimensions in the search space and

 corresponding to the decision variable vector value.

 The decision variables are stored in a numerical matrix of size

 Nind&#183;Nvar.

 Again, each row corresponds to a particular individual's phenotype.

 An example of the phenotype data structure is given below, where

 decode is used to

 represent a decoding function (for instance bin2real

 from the GA Toolbox), mapping the genotypes onto the phenotypes.

    Phen = decode(Chrom)    % map genotype to phenotype

           x1,1     x1,2     x1,3    ...  x1,Nvar        individual 1

           x2,1     x2,2     x2,3    ...  x2,Nvar        individual 2

    Phen = x3,1     x3,2     x3,3    ...  x3,Nvar        individual 3

            .       .       .     ...   .

           xNind,1   xNind,2   xNind,3   ...  xNind,Nvar     individual Nind

 The actual mapping between the chromosome representation and their

 phenotypic values depends upon the decode

 function used. It is perfectly feasible using this representation

 to have vectors of decision variables of different types. For

 example, it is possible to mix integer, real-valued and binary

 decision variables in the same Phen

 data structure.

 Remark:

 Many problems don't need a mapping from the chromosome to phenotype

 structure. For instance, if the variables are real valued and

 the genetic algorithm works with this real valued variables, there

 is no mapping necessary. Similar for binary variables and a genetic

 algorithm, that uses binary variables. Then, chromosomes and phenotypes

 are identical. Thus, throughout the whole documentation the term

 individual is used for both, chromosomes and phenotypes. Only

 if there should be distinguished between both, the original terms

 will be used. Please read the section about How to work with binary/integer/real variable representation

 as well.

### 6.3 Objective

 function values

 An objective function is used to evaluate the performance of the

 phenotypes in the problem domain. Objective function values can

 be scalar or, in the case of multiobjective problems, vectorial.

 Note that objective function values are not necessarily the same

 as the fitness values.

 Objective function values are stored in a numerical matrix of

 size Nind&#183;Nobj,

 where Nobj is the

 number of objectives. Each row corresponds to a particular individual's

 objective vector. An example of the objective function values

 data structure is shown below, with objfun

 representing an arbitrary objective function.

    ObjV = objfun(Phen)     % objective function

           y1,1     y1,2     y1,3    ...  y1,Nobj        individual 1

           y2,1     y2,2     y2,3    ...  y2,Nobj        individual 2

    ObjV = y3,1     y3,2     y3,3    ...  y3,Nobj        individual 3

            .       .       .     ...   .

           yNind,1   yNind,2   yNind,3   ...  yNind,Nobj     individual Nind

### 6.4 Fitness values

 Fitness values are derived from the objective function values

 through a scaling or ranking function. Fitness values are non-negative

 scalars and are stored in column vectors of length Nind,

 an example of which is shown below. Again, fitness

 is an arbitrary fitness function.

    Fitn = fitness(ObjV)     % fitness function

           f1     individual 1

           f2     individual 2

    Fitn = f3     individual 3

            .

           fNind   individual Nind

 Note that for multiobjective functions, the fitness of a particular

 individual is a function of a vector of objective function values.

 Multiobjective problems are characterized by having no single

 unique solution, but a family of equally fit solutions with different

 values of decision variables. Care should therefore be taken to

 adopt some mechanism to ensure that the population is able to

 evolve the set of Pareto optimal solutions.

### 6.5 Multiple subpopulations

 The Genetic Algorithm Toolbox supports the use of a single population

 divided into a number of subpopulations or demes by modifying

 the use of data structures such that subpopulations are stored

 in contiguous blocks within a single matrix. For example, the

 chromosome data structure, Chrom,

 composed of Subpop

 subpopulations each of length N

 individuals is stored as:

            Ind1 Subpop1

            Ind2 Subpop1

                ...

            IndN Subpop1

            Ind1 Subpop2

            Ind2 Subpop2

    Chrom =     ...

            IndN Subpop2

                ...

            Ind1 SubpopSubpop

            Ind2 SubpopSubpop

                ...

            IndN SubpopSubpop

 This is known as the Migration, or Island, model.

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
