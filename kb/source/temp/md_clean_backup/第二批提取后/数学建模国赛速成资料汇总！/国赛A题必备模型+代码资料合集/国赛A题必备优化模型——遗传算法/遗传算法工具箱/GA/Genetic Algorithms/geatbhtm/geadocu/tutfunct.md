GEATbx: Tutorial
 
 

 
 
 
 
 
 
 
 
 
 
 
 
 
 2 Variable representation
 Tutorial - Contents
 4 Calling Tree of functions
 
 
 
 
 
 
 
 
 
## 3 Writing Objective
 Functions

 
 
 When using the toolbox the implementation of an objective function
 constitutes most of the work. Inside this function all the problem
 specific variables are defined. The kind of implementation determines,
 how good the genetic algorithm can work on and solve the problem.
 
 The quickest way for implementing the objective function is to
 provide the function as matlab expression directly (see quick start).
 However, this is only applicable for small problems.
 
 Included in the distributed version of the toolbox are many examples
 of objective functions (obj*.m). These functions implement a broad
 class of problems. Using these functions as a template it will
 be easier to implement own functions/problems. For an overview
 of the mathematical description see Examples of objective functions.
 
 Consider the following tasks:
 
 
- The objective function is called with a matrix with
 as many rows as individuals. Every row corresponds to
 one individual. The number of columns determines the dimension/the
 number of variables of the objective function.
 
- Because of being called with many individuals the objective
 function calculates the same mathematical expressions more than
 ones. This could be done in a for-loop. However, here is a highly
 recommended place for vectorization.
 
- Beside calculating the objective values the objective function
 could be used for defining default values for
 lower and upper bound and a default dimension of the problem.
 Additionally, the example functions provide a descriptive string
 for labeling plots and, if known, the minimal objective value.
 
 
 
 
 
### 3.1 Parametric optimization
 functions

 
 
 Let's finish the theory. Here is a first example.
 
 Consider implementing the simple quadratic function (sum of quadrate
 or bowl function; known as DE JONG's function 1).
 This functions works on real value variables.
 
 function objval = objfun1(x)
    objval=sum((x.^2)')';   % vectorized, thus fast
    % for i=1:size(x,1), objval(i)=sum(x(i,:).^2); end
 
 
 
 objfun1 returns the
 objective values of all individuals and because of the vectorization
 it will be fast. The second line (commented) shows the implementation
 of this function unvectorized. Every individual will be computed
 separately. The result is the same, however, Matlab takes
 a considerably longer time.
 
 The next step is defining default values. During the work on the
 toolbox the following style developed and is implemented inside
 all provided objective functions: Call the objective function
 with no individuals (the matrix with the individuals is empty).
 A second parameter determines which default parameter to return.
 
 function objval = objfun1(x,switch)
    [Nind,Nvar]=size(x);
    if Nind== 0,
       if switch==2, objval='DE JONG function 1';
       elseif switch==3, objval=0;
       else Dim=20; objval=rep([-512;+512],[1 Dim]);
    end
    else
       objval=sum((x.^2)')';
    end
 
 
 
 The line objfun1([],1)
 will return the default boundaries (including the dimension) of
 the objective function. This is used inside, for instance, scrgtx01
 for retrieving default boundaries.
 
 objfun='objfun1';
 bounds=feval(objfun,[],1);
 VLB=bounds(1,:); VUB=bounds(2,:);
 tbxmpga(objfun,[],VLB,VUB)
 
 
 
 Getting the descriptive name of the objective function (objfun1([],2))
 or the minimal objective value (objfun1([],3))
 is not used in the distributed version of the toolbox. However,
 when comparing different algorithms and defining a termination
 criterion against the minimal objective value it would be useful.
 
 A fully documented version of the above objective function is
 implemented in objfun1.
 
 Other examples of objective functions
 (using real value variables, vectorized and definable number of
 dimensions) as objfun1 are:
 
 
- objfun1a (axis parallel hyper-ellipsoid)
 
- objfun1b (rotated hyper-ellipsoid)
 
- objfun2 (ROSENBROCK's function)
 
- objfun6 (RASTRIGIN's function)
 
- objfun7 (SCHWEFEL's function)
 
- objfun8 (GRIEWANGK's function)
 
- objfun9 (sum of different power)
 
- objfun10 (ACKLEY's path)
 
- objfun11 (LANGERMANN's function)
 
- objfun12 (MICHALEWICZ's function)
 
 
 
 These functions are very often used as a standard set of test
 functions for evaluation of the performance of different genetic
 algorithms.
 
 
 
### 3.2 Optimization of dynamic systems
 

 
 
 Often the solution of a problem involves the simulation of a system
 or the call of other functions. Consider the optimization of the
 control vector of a double integrator (push cart system). For
 an overview see description of the double integrator.
 
 function objval=objdopi(Chrom,switch)
    [Nind,Nvar]=size(Chrom);
    XINIT=[0;-1];XEND=[0;0];
    TSTART=0; TEND=1;TIMEVEC=linspace(TSTART,TEND,Nvar)';
    if Nind==0,
    % see above example or objdopi
    else
       STEP=abs((TEND-TSTART)/(Nvar-1)));
       for indrun=1:Nind
          control=[TIMEVEC [Chrom(indrun,:)]'];
          [t x]=rk23('simdopiv',[TSTART TEND],XINIT,[1e-3,STEP,STEP],control);
          % Calculate objective function
          objval(indrun)=sum(abs(x(size(x,1),:)'-XEND))+ ...
                         trapz(t,Chrom(indrun,:).^2));
       end
    end
 
 
 
 At the beginning of the calculation of the objective values problem
 specific parameters are defined (XINIT,
 XEND, TSTART,
 TEND, TIMEVEC).
 The direct calculation is done separately for every individual
 (rk23 is written
 for only one system at one time). Every individual is converted
 in the form rk23
 requires it (vector of time values in the first column, next column(s)
 contain control values at specified time). The simulation function
 is called with appropriate parameters, the state values are returned.
 
 The objective value is an combination from two terms:
 
 
- sum of all values of the individual (the needed energy/force
 to change the state of the system) and
 
- difference between reached and needed endvalue of the states.
 
 
 
 The objective function is finished. However, there is still another
 function needed - the s-function for the simulation routine simdopiv.
 (for an introduction of writing s-function see the Simulink
 reference guide or look at the provided s-functions of the
 Genetic Algorithm Toolbox sim*.m).
 
 function [sys,x0]=simdopiv(t,x,u,flag);
    if abs(flag) == 1
       sys(1,:) = u(1,:);
       sys(2,:) = x(1,:);
    elseif abs(flag)==0
       sys=[2,0,0,1,0,0]; x0 = [0; -1];
    end
 
 
 
 Let's go one step further. The toolbox provides the possibility
 to pass up to 10 parameters to the objective function. In the
 above example it could be useful to have the chance of changing
 TSTART/TEND/XINIT/XEND
 from outside and thus optimizing different situations of the double
 integrator system. The beginning of the function would be changed
 to:
 
 function objval=objdopi(Chrom,switch,TSTART,TEND,XINIT,XEND)
    [Nind,Nvar]=size(Chrom);
    if nargin<3, TSTART=0; end
    if nargin<4, TEND=1; end
    if nargin<5, XINIT=[0;-1]; end
    if nargin<6, XEND=[0;0]; end
 
 
 
 The problem specific parameters are checked and if not provided
 are set to default values. Thus, if necessary the parameters can
 be passed to the function or default values can be used. For optimizing
 objdopi the script would be:
 
 objfun='objdopi';
 bounds=feval(objfun,[],1);
 VLB=bounds(1,:); VUB=bounds(2,:);
 TSTART=0; TEND=2; XINIT=[0;-2]; XEND=[0;0];
 tbxmpga(objfun,[],VLB,VUB,0,TSTART,TEND,XINIT,XEND)
 
 
 
 An even more advanced parameter checking could be done with (example):
 
    if nargin<3, TSTART=[]; end
    if isempty(TSTART), TSTART=0; end
    if nargin<4, TEND=[]; end
    if isempty(TEND), TEND=1; end
 
 
 
 The parameter passing mechanism offers the possibility of getting
 multiple solutions at once without editing the objective function:
 
    for i=1:10,
    XINIT=[0;-i];
       tbxmpga(objfun,[],VLB,VUB,0,[],[],XINIT)
    end
 
 
 
 Undefined parameters (TSTART,
 TEND, XEND)
 will be set to default values - really useful in day to day work.
 
 One problem remains - vectorization. Many simulation problems
 are not vectorizable and thus slow. The genetic algorithm spends
 most of the time calculating the objective values. For simulation
 functions there are actually two problems: The Matlab-provided
 integration functions (rk23,
 rk45 aso) are not
 vectorized. And it's often difficult to vectorize the s-function
 (see sim*.m). However,
 for this example both of these problems are solved. The s-function
 simdopiv is vectorized and together
 with the Genetic Algorithm Toolbox an vectorized integration routine,
 intrk4, is provided. For more information
 see the documentation of intrk4 and
 method=12 inside objdopi.
 
 If the objective function computes quite a few temporary results,
 that are not part of the objective value, it is good style to
 return them as additional output parameters.
 
 function [objval, t, x]=objdopi(...)
 
 
 
 What is the benefit? This opens the possibility of writing problem
 specific result plotting or special result computing routines.
 An example is implemented for the double integrator, which serves
 at the same time as an example for these advanced problem specific
 features, i.e.:
 
 
- special initialization function (initdopi),
 [provide problem specific knowledge during initialization of the
 population]
 
- special state plot function (plotdopi),
 [plot special results for best individual during optimization,
 for instance state and output variables of simulation]
 
 
 
 For using these features the appropriate option parameters
 (parameter 29 and 30) and the corresponding name of the special
 function in gatbxini must be defined
 (example for state plot: . Inside gatbxini
 set the appropriate line under state_plot
 and objdopi to plotdopi.
 When calling the genetic algorithm option(30) should be set to
 1 or greater.). The concept of setting the parameter in the options
 structure for using or not the special feature and defining the
 name of the special function in gatbxini
 is very flexible. For every objective function a special function
 for initialization or state plot can be defined (every problem
 needs it's own initialization or state plot function, thus the
 dependence on the objective function name in gatbxini).
 Via parameter the use can be switched on or off. An example of
 all this is provided with the start script scrdopi,
 the objective function objdopi , the
 initialization function initdopi
 and the state plot function plotdopi.
 
 
 
### 3.3 Remark

 
 
 Two things should be stated at the end:
 
 
- Before starting to write own functions have a look to the
 provided example functions. It's much easier to use one of them
 as an template than starting from scratch. It is not necessary,
 that everybody solves the same problems again and again.
 
- If good examples are known, that could be used for introducing
 a whole class of problems, please send it to the author. If appropriate
 they will be included into the documentation of the toolbox and
 this introduction as an example function.
 
 
 
 

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions





   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).


   The Genetic and Evolutionary Algorithm Toolbox is not public domain.


   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,
      (pohlheim@systemtechnik.tu-ilmenau.de).
