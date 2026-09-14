LIBSVM FAQ

# LIBSVM  FAQ

last modified :

Sun, 13 Mar 2011 13:30:52 GMT

- All Questions(74)

- Q1:_Some_sample_uses_of_libsvm(2)

- Q2:_Installation_and_running_the_program(12)

- Q3:_Data_preparation(7)

- Q4:_Training_and_prediction(33)

- Q5:_Probability_outputs(3)

- Q6:_Graphic_interface(3)

- Q7:_Java_version_of_libsvm(4)

- Q8:_Python_interface(1)

- Q9:_MATLAB_interface(9)

- Some courses which have used libsvm as a tool

- Some applications/tools which have used libsvm

- Where can I find documents of libsvm ?

- Where are change log and earlier versions?

- How to cite LIBSVM?

- I would like to use libsvm in my software. Is there any license problem?

- Is there a repository of additional tools based on libsvm?

- On unix machines, I got "error in loading shared libraries" or "cannot open shared object file." What happened ?

- I have modified the source and would like to build the graphic interface "svm-toy" on MS windows. How should I do it ?

- I am an MS windows user but why only one (svm-toy) of those precompiled .exe actually runs ?

- What is the difference between "." and "*" outputed during training?

- Why occasionally the program (including MATLAB or other interfaces) crashes and gives a segmentation fault?

- How to build a dynamic library (.dll file) on MS windows?

- On some systems (e.g., Ubuntu), compiling LIBSVM gives many warning messages. Is this a problem and how to disable the warning message?

- Why sometimes not all attributes of a data appear in the training/model files ?

- What if my data are non-numerical ?

- Why do you consider sparse format ? Will the training of dense data be much slower ?

- Why sometimes the last line of my data is not read by svm-train?

- Is there a program to check if my data are in the correct format?

- May I put comments in data files?

- How to convert other data formats to LIBSVM format?

- The output of training C-SVM is like the following. What do they mean?

- Can you explain more about the model file?

- Should I use float or double to store numbers in the cache ?

- How do I choose the kernel?

- Does libsvm have special treatments for linear SVM?

- The number of free support vectors is large. What should I do?

- Should I scale training and testing data in a similar way?

- Does it make a big difference  if I scale each attribute to [0,1] instead of [-1,1]?

- The prediction rate is low. How could I improve it?

- My data are unbalanced. Could libsvm handle such problems?

- What is the difference between nu-SVC and C-SVC?

- The program keeps running (without showing any output). What should I do?

- The program keeps running (with output, i.e. many dots). What should I do?

- The training time is too long. What should I do?

- Does shrinking always help?

- How do I get the decision value(s)?

- How do I get the distance between a point and the hyperplane?

- On 32-bit machines, if I use a large cache (i.e. large -m) on a linux machine, why sometimes I get "segmentation fault ?"

- How do I disable screen output of svm-train?

- I would like to use my own kernel. Any example? In svm.cpp, there are two subroutines for kernel evaluations: k_function() and kernel_function(). Which one should I modify ?

- What method does libsvm use for multi-class SVM ? Why don't you use the "1-against-the rest" method ?

- After doing cross validation, why there is no model file outputted ?

- Why my cross-validation results are different from those in the Practical Guide?

- On some systems CV accuracy is the same in several runs. How could I use different data partitions? In other words, how do I set random seed in LIBSVM?

- I would like to solve L2-loss SVM (i.e., error term is quadratic). How should I modify the code ?

- How do I choose parameters for one-class svm as training data are in only one class?

- Why the code gives NaN (not a number) results?

- Why on windows sometimes grid.py fails?

- Why grid.py/easy.py sometimes generates the following warning message?

- Why the sign of predicted labels and decision values are sometimes reversed?

- I don't know class labels of test data. What should I put in the first column of the test file?

- How can I use OpenMP to parallelize LIBSVM on a multicore/shared-memory computer?

- How could I know which training instances are support vectors?

- Why training a probability model (i.e., -b 1) takes a longer time?

- Why using the -b option does not give me better accuracy?

- Why using svm-predict -b 0 and -b 1 gives different accuracy values?

- How can I save images drawn by svm-toy?

- I press the "load" button to load data points but why svm-toy does not draw them ?

- I would like svm-toy to handle more than three classes of data, what should I do ?

- What is the difference between Java version and C++ version of libsvm?

- Is the Java version significantly slower than the C++ version?

- While training I get the following error message: java.lang.OutOfMemoryError. What is wrong?

- Why you have the main source file svm.m4 and then transform it to svm.java?

- Except the python-C++ interface provided, could I use Jython to call libsvm ?

- I compile the MATLAB interface without problem, but why errors occur while running it?

- On 64bit Windows I compile the MATLAB interface without problem, but why errors occur while running it?

- Does the MATLAB interface provide a function to do scaling?

- How could I use MATLAB interface for parameter selection?

- I use MATLAB parallel programming toolbox on a multi-core environment for parameter selection. Why the program is even slower?

- How do I use LIBSVM with OpenMP under MATLAB?

- How could I generate the primal variable w of linear SVM?

- Is there an OCTAVE interface for libsvm?

- How to handle the name conflict between svmtrain in the libsvm matlab interface and that in MATLAB bioinformatics toolbox?

Q: Some courses which have used libsvm as a tool

- Institute for Computer Science,

Faculty of Applied Science, University of Freiburg, Germany

-

Division of Mathematics and Computer Science.

Faculteit der Exacte Wetenschappen

Vrije Universiteit, The Netherlands.

-

Electrical and Computer Engineering Department,

University of Wisconsin-Madison

-

Technion (Israel Institute of Technology), Israel.

-

Computer and Information Sciences Dept., University of Florida

-

The Institute of Computer Science,

University of Nairobi, Kenya.

-

Applied Mathematics and Computer Science, University of Iceland.

-

SVM tutorial in machine learning

summer school, University of Chicago, 2005.

[Go Top]

Q: Some applications/tools which have used libsvm

(and maybe liblinear).

-

LIBPMK: A Pyramid Match Toolkit

- Maltparser:

a system for data-driven dependency parsing

-

PyMVPA: python tool for classifying neuroimages

-

SOLpro: protein solubility predictor

-

BDVal: biomarker discovery in high-throughput datasets.

-

Realtime object recognition

-

scikits.learn: machine learning in Python

[Go Top]

Q: Where can I find documents of libsvm ?

-

Official implementation document:

C.-C. Chang and

C.-J. Lin.

LIBSVM

: a library for support vector machines.

-  Instructions for using LIBSVM are in the README files of some directories

README in the main directory: details all options, data format, and library calls.

tools/README: parameter selection and other tools

-

A guide for beginners:

C.-W. Hsu, C.-C. Chang, and

C.-J. Lin.

A practical guide to support vector classification

[Go Top]

Q: Where are change log and earlier versions?

See the change log.

 You can download earlier versions

here.

[Go Top]

Q: How to cite LIBSVM?

Please cite the following document:

Chih-Chung Chang and Chih-Jen Lin, LIBSVM

: a library for support vector machines, 2001.

Software available at http://www.csie.ntu.edu.tw/~cjlin/libsvm

The bibtex format is

@Manual{CC01a,

  author =	 {Chih-Chung Chang and Chih-Jen Lin},

  title =	 {{LIBSVM}: a library for support vector machines},

  year =	 {2001},

  note =	 {Software available at \url{http://www.csie.ntu.edu.tw/~cjlin/libsvm}}

}

[Go Top]

Q: I would like to use libsvm in my software. Is there any license problem?

The libsvm license ("the modified BSD license")

is compatible with many

free software licenses such as GPL. Hence, it is very easy to

use libsvm in your software.

Please check the COPYRIGHT file in detail. Basically

you need to

-

Clearly indicate that LIBSVM is used.

-

Retain the LIBSVM COPYRIGHT file in your software.

It can also be used in commercial products.

[Go Top]

Q: Is there a repository of additional tools based on libsvm?

Yes, see libsvm

tools

[Go Top]

Q: On unix machines, I got "error in loading shared libraries" or "cannot open shared object file." What happened ?

This usually happens if you compile the code

on one machine and run it on another which has incompatible

libraries.

Try to recompile the program on that machine or use static linking.

[Go Top]

Q: I have modified the source and would like to build the graphic interface "svm-toy" on MS windows. How should I do it ?

Build it as a project by choosing "Win32 Project."

On the other hand, for "svm-train" and "svm-predict"

you want to choose "Win32 Console Project."

After libsvm 2.5, you can also use the file Makefile.win.

See details in README.

If you are not using Makefile.win and see the following

link error

LIBCMTD.lib(wwincrt0.obj) : error LNK2001: unresolved external symbol

_wWinMain@16

you may have selected a wrong project type.

[Go Top]

Q: I am an MS windows user but why only one (svm-toy) of those precompiled .exe actually runs ?

You need to open a command window

and type  svmtrain.exe to see all options.

Some examples are in README file.

[Go Top]

Q: What is the difference between "." and "*" outputed during training?

"." means every 1,000 iterations (or every #data

iterations is your #data is less than 1,000).

"*" means that after iterations of using

a smaller shrunk problem,

we reset to use the whole set. See the

implementation document for details.

[Go Top]

Q: Why occasionally the program (including MATLAB or other interfaces) crashes and gives a segmentation fault?

Very likely the program consumes too much memory than what the

operating system can provide. Try a smaller data and see if the

program still crashes.

[Go Top]

Q: How to build a dynamic library (.dll file) on MS windows?

The easiest way is to use Makefile.win.

See details in README.

Alternatively, you can use Visual C++. Here is

the example using Visual Studio .Net 2008:

- Create a Win32 empty DLL project and set (in Project->$Project_Name

Properties...->Configuration) to "Release."

   About how to create a new dynamic link library, please refer to

http://msdn2.microsoft.com/en-us/library/ms235636(VS.80).aspx

-  Add svm.cpp, svm.h to your project.

-  Add __WIN32__ and _CRT_SECURE_NO_DEPRECATE to Preprocessor definitions (in

Project->$Project_Name Properties...->C/C++->Preprocessor)

-  Set Create/Use Precompiled Header to Not Using Precompiled Headers

(in Project->$Project_Name Properties...->C/C++->Precompiled Headers)

-  Set the path for the Modulation Definition File svm.def (in

Project->$Project_Name Properties...->Linker->input

-  Build the DLL.

-  Rename the dll file to libsvm.dll and move it to the correct path.

[Go Top]

Q: On some systems (e.g., Ubuntu), compiling LIBSVM gives many warning messages. Is this a problem and how to disable the warning message?

The warning message is like

svm.cpp:2730: warning: ignoring return value of int fscanf(FILE*, const char*, ...), declared with attribute warn_unused_result

but this is not a problem. In the future we may modify the code

so that these messages do not appear.

At this moment, to disable the warning message you can replace

CFLAGS = -Wall -Wconversion -O3 -fPIC

with

CFLAGS = -Wall -Wconversion -O3 -fPIC -U_FORTIFY_SOURCE

in Makefile.

[Go Top]

Q: Why sometimes not all attributes of a data appear in the training/model files ?

libsvm uses the so called "sparse" format where zero

values do not need to be stored. Hence a data with attributes

1 0 2 0

is represented as

1:1 3:2

[Go Top]

Q: What if my data are non-numerical ?

Currently libsvm supports only numerical data.

You may have to change non-numerical data to

numerical. For example, you can use several

binary attributes to represent a categorical

attribute.

[Go Top]

Q: Why do you consider sparse format ? Will the training of dense data be much slower ?

This is a controversial issue. The kernel

evaluation (i.e. inner product) of sparse vectors is slower

so the total training time can be at least twice or three times

of that using the dense format.

However, we cannot support only dense format as then we CANNOT

handle extremely sparse cases. Simplicity of the code is another

concern. Right now we decide to support

the sparse format only.

[Go Top]

Q: Why sometimes the last line of my data is not read by svm-train?

We assume that you have '\n' in the end of

each line. So please press enter in the end

of your last line.

[Go Top]

Q: Is there a program to check if my data are in the correct format?

The svm-train program in libsvm conducts only a simple check of the input data. To do a

detailed check, after libsvm 2.85, you can use the python script tools/checkdata.py. See tools/README for details.

[Go Top]

Q: May I put comments in data files?

We don't officially support this. But, cureently LIBSVM

is able to process data in the following

format:

1 1:2 2:1 # your comments

Note that the character ":" should not appear in your

comments.

test.txt

1 1:2 2:1 # proten A

then on unix machines you can do

cut -d '#' -f 1  test.features

cut -d '#' -f 2  test.comments

svm-predict test.feature train.model test.predicts

paste -d '#' test.predicts test.comments | sed 's/#/ #/' > test.results

-->

[Go Top]

Q: How to convert other data formats to LIBSVM format?

It depends on your data format.

We have a simple C code to transfer space/colon

separated format to libsvm format. Please contact

us if needed.

Alternatively, a simple way is to use

libsvmwrite in the libsvm matlab/octave interface.

Take a CSV (colon separated format) file

in UCI machine learning repository as an example.

We download SPECTF.train.

Labels are in the first column. The following steps produce

a file in the libsvm format.

matlab> SPECTF = csvread('SPECTF.train'); % read a csv file

matlab> labels = SPECTF(:, 1); % labels from the 1st column

matlab> features = SPECTF(:, 2:end);

matlab> features_sparse = sparse(features); % features must be in a sparse matrix

matlab> libsvmwrite('SPECTFlibsvm.train', labels, features_sparse);

The tranformed data are stored in SPECTFlibsvm.train.

[Go Top]

Q: The output of training C-SVM is like the following. What do they mean?

optimization finished, #iter = 219

nu = 0.431030

obj = -100.877286, rho = 0.424632

nSV = 132, nBSV = 107

Total nSV = 132

obj is the optimal objective value of the dual SVM problem.

rho is the bias term in the decision function

sgn(w^Tx - rho).

nSV and nBSV are number of support vectors and bounded support

vectors (i.e., alpha_i = C). nu-svm is a somewhat equivalent

form of C-SVM where C is replaced by nu. nu simply shows the

corresponding parameter. More details are in

libsvm document.

[Go Top]

Q: Can you explain more about the model file?

After the parameters, each line represents a support vector.

Support vectors are listed in the order of "labels" listed earlier.

(i.e., those from the first class in the "labels" list are

grouped first, and so on.)

If k is the total number of classes,

in front of a support vector in class j, there are

k-1 coefficients

y*alpha where alpha are dual solution of the

following two class problems:

1 vs j, 2 vs j, ..., j-1 vs j, j vs j+1, j vs j+2, ..., j vs k

and y=1 in first j-1 coefficients, y=-1 in the remaining

k-j coefficients.

For example, if there are 4 classes, the file looks like:

+-+-+-+--------------------+

|1|1|1|                    |

|v|v|v|  SVs from class 1  |

|2|3|4|                    |

+-+-+-+--------------------+

|1|2|2|                    |

|v|v|v|  SVs from class 2  |

|2|3|4|                    |

+-+-+-+--------------------+

|1|2|3|                    |

|v|v|v|  SVs from class 3  |

|3|3|4|                    |

+-+-+-+--------------------+

|1|2|3|                    |

|v|v|v|  SVs from class 4  |

|4|4|4|                    |

+-+-+-+--------------------+

See also

 an illustration using

MATLAB/OCTAVE.

[Go Top]

Q: Should I use float or double to store numbers in the cache ?

We have float as the default as you can store more numbers

in the cache.

In general this is good enough but for few difficult

cases (e.g. C very very large) where solutions are huge

numbers, it might be possible that the numerical precision is not

enough using only float.

[Go Top]

Q: How do I choose the kernel?

In general we suggest you to try the RBF kernel first.

A recent result by Keerthi and Lin

(

download paper here)

shows that if RBF is used with model selection,

then there is no need to consider the linear kernel.

The kernel matrix using sigmoid may not be positive definite

and in general it's accuracy is not better than RBF.

(see the paper by Lin and Lin

(

download paper here).

Polynomial kernels are ok but if a high degree is used,

numerical difficulties tend to happen

(thinking about dth power of (1) goes to infinity).

[Go Top]

Q: Does libsvm have special treatments for linear SVM?

No, libsvm solves linear/nonlinear SVMs by the

same way.

Some tricks may save training/testing time if the

linear kernel is used,

so libsvm is NOT particularly efficient for linear SVM,

especially when

C is large and

the number of data is much larger

than the number of attributes.

You can either

-

Use small C only. We have shown in the following paper

that after C is larger than a certain threshold,

the decision function is the same.

S. S. Keerthi

and

C.-J. Lin.

Asymptotic behaviors of support vector machines with

Gaussian kernel

.

Neural Computation, 15(2003), 1667-1689.

-

Check liblinear,

which is designed for large-scale linear classification.

 Please also see our SVM guide

on the discussion of using RBF and linear

kernels.

[Go Top]

Q: The number of free support vectors is large. What should I do?

This usually happens when the data are overfitted.

If attributes of your data are in large ranges,

try to scale them. Then the region

of appropriate parameters may be larger.

Note that there is a scale program

in libsvm.

[Go Top]

Q: Should I scale training and testing data in a similar way?

Yes, you can do the following:

> svm-scale -s scaling_parameters train_data > scaled_train_data

> svm-scale -r scaling_parameters test_data > scaled_test_data

[Go Top]

Q: Does it make a big difference  if I scale each attribute to [0,1] instead of [-1,1]?

For the linear scaling method, if the RBF kernel is

used and parameter selection is conducted, there

is no difference. Assume Mi and mi are

respectively the maximal and minimal values of the

ith attribute. Scaling to [0,1] means

                x'=(x-mi)/(Mi-mi)

For [-1,1],

                x''=2(x-mi)/(Mi-mi)-1.

In the RBF kernel,

                x'-y'=(x-y)/(Mi-mi), x''-y''=2(x-y)/(Mi-mi).

Hence, using (C,g) on the [0,1]-scaled data is the

same as (C,g/2) on the [-1,1]-scaled data.

 Though the performance is the same, the computational

time may be different. For data with many zero entries,

[0,1]-scaling keeps the sparsity of input data and hence

may save the time.

[Go Top]

Q: The prediction rate is low. How could I improve it?

Try to use the model selection tool grid.py in the python

directory find

out good parameters. To see the importance of model selection,

please

see my  talk:

A practical guide to support vector

classification

[Go Top]

Q: My data are unbalanced. Could libsvm handle such problems?

Yes, there is a -wi options. For example, if you use

> svm-train -s 0 -c 10 -w1 1 -w-1 5 data_file

the penalty for class "-1" is larger.

Note that this -w option is for C-SVC only.

[Go Top]

Q: What is the difference between nu-SVC and C-SVC?

Basically they are the same thing but with different

parameters. The range of C is from zero to infinity

but nu is always between [0,1]. A nice property

of nu is that it is related to the ratio of

support vectors and the ratio of the training

error.

[Go Top]

Q: The program keeps running (without showing any output). What should I do?

You may want to check your data. Each training/testing

data must be in one line. It cannot be separated.

In addition, you have to remove empty lines.

[Go Top]

Q: The program keeps running (with output, i.e. many dots). What should I do?

In theory libsvm guarantees to converge.

Therefore, this means you are

handling ill-conditioned situations

(e.g. too large/small parameters) so numerical

difficulties occur.

[Go Top]

Q: The training time is too long. What should I do?

For large problems, please specify enough cache size (i.e.,

-m).

Slow convergence may happen for some difficult cases (e.g. -c is large).

You can try to use a looser stopping tolerance with -e.

If that still doesn't work, you may train only a subset of the data.

You can use the program subset.py in the directory "tools"

to obtain a random subset.

If you have extremely large data and face this difficulty, please

contact us. We will be happy to discuss possible solutions.

 When using large -e, you may want to check if -h 0 (no shrinking) or -h 1 (shrinking) is faster.

See a related question below.

[Go Top]

Q: Does shrinking always help?

If the number of iterations is high, then shrinking

often helps.

However, if the number of iterations is small

(e.g., you specify a large -e), then

probably using -h 0 (no shrinking) is better.

See the

implementation document for details.

[Go Top]

Q: How do I get the decision value(s)?

We print out decision values for regression. For classification,

we solve several binary SVMs for multi-class cases. You

can obtain values by easily calling the subroutine

svm_predict_values. Their corresponding labels

can be obtained from svm_get_labels.

Details are in

README of libsvm package.

We do not recommend the following. But if you would

like to get values for

TWO-class classification with labels +1 and -1

(note: +1 and -1 but not things like 5 and 10)

in the easiest way, simply add

		printf("%f\n", dec_values[0]*model->label[0]);

after the line

		svm_predict_values(model, x, dec_values);

of the file svm.cpp.

Positive (negative)

decision values correspond to data predicted as +1 (-1).

[Go Top]

Q: How do I get the distance between a point and the hyperplane?

The distance is |decision_value| / |w|.

We have |w|^2 = w^Tw = alpha^T Q alpha = 2*(dual_obj + sum alpha_i).

Thus in svm.cpp please find the place

where we calculate the dual objective value

(i.e., the subroutine Solve())

and add a statement to print w^Tw.

[Go Top]

Q: On 32-bit machines, if I use a large cache (i.e. large -m) on a linux machine, why sometimes I get "segmentation fault ?"

On 32-bit machines, the maximum addressable

memory is 4GB. The Linux kernel uses 3:1

split which means user space is 3G and

kernel space is 1G. Although there are

3G user space, the maximum dynamic allocation

memory is 2G. So, if you specify -m near 2G,

the memory will be exhausted. And svm-train

will fail when it asks more memory.

For more details, please read

this article.

The easiest solution is to switch to a

 64-bit machine.

Otherwise, there are two ways to solve this. If your

machine supports Intel's PAE (Physical Address

Extension), you can turn on the option HIGHMEM64G

in Linux kernel which uses 4G:4G split for

kernel and user space. If you don't, you can

try a software `tub' which can eliminate the 2G

boundary for dynamic allocated memory. The `tub'

is available at

http://www.bitwagon.com/tub.html.

Note: This problem is specific to

gnu C library which is used in linux.

The solution is as follows:

In our program we have malloc() which uses two methods

to allocate memory from kernel. One is

sbrk() and another is mmap(). sbrk is faster, but mmap

has a larger address

space. So malloc uses mmap only if the wanted memory size is larger

than some threshold (default 128k).

In the case where each row is not large enough (#elements

Therefore, in the main program (i.e. svm-train.c) you want

to have

      #include <malloc.h>

and then in main():

      mallopt(M_MMAP_THRESHOLD, 32768);

      mallopt(M_MMAP_MAX,1000000);

You can also set the environment variables instead

of writing them in the program:

$ M_MMAP_MAX=1000000 M_MMAP_THRESHOLD=32768 ./svm-train .....

More information can be found by

$ info libc "Malloc Tunable Parameters"

-->

[Go Top]

Q: How do I disable screen output of svm-train?

For commend-line users, use the -q option:

> ./svm-train -q heart_scale

For library users, set the global variable

extern void (*svm_print_string) (const char *);

to specify the output format. You can disable the output by the following steps:

-

Declare a function to output nothing:

void print_null(const char *s) {}

-

Assign the output function of libsvm by

svm_print_string = &print_null;

Finally, a way used in earlier libsvm

is by updating svm.cpp from

#if 1

void info(const char *fmt,...)

to

#if 0

void info(const char *fmt,...)

[Go Top]

Q: I woulments

An example is "LIBSVM for string data" in LIBSVM Tools.

The reason why we have two functions is as follows.

For the RBF kernel exp(-g |xi - xj|^2), if we calculate

xi - xj first and then the norm square, there are 3n operations.

Thus we consider exp(-g (|xi|^2 - 2dot(xi,xj) +|xj|^2))

and by calculating all |xi|^2 in the beginning,

the number of operations is reduced to 2n.

This is for the training.  For prediction we cannot

do this so a regular subroutine using that 3n operations is

needed.

The easiest way to have your own kernel is

to  put the same code in these two

subroutines by replacing any kernel.

[Go Top]

Q: What method does libsvm use for multi-class SVM ? Why don't you use the "1-against-the rest" method ?

It is one-against-one. We chose it after doing the following

comparison:

C.-W. Hsu and C.-J. Lin.

A comparison of methods

for multi-class support vector machines

,

IEEE Transactions on Neural Networks, 13(2002), 415-425.

"1-against-the rest" is a good method whose performance

is comparable to "1-against-1." We do the latter

simply because its training time is shorter.

[Go Top]

Q: After doing cross validation, why there is no model file outputted ?

Cross validation is used for selecting good parameters.

After finding them, you want to re-train the whole

data without the -v option.

[Go Top]

Q: Why my cross-validation results are different from those in the Practical Guide?

Due to random partitions of

the data, on different systems CV accuracy values

may be different.

[Go Top]

Q: Osubroutines by replacing any kernel.

[Go Top]

If you use GNU C library,

the default seed 1 is considered. Thus you always

get the same result of running svm-train -v.

To have different seeds, you can add the following code

in svm-train.c:

#include <time.h>

and in the beginning of the subroutine do_cross_validation(),

srand(time(0));

Alternatively, if you are not using GNU C library

and would like to use a fixed seed, you can have

srand(1);

For Java, the random number generator

is initialized using the time information.

So results of two CV runs are different.

To fix the seed, after version 3.1 (released

in mid 2011), you can add

svm.rand.setSeed(0);

in the main() function of svm_train.java.

[Go Top]

Q: I would like to solve L2-loss SVM (i.e., error term is quadratic). How should I modify the code ?

It is extremely easy. Taking c-svc for example, to solve

min_w w^Tw/2 + C \sum max(0, 1- (y_i w^Tx_i+b))^2,

only two

places of svm.cpp have to be changed.

First, modify the following line of

solve_c_svc from

	s.Solve(l, SVC_Q(*prob,*param,y), minus_ones, y,

		alpha, Cp, Cn, param->eps, si, param->shrinking);

to

	s.Solve(l, SVC_Q(*prob,*param,y), minus_ones, y,

		alpha, INF, INF, param->eps, si, param->shrinking);

Second, in  the class  of SVC_Q, declare C as

a private variable:

	double C;

In the constructor replace

	for(int i=0;i<prob.l;i++)

		QD[i]= (Qfloat)(this->*kernel_function)(i,i);

with

        this->C = param.C;

	for(int i=0;i<prob.l;i++)

		QD[i]= (Qfloat)(this->*kernel_function)(i,i)+0.5/C;

Then in the subroutine get_Q, after the for loop, add

        if(i >= start && i

For one-class svm, the modification is exactly the same. For SVR, you don't need an if statement like the above. Instead, you only need a simple assignment:

	data[real_i] += 0.5/C;

For large linear L2-loss SVM, please use

LIBLINEAR.

[Go Top]

Q: How do I choose parameters for one-class svm as training data are in only one class?

You have pre-specified true positive rate in mind and then search for

parameters which achieve similar cross-validation accuracy.

[Go Top]

Q: Why the code gives NaN (not a number) results?

This rarely happens, but few users reported the problem.

It seems that their

computers for training libsvm have the VPN client

running. The VPN software has some bugs and causes this

problem. Please try to close or disconnect the VPN client.

[Go Top]

Q: Why on windows sometimes grid.py fails?

This problem shouldn't happen after version

2.85. If you are using earlier versions,

please download the latest one.

If you are using earlier

versions, the error message is probably

Traceback (most recent call last):

  File "grid.py", line 349, in ?

    main()

  File "grid.py", line 344, in main

    redraw(db)

  File "grid.py", line 132, in redraw

    gnuplot.write("set term windows\n")

IOError: [Errno 22] Invalid argument

Please try to close gnuplot windows and rerun.

If the problem still occurs, comment the following

two lines in grid.py by inserting "#" in the beginning:

        redraw(db)

        redraw(db,1)

Then you get accuracy only but not cross validation contours.

-->

[Go Top]

Q: Why grid.py/easy.py sometimes generates the following warning message?

Warning: empty z range [62.5:62.5], adjusting to [61.875:63.125]

Notice: cannot contour non grid data!

Nothing is wrong and please disregard the

message. It is from gnuplot when drawing

the contour.

[Go Top]

Q: Why the sign of predicted labels and decision values are sometimes reversed?

Nothing is wrong. Very likely you have two labels +1/-1 and the first instance in your data

has -1.

Think about the case of labels +5/+10. Since

SVM needs to use +1/-1, internally

we map +5/+10 to +1/-1 according to which

label appears first.

Hence a positive decision value implies

that we should predict the "internal" +1,

which may not be the +1 in the input file.

[Go Top]

Q: I don't know class labels of test data. What should I put in the first column of the test file?

Any value is ok. In this situation, what you will use is the output file of svm-predict, which gives predicted class labels.

[Go Top]

Q: How can I use OpenMP to parallelize LIBSVM on a multicore/shared-memory computer?

It is very easy if you are using GCC 4.2

or after.

 In Makefile, add -fopenmp  to CFLAGS.

 In class SVC_Q of svm.cpp, modify the for loop

of get_Q to:

#pragma omp parallel for private(j)

			for(j=start;j<len;j++)

 In the subroutine svm_predict_values of svm.cpp, add one line to the for loop:

#pragma omp parallel for private(i)

		for(i=0;i<l;i++)

			kvalue[i] = Kernel::k_function(x,model->SV[i],model->param);

For regression, you need a reduction clause for the variable sum:

#pragma omp parallel for private(i) reduction(+:sum)

		for(i=0;i<model->l;i++)

			sum += sv_coef[i] * Kernel::k_function(x,model>SV[i],model>param);

 Then rebuild the package. Kernel evaluations in training/testing will be parallelized. An example of running this modification on

an 8-core machine using the data set

ijcnn1:

 8 cores:

%setenv OMP_NUM_THREADS 8

%time svm-train -c 16 -g 4 -m 400 ijcnn1

27.1sec

1 core:

%setenv OMP_NUM_THREADS 1

%time svm-train -c 16 -g 4 -m 400 ijcnn1

79.8sec

For this data, kernel evaluations take 80% of training time. In the above example, we assume you use csh. For bash, use

export OMP_NUM_THREADS=8

instead.

 For Python interface, you need to add the -lgomp link option:

$(CXX) -lgomp -shared -dynamiclib svm.o -o libsvm.so.$(SHVER)

[Go Top]

Q: How could I know which training instances are support vectors?

It's very simple. Please replace

			if(nonzero[i]) model->SV[p++] = x[i];

in svm_train() of svm.cpp with

			if(nonzero[i])

			{

				model->SV[p++] = x[i];

				info("%d\n", perm[i]);

			}

If there are many requests, we may

provide a function to return indices

of support vectors. In the mean time,

if you need such information in your code,

you can add the array nonzero to the model

structure. This array has the same size as

the number of data, so alternatively you can

store only indices of support vectors.

 If you use matlab interface, you can easily

compare support vectors and training data to know

the indices:

[tmp index]=ismember(model.SVs, training_data,'rows');

[Go Top]

Q: Why training a probability model (i.e., -b 1) takes a longer time?

To construct this probability model, we internally conduct a

cross validation, which is more time consuming than

a regular training.

Hence, in general you do parameter selection first without

-b 1. You only use -b 1 when good parameters have been

selected. In other words, you avoid using -b 1 and -v

together.

[Go Top]

Q: Why using the -b option does not give me better accuracy?

There is absolutely no reason the probability outputs guarantee

you better accuracy. The main purpose of this option is

to provide you the probability estimates, but not to boost

prediction accuracy. From our experience,

after proper parameter selections, in general with

and without -b have similar accuracy. Occasionally there

are some differences.

It is not recommended to compare the two under

just a fixed parameter

set as more differences will be observed.

[Go Top]

Q: Why using svm-predict -b 0 and -b 1 gives different accuracy values?

Let's just consider two-class classification here. After probability information is obtained in training,

we do not have

prob > = 0.5 if and only if decision value >= 0.

So predictions may be different with -b 0 and 1.

[Go Top]

Q: How can I save images drawn by svm-toy?

For Microsoft windows, first press the "print screen" key on the keyboard.

Open "Microsoft Paint"

(included in Windows)

and press "ctrl-v." Then you can clip

the part of picture which you want.

For X windows, you can

use the program "xv" or "import" to grab the picture of the svm-toy window.

[Go Top]

Q: I press the "load" button to load data points but why svm-toy does not draw them ?

The program svm-toy assumes both attributes (i.e. x-axis and y-axis

values) are in (0,1). Hence you want to scale your

data to between a small positive number and

a number less than but very close to 1.

Moreover, class labels must be 1, 2, or 3

(not 1.0, 2.0 or anything else).

[Go Top]

Q: I would like svm-toy to handle more than three classes of data, what should I do ?

Taking windows/svm-toy.cpp as an example, you need to

modify it and  the difference

from the original file is as the following: (for five classes of

data)

30,32c30

 	RGB(200,0,200)

39c37

 HBRUSH brush1, brush2, brush3;

113,114d110

 	else return brush3;

325d318

 		svm_node *x_space = new svm_node[3 * prob.l];

333,338c326,331

x;

y;

 			x_space[3 * i].index = 1;

> 			x_space[3 * i].value = q->x;

> 			x_space[3 * i + 1].index = 2;

> 			x_space[3 * i + 1].value = q->y;

> 			x_space[3 * i + 2].index = -1;

> 			prob.x[i] = &x_space[3 * i];

397c390

 5) current_value = 1;

---

> 				if(current_value > 3) current_value = 1;

[Go Top]

Q: What is the difference between Java version and C++ version of libsvm?

They are the same thing. We just rewrote the C++ code

in Java.

[Go Top]

Q: Is the Java version significantly slower than the C++ version?

This depends on the VM you used. We have seen good

VM which leads the Java version to be quite competitive with

the C++ code. (though still slower)

[Go Top]

Q: While training I get the following error message: java.lang.OutOfMemoryError. What is wrong?

You should try to increase the maximum Java heap size.

For example,

java -Xmx2048m -classpath libsvm.jar svm_train ...

sets the maximum heap size to 2048M.

[Go Top]

Q: Why you have the main source file svm.m4 and then transform it to svm.java?

Unlike C, Java does not have a preprocessor built-in.

However,  we need some macros (see first 3 lines of svm.m4).

[Go Top]

Q: Except the python-C++ interface provided, could I use Jython to call libsvm ?

 Yes, here are some examples:

$ export CLASSPATH=$CLASSPATH:~/libsvm-2.91/java/libsvm.jar

$ ./jython

Jython 2.1a3 on java1.3.0 (JIT: jitc)

Type "copyright", "credits" or "license" for more information.

>>> from libsvm import *

>>> dir()

['__doc__', '__name__', 'svm', 'svm_model', 'svm_node', 'svm_parameter',

'svm_problem']

>>> x1 = [svm_node(index=1,value=1)]

>>> x2 = [svm_node(index=1,value=-1)]

>>> param = svm_parameter(svm_type=0,kernel_type=2,gamma=1,cache_size=40,eps=0.001,C=1,nr_weight=0,shrinking=1)

>>> prob = svm_problem(l=2,y=[1,-1],x=[x1,x2])

>>> model = svm.svm_train(prob,param)

*

optimization finished, #iter = 1

nu = 1.0

obj = -1.018315639346838, rho = 0.0

nSV = 2, nBSV = 2

Total nSV = 2

>>> svm.svm_predict(model,x1)

1.0

>>> svm.svm_predict(model,x2)

-1.0

>>> svm.svm_save_model("test.model",model)

[Go Top]

Q: I compile the MATLAB interface without problem, but why errors occur while running it?

Your compiler version may not be supported/compatible for MATLAB.

Please check this MATLAB page first and then specify the version

number. For example, if g++ X.Y is supported, replace

CXX = g++

in the Makefile with

CXX = g++-X.Y

[Go Top]

Q: On 64bit Windows I compile the MATLAB interface without problem, but why errors occur while running it?

Please make sure that you have modified make.m

to use -largeArrayDims option. For example,

mex -largeArrayDims -O -c svm.cpp

Moreover, if you use Microsoft Visual Studio,

probabally it is not properly installed.

See the explanation

here.

[Go Top]

Q: Does the MATLAB interface provide a function to do scaling?

It is extremely easy to do scaling under MATLAB.

The following one-line code scale each feature to the range

of [0.1]:

(data - repmat(min(data,[],1),size(data,1),1))*spdiags(1./(max(data,[],1)-min(data,[],1))',0,size(data,2),size(data,2))

[Go Top]

Q: How could I use MATLAB interface for parameter selection?

One can do this by a simple loop.

See the following example:

bestcv = 0;

for log2c = -1:3,

  for log2g = -4:1,

    cmd = ['-v 5 -c ', num2str(2^log2c), ' -g ', num2str(2^log2g)];

    cv = svmtrain(heart_scale_label, heart_scale_inst, cmd);

    if (cv >= bestcv),

      bestcv = cv; bestc = 2^log2c; bestg = 2^log2g;

    end

    fprintf('%g %g %g (best c=%g, g=%g, rate=%g)\n', log2c, log2g, cv, bestc, bestg, bestcv);

  end

end

You may adjust the parameter range in the above loops.

[Go Top]

Q: I use MATLAB parallel programming toolbox on a multi-core environment for parameter selection. Why the program is even slower?

Fabrizio Lacalandra of University of Pisa reported this issue.

It seems the problem is caused by the screen output.

If you disable the info function

using #if 0, then the problem

may be solved.

[Go Top]

Q: How do I use LIBSVM with OpenMP under MATLAB?

In Makefile,

you need to add -fopenmp to CFLAGS and -lgomp to MEX_OPTION. For Octave, you need the same modification.

 However, a minor problem is that

the number of threads cannot

be specified in MATLAB. We tried Version 7.7 (R2008b) and gcc-4.3.3.

% export OMP_NUM_THREADS=4; matlab

>> setenv('OMP_NUM_THREADS', '1');

Then OMP_NUM_THREADS is still 4 while running the program. Please contact us if you

see how to solve this problem.

[Go Top]

Q: How could I generate the primal variable w of linear SVM?

Let's start from the binary class and

assume you have two labels -1 and +1.

After obtaining the model from calling svmtrain,

do the following to have w and b:

w = model.SVs' * model.sv_coef;

b = -model.rho;

if model.Label(1) == -1

  w = -w;

  b = -b;

end

If you do regression or one-class SVM, then the if statement is not needed.

 For multi-class SVM, we illustrate the setting

in the following example of running the iris

data, which have 3 classes

> [y, x] = libsvmread('../../htdocs/libsvmtools/datasets/multiclass/iris.scale');

> m = svmtrain(y, x, '-t 0')

m =

    Parameters: [5x1 double]

      nr_class: 3

       totalSV: 42

           rho: [3x1 double]

         Label: [3x1 double]

         ProbA: []

         ProbB: []

           nSV: [3x1 double]

       sv_coef: [42x2 double]

           SVs: [42x4 double]

sv_coef is like:

+-+-+--------------------+

|1|1|                    |

|v|v|  SVs from class 1  |

|2|3|                    |

+-+-+--------------------+

|1|2|                    |

|v|v|  SVs from class 2  |

|2|3|                    |

+-+-+--------------------+

|1|2|                    |

|v|v|  SVs from class 3  |

|3|3|                    |

+-+-+--------------------+

so we need to see nSV of each classes.

> m.nSV

ans =

     3

    21

    18

Suppose the goal is to find the vector w of classes

1 vs 3. Then

y_i alpha_i of training 1 vs 3 are

> coef = [m.sv_coef(1:3,2); m.sv_coef(25:42,1)];

and SVs are:

> SVs = [m.SVs(1:3,:); m.SVs(25:42,:)];

Hence, w is

> w = SVs'*coef;

For rho,

> m.rho

ans =

    1.1465

    0.3682

   -1.9969

> b = -m.rho(2);

because rho is arranged by 1vs2 1vs3 2vs3.

[Go Top]

Q: Is there an OCTAVE interface for libsvm?

Yes, after libsvm 2.86, the matlab interface

works on OCTAVE as well. Please type

make octave

for installation.

[Go Top]

Q: How to handle the name conflict between svmtrain in the libsvm matlab interface and that in MATLAB bioinformatics toolbox?

The easiest way is to rename the svmtrain binary

file (e.g., svmtrain.mexw32 on 32-bit windows)

to a different

name (e.g., svmtrain2.mexw32).

[Go Top]

LIBSVM home page
