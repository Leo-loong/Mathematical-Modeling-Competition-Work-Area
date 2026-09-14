<!-- 第 1 页 -->

# ℓ1-magic : Recovery of Sparse Signals

# via Convex Programming

### Emmanuel Cand`es and Justin Romberg, Caltech

### October 2005

## 1 Seven problems

A recent series of papers [3–8] develops a theory of signal recovery from highly incomplete
information. The central results state that a sparse vector x0 ∈RN can be recovered from a
small number of linear measurements b = Ax0 ∈RK, K ≪N (or b = Ax0 + e when there is
measurement noise) by solving a convex program.
As a companion to these papers, this package includes MATLAB code that implements this
recovery procedure in the seven contexts described below. The code is not meant to be cutting-
edge, rather it is a proof-of-concept showing that these recovery procedures are computationally
tractable, even for large scale problems where the number of data points is in the millions.
The problems fall into two classes: those which can be recast as linear programs (LPs), and
those which can be recast as second-order cone programs (SOCPs). The LPs are solved using
a generic path-following primal-dual method. The SOCPs are solved with a generic log-barrier
algorithm. The implementations follow Chapter 11 of [2].
For maximum computational eﬃciency, the solvers for each of the seven problems are imple-
mented separately. They all have the same basic structure, however, with the computational
bottleneck being the calculation of the Newton step (this is discussed in detail below). The code
can be used in either “small scale” mode, where the system is constructed explicitly and solved
exactly, or in “large scale” mode, where an iterative matrix-free algorithm such as conjugate
gradients (CG) is used to approximately solve the system.
Our seven problems of interest are:

- Min-ℓ1 with equality constraints. The program
(P1) min ∥x∥1 subject to Ax = b,
also known as basis pursuit, ﬁnds the vector with smallest ℓ1 norm
∥x∥1 := X |xi|
i
that explains the observations b. As the results in [4, 6] show, if a suﬃciently sparse x0
exists such that Ax0 = b, then (P1) will ﬁnd it. When x, A, b have real-valued entries, (P1)
can be recast as an LP (this is discussed in detail in [10]).
- Minimum ℓ1 error approximation. Let A be a M × N matrix with full rank. Given
y ∈RM, the program
(PA) min ∥y −Ax∥1
x

<!-- 第 2 页 -->
ﬁnds the vector x ∈RN such that the error y −Ax has minimum ℓ1 norm (i.e. we are
asking that the diﬀerence between Ax and y be sparse). This program arises in the context
of channel coding [8].
Suppose we have a channel code that produces a codeword c = Ax for a message x. The
message travels over the channel, and has an unknown number of its entries corrupted.
The decoder observes y = c + e, where e is the corruption. If e is sparse enough, then the
decoder can use (PA) to recover x exactly. Again, (PA) can be recast as an LP.
- Min-ℓ1 with quadratic constraints. This program ﬁnds the vector with minimum ℓ1
norm that comes close to explaining the observations:
(P2) min ∥x∥1 subject to ∥Ax −b∥2 ≤ϵ,
where ϵ is a user speciﬁed parameter. As shown in [5], if a suﬃciently sparse x0 exists such
that b = Ax0 + e, for some small error term ∥e∥2 ≤ϵ, then the solution x⋆2 to (P2) will be
close to x0. That is, ∥x⋆2 −x0∥2 ≤C · ϵ, where C is a small constant. (P2) can be recast
as a SOCP.
- Min-ℓ1 with bounded residual correlation. Also referred to as the Dantzig Selector,
the program
(PD) min ∥x∥1 subject to ∥A∗(Ax −b)∥∞≤γ,
where γ is a user speciﬁed parameter, relaxes the equality constraints of (P1) in a diﬀerent
way. (PD) requires that the residual Ax −b of a candidate vector x not be too correlated
with any of the columns of A (the product A∗(Ax−b) measures each of these correlations).
If b = Ax0+e, where ei ∼N(0, σ2), then the solution x⋆D to (PD) has near-optimal minimax
risk:
E∥x⋆D −x0∥22 ≤C(log N) · X min(x0(i)2, σ2),
i
(see [7] for details). For real-valued x, A, b, (PD) can again be recast as an LP; in the
complex case, there is an equivalent SOCP.

It is also true that when x, A, b are complex, the programs (P1), (PA), (PD) can be written as
SOCPs, but we will not pursue this here.
If the underlying signal is a 2D image, an alternate recovery model is that the gradient is
sparse [18]. Let xij denote the pixel in the ith row and j column of an n×n image x, and deﬁne
the operators
(xi+1,j −xij i < n (xi,j+1 −xij j < n
Dh;ijx = Dv;ijx = j = n ,

# 0 i = n 0

and  Dh;ijx

Dijx = . (1)
Dv;ijx
The 2-vector Dijx can be interpreted as a kind of discrete gradient of the digital image x. The
total variation of x is simply the sum of the magnitudes of this discrete gradient at every point:
X q(Dh;ijx)2 + (Dv;ijx)2 = X
TV(x) := ∥Dijx∥2.
ij ij

With these deﬁnitions, we have three programs for image recovery, each of which can be recast
as a SOCP:

<!-- 第 3 页 -->
- Min-TV with equality constraints.
(TV1) min TV(x) subject to Ax = b
If there exists a piecewise constant x0 with suﬃciently few edges (i.e. Dijx0 is nonzero for
only a small number of indices ij), then (TV1) will recover x0 exactly — see [4].
- Min-TV with quadratic constraints.
(TV2) min TV(x) subject to ∥Ax −b∥2 ≤ϵ
Examples of recovering images from noisy observations using (TV2) were presented in [5].
Note that if A is the identity matrix, (TV2) reduces to the standard Rudin-Osher-Fatemi
image restoration problem [18]. See also [9,11–13] for SOCP solvers speciﬁcally designed
for the total-variational functional.
- Dantzig TV.
(TVD) min TV(x) subject to ∥A∗(Ax −b)∥∞≤γ
This program was used in one of the numerical experiments in [7].

In the next section, we describe how to solve linear and second-order cone programs using modern
interior point methods.

## 2 Interior point methods

Advances in interior point methods for convex optimization over the past 15 years, led by the
seminal work [14], have made large-scale solvers for the seven problems above feasible. Below we
overview the generic LP and SOCP solvers used in the ℓ1-magic package to solve these problems.

### 2.1 A primal-dual algorithm for linear programming

In Chapter 11 of [2], Boyd and Vandenberghe outline a relatively simple primal-dual algorithm
for linear programming which we have followed very closely for the implementation of (P1),(PA),
and (PD). For the sake of completeness, and to set up the notation, we brieﬂy review their
algorithm here.
The standard-form linear program is
min ⟨c0, z⟩ subject to A0z = b,
z
fi(z) ≤0,
where the search vector z ∈RN, b ∈RK, A0 is a K ×N matrix, and each of the fi, i = 1, . . . , m
is a linear functional:
fi(z) = ⟨ci, z⟩+ di,
for some ci ∈RN, di ∈R. At the optimal point z⋆, there will exist dual vectors ν⋆∈RK, λ⋆∈
Rm, λ⋆≥0 such that the Karush-Kuhn-Tucker conditions are satisﬁed:
(KKT) c0 + AT0 ν⋆+ X λ⋆i ci = 0,
i
λ⋆i fi(z⋆) = 0, i = 1, . . . , m,
A0z⋆= b,
fi(z⋆) ≤0, i = 1, . . . , m.

<!-- 第 4 页 -->
In a nutshell, the primal dual algorithm ﬁnds the optimal z⋆(along with optimal dual vectors
ν⋆and λ⋆) by solving this system of nonlinear equations. The solution procedure is the classical
Newton method: at an interior point (zk, νk, λk) (by which we mean fi(zk) < 0, λk > 0), the
system is linearized and solved. However, the step to new point (zk+1, νk+1, λk+1) must be
modiﬁed so that we remain in the interior.
In practice, we relax the complementary slackness condition λifi = 0 to
λki fi(zk) = −1/τ k, (2)
where we judiciously increase the parameter τ k as we progress through the Newton iterations.
This biases the solution of the linearized equations towards the interior, allowing a smooth, well-
deﬁned “central path” from an interior point to the solution on the boundary (see [15,20] for an
extended discussion).
The primal, dual, and central residuals quantify how close a point (z, ν, λ) is to satisfying (KKT)
with (2) in place of the slackness condition:
rdual = c0 + AT0 ν + X λici
i
rcent = −Λf −(1/τ)1
rpri = A0z −b,

fm(z)T .
where Λ is a diagonal matrix with (Λ)ii = λi, and f = f1(z) . . .
From a point (z, ν, λ), we want to ﬁnd a step (∆z, ∆ν, ∆λ) such that
rτ(z + ∆z, ν + ∆ν, λ + ∆λ) = 0. (3)
Linearizing (3) with the Taylor expansion around (z, ν, λ),
∆z
rτ(z + ∆z, ν + ∆ν, λ + ∆λ) ≈rτ(z, ν, λ) + Jrτ (z, νλ) ∆ν,

∆λ
where Jrτ (z, νλ) is the Jacobian of rτ, we have the system
 0 AT CT  ∆z c0 + AT0 ν + Pi λici
0
−ΛC 0 −F ∆v= − −Λf −(1/τ)1 ,

A0 0 0 ∆λ A0z −b
where m × N matrix C has the cTi as rows, and F is diagonal with (F)ii = fi(z). We can
eliminate ∆λ using:
∆λ = −ΛF −1C∆z −λ −(1/τ)f −1 (4)
leaving us with the core system
−CT F −1ΛC AT  ∆z −c0 + (1/τ)CT f −1 −AT

# 0 ν

# 0 = . (5)
A0 0 ∆ν b −A0z

With the (∆z, ∆ν, ∆λ) we have a step direction. To choose the step length 0 < s ≤1, we ask
that it satisfy two criteria:

1. z + s∆z and λ + s∆λ are in the interior, i.e. fi(z + s∆z) < 0, λi > 0 for all i.
2. The norm of the residuals has decreased suﬃciently:
∥rτ(z + s∆z, ν + s∆ν, λ + s∆λ)∥2 ≤(1 −αs) · ∥rτ(z, ν, λ)∥2,
where α is a user-spreciﬁed parameter (in all of our implementations, we have set α = 0.01).

<!-- 第 5 页 -->
Since the fi are linear functionals, item 1 is easily addressed. We choose the maximum step size
that just keeps us in the interior. Let
I+f = {i : ⟨ci, ∆z⟩> 0}, I−λ {i : ∆λ < 0},
and set
smax = 0.99 · min{1, {−fi(z)/⟨ci, ∆z⟩, i ∈I+f }, {−λi/∆λi, i ∈I−λ }}.
Then starting with s = smax, we check if item 2 above is satisﬁed; if not, we set s′ = β · s and
try again. We have taken β = 1/2 in all of our implementations.
When rdual and rpri are small, the surrogate duality gap η = −f T λ is an approximation to how
close a certain (z, ν, λ) is to being opitmal (i.e. ⟨c0, z⟩−⟨c0, z⋆⟩≈η). The primal-dual algorithm
repeats the Newton iterations described above until η has decreased below a given tolerance.
Almost all of the computational burden falls on solving (5). When the matrix −CT F −1ΛC is
easily invertible (as it is for (P1)), or there are no equality constraints (as in (PA), (PD)), (5)
can be reduced to a symmetric positive deﬁnite set of equations.
When N and K are large, forming the matrix and then solving the linear system of equations
in (5) is infeasible. However, if fast algorithms exist for applying C, CT and A0, AT

# 0 , we can use
a “matrix free” solver such as Conjugate Gradients. CG is iterative, requiring a few hundred
applications of the constraint matrices (roughly speaking) to get an accurate solution. A CG
solver (based on the very nice exposition in [19]) is included with the ℓ1-magic package.
The implementations of (P1), (PA), (PD) are nearly identical, save for the calculation of the
Newton step. In the Appendix, we derive the Newton step for each of these problems using
notation mirroring that used in the actual MATLAB code.

### 2.2 A log-barrier algorithm for SOCPs

Although primal-dual techniques exist for solving second-order cone programs (see [1,13]), their
implementation is not quite as straightforward as in the LP case. Instead, we have implemented
each of the SOCP recovery problems using a log-barrier method. The log-barrier method, for
which we will again closely follow the generic (but eﬀective) algorithm described in [2, Chap.
11], is conceptually more straightforward than the primal-dual method described above, but at
its core is again solving for a series of Newton steps.
Each of (P2), (TV1), (TV2), (TVD) can be written in the form
min ⟨c0, z⟩ subject to A0z = b
z
fi(z) ≤0, i = 1, . . . , m (6)
where each fi describes either a constraint which is linear
fi = ⟨ci, z⟩+ di
or second-order conic
fi(z) = 1
∥Aiz∥22 −(⟨ci, z⟩+ di)2
2
(the Ai are matrices, the ci are vectors, and the di are scalars).
The standard log-barrier method transforms (6) into a series of linearly constrained programs:
⟨c0, z⟩+ 1
min X −log(−fi(z)) subject to A0z = b, (7)
z τ k
i

<!-- 第 6 页 -->
where τ k > τ k−1. The inequality constraints have been incorporated into the functional via a
penalty function1 which is inﬁnite when the constraint is violated (or even met exactly), and
smooth elsewhere. As τ k gets large, the solution zk to (7) approaches the solution z⋆to (6): it
can be shown that ⟨c0, zk⟩−⟨c0, z⋆⟩< m/τ k, i.e. we are within m/τ k of the optimal value after
iteration k (m/τ k is called the duality gap). The idea here is that each of the smooth subproblems
can be solved to fairly high accuracy with just a few iterations of Newton’s method, especially
since we can use the solution zk as a starting point for subproblem k + 1.
At log-barrier iteration k, Newton’s method (which is again iterative) proceeds by forming a series
of quadratic approximations to (7), and minimizing each by solving a system of equations (again,
we might need to modify the step length to stay in the interior). The quadratic approximation
of the functional
f0(z) = ⟨c0, z⟩+ 1
X −log(−fi(z))
τ
i
in (7) around a point z is given by
f0(z + ∆z) ≈z + ⟨gz, ∆z⟩+ 1
2⟨Hz∆z, ∆z⟩:= q(z + ∆z),
where gz is the gradient
gz = c0 + 1 1
X −fi(z)∇fi(z)
τ
i
and Hz is the Hessian matrix
Hz = 1 fi(z)2 ∇fi(z)(∇fi(z))T + 11 1
X X −fi(z)∇2fi(z).
τ τ
i i
Given that z is feasible (that A0z = b, in particular), the ∆z that minimizes q(z + ∆z) subject
to A0z = b is the solution to the set of linear equations
Hz AT  ∆z
τ 0 = −τgz. (8)
A0 0 v
(The vector v, which can be interpreted as the Lagrange multipliers for the quality constraints
in the quadratic minimization problem, is not directly used.)
In all of the recovery problems below with the exception of (TV1), there are no equality con-
straints (A0 = 0). In these cases, the system (8) is symmetric positive deﬁnite, and thus can be
solved using CG when the problem is “large scale”. For the (TV1) problem, we use the SYMMLQ
algorithm (which is similar to CG, and works on symmetric but indeﬁnite systems, see [16]).
With ∆z in hand, we have the Newton step direction. The step length s ≤1 is chosen so that

1. fi(z + s∆z) < 0 for all i = 1, . . . , m,
2. The functional has decreased suﬃently:
f0(z + s∆z) < f0(z) + αs∆z⟨gz, ∆z⟩,
where α is a user-speciﬁed parameter (each of the implementations below uses α = 0.01).
This requirement basically states that the decrease must be within a certain percentage of
that predicted by the linear model at z.

As before, we start with s = 1, and decrease by multiples of β until both these conditions are
satisﬁed (all implementations use β = 1/2).
The complete log-barrier implementation for each problem follows the outline:
1The choice of −log(−x) for the barrier function is not arbitrary, it has a property (termed self-concordance)
that is very important for quick convergence of (7) to (6) both in theory and in practice (see the very nice
exposition in [17]).

<!-- 第 7 页 -->
1. Inputs: a feasible starting point z0, a tolerance η, and parameters µ and an initial τ 1. Set
k = 1.
2. Solve (7) via Newton’s method (followed by the backtracking line search), using zk−1 as
an initial point. Call the solution zk.

### 3. If m/τ k < η, terminate and return zk.

4. Else, set τ k+1 = µτ k, k = k + 1 and go to step 2.

In fact, we can calculate in advance how many iterations the log-barrier algorithm will need:
log m −log η −log τ 1
barrier iterations = .
log µ
The ﬁnal issue is the selection of τ 1. Our implementation chooses τ 1 conservatively; it is set so
that the duality gap m/τ 1 after the ﬁrst iteration is equal to ⟨c0, z0⟩.
In Appendix, we explicitly derive the equations for the Newton step for each of (P2), (TV1), (TV2), (TVD),
again using notation that mirrors the variable names in the code.

## 3 Examples

To illustrate how to use the code, the ℓ1-magic package includes m-ﬁles for solving speciﬁc
instances of each of the above problems (these end in “ example.m” in the main directory).

### 3.1 ℓ1 with equality constraints

We will begin by going through l1eq example.m in detail. This m-ﬁle creates a sparse signal,
takes a limited number of measurements of that signal, and recovers the signal exactly by solving
(P1). The ﬁrst part of the procedure is for the most part self-explainatory:

% put key subdirectories in path if not already there
path(path, ’./Optimization’);
path(path, ’./Data’);

% load random states for repeatable experiments
load RandomStates
rand(’state’, rand_state);
randn(’state’, randn_state);

% signal length
N = 512;
% number of spikes in the signal
T = 20;
% number of observations to make
K = 120;

% random +/- 1 signal
x = zeros(N,1);
q = randperm(N);
x(q(1:T)) = sign(randn(T,1));

<!-- 第 8 页 -->
We add the ’Optimization’ directory (where the interior point solvers reside) and the ’Data’
directories to the path. The ﬁle RandomStates.m contains two variables: rand state and
randn state, which we use to set the states of the random number generators on the next
two lines (we want this to be a “repeatable experiment”). The next few lines set up the prob-
lem: a length 512 signal that contains 20 spikes is created by choosing 20 locations at random
and then putting ±1 at these locations. The original signal is shown in Figure 1(a). The next
few lines:

% measurement matrix
disp(’Creating measurment matrix...’);
A = randn(K,N);
A = orth(A’)’;
disp(’Done.’);

% observations
y = A*x;

% initial guess = min energy
x0 = A’*y;

create a measurement ensemble by ﬁrst creating a K × N matrix with iid Gaussian entries,
and then orthogonalizing the rows. The measurements y are taken, and the “minimum energy”
solution x0 is calculated (x0, which is shown in Figure 1 is the vector in {x : Ax = y} that is
closest to the origin). Finally, we recover the signal with:

% solve the LP
tic
xp = l1eq_pd(x0, A, [], y, 1e-3);
toc

The function l1eq pd.m (found in the ’Optimization’ subdirectory) implements the primal-dual
algorithm presented in Section 2.1; we are sending it our initial guess x0 for the solution, the
measurement matrix (the third argument, which is used to specify the transpose of the measure-
ment matrix, is unnecessary here — and hence left empty — since we are providing A explicitly),
the measurements, and the precision to which we want the problem solved (l1eq pd will termi-
nate when the surrogate duality gap is below 10−3). Running the example ﬁle at the MATLAB
prompt, we have the following output:

>> l1eq_example
Creating measurment matrix...
Done.
Iteration = 1, tau = 1.921e+02, Primal = 5.272e+01, PDGap = 5.329e+01, Dual res = 9.898e+00, Primal res = 1.466e-14
H11p condition number = 1.122e-02
Iteration = 2, tau = 3.311e+02, Primal = 4.383e+01, PDGap = 3.093e+01, Dual res = 5.009e+00, Primal res = 7.432e-15
H11p condition number = 2.071e-02
Iteration = 3, tau = 5.271e+02, Primal = 3.690e+01, PDGap = 1.943e+01, Dual res = 2.862e+00, Primal res = 1.820e-14
H11p condition number = 2.574e-04
Iteration = 4, tau = 7.488e+02, Primal = 3.272e+01, PDGap = 1.368e+01, Dual res = 1.902e+00, Primal res = 1.524e-14
H11p condition number = 8.140e-05
Iteration = 5, tau = 9.731e+02, Primal = 2.999e+01, PDGap = 1.052e+01, Dual res = 1.409e+00, Primal res = 1.380e-14
H11p condition number = 5.671e-05
Iteration = 6, tau = 1.965e+03, Primal = 2.509e+01, PDGap = 5.210e+00, Dual res = 6.020e-01, Primal res = 4.071e-14
H11p condition number = 2.054e-05
Iteration = 7, tau = 1.583e+04, Primal = 2.064e+01, PDGap = 6.467e-01, Dual res = 6.020e-03, Primal res = 3.126e-13
H11p condition number = 1.333e-06
Iteration = 8, tau = 1.450e+05, Primal = 2.007e+01, PDGap = 7.062e-02, Dual res = 6.020e-05, Primal res = 4.711e-13
H11p condition number = 1.187e-07
Iteration = 9, tau = 1.330e+06, Primal = 2.001e+01, PDGap = 7.697e-03, Dual res = 6.020e-07, Primal res = 2.907e-12
H11p condition number = 3.130e-09
Iteration = 10, tau = 1.220e+07, Primal = 2.000e+01, PDGap = 8.390e-04, Dual res = 6.020e-09, Primal res = 1.947e-11
H11p condition number = 3.979e-11
Elapsed time is 0.141270 seconds.

The recovered signal xp is shown in Figure 1(c). The signal is recovered to fairly high accuracy:

>> norm(xp-x)

<!-- 第 9 页 -->

### 0.4

# 1 1

## 0.8 0.3 0.8

## 0.6 0.2 0.6

## 0.4 0.4

## 0.2 0.1 0.2

# 0 0 0
−0.2 −0.2
−0.1
−0.4 −0.4
−0.6 −0.2 −0.6
−0.8 −0.3 −0.8
−1 −1
0 50 100 150 200 250 300 350 400 450 500 −0.40 50 100 150 200 250 300 350 400 450 500 0 50 100 150 200 250 300 350 400 450 500
(a) Original (b) Minimum energy reconstruction (c) Recovered
Figure 1: 1D recovery experiment for ℓ1 minimization with equality constraints. (a) Original length
512 signal x consisting of 20 spikes. (b) Minimum energy (linear) reconstruction x0. (c) Minimum ℓ1
reconstruction xp.

ans =

### 8.9647e-05

### 3.2 Phantom reconstruction

A large scale example is given in tveq phantom example.m. This ﬁles recreates the phantom
reconstruction experiment ﬁrst published in [4]. The 256×256 Shepp-Logan phantom, shown in
Figure 2(a), is measured at K = 5481 locations in the 2D Fourier plane; the sampling pattern is
shown in Figure 2(b). The image is then reconstructed exactly using (TV1).
The star-shaped Fourier-domain sampling pattern is created with

% number of radial lines in the Fourier domain
L = 22;

% Fourier samples we are given
[M,Mh,mh,mhi] = LineMask(L,n);
OMEGA = mhi;

The auxiliary function LineMask.m (found in the ‘Measurements’ subdirectory) creates the star-
shaped pattern consisting of 22 lines through the origin. The vector OMEGA contains the locations
of the frequencies used in the sampling pattern.
This example diﬀers from the previous one in that the code operates in large-scale mode. The
measurement matrix in this example is 5481 × 65536, making the system (8) far too large to
solve (or even store) explicitly. (In fact, the measurment matrix itself would require almost 3
gigabytes of memory if stored in double precision.) Instead of creating the measurement matrix
explicitly, we provide function handles that take a vector x, and return Ax. As discussed above,
the Newton steps are solved for using an implicit algorithm.
To create the implicit matrix, we use the function handles

A = @(z) A_fhp(z, OMEGA);
At = @(z) At_fhp(z, OMEGA, n);

<!-- 第 10 页 -->
(a) Phantom (b) Sampling pattern (c) Min energy (d) min-TV reconstruction
Figure 2: Phantom recovery experiment.

The function A fhp.m takes a length N vector (we treat n × n images as N := n2 vectors), and
returns samples on the K frequencies. (Actually, since the underlying image is real, A fhp.m
return the real and imaginary parts of the 2D FFT on the upper half-plane of the domain shown
in Figure 2(b).)
To solve (TV1), we call

xp = tveq_logbarrier(xbp, A, At, y, 1e-1, 2, 1e-8, 600);

The variable xbp is the initial guess (which is again the minimal energy reconstruction shown
in Figure 2(c)), y are the measurements, and1e-1 is the desired precision. The sixth input is
the value of µ (the amount by which to increase τ k at each iteration; see Section 2.2). The last
two inputs are parameters for the large-scale solver used to ﬁnd the Newton step. The solvers
are iterative, with each iteration requiring one application of A and one application of At. The
seventh and eighth arguments above state that we want the solver to iterate until the solution
has precision 10−8 (that is, it ﬁnds a z such that ∥Hz −g∥2/∥g∥2 ≤10−8), or it has reached 600
iterations.
The recovered phantom is shown in Figure 2(d). We have ∥XT V −X∥2/∥X∥2 ≈8 · 10−3.

### 3.3 Optimization routines

We include a brief description of each of the main optimization routines (type help <function>
in MATLAB for details). Each of these m-ﬁles is found in the Optimization subdirectory.

<!-- 第 11 页 -->
Solves Ax = b, where A is symmetric positive deﬁnite, using the
cgsolve Conjugate Gradient method.
l1dantzig pd Solves (PD) (the Dantzig selector) using a primal-dual algorithm.
Solves the norm approximation problem (PA) (for decoding via
l1decode pd linear programming) using a primal-dual algorithm.
Solves the standard Basis Pursuit problem (P1) using a primal-dual
l1eq pd algorithm.
Barrier (“outer”) iterations for solving quadratically constrained
l1qc logbarrier ℓ1 minimization (P2).
Newton (“inner”) iterations for solving quadratically constrained
l1qc newton ℓ1 minimization (P2).
tvdantzig logbarrier Barrier iterations for solving the TV Dantzig selector (TVD).
tvdantzig newton Newton iterations for (TVD).
tveq logbarrier Barrier iterations for equality constrained TV minimizaiton (TV1).
tveq newton Newton iterations for (TV1).
Barrier iterations for quadratically constrained TV minimization
tvqc logbarrier (TV2).
tvqc newton Newton iterations for (TV2).

## 4 Error messages

Here we brieﬂy discuss each of the error messages that the ℓ1-magic may produce.

- Matrix ill-conditioned. Returning previous iterate. This error can occur when
the code is running in small-scale mode; that is, the matrix A is provided explicitly. The
error message is produced when the condition number of the linear system we need to solve
to ﬁnd the step direction (i.e. (5) for the linear programs, and (8) for the SOCPs) has an
estimated condition number of less than 10−14.
This error most commonly occurs during the last iterations of the primal-dual or log-barrier
algorithms. While it means that the solution is not within the tolerance speciﬁed (by the
primal-dual gap), in practice it is usually pretty close.
- Cannot solve system. Returning previous iterate. This error is the large-scale
analog to the above. The error message is produced when the residual produced by the
conjugate gradients algorithm was above 1/2; essentially this means that CG has not solved
the system in any meaningful way. Again, this error typically occurs in the late stages of
the optimization algorithm, and is a symptom of the system being ill-conditioned.
- Stuck backtracking, returning last iterate. This error occurs when the algorithm,
after computing the step direction, cannot ﬁnd a step size small enough that decreases the
objective. It is generally occurs in large-scale mode, and is a symptom of CG not solving
for the step direction to suﬃcient precision (if the system is solved perfectly, a small enough
step size will always be found). Again, this will typically occur in the late stages of the
optimization algorithm.
- Starting point infeasible; using x0 = At*inv(AAt)*y. Each of the optimization
programs expects an initial guess which is feasible (obeys the constraints). If the x0
provided is not, this message is produced, and the algorithm proceeds using the least-
squares starting point x0 = AT (AAT )−1b.

<!-- 第 12 页 -->

## Appendix

## A ℓ1 minimization with equality constraints

When x, A and b are real, then (P1) can be recast as the linear program
min X ui subject to xi −ui ≤0
x,u
i −xi −ui ≤0,
Ax = b
which can be solved using the standard primal-dual algorithm outlined in Section 2.1 (again,
see [2, Chap.11] for a full discussion). Set
fu1;i := xi −ui
fu2;i := −xi −ui,
with λu1;i, λu2;i the corresponding dual variables, and let fu1 be the vector (fu1;1 . . . fu1;N)T
(and likewise for fu2, λu1, λu2). Note that
 δi
 −δi
∇fu1;i = , ∇fu2;i = , ∇2fu1;i = 0, ∇2fu2;i = 0,
−δi −δi
where δi is the standard basis vector for component i. Thus at a point (x, u; v, λu1, λu2), the
central and dual residuals are
−Λu1fu1
rcent = −(1/τ)1,
−Λu2fu2
λu1 −λu2 + AT v
rdual = ,

# 1 −λu1 −λu2
and the Newton step (5) is given by:
 AT      (−1/τ) · (−f −1u1 + f −1u2 ) −AT v
Σ1 Σ2 ∆x w1
Σ2 Σ1 0 ∆u= w2:= −1 −(1/τ) · (f −1u1 + f −1u2 ) ,

A 0 0 ∆v w3 b −Ax
with
Σ1 = Λu1F −1u1 −Λu2F −1u2 , Σ2 = Λu1F −1u1 + Λu2F −1u2 ,
(The F•, for example, are diagonal matrices with (F•)ii = f•;i, and f −1•;i = 1/f•;i.) Setting
Σx = Σ1 −Σ22Σ−11 ,
we can eliminate
Σ−1x (w1 −Σ2Σ−11 w2 −AT ∆v)
∆x =
∆u = Σ−11 (w2 −Σ2∆x),
and solve
−AΣ−11 AT ∆v = w3 −A(Σ−1x w1 −Σ−1x Σ2Σ−1

# 1 w2).
This is a K×K positive deﬁnite system of equations, and can be solved using conjugate gradients.
Given ∆x, ∆u, ∆v, we calculate the change in the inequality dual variables as in (4):
∆λu1 = Λu1F −1u1 (−∆x + ∆u) −λu1 −(1/τ)f −1
u1
∆λu2 = Λu2F −1u2 (∆x + ∆u) −λu2 −(1/τ)f −1u2 .

<!-- 第 13 页 -->

## B ℓ1 norm approximation

The ℓ1 norm approximation problem (PA) can also be recast as a linear program:
M
min X um subject to Ax −u −y ≤0
x,u
m=1 −Ax −u + y ≤0,
(recall that unlike the other 6 problems, here the M ×N matrix A has more rows than columns).
For the primal-dual algorithm, we deﬁne
fu1 = Ax −u −y, fu2 = −Ax −u + y.
Given a vector of weights σ ∈RM,
AT σ −AT σ
X σm∇fu1;m = , X σm∇fu2;m = ,
−σ −σ
m m
AT ΣA −AT Σ AT ΣA AT Σ
X σm∇fu1;m∇f Tu1;m = , X σm∇fu2;m∇f Tu2;m = .
−ΣA Σ ΣA Σ
m m
At a point (x, u; λu1, λu2), the dual residual is
AT (λu1 −λu2)
rdual = ,
−λu1 −λu2
and the Newton step is the solution to
AT Σ11A AT Σ12 ∆x −(1/τ) · AT (−f −1u1 + f −1  w1
u2 )
= :=
Σ12A Σ11 ∆u −1 −(1/τ) · (f −1u1 + f −1u2 ) w2
where
Σ11 = −Λu1F −1u1 −Λu2F −1
u2
Σ12 = Λu1F −1u1 −Λu2F −1u2 .
Setting
Σx = Σ11 −Σ212Σ−111 ,
we can eliminate ∆u = Σ−111 (w2 −Σ22A∆x), and solve
AT ΣxA∆x = w1 −AT Σ22Σ−1

# 11 w2
for ∆x. Again, AT ΣxA is a N × N symmetric positive deﬁnite matrix (it is straightforward to
verify that each element on the diagonal of Σx will be strictly positive), and so the Conjugate
Gradients algorithm can be used for large-scale problems.
Given ∆x, ∆u, the step directions for the inequality dual variables are given by
∆λu1 = −Λu1F −1u1 (A∆x −∆u) −λu1 −(1/τ)f −1
u1
∆λu2 = Λu2F −1u2 (A∆x + ∆u) −λu2 −(1/τ)f −1u2 .

## C ℓ1 Dantzig selection

An equivalent linear program to (PD) in the real case is given by:
min X ui subject to x −u ≤0,
x,u
i −x −u ≤0,
AT r −ϵ ≤0,
−AT r −ϵ ≤0,

<!-- 第 14 页 -->
where r = Ax −b. Taking
fϵ1 = AT r −ϵ, fϵ2 = −AT r −ϵ,
fu1 = x −u, fu2 = −x −u,
the residuals at a point (x, u; λu1, λu2, λϵ1, λϵ2), the dual residual is
λu1 −λu2 + AT A(λϵ1 −λϵ2)
rdual = ,

# 1 −λu1 −λu2
and the Newton step is the solution to
AT AΣaAT A + Σ11  ∆x −(1/τ) · (AT A(−f −1ϵ1 + f −1ϵ2 )) −f −1u1 + f −1 w1
Σ12
= u2 :=
Σ12 Σ11 ∆u −1 −(1/τ) · (f −1u1 + f −1u2 ) w2
where
Σ11 = −Λu1F −1u1 −Λu2F −1
u2
Σ12 = Λu1F −1u1 −Λu2F −1
u2
Σa = −Λϵ1F −1ϵ1 −Λϵ2F −1ϵ2 .
Again setting
Σx = Σ11 −Σ212Σ−111 ,
we can eliminate
∆u = Σ−111 (w2 −Σ12∆x),
and solve
(AT AΣaAT A + Σx)∆x = w1 −Σ12Σ−1

# 11 w2
for ∆x. As before, the system is symmetric positive deﬁnite, and the CG algorithm can be used
to solve it.
Given ∆x, ∆u, the step directions for the inequality dual variables are given by
∆λu1 = −Λu1F −1u1 (∆x −∆u) −λu1 −(1/τ)f −1
u1
∆λu2 = −Λu2F −1u2 (−∆x −∆u) −λu2 −(1/τ)f −1
u2
−Λϵ1F −1ϵ1 (AT A∆x) −λϵ1 −(1/τ)f −1
∆λϵ1 =
ϵ1
−Λϵ2F −1ϵ2 (−AT A∆x) −λϵ2 −(1/τ)f −1
∆λϵ2 = ϵ2 .

## D ℓ1 minimization with quadratic constraints

The quadractically constrained ℓ1 minimization problem (P2) can be recast as the second-order
cone program
min X ui subject to x −u ≤0,
x,u
i −x −u ≤0,
1
∥Ax −b∥22 −ϵ2 ≤0.
2
Taking
fϵ = 1
fu1 = x −u, fu2 = −x −u, ∥Ax −b∥22 −ϵ2 ,
we can write the Newton step (as in (8)) at a point (x, u) for a given τ as
Σ11 −f −1AT A + f −2AT rrT A  ∆x f −1u1 −f −1u2 + f −1AT r w1
Σ12
ϵ ϵ = ϵ :=
Σ12 Σ11 ∆u −τ1 −f −1u1 −f −1 w2
u2

<!-- 第 15 页 -->
where r = Ax −b, and
Σ11 = F −2u1 + F −2
u2
Σ12 = −F −2u1 + F −2u2 .
As before, we set
Σx = Σ11 −Σ212Σ−1
11
and eliminate ∆u
∆u = Σ−111 (w2 −Σ12∆x),
leaving us with the reduced system
(Σx −f −1AT A + f −2AT rrT A)∆x = w1 −Σ12Σ−1

# 11 w2
ϵ ϵ
which is symmetric positive deﬁnite and can be solved using CG.

## E Total variation minimization with equality constraints

The equality constrained TV minimization problem
min TV(x) subject to Ax = b,
x
can be rewritten as the SOCP
min X tij s.t. ∥Dijx∥2 ≤tij
t,x
ij
Ax = b.
Deﬁning the inequality functions
ftij = 1
∥Dij∥22 −t2  i, j = 1, . . . , n (9)

# 2 ij
we have  DT
ijDijx
∇ftij =
−tijδij
DTijDijxxT DT −tijDTijDijxδT  D∗
ijDij ijDij 0
∇ftij∇f Ttij = ij , ∇2ftij = ,
−tijδijxT DT t2ijδijδT −δijδT
ijDij 0
ij ij
where δij is the Kronecker vector that is 1 in entry ij and zero elsewhere. For future reference:
DTh ΣDhx + DTv ΣDvx
X σij∇ftij = ,
−σt
ij
 BΣBT −BTΣ
X σij∇ftij∇f Ttij = ,
−ΣTBT ΣT 2
ij
 DTh ΣDh + DTv ΣDv 0
X σij∇2ftij =

# 0 −Σ
ij
where Σ = diag({σij}), T = diag(t), Dh has the Dh;ij as rows (and likewise for Dv), and B is a
matrix that depends on x:
B = DTh Σ∂h + DTv Σ∂v.
with Σ∂h = diag(Dhx), Σ∂v = diag(Dvx).

<!-- 第 16 页 -->
The Newton system (8) for the log-barrier algorithm is then
 H11 BΣ12 AT  ∆x DTh F −1Dhx + DTv F −1Dvx w1
t t
Σ12BT Σ22 0 ∆t= −τ1 −F −1t := w2,
    t
A 0 0 ∆v 0 0
where
H11 = DTh (−F −1)Dh + DTv (−F −1)Dv + BF −2BT .
t t t
Eliminating ∆t
Σ−122 (w2 −Σ12BT ∆x)
∆t =
= Σ−122 (w2 −Σ12Σ∂hDh∆x −Σ12Σ∂vDv∆x),
the reduced (N + K) × (N + K) system is
H′ AT  ∆x w′

# 11 = 1 (10)
A 0 ∆v 0
with
H′11 = H11 −BΣ212Σ−122 BT
= DTh (ΣbΣ2∂h −F −1)Dh + DTv (ΣbΣ2∂v −F −1)Dv +
t t
DTh (ΣbΣ∂hΣ∂v)Dv + DTv (ΣbΣ∂hΣ∂v)Dh
w′1 = w1 −BΣ12Σ−122 w2
= w1 −(DTh Σ∂h + DTv Σ∂v)Σ12Σ−122 w2
Σb = F −2 −Σ−122 Σ212.
t

The system of equations (10) is symmetric, but not positive deﬁnite. Note that Dh and Dv are
(very) sparse matrices, and hence can be stored and applied very eﬃciently. This allows us to
again solve the system above using an iterative method such as SYMMLQ [16].

## F Total variation minimization with quadratic constraints

We can rewrite (TV2) as the SOCP
min X tij subject to ∥Dijx∥2 ≤tij, i, j = 1, . . . , n
x,t
ij ∥Ax −b∥2 ≤ϵ
where Dij is as in (1). Taking ftij as in (9) and
fϵ = 1
∥Ax −b∥22 −ϵ2 ,
2
with
AT r AT rrT A  A∗A

# 0 0
∇fϵ = , ∇fϵ∇f Tϵ = , ∇2fϵ =

# 0 0 0 0 0
where r = Ax −b.
Also,
 D∗  A∗A
ijDij 0  0
∇2ftij = ∇2fϵ = .

# 0 −δijδT 0 0
ij

<!-- 第 17 页 -->
The Newton system is similar to that in equality constraints case:
 H11
 ∆x DTh F −1Dhx + DTv F −1Dvx + f −1AT r w1
BΣ12
= t t ϵ := .
Σ12BT Σ22 ∆t −τ1 −tf −1 w2
t
where (tf −1)ij = tij/ftij, and
t
H11 = DTh (−F −1)Dh + DTv (−F −1)Dv + BF −2BT −
t t t
f −1AT A + f −2AT rrT A,
ϵ ϵ
Σ12 = −TF −2,
t
Σ22 = F −1 + F −2T 2,
t t
Again eliminating ∆t
∆t = Σ−122 (w2 −Σ12Σ∂hDh∆x −Σ12Σ∂vDv∆x),
the key system is
H′11∆x = w1 −(DTh Σ∂h + DTv Σ∂v)Σ12Σ−122 w2
where
H′11 = H11 −BΣ212Σ−122 BT
= DTh (ΣbΣ2∂h −F −1)Dh + DTv (ΣbΣ2∂v −F −1)Dv +
t t
DTh (ΣbΣ∂hΣ∂v)Dv + DTv (ΣbΣ∂hΣ∂v)Dh −
f −1AT A + f −2AT rrT A,
ϵ ϵ
Σb = F −2 −Σ212Σ−122 .
t

The system above is symmetric positive deﬁnite, and can be solved with CG.

## G Total variation minimization with bounded residual cor-

## relation

The TV Dantzig problem has an equivalent SOCP as well:
min X tij subject to ∥Dijx∥2 ≤tij, i, j = 1, . . . , n
x,t AT (Ax −b) −ϵ ≤0
ij
−AT (Ax −b) −ϵ ≤0.
The inequality constraint functions are
1
ftij = ∥Dijx∥22 −t2  i, j = 1, . . . , n

# 2 ij
AT (Ax −b) −ϵ,
fϵ1 =
−AT (Ax −b) −ϵ,
fϵ2 =
with
AT Aσ −AT Aσ
X σij∇fϵ1;ij = , X σij∇fϵ2;ij = ,

# 0 0
ij ij
and
AT AΣAT A
X σij∇fϵ1;ij∇f Tϵ1;ij = X σij∇fϵ2;ij∇f Tϵ2;ij = .

# 0 0
ij ij

<!-- 第 18 页 -->
Thus the log barrier Newton system is nearly the same as in the quadratically constrained case:
 H11
   DTh F −1Dhx + DTv F −1Dvx + AT A(f −1ϵ1 −f −1
BΣ12 ∆x ϵ2 ) w1
= t t := .
Σ12BT Σ22 ∆t −τ1 −tf −1 w2
t
where
H11 = DTh (−F −1)Dh + DTv (−F −1)Dv + BF −2BT + AT AΣaAT A,
t t t
Σ12 = −TF −2,
t
Σ22 = F −1 + F −2T 2,
t t
Σa = F −2ϵ1 + F −2ϵ2 .
Eliminating ∆t as before
∆t = Σ−122 (w2 −Σ12Σ∂hDh∆x −Σ12Σ∂vDv∆x),
the key system is
H′11∆x = w1 −(DTh Σ∂h + DTv Σ∂v)Σ12Σ−122 w2
where
H′11 = DTh (ΣbΣ2∂h −F −1)Dh + DTv (ΣbΣ2∂v −F −1)Dv +
t t
DTh (ΣbΣ∂hΣ∂v)Dv + DTv (ΣbΣ∂hΣ∂v)Dh + AT AΣaAT A,
Σb = F −2 −Σ212Σ−122 .
t

## References

[1] F. Alizadeh and D. Goldfarb. Second-order cone programming. Math. Program., Ser. B,
95:3–51, 2003.
[2] S. Boyd and L. Vandenberghe. Convex Optimization. Cambridge University Press, 2004.
[3] E. Cand`es and J. Romberg. Quantitative robust uncertainty principles and optimally sparse
decompositions. To appear in Foundations of Comput. Math., 2005.
[4] E. Cand`es, J. Romberg, and T. Tao. Robust uncertainty principles: Exact signal recon-
struction from highly incomplete frequency information. Submitted to IEEE Trans. Inform.
Theory, June 2004. Available on theArXiV preprint server: math.GM/0409186.
[5] E. Cand`es, J. Romberg, and T. Tao. Stable signal recovery from incomplete and inaccurate
measurements. Submitted to Communications on Pure and Applied Mathematics, March
2005.
[6] E. Cand`es and T. Tao. Near-optimal signal recovery from random projections and universal
encoding strategies. submitted to IEEE Trans. Inform. Theory, November 2004. Available
on the ArXiV preprint server: math.CA/0410542.
[7] E. Cand`es and T. Tao. The Dantzig selector: statistical estimation when p is much smaller
than n. Manuscript, May 2005.
[8] E. J. Cand`es and T. Tao. Decoding by linear programming. To appear in IEEE Trans.
Inform. Theory, December 2005.

<!-- 第 19 页 -->
[9] T. Chan, G. Golub, and P. Mulet. A nonlinear primal-dual method for total variation-based
image restoration. SIAM J. Sci. Comput., 20:1964–1977, 1999.
[10] S. S. Chen, D. L. Donoho, and M. A. Saunders. Atomic decomposition by basis pursuit.
SIAM J. Sci. Comput., 20:33–61, 1999.
[11] D. Goldfarb and W. Yin. Second-order cone programming methods for total variation-based
image restoration. Technical report, Columbia University, 2004.
[12] H. Hinterm¨uller and G. Stadler. An infeasible primal-dual algorithm for TV-based inf-
convolution-type image restoration. To appear in SIAM J. Sci. Comput., 2005.
[13] M. Lobo, L. Vanderberghe, S. Boyd, and H. Lebret. Applications of second-order cone
programming. Linear Algebra and its Applications, 284:193–228, 1998.
[14] Y. E. Nesterov and A. S. Nemirovski. Interior Point Polynomial Methods in Convex Pro-
gramming. SIAM Publications, Philadelphia, 1994.
[15] J. Nocedal and S. J. Wright. Numerical Optimization. Springer, New York, 1999.
[16] C. C. Paige and M. Saunders. Solution of sparse indeﬁnite systems of linear equations.
SIAM J. Numer. Anal., 12(4), September 1975.
[17] J. Renegar. A mathematical view of interior-point methods in convex optimization. MPS-
SIAM Series on Optimization. SIAM, 2001.
[18] L. I. Rudin, S. Osher, and E. Fatemi. Nonlinear total variation noise removal algorithm.
Physica D, 60:259–68, 1992.
[19] J. R. Shewchuk. An introduction to the conjugate gradient method without the agonizing
pain. Manuscript, August 1994.
[20] S. J. Wright. Primal-Dual Interior-Point Methods. SIAM Publications, 1997.
