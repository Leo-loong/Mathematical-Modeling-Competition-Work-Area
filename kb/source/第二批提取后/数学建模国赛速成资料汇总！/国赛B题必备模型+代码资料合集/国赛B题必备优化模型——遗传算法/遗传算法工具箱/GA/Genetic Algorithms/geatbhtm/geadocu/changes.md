GEATbx: What's new - version history and changes

## What's new - version history and changes

### 07.97

- Version 1.91 fixed maintenance update for Matlab5,

 (removing warnings due to changes in Matlab5), no substantial changes

 in documentation

### 10.96 - 06.97

- many small changes inside a lot of functions (see history inside each function)

- main function genalg1.m renamed to geamain

- all dga*.m functions checked and rewritten for current version

- functions bin2real and

 bin2int rewritten, now high-level functions

 to bindecod; error removed, which caused incorrect

 decoding when binary integer were used

- functions crt*.m renamed to init*.m (initbp,

 initrp)

- function ranking rewritten

- function expand.m renamed to expandm

 (name clash with Matlab5)

- variables called switch renamed to option inside

 all obj*.m functions (name clash with Matlab5)

### 09.96

- update of documentation to remove some small errors

- all fcn*.m functions checked and updated, definition of EASOM's

 function corrected

- Version 1.83 fixed (documentation), no change

 in m-files

### 09.05.96

- rewrite of chekgopt; incorporates

 merging of 2 parameter sets and the default parameters, one merging

 could be removed from all tbx*.m functions, thus, all tbx*.m functions

 are smaller now and easier to create, update and manage; the change

 is transparent for the user, however, own tbx*.m functions should

 be updated

- all tbx*.m functions checked and updated

- Version 1.81 fixed (m-files and documentation)

### 29.04.96

- problem with not appearing error message inside lower level

 functions removed;

 source of problem: eval function; if output parameter of

 eval function (x=eval(bla)) are defined, output of error function

 doesn't appear on screen, thus, the user don't know, where the

 error took place (only the name of the function with the problematic

 eval function was given);

 solution: put the whole expression inside the eval function

 (eval(x=bla) and the problem is solved, all files with eval of

 toolbox checked and updated

### 18.04.96

- Version 1.80 fixed (m-files and documentation)

### 15.04.96

- rewrite of Examples of Objective Functions documentation

 (tbxfncs.html), divided in many parts (fcn*.html), each part much

 smaller now, faster loading and viewing

### 11.04.96

- rewrite of Introduction to Genetic Algorithms documentation

 (gaalg.html), divided in many parts (alg*.html), each part much

 smaller now, faster loading and viewing

### 25.03.96

- new representation format: integer

 Now it's possible to use an integer representation for the

 variables. Internal the toolbox works on a binary representation,

 however, the user sees only the integer variables. See scrint1

 for usage (set parameter(19) = 3)

 and objint2 for an objective function

 example.

 At the moment there are no recombination operators, that can work

 on an integer representation.

- Error in defining mutation rate for binary representation

 corrected: mutation rate was set much to high. Now one mutation

 point per individual is really used.

### 15.03.96

- Evolutionary Strategy mutevo1

 incorporated in GA Toolbox, some internal changes for maintaining

 additional sets for mutation step sizes. This evolutionary strategy

 is implemented as a mutation function, use it without recombination.

 See scres1 and tbxres1

 for usage.

### 05.03.96

- Version 1.79 fixed (m-files and documentation)

### 04.03.96

- First example in tutorial changed to 2 dimension.

- GOPTIONS structure can now be empty, this special case is

 handled correct now (update of chekgopt.m, and all tbx*.m)

### 05.02.96

- rewrite of tutorial documentation (gaintro.html), divided

 in many parts (tut*.html), each part much smaller now, faster

 loading and viewing

### 23.01.96

- Download of complete documentation

 in two zip-files possible

### 02.11.95

- Version 1.78 fixed (m-files and documentation)

### 31.10./01.11.95

- theoretical aspects of selection methods added, comparison of selection methods

### 29.10.95

- documentation for extended line recombination

 and tournament selection

 added

### 28.10.95

- Naming conventions of GA Toolbox

 added

- Data structures

 of GA Toolbox added

### 11.10.95

- tournament selection added, seltour

### 06.10.95

- Version 1.77 fixed (m-files and documentation)

- Documentation for objective functions added

 LANGERMANN's function 11

 MICHALEWICZ's function 12

 BRANIN's rcos function

 EASOM's function

 GOLDSTEIN-PRICE's function

 Six hump camel back function

### 05.10.95

- LANGERMANN's function 11 objfun11

 as example objective function added

- MICHALEWICZ's function 12 objfun12

 as example objective function added

### 04.10.95

- Documentation Examples of objective functions of the GA Toolbox

 reviewed, 3-dimensional pictures for Parametric functions

 added and figures for Dynamic systems

 redone (in colour)

- function dgamesh reworked, new

 parameters for boundaries and number of mesh plot points added,

 this function was used for making the pictures of the parametric

 example functions above

### 05.09.95

- Documentation Genetic Algorithms: Methods, Principles and Algorithms

 finished, includes many figures and graphics

- Documentation for version 1.75 fixed

### 31.08.95

- Documentation Genetic Algorithm Toolbox - Tutorial

 improved, includes a graphical Calling Tree of GA Toolbox functions

### 21.08.95

- changes in geamain

- function name mapping for selection, mutation and recombination

 moved to gatbxini

- changes in gatbxini

- see above, gatbxini should be the only file for defining function

 names and file names

- support for user defined selection/mutation/recombination

 function added

### 18.08.95

- version 1.75 produced, includes multiple strategy support

 and enhanced documentation

### 14. - 18.08.95

- html documentation enhanced, test functions added

- perl script for automatic m-file documentation enhanced, (table,

 signature)

### 07.08.95

- changes in recombin

- multiple parameter sets supported (only REC_F)

- special call of recmut now inside

 recombin and not in geamain

- parameter VLUB added to recombin, used only for recmut

- changes in mutate

- multiple parameter sets supported (only MUT_F)

- changes in geamain

- special call of recmut now in recombin

- calling syntax of recombin changed

- computation of results of multiple strategies, which subpopulation

 (which parameter set) ist the most sucessful, display and save

 these values as well

- changes in recmut

- parameter checking shortened

- realmin removed, eps included, realmin didn't work, produced

 too many NaN

### 04.08.95

- changes in geamain (temporarily

 renamed in genalg2)

- produce as many parameter sets as subpopulation

- print to file all sets

- changes in select

- multiple parameter sets supported (only SEL_F and SelOpt)

- save to file only every SAVE2FILE generation (goption(28))

### 03.08.95

- use of special initialization function goption(29) possible

- changes in geamain; begin for use

 of multiple parameter sets

- changed chekgopt, GOPTIONSIN could

 be a matrix, still works with a vector

- changed tbxmpga, see above

### June 1995

- version 1.7 fixed, released to selected test sites

### April 1994

- First non-public beta release of Genetic Algorithm Toolbox

 for use with Matlab version 1.2. (includes documentation

 in Postscript)

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
