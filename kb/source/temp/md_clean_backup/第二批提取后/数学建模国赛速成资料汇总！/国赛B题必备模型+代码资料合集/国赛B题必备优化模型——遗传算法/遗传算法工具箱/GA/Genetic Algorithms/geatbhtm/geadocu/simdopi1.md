GEATbx: Function simdopi1




# Documentation of simdopi1


Index of Functions of GEA Toolbox for Matlab




## Function Synopsis

[ret, x0, str] = simdopi1(t, x, u, flag);


## Help text


 M-file description of the SIMULINK system named SIMDOPI1
	The block-diagram can be displayed by typing: SIMDOPI1.

	SYS=SIMDOPI1(T,X,U,FLAG) returns depending on FLAG certain
	system values given time point, T, current state vector, X,
	and input vector, U.
	FLAG is used to indicate the type of output to be returned in SYS.

	Setting FLAG=1 causes SIMDOPI1 to return state derivatives, FLAG=2
	discrete states, FLAG=3 system outputs and FLAG=4 next sample
	time. For more information and other options see SFUNC.

	Calling SIMDOPI1 with a FLAG of zero:
	[SIZES]=SIMDOPI1([],[],[],0),  returns a vector, SIZES, which
	contains the sizes of the state vector and other parameters.
		SIZES(1) number of states
		SIZES(2) number of discrete states
		SIZES(3) number of outputs
		SIZES(4) number of inputs.
	For the definition of other parameters in SIZES, see SFUNC.
	See also, TRIM, LINMOD, LINSIM, EULER, RK23, RK45, ADAMS, GEAR.



## Cross-Reference Information




This function is called by




- objdopi






GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions





   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).


   The Genetic and Evolutionary Algorithm Toolbox is not public domain.


   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,
      (pohlheim@systemtechnik.tu-ilmenau.de).
