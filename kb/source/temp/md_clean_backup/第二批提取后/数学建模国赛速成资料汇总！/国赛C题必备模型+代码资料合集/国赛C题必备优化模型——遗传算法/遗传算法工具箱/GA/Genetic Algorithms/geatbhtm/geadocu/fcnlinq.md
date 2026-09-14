GEATbx: Examples of Objective Functions
 
 

 
 
 
 
 
 
 
 
 
 
 
 
 
 2.1 Double integrator
 Contents2.3 Harvest system
 
 
 
 
 
 
 
 
 
## 2 Optimization of dynamic
 systems

 
 
 
 
### 2.2 Linear-quadratic
 system

 
 
 The linear-quadratic system [Mic92]
 is one-dimensional:
 x(k+1=a&#183;x(k)+b&#183;u(k),
 k=1,2,...,N.
 The objective function for minimization is defined as:
 f(x,u)=q&#183;x(N+1)^2+sum(s&#183;x(k)^2+r&#183;u(k)^2),
 k=1:N.
 
 
 
  
 
 
 
 
 set
 
 
 
 N
 
 
 
 
 x(0)
 
 
 
 s
 
 
 
 
 r
 
 
 
 q
 
 
 
 
 a
 
 
 
 b
 
 
 
 
 exact solution
 
 
 
 145100111
 1116180.3399
 
 2451001011
 11109160.7978
 
 345100100011
 1110009990.0200
 
 4451001101
 1137015.6212
 
 545100110001
 11287569.3725
 
 645100110
 1116180.3399
 
 745100111000
 1116180.3399
 
 845100111
 0.01110000.5000
 
 945100111
 10.01431004.0987
 
 1045100111
 110010000.9999
 
 
 
 
 Table 1: Parameter sets for linear-quadratic
 system
 
 The ten test cases described by Michalewicz  [Mic92]
 are all implemented in objlinq. The
 values of the parameter sets are shown in table 1.
 The solution obtained for the first test case is shown in figure
 3.
 
 Fig. 1: Optimal control vector
 for the linear-quadratic system set 1
 
 
 
 The linear-quadratic system is identical to a single integrator
 with positive feedback. A continuous version of this problem using
 a Simulink model, an s-function and Control System
 Toolbox routines is implemented in objlinq2.
 The model used by the objective function is chosen through the
 first parameter of the function, the default is the Simulink
 model.
 
 Fig. 2: Block diagram of linear-quadratic
 system
 
 
 
 The Simulink method uses the model in figure 2
 (simlinq1).
 
 The s-function solves the linear equations (simlinq2):
 dx1/dt=x1+u;
 y=x1.
 
 
 
  
 
 and the third method (Control System Toolbox) uses
 the transfer function:
 G(s)=1/(s-1).
 
 
 
 

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions





   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).


   The Genetic and Evolutionary Algorithm Toolbox is not public domain.


   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,
      (pohlheim@systemtechnik.tu-ilmenau.de).
