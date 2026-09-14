GEATbx: Function intrk4

# Documentation of intrk4

Index of Functions of GEA Toolbox for Matlab

## Function Synopsis

[Timesim, Result] = intrk4(SIM_F, Times, XINIT, Options, Control, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10)

## Help text

 INtegration of ODE's using RUNGE-KUTTA-formula 4

 This function implements the vectorized RUNGE-KUTTA-Integrator 4.

 Syntax:  [Timevec, Result] = intrk4(SIM_F, Times, XINIT, Options, Control, P1-Px)

 Input parameters:

    SIM_F     - function to simulate

    Times     - vector containing TStart (start time - optional) and TEnd (end time)

    XINIT     - initial values for the simulation of the individuals

                every row contains the initial values for 1 individual

    Options   - vector containing [ERRMAX: max. rel. error, STEPMIN: min. stepsize, STEPMAX: max. stepsize, ...

                                   (optional) NCONTR: number of control variables]

    Control   - control vector/matrix, every row is one control vector

                format:   1. ControlVariable  2. ControlVariable ...  NCONTR. ControlVariable

                         --------------------------------------------------------------------

                  Ind1: | 1:ControlSteps      1:ControlSteps     ...  1:ControlSteps

                  Ind2: | 1:ControlSteps      1:ControlSteps     ...  1:ControlSteps

    P1 - Px   - (optional) parameters passed through to simulation function

 Output parameters:

    Timesim   - vector containing time of simulation steps

    Result    - results, state vectors

                format:   1. ControlVariable  2. ControlVariable ...  NCONTR. ControlVariable

                         --------------------------------------------------------------------

                  Ind1: | 1:ControlSteps      1:ControlSteps     ...  1:ControlSteps

                  Ind2: | 1:ControlSteps      1:ControlSteps     ...  1:ControlSteps

 See also: objdopi, inteul

## Cross-Reference Information

This function calls

This function is called by

- expandm

- objdopi

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
