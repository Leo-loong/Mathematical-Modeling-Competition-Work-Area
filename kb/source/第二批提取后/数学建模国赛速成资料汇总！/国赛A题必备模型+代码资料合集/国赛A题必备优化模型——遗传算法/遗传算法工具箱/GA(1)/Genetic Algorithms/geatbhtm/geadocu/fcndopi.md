GEATbx: Examples of Objective Functions

 1.15 Six-hump camel back function

 Contents2.2 Linear-quadratic system

## 2 Optimization of dynamic

 systems

### 2.1 Double integrator

 The double integrator problem is described by the following

 state equations:

 dx1/dt=u; dx2/dt=x1;

 y=x2

 The value of x2 has to be changed during

 a time period with as little control effort as possible and the

 final conditions must be met, such that the following criteria

 are satisfied.

 time:

 0<=t<=1,

 initial conditions:

 x1(0)=0, x2(0)=-1,

 final conditions:

 x1(0)=0, x2(0)=0,

 The objective function to be minimized is:

 f(u)=integral(u(t)^2 dt), 0<=t<=1.

 For these conditions an analytical solution is found to be:

 u=6-12&#183;t, Minimum=12.

 Figure 1 shows the optimal control

 vector and states for the continuous system:

 Fig. 1: Input and states of double

 integrator for optimal solution

 The double integrator is implemented in the m-file objdopi

 using a Simulink model, an s-function and Control

 System Toolbox routines. The model used by the objective

 function is chosen through the first parameter of the function,

 the default is the Simulink model.

 Fig. 2: Block diagram of double integrator

 The Simulink method uses the model in figure 2

 (simdopi1). The s-function solves

 the linear equations (simdopiv) given

 above and the third method (Control System Toolbox) uses

 the transfer function:

 G(s)=1/s^2.

 The double integrator is the preferred system for learning the

 advanced features of the Genetic Algorithm Toolbox, i.e.:

- special initialization function (initdopi),

 [provide problem specific knowledge during initialization of the

 population]

- special state plot function (plotdopi),

 [plot special results for best individual during optimization,

 for instance state and output variables of simulation]

- vectorized simulation/integration (simdopiv,

 using intrk4), [speed up simulation

 and thus overall computation time].

 For using the first 2 features the appropriate option parameters

 (parameter 29 and 30) and the corresponding name of the special

 function in gatbxini must be set.

 The concept of setting the parameter in the options structure

 for using or not the special feature and defining the name of

 the special function in gatbxini

 is very flexible. For every objective function a special function

 for initialization or state plot can be defined (every problem

 needs it's own initialization or state plot function, thus the

 dependence on the objective function name in gatbxini)

 and via parameter the use can be switched on or off. An example

 of all this is provided with the start script scrdopi,

 the objective function objdopi , the

 initialization function initdopi

 and the state plot function plotdopi.

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
