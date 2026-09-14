GEATbx: Tutorial

 Tutorial - Contents

 2 Variable representation

## 1 Quick Start

 The Genetic and Evolutionary Algorithm Toolbox is modularized.

 For all parameters, default values depending on the size of the

 problem are defined.

 To minimize the simplest quadratic function x^2

 for x in [-5,5]

 for 2 dimensions the Matlab call will be:

 tbxmpga('sum((x.^2)'')''',[],[-5,-5],[5,5])

 The toolbox function tbxmpga implements

 the Multi Population Genetic Algorithm. The first parameter is

 the objective function (here direct as a matlab expression, x

 includes the actual variable values, take care of the multiple

 individuals used by the genetic algorithm - therefore x.^2

 and not x^2!). There

 are no parameters provided, the options vector is empty and will

 be set internally to useful default values. The third parameter

 defines the lower bound of the variable and parameter four the

 upper bound. After waiting a few seconds or minutes (depends on

 the used computer) the function returns the best found individual

 (the values of the variables). For the x^2

 example, the optimum is 0 (zero) for all variables, thus very

 small values are returned:

 ans =

   1.0e-005 *

     0.0666   -0.9130

 This example can be easily expanded to higher dimensions. Let's

 minimize x^2 in 5

 dimensions:

 tbxmpga('sum((x.^2)'')''',[1],[-5,-5,-5,-5,-5],[5,5,5,5,5])

 By defining five lower and upper bounds, the dimension of the

 problem is defined.

 In most cases it will be more appropriate to write a separate

 objective function. The last example could as well implemented

 as:

 function objval = objtest1(x)

 objval = sum((x.^2)')';

 Using this function the minimization would be started with:

 tbxmpga('objtest1',[],[-5,-5,-5,-5,-5],[5,5,5,5,5])

 Until now only default parameters were used. However, using different

 parameter values the behaviour of the genetic algorithm can be

 changed easily. The table of Genetic and Evolutionary Algorithm Toolbox Options

 gives an overview of the parameters and describes them in detail.

 The first option parameter defines the output of results during

 the optimization. Setting it to 1 prints the results in tabular

 format in the command window after every generation (identical

 to Optimization Toolbox):

 tbxmpga('objtest1',1,[-5,-5,-5,-5,-5],[5,5,5,5,5])

 For changing other option values it is easier to define the options

 structure forehand and provide it as a parameter:

 opt(1)=3;opt(14)=50;opt(20)=15;opt(21)=2;

 tbxmpga('objtest1',opt,[-5,-5,-5,-5,-5],[5,5,5,5,5])

 The maximal number of generations is set to 50 and the genetic

 algorithm runs with 2 subpopulation and 15 individuals each. The

 results are plotted in graphical form.

 The function tbxmpga is nothing more

 than a function setting some of the options to special values,

 thus defining a special genetic algorithm. Other examples are

 tbxdbga and tbxdbin.

 The shown examples will be enough for the first steps using the

 Genetic and Evolutionary Algorithm Toolbox. The next

 step will be learning more about writing an objective function

 and how to handle the different representations of variables

 in the objective function and the genetic algorithm.

 For a brief overview of the structure of the toolbox look at the

 calling tree of the toolbox.

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
