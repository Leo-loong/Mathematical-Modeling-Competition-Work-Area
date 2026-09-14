Genetic Algorithm Demo
Version 1.2
Ron Shaffer
Naval Research Laboratory
Chemistry Division, Code 6110
Environmental Chemistry and Sensor Chemistry Section
Washington, DC  20375

Introduction
To promote interest in their fields, many scientists write demonstration programs showing off their "pet" algorithms. My favorite optimization technique is the genetic algorithm (GA). I have used GAs for many applications such as training neural networks, wavelength selection in infrared spectroscopy, selecting optimal regression models, and discriminant (pattern recognition) optimization. I have been studying GAs for about 3 years now and have implemented them both in FORTRAN and MATLAB. For many novice programmers, MATLAB is much simpler to understand. Thus, when I decided to write a GA demo I chose to implement it in MATLAB. While the program is intended to be a demonstration of the operating principles of a genetic algorithm, the individual m-files included in the package can modified by the user for more specific applications. I have made little effort to improve the speed of the code, nor do I claim that it is bug-free. If you find any bugs or have ideas for improvements, please feel free to contact me shaffer@ccf.nrl.navy.mil.

A Practical Guide to Genetic Algorithms
In addition to downloading the GA demo, I recommend downloading the practical guide that I have written. This document explains the basics of genetic algorithms and gives references for further study.
http://chem1.nrl.navy.mil/~shaffer/practga.html

Description of GA Demo
GA demo version 1.1 features a text-based (sorry, no GUI yet) interface with two built-in fitness functions. For both fitness function a binary coding (i.e. each gene is a zero or a one) is used on the chromosome. The first fitness function attempts to create a chromosome of all 1's by summing up the values on the chromosome. Thus, the more ones in the chromosome the higher the fitness score. This fitness function is useful for watching how the GA evolves better chromosomes over time. With full description output turned on, the effect of different GA configuration settings can be studied using this simple system.
The second fitness function is a multi-modal optimization problem developed by Bohachevesky.
f(x,y) = - x2 + 2y2 - 0.3 cos(3pix) - 0.4 cos(4piy) + 0.7
For this fitness function the binary chromosome is converted to a real number and employed in the above equation. The global maximum is located at x=0 and y=0. In the conversion process, the range of real numbers is limited from 1 to -1. Most applications in analytical chemistry involve the optimization of real numbers. The ability to convert from binary chromosomes to real numbered variable settings allows the use of a binary-coded GA.
After placing the GA demo in an appropriate subdirectory on your system, the demo can be started by typing gademo at the MATLAB command line. The following menu will then appear.
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
Current GA Configuration
1 Chromosome Length 10
2 Population Size 20
3 Number of Generations 10
4 Mutation Rate 0.100
5 Crossover Rate 0.950
6 Crossover Type: Single
7 Elitist Operator: On
8 Function: Simple
9 Gray Coding: Off
10 Start GA Optimization (Full Printout)
11 Start GA Optimization (Minimal Printout)
12 Quit GA Demo
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
Enter Option (1-12) >
Chromosome Length is the number of genes present on the chromosome. For this demo, each gene can take on two values (0 or 1). The default settings is a length of 10. The chromosome length is an important consideration when optimizing a real variable problem. Longer chromosomes allow better conversion from the binary chromosome to the real number variable. However, the longer chromosome is computationally more inefficient and generally takes longer to find the optimal region. This concept can be studied by changing the fitness function to the bohachevsky function.

Population Size is the number of chromosomes in the population. Larger population sizes increase the amount of variation present in the population at the expense of requiring more fitness function evaluations. I have found that the best population size is dependent upon both the application and the length of the chromosome. For longer chromosomes or more challenging the optimization problems, I usually use of population size greater than 100, while for simpler problems a population size of 20 will lead to good results.

Number of Generations is the maximum number of generations that will be performed.

Mutation Rate is the probability of mutation occurring. Mutation is the random flipping of one of the bits or genes (i.e., change a 0 to 1). Mutation is employed to give new information to the population. It also prevents the population from becoming saturated with chromosomes that all look alike (premature convergence). Large mutation rates increase the probability of destroying a good chromosome, but prevents premature convergence. The best mutation rate is application dependent and related to both the length of the chromosome and the size of the population. For most applications a mutation rate of 0.1 to 0.01 is employed.

Crossover Rate is the probability of crossover reproduction being performed. A high crossover is used to encourage good mixing of the chromosomes. For most applications a crossover rate of 0.75 to 0.95 is employed.

Crossover Type is the type of crossover reproduction that is employed. The GA demo allows three different types of crossover: single, double, and uniform. The choice of crossover type is primarily application dependent.

Elitist Operator determines whether the best chromosome for each population is placed into the next generation unchanged. Most applications that I have seen use some form of elitist operator. If the elitist operator is turned on, the best fitness score from one population to the next will never decrease.

Fitness Function allows the user to decide which fitness function the GA should employ. The first fitness function is called the simple function and consists of the summation of the chromosome. The second fitness function finds chromosomes which optimize the Bohachevsky function.

Gray Coding determines whether gray coding is used when converting binary chromosomes to real number valued variable settings.  For multiparameter
real number functions such as the Bohachevsky function many GA practioners
recommend using the gray coding feature.  Gray coding lessens the impact of
hamming cliffs in the binary representation.

Optimization with Full Printout displays each chromosome in the population along with its fitness score and at the end of each generation it prints out some statistics about the population.

Optimization with Minimal Printout displays only the GA optimization statistics for each generation.

Quit allows the user to quit the demo and return to MATLAB.

After the optimization is finished two plots and some text will appear. Figure 1 is a plot showing the fitness score for the best chromosome and the mean fitness score for all chromosomes for each generation. Figure 2 is a histogram showing the number times each gene is "on" (a value of 1) across the final population. The text will show the best chromosome and its fitness score.
