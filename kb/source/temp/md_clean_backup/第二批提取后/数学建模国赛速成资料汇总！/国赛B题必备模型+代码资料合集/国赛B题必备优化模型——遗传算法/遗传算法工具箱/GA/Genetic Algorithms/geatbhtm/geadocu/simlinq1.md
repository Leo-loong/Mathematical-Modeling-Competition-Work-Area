GEATbx: Function simlinq1




# Documentation of simlinq1


Index of Functions of GEA Toolbox for Matlab




## Function Synopsis

[ret,x0,str]=simlinq1(t,x,u,flag);


## Help text


 M-file description of the SIMULINK system named SIMLINQ1
	The block-diagram can be displayed by typing: SIMLINQ1.

	SYS=SIMLINQ1(T,X,U,FLAG) returns depending on FLAG certain
	system values given time point, T, current state vector, X,
	and input vector, U.
	FLAG is used to indicate the type of output to be returned in SYS.

	Setting FLAG=1 causes SIMLINQ1 to return state derivatives, FLAG=2
	discrete states, FLAG=3 system outputs and FLAG=4 next sample
	time. For more information and other options see SFUNC.

	Calling SIMLINQ1 with a FLAG of zero:
	[SIZES]=SIMLINQ1([],[],[],0),  returns a vector, SIZES, which
	contains the sizes of the state vector and other parameters.
		SIZES(1) number of states
		SIZES(2) number of discrete states
		SIZES(3) number of outputs
		SIZES(4) number of inputs.
	For the definition of other parameters in SIZES, see SFUNC.
	See also, TRIM, LINMOD, LINSIM, EULER, RK23, RK45, ADAMS, GEAR.



## Cross-Reference Information




This function is called by




- objlinq2






GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions





   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).


   The Genetic and Evolutionary Algorithm Toolbox is not public domain.


   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,
      (pohlheim@systemtechnik.tu-ilmenau.de).
