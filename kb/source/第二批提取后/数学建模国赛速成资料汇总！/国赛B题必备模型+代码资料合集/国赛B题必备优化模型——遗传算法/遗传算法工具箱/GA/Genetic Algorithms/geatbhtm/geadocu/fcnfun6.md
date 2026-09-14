GEATbx: Examples of Objective Functions

 1.4 Rosenbrock's valley (De Jong's function 2)

 Contents1.6 Schwefel's function 7

## 1 Parametric Optimization

### 1.5 Rastrigin's function 6

 Rastrigin's function is based on function 1 with the addition

 of cosine modulation to produce many local minima. Thus, the test

 function is highly multimodal. However, the location of the minima

 are regularly distributed.

 function definition

 f6(x)=10&#183;n+sum(x(i)^2-10&#183;cos(2&#183;pi&#183;x(i))),

 i=1:n;

 -5.12<=x(i)<=5.12.

 global minimum

 f(x)=0; x(i)=0, i=1:n.

 This function is implemented in objfun6.

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
