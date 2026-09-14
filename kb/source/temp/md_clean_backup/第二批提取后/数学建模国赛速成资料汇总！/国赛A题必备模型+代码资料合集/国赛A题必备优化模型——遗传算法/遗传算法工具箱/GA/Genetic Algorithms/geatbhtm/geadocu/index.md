GEATbx: Genetic and Evolutionary Algorithm Toolbox for MATLAB 
 
 
 

 
 
 
 
 
# GEATbx: Genetic and Evolutionary Algorithm Toolbox for use
 with MATLAB

 
 
 Version 1.91 (July 1997)
 
 Hartmut Pohlheim
 
 
 
## Contents

 
 
 
- User Guide
 
 
- Tutorial
 
- Introduction to Evolutionary Algorithms
 
- Reference
 
 
 
- Features and Implementation
 
- Installation
 
- What's new - version history and changes
 
- Download of documentation
 
 
 
 
 
 There has been widespread interest using Genetic and Evolutionary
 Algorithms (EA: Evolutionary Algorithms). Compared to traditional
 search and optimization procedures, such as calculus-based and
 enumerative strategies, the EA's are robust, global and generally
 more straightforward to apply in situations where there is little
 or no a priori knowledge about the problem to solve. As EA's require
 no derivative information or formal initial estimates of the solution,
 and because they are stochastic in nature, EA's are capable of
 searching the entire solution space with more likelihood of finding
 the global optimum.
 
 Matlab has become a de-facto standard in Computer Aided
 Control System Design (CACSD). Many areas are catered for by a
 wide range of toolboxes, notably the Control System,
 Neural Network and Optimization Toolboxes, and
 the Simulink non-linear simulation package along with
 extensive visualization and analysis tools. In addition, Matlab
 has an open and extensible architecture allowing individual users
 to develop further routines for their own applications. These
 qualities provide a uniform and familiar environment on which
 to build genetic and evolutionary algorithm tools.
 
 The Genetic and Evolutionary Algorithm Toolbox provides
 a set of versatile tools for implementing a wide range of genetic
 and evolutionary algorithm methods.
 
 
 
## User Guide

 
 
### 1 Tutorial

 
 
 
- Tutorial - Index
 
 
- 1 Quick Start
 
- 2 Variable representation
 
- 3 Writing Objective Functions
 
- 4 Calling Tree of functions
 
- 5 Naming conventions
 
- 6 Data structures
 
 
 
- Examples of objective functions
 
 
- 1 Parametric Optimization
 
- 2 Optimization of dynamic systems
 
 
 
 
 
### 2 Introduction to Evolutionary
 Algorithms

 
 
 
- Genetic Algorithms: Principles, Methods and Algorithms
 
 
- 1 Introduction
 
- 2 Overview
 
- 3 Selection
 
- 4 Recombination
 
- 5 Mutation
 
- 6 Reinsertion
 
- 7 Parallel implementations
 
 
 
 
 
### 3 Reference

 
 
 
- Reference of GEA Toolbox Matlab-Files - Index
 (purpose, syntax and examples of all routines)
 
- Parameter Settings of GEA Toolbox
 
- What's new - version history and changes
 
- References
 
 
 
 
 
## Features

 
 
 
- real, integer and binary (linear and logarithmic scaling,
 gray coding) variable representation
 
- high level functions to all operators
 
- multiple population support
 
- broad class of operators
 
 
- selection: linear/non-linear ranking, stochastic universal
 sampling, local, truncation, tournament selection
 
- recombination: discrete, intermediate, line, extended
 line
 
- crossover: single/double point, shuffle, reduced surrogate
 
- mutation: binary, real valued
 
- reinsertion: global, local
 
- migration: unrestricted, ring, neighbourhood
 
 
 
- multiple strategy support
 
- sophisticated visualization
 
- comfortable monitoring and storing of results
 
- incorporation of problem specific knowledge
 
 
 
 
 
## Implementation

 
 
 
- m-file implementation
 
- compatible on all computer platforms
 
- modular, user-friendly structure
 
- high entry functions
 
- compatible with Optimization toolbox
 
- many example and test functions included (ready to run)
 
- extensive documentation
 
 
- tutorial
 
- quick start
 
- overview of structure
 
- explanation of algorithms
 
- reference of all operators and functions
 
- written in HTML-format
 
 
 
- default parameter settings
 
- easily extensible
 
 
 
 
 
 
 
## Installation

 
 
 Instructions for installing the Matlab toolboxes are
 found in the Matlab installation instructions. It is
 recommended that the files for the Genetic and Evolutionary
 Algorithm Toolbox are stored in a directory named genevo
 off the main matlab/toolbox
 directory.
 
 
 
## What's new - version history and changes
 

 
 
 In September 1994 I started developing my own toolbox for working
 with genetic and evolutionary algorithms in Matlab. My earlier
 work provided a starting point. During the last years a much enhanced
 version was written. The handling of the toolbox is now compatible
 with the Optimization Toolbox. Many new functions were added,
 existing functions rewritten and extended. Thus, a new toolbox
 was developed. The new name Genetic and Evolutionary Algorithm
 Toolbox for use with Matlab reflects this development.
 Version 1.7 was the first test release (June 1995).
 
 For a detailed record of all changes since version 1.7 see Version history/Changes of GEA Toolbox.
 
 
 
## Download of documentation

 
 
 I offer the possibility to download the whole documentation in
 compressed format. This offers users with slower connections easier
 viewing and browsing. The documentation comes in two files: one
 contains all the html-files, the other all the gif-files. Both
 files are zip-ed.
 
 Before downloading the documentation, please consider the following:
 The use of this documentation is allowed only for personal
 information. Additionally, you can copy this documentation
 in unchanged form on your internal net for internal
 use as documentation of the Genetic and Evolutionary Algorithm
 Toolbox. It is prohibited to use the documentation or part
 of it in changed form. (However, if you want to use part of it,
 text or graphics for lectures, another documentation or anything
 else, please contact the author.)
 
 If you agree with this, you can download
 
 
- HTML-text-files of GEA Toolbox
 (~200K),
 
- GIF-graphics-files of GEA Toolbox
 (~550K).
 
 
 
 Extract all files into one directory and open the file index.html.
 
 

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions





   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).


   The Genetic and Evolutionary Algorithm Toolbox is not public domain.


   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,
      (pohlheim@systemtechnik.tu-ilmenau.de).
