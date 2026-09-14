<!-- 第 1 页 -->

# l1 ls: A Matlab Solver for

# Large-Scale ℓ1-Regularized Least Squares Problems

### Kwangmoo Koh Seungjean Kim Stephen Boyd

### deneb1@stanford.edu sjkim@stanford.edu boyd@stanford.edu

### May 15, 2008

l1 ls solves ℓ1-regularized least squares problems (LSPs) using the truncated Newton
interior-point method described in [KKL+07].

## 1 The problems
l1 ls solves an optimization problem of the form
∥Ax −y∥2 + λ∥x∥1,
minimize (1)
where the variable is x ∈Rn and the problem data are A ∈Rm×n and y ∈Rm. Here,
λ ≥0 is the regularization parameter. We refer to the problem (1) as an ℓ1-regularized least
squares problem.
l1 ls can also solve ℓ1-regularized LSPs with nonnegativity constraints:
∥Ax −y∥2 + λ Pn
minimize i=1 xi
(2)
subject to xi ≥0, i = 1, . . . , n.

## 2 Calling sequences
The package l1 ls has two solver ﬁles, l1 ls.m and l1 ls nonneg.m: l1 ls.m solves prob-
lem (1) and l1 ls nonneg.m solves problem (2). Both solvers supports two calling styles.
The simple calling style works when A is given as a matrix. The more complex calling style
handles the case when A and its transpose are given as operators.
The simple calling sequence of l1 ls is
>> [x,status] = l1_ls(A,y,lambda,rel_tol,quiet);
The more complex calling sequence of l1 ls is
>> [x,status] = l1_ls(A,At,m,n,y,lambda,rel_tol,quiet);

<!-- 第 2 页 -->
In both cases, the last two arguments are optional. Input arguments represent the prob-
lem data of (1). Output arguments are the optimal point (up to the given tolerance) and its
status.
l1 ls nonneg.m has the same calling styles as l1 ls.m.

### 2.1 Input arguments
- A: data matrix with n columns and m rows. For the simple calling sequence, A is a
matrix in dense or sparse format. For the complex calling sequence, A is a Matlab
object with which we can evaluate A*z with a vector z in Rn by overloading the
multiplication operator.
- At: transpose of A. For the complex calling sequence, At is a Matlab object with which
we can evaluate At*w with a vector w in Rm by overloading the multiplication operator.
- m: number of observations.
- n: number of unknowns.
- y: vector of length m.
- lambda: regularization parameter.
- rel_tol: target relative tolerance, deﬁned as duality gap divided by the dual objective
value, which is an upper bound on the relative suboptimality.
- quiet: boolean. Suppresses print messages during execution if true. The default value
is false.

For the simple calling sequence, m and n are obtained internally from the size of A.

### 2.2 Output arguments
- x: n-vector. If status is ’Solved’, x is a solution (up to the given relative tolerance);
otherwise it is the last iterate of the truncated Newton interior-point method. (If
status is ’Failed’, x is the last value before the failure.)
- status: string; possible values are ‘Solved’ and ‘Failed’.

## 3 Hints and caveats
Here are some hints on using l1_ls.
- If your problem is large and sparse, be sure that A (and At, if you use the complex
calling style) are in sparse format.

<!-- 第 3 页 -->
- If A and At are dense but there are fast algorithms for the matrix-vector products
A*z and At*w, be sure that A and At are Matlab operators and the fast algorithms
are supported by overloading the multiplication operator *, using the object-oriented
programming of Matlab. For example, when A is a matrix formed by sampling m rows
of the discrete cosine transform (DCT) matrix F ∈Rn×n, A*z can be computed by
using the fast DCT algorithm, and At*w can be by using the fast inverse transform
algorithm.
Now, a caveat. The truncated Newton interior-point method can work poorly (i.e., be
slow) when the regularization parameter is too small (which corresponds to the case when
the solution x is not very sparse), and the mutual coherence of the data matrix A,
|ATi Aj|
µ = max
i̸=j ∥Ai∥∥Aj∥
where Ai is the ith column of A, is high (i.e., near 1). We recommend keeping λ/λmax greater
than 10−4 or so.

## 4 Utility functions
The utility function find_lambdamax_l1_ls.m computes λmax of ℓ1-regularized LSP (1). For
any larger value of λ, the optimal solution obtained from ℓ1-regularized least squares is zero.
The function find_lambdamax_l1_ls_nonneg.m computes λmax of ℓ1-regularized LSP with
nonnegativity constraints (2).

## 5 Examples

### 5.1 A small example for the simple calling sequence
We give a simple example to illustrate the usage of the simple calling sequence, with the
problem data
 1 0 0 0.5   1 
A =  0 1 0.2 0.3 , y =  0.2 .

# 0 0.1 1 0.2 1
The Matlab code for ﬁnding a point which is guaranteed to be no more 1%-suboptimal is
shown below.

>> % Matlab script for solving the simple problem given above.
>> A = [1 0 0 0.5;...\

# 0 1 0.2 0.3;...\

# 0 0.1 1 0.2];
>> x0 = [1 0 1 0]’; % original signal

<!-- 第 4 页 -->
>> y = A*x0; % measurements with no noise
>> lambda = 0.01; % regularization parameter
>> rel_tol = 0.01; % relative target duality gap

[x,status]=l1_ls(A,y,lambda,rel_tol);

After executing the code, you can see the result by typing x in Matlab.
>> x

x =

### 0.9930

### 0.0004

### 0.9941

### 0.0040

### 5.2 An example for the complex calling sequence
We give a simple example to illustrate the usage of the complex calling sequence that involves
the object-oriented programming feature of Matlab. We consider a sparse signal recovery
problem with a signal x ∈R1024 which consists of 10 spikes with amplitude ±1, shown at
the top plot of ﬁgure 1. Suppose we observe
y = Ax + v ∈R128
where v is drawn according to the Gaussian distribution N(0, 0.012I) on R128. Here, Ax gives
the discrete cosine transform of x at m = 128 frequencies, chosen from uniform distribution
over the indices 1, . . . , 1024.
The Matlab code for ﬁnding a point which is guaranteed to be no more than 1%-
suboptimal is shown below.

>> % Matlab script for solving the sparse signal recovery problem
>> % using the object-oriented programming feature of Matlab.
>> % The three m files in ./@partialDCT/ implement the partial DCT class
>> % with the multiplication and transpose operators overloaded.
>>
>> rand(’state’,0);randn(’state’,0); %initialize (for reproducibility)
>>
>> n = 1024; % signal dimension
>> m = 128; % number of measurements
>>
>> J = randperm(n); J = J(1:m); % m randomly chosen indices
>>

<!-- 第 5 页 -->
>> % generate the m*n partial DCT matrix whose m rows are
>> % the rows of the n*n DCT matrix at the indices specified by J
>> % see files at @partialDCT/
>> A = partialDCT(n,m,J); % A
>> At = A’; % transpose of A
>>
>> % spiky signal generation
>> T = 10; % number of spikes
>> x0 = zeros(n,1);
>> q = randperm(n);
>> x0(q(1:T)) = sign(randn(T,1));
>>
>> % noisy observations
>> sigma = 0.01; % noise standard deviation
>> y = A*x0 + sigma*randn(m,1);
>>
>> lambda = 0.01; % regularization parameter
>> rel_tol = 0.01; % relative target duality gap
>>
>> %run the l1-regularized least squares solver
>> [x,status]=l1_ls(A,At,m,n,y,lambda,rel_tol);

After executing the code, you can see the result by typing x in Matlab.
>> figure(1)
>> subplot(2,1,1); bar(x0); ylim([-1.1 1.1]); title(’original signal x0’);
>> subplot(2,1,2); bar(x); ylim([-1.1 1.1]); title(’reconstructed signal x’);
Figure 1 shows the result.

## References
[KKL+07] S.-J. Kim, K. Koh, M. Lustig, S. Boyd, and D. Gorinevsky. A method for large-
scale l1-regularized least squares. IEEE Journal on Selected Topics in Signal
Processing, 1(4):606–617, 2007.

<!-- 第 6 页 -->
original signal x0
1

### 0.5

0

−0.5

−1

# 0 200 400 600 800 1000 1200

reconstructed signal x
1

### 0.5

0

−0.5

−1

# 0 200 400 600 800 1000 1200

Figure 1: Reconstruction results. Original spike signal (Top). Reconstructed signal
via ℓ1-regularized least squares (Bottom).
