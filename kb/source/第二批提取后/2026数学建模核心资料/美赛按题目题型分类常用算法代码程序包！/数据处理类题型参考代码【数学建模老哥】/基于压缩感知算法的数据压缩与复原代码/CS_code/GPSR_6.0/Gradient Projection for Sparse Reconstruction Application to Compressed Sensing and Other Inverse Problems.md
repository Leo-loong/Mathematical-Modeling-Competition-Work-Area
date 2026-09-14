<!-- 第 1 页 -->
TO APPEAR IN THE IEEE JOURNAL OF SELECTED TOPICS IN SIGNAL PROCESSING, 2007. 1

# Gradient Projection for Sparse Reconstruction:

# Application to Compressed Sensing and Other

# Inverse Problems

## M´ario A. T. Figueiredo, Robert D. Nowak, Stephen J. Wright

Abstract—Many problems in signal processing and statistical technique to overcome the ill-conditioned, or even singular,
inference involve ﬁnding sparse solutions to under-determined, nature of matrix A, when trying to infer x from noiseless
or ill-conditioned, linear systems of equations. A standard observations y = Ax or from noisy observations as in (2).
approach consists in minimizing an objective function which
includes a quadratic (squared ℓ2) error term combined with The presence of the ℓ1 term encourages small components
a sparseness-inducing (ℓ1) regularization term.Basis pursuit, the of x to become exactly zero, thus promoting sparse solutions
least absolute shrinkage and selection operator (LASSO), wavelet- [11], [54]. Because of this feature, (1) has been used for
based deconvolution, and compressed sensing are a few well- more than three decades in several signal processing problems
known examples of this approach. This paper proposes gradient
where sparseness is sought; some early references are [12],
projection (GP) algorithms for the bound-constrained quadratic
[37], [50], [53]. In the 1990’s, seminal work on the use of
programming (BCQP) formulation of these problems. We test
variants of this approach that select the line search parameters ℓ1 sparseness-inducing penalties/log-priors appeared in the
in different ways, including techniques based on the Barzilai- literature: the now famous basis pursuit denoising (BPDN,
Borwein method. Computational experiments show that these GP [11, Section 5]) criterion and the least absolute shrinkage and
approaches perform well in a wide range of applications, often
selection operator (LASSO, [54]). For brief historical accounts
being signiﬁcantly faster (in terms of computation time) than
on the use of the ℓ1 penalty in statistics and signal processing,
competing methods. Although the performance of GP methods
tends to degrade as the regularization term is de-emphasized, see [41], [55].
we show how they can be embedded in a continuation scheme Problem (1) is closely related to the following convex
to recover their efﬁcient practical performance. constrained optimization problems:
minx ∥x∥1 subject to ∥y −Ax∥22 ≤ε (3)
I. INTRODUCTION
A. Background and
There has been considerable interest in solving the convex minx ∥y −Ax∥2 subject to ∥x∥1 ≤t, (4)
2
unconstrained optimization problem
where ε and t are nonnegative real parameters. Problem (3) is
1
min 2∥y −Ax∥22 + τ∥x∥1, (1) a quadratically constrained linear program (QCLP) whereas
x
(4) is a quadratic program (QP). Convex analysis can be used
where x ∈Rn, y ∈Rk, A is an k × n matrix, τ is a to show that a solution of (3) (for any ε such that this problem
nonnegative parameter, ∥v∥2 denotes the Euclidean norm of is feasible) is either x = 0, or else is a minimizer of (1), for
v, and ∥v∥1 = Pi |vi| is the ℓ1 norm of v. Problems of the some τ > 0. Similarly, a solution of (4) for any t ≥0 is also a
form (1) have become familiar over the past three decades, minimizer of (1) for some τ ≥0. These claims can be proved
particularly in statistical and signal processing contexts. From using [49, Theorem 27.4].
a Bayesian perspective, (1) can be seen as a maximum a The LASSO approach to regression has the form (4), while
posteriori criterion for estimating x from observations the basis pursuit criterion [11, (3.1)] has the form (3) with
ε = 0, i.e., a linear program (LP)
y = Ax + n, (2)
where n is white Gaussian noise of variance σ2, and the prior minx ∥x∥1 subject to y = Ax. (5)
on x is Laplacian (that is, log p(x) = −λ∥x∥1 + K) [1],
Problem (1) also arises in wavelet-based image/signal re-
[25], [54]. Problem (1) can also be viewed as a regularization
construction and restoration (namely deconvolution); in those
M. Figueiredo is with the Instituto de Telecomunicac¸ ˜oes and Department problems, matrix A has the form A = RW, where R is (a ma-
of Electrical and Computer Engineering, Instituto Superior T´ecnico, 1049- trix representation of) the observation operator (for example,
001 Lisboa, Portugal. R. Nowak is with the Department of Electrical and
convolution with a blur kernel or a tomographic projection),
Computer Engineering, University of Wisconsin, Madison, WI 53706, USA.
S. Wright is with Department of Computer Sciences, University of Wisconsin, W contains a wavelet basis or a redundant dictionary (that
Madison, WI 53706, USA. is, multiplying by W corresponds to performing an inverse
This work was partially supported by NSF, grants CCF-0430504 and CNS-
wavelet transform), and x is the vector of representation
0540147, and by Fundac¸˜ao para a Ciˆencia e Tecnologia, POSC/FEDER, grant
POSC/EEA-CPS/61271/2004. coefﬁcients of the unknown image/signal [24], [25], [26].

<!-- 第 2 页 -->
TO APPEAR IN THE IEEE JOURNAL OF SELECTED TOPICS IN SIGNAL PROCESSING, 2007. 2

We mention also image restoration problems under to- The method in [39] provides the solution path for (1), for
tal variation (TV) regularization [10], [47]. In the one- a range of values of τ. The least angle regression (LARS)
dimensional (1D) case, a change of variables leads to the procedure described in [22] can be adapted to solve the
formulation (1). In 2D, however, the techniques of this paper LASSO formulation (4). These are all essentially homotopy
cannot be applied directly. methods that perform pivoting operations involving subma-
trices of A or AT A at certain critical values of the cor-
Another intriguing new application for the optimization
problems above is compressed sensing1 (CS) [6], [7], [8],
responding parameter (τ, t, or ε). These methods can be
[9], [18]. Recent results show that a relatively small num- implemented so that only the submatrix of A corresponding
ber of random projections of a sparse signal can contain to nonzero components of the current vector x need be known
most of its salient information. It follows that if a signal is explicitly, so that if x has few nonzeros, these methods may
sparse or approximately sparse in some orthonormal basis, be competitive even for problems of very large scale. (See
then an accurate reconstruction can be obtained from random for example the SolveLasso function in the SparseLab
projections, which suggests a potentially powerful alternative toolbox, available from sparselab.stanford.edu.) In
to conventional Shannon-Nyquist sampling. In the noiseless some signal processing applications, however, the number of
setting, accurate approximations can be obtained by ﬁnding nonzero x components may be signiﬁcant, and since these
a sparse signal that matches the random projections of the methods require at least as many pivot operations as there
original signal. This problem can be cast as (5), where again are nonzeros in the solution, they may be less competitive
matrix A has the form A = RW, but in this case R represents on such problems. The interior-point (IP) approach in [58],
a low-rank randomized sensing matrix (e.g., a k × d matrix which solves a generalization of (4), also requires explicit
of independent realizations of a random variable), while the construction of AT A, though the approach could in principle
columns of W contain the basis over which the signal has modiﬁed to allow iterative solution of the linear system at each
a sparse representation (e.g., a wavelet basis). Problem (1) primal-dual iteration.
is a robust version of this reconstruction process, which is Algorithms that require only matrix-vector products involv-
ing A and AT have been proposed in a number of recent
resilient to errors and noisy data, and similar criteria have
been proposed and analyzed in [8], [32]. works. In [11], the problems (5) and (1) are solved by ﬁrst
reformulating them as “perturbed linear programs” (which
are linear programs with additional terms in the objective
B. Previous Algorithms
which are squared norms of the unknowns), then applying a
Several optimization algorithms and codes have been pro-
standard primal-dual IP approach [60]. The linear equations
posed to solve the QCLP (3), the QP (4), the LP (5), and
or least-squares problems that arise at each IP iteration are
the unconstrained (but nonsmooth) formulation (1). We review
then solved with iterative methods such as LSQR [48] or
that work here, identifying those contributions that are most
conjugate gradients (CG). Each iteration of these methods
suitable for signal processing applications, which are the target requires one multiplication each by A and AT . MATLAB
of this paper.
implementations of related approaches are available in the
In the class of applications that motivates this paper, the
SparseLab toolbox; see in particular the routines SolveBP
matrix A cannot be stored explicitly, and it is costly and
and pdco. For additional details see [51].
impractical to access signiﬁcant portions of A and AT A. In
Another IP method was recently proposed to solve a
wavelet-based image reconstruction and some CS problems,
quadratic programming reformulation of (1), different from
for which A = RW, explicit storage of A, R, or W is not
the one used here. Each search step is computed us-
practical for problems of interesting scale. However, matrix-
ing preconditioned conjugate gradient (PCG) and requires
vector products involving R and W can be done quite efﬁ- only products by A and AT [36]. The code, available at
ciently. For example, if the columns of W contain a wavelet
www.stanford.edu/˜boyd/l1_ls/, is reported to be
basis, then any multiplication of the form Wv or WT v can
faster than competing codes on the problems tested in [36].
be performed by a fast wavelet transform (see Section III-G,
The ℓ1-magic suite of codes (which is available at
for details). Similarly, if R represents a convolution, then
www.l1-magic.org) implements algorithms for several of
multiplications of the form Rv or RT v can be performed
the formulations described in Section I-A. In particular, the
with the help of the fast Fourier transform (FFT) algorithm.
formulation (3) is solved by recasting it as a second-order
In some CS applications, if the dimension of y is not too large,
cone program (SOCP), then applying a primal log-barrier
R can be explicitly stored; however, A is still not available
approach. For each value of the log-barrier parameter, the
explicitly, because the large and dense nature of W makes it
smooth unconstrained subproblem is solved using Newton’s
highly impractical to compute and store RW.
method with line search, where the Newton equations may be
Homotopy algorithms that ﬁnd the full path of solutions,
solved using CG. (Background on this approach can be found
for all nonnegative values of the scalar parameters in the
in [6], [9].) As in [11] and [36], each CG iteration requires
various formulations (τ in (1), ε in (3), and t in (4)), have only multiplications by A and AT ; these matrices need not
been proposed in [22], [39], [46], and [57]. The formulation
be known or stored explicitly.
(4) is addressed in [46], while [57] addresses (1) and (4).
Iterative shrinkage/thresholding (IST) algorithms can also
1A comprehensive repository of CS literature and software can be fond in be used to handle (1) and only require matrix-vector multi-
plications involving A and AT . Initially, IST was presented
www.dsp.ece.rice.edu/cs/.

<!-- 第 3 页 -->
TO APPEAR IN THE IEEE JOURNAL OF SELECTED TOPICS IN SIGNAL PROCESSING, 2007. 3

as an EM algorithm, in the context of image deconvolution obtained for a particular τ, it can be used as a “warm-start”
problems [45], [25]. IST can also be derived in a majorization- for a nearby value. Solutions can therefore be computed for a
minimization (MM) framework2 [16], [26] (see also [23],
range of τ values for a small multiple of the cost of solving
for a related algorithm derived from a different perspective). for a single τ value from a “cold start.” This feature of GPSR
Convergence of IST algorithms was shown in [13], [16]. is somewhat related to that of LARS and other homotopy
IST algorithms are based on bounding the matrix AT A (the
schemes, which compute solutions for a range of parameter
Hessian of ∥y −Ax∥22) by a diagonal D (i.e., D −AT A values in succession. In particular, “warm-starting” allows
is positive semi-deﬁnite), thus attacking (1) by solving a using GPSR within a continuation scheme (as suggested in
sequence of simpler denoising problems. While this bound [31]). IP methods such as those in [11], [36], and ℓ1-magic
may be reasonably tight in the case of deconvolution (where have been less successful in making effective use of warm-
R is usually a square matrix), it may be loose in the CS case, start information, though this issue has been investigated in
where matrix R usually has many fewer rows than columns. various contexts (see, e.g., [30], [35], [61]). To beneﬁt from
For this reason, IST may not be as effective for solving (1) in a warm start, IP methods require the initial point to be not
CS applications, as it is in deconvolution problems. only close to the solution but also sufﬁciently interior to the
Finally, we mention matching pursuit (MP) and orthogonal feasible set and close to a “central path,” which is difﬁcult to
MP (OMP) [5], [17], [20], [56], which are greedy schemes satisfy in practice.
to ﬁnd a sparse representation of a signal on a dictionary of
functions. (Matrix A is seen as an n-element dictionary of
II. PROPOSED FORMULATION
k-dimensional signals). MP works by iteratively choosing the
dictionary element that has the highest inner product with the A. Formulation as a Quadratic Program
current residual, thus most reduces the representation error.
OMP includes an extra orthogonalization step, and is known The ﬁrst key step of our GPSR approach is to express (1)
to perform better than standard MP. Low computational cost as a quadratic program; as in [28], this is done by splitting
is one of the main arguments in favor of greedy schemes like the variable x into its positive and negative parts. Formally,
OMP, but such methods are not designed to solve any of the we introduce vectors u and v and make the substitution
optimization problems above. However, if y = Ax, with x
x = u −v, u ≥0, v ≥0. (6)
sparse and the columns of A sufﬁciently incoherent, then OMP
ﬁnds the sparsest representation [56]. It has also been shown
These relationships are satisﬁed by ui = (xi)+ and vi =
that, under similar incoherence and sparsity conditions, OMP
(−xi)+ for all i = 1, 2, . . . , n, where (·)+ denotes the
is robust to small levels of noise [20].
positive-part operator deﬁned as (x)+ = max{0, x}. We thus
have ∥x∥1 = 1Tnu + 1Tnv, where 1n = [1, 1, . . ., 1]T is the
C. Proposed Approach vector consisting of n ones, so (1) can be rewritten as the
The approach described in this paper also requires only following bound-constrained quadratic program (BCQP):
matrix-vector products involving A and AT , rather than
1
explicit access to A. It is essentially a gradient projection (GP) min 2 ∥y −A(u −v)∥22 + τ 1Tnu + τ 1Tnv,
u,v
algorithm applied to a quadratic programming formulation of
s.t. u ≥0 (7)
(1), in which the search path from each iterate is obtained by
v ≥0.
projecting the negative-gradient direction onto the feasible set.
(See [3], for example, for background on gradient projection
Note that the ℓ2-norm term is unaffected if we set u ←u+s
algorithms.) We refer to our approach as GPSR (gradient
and v ←v + s, where s ≥0 is a shift vector. However such
projection for sparse reconstruction). Various enhancements to
a shift increases the other terms by 2 τ 1Tns ≥0. It follows
this basic approach, together with careful choice of stopping
that, at the solution of the problem (7), ui = 0 or vi = 0, for
criteria and a ﬁnal debiasing phase (which ﬁnds the least
i = 1, 2, . . . , n, so that in fact ui = (xi)+ and vi = (−xi)+
squares ﬁt over the support set of the solution to (1)), are
for all i = 1, 2, . . . , n, as desired.
also important in making the method practical and efﬁcient.
Problem (7) can be written in more standard BCQP form,
Unlike the MM approach, GPSR does not involve bounds
on the matrix AT A. In contrasts with the IP approaches
cT z + 12 zT Bz ≡F(z),
discussed above, GPSR involves only one level of iteration. min
z
(The approaches in [11] and [36] have two iteration levels—an s.t. z ≥0, (8)
outer IP loop and an inner CG, PCG, or LSQR loop. The ℓ1-
magic algorithm for (3) has three nested loops—an outer log- where
barrier loop, an intermediate Newton iteration, and an inner  u  −b
 b = AT y,
CG loop.) z = , c = τ 12n +
v b
GPSR is able to solve a sequence of problems (1) efﬁciently
for a sequence of values of τ. Once a solution has been and
 AT A −AT A
2Also known as bound optimization algorithms (BOA). For a general B = −AT A AT A . (9)
introduction to MM/BOA, see [33].

<!-- 第 4 页 -->
TO APPEAR IN THE IEEE JOURNAL OF SELECTED TOPICS IN SIGNAL PROCESSING, 2007. 4

B. Dimensions of the BCQP A. Basic Gradient Projection: The GPSR-Basic Algorithm
In the basic approach, we search from each iterate z(k) along
It may be observed that the dimension of problem (8) is
twice that of the original problem (1): x ∈Rn, while z ∈ the negative gradient −∇F(z(k)), projecting onto the non-
R2n. However, this increase in dimension has only a minor negative orthant, and performing a backtracking line search
impact. Matrix operations involving B can be performed more until a sufﬁcient decrease is attained in F. (Bertsekas [3,
economically than its size suggests, by exploiting its particular p. 226] refers to this strategy as “Armijo rule along the
structure (9). For a given z = [uT vT ]T , we have projection arc.”) We use an initial guess for α(k) that would
 u yield the exact minimizer of F along this direction if no new
  AT A(u −v)
bounds were to be encountered. Speciﬁcally, we deﬁne the
Bz = B = −AT A(u −v) , vector g(k) by
v
indicating that Bz can be found by computing the vector ( (∇F(z(k)))i, if z(k) > 0 or (∇F(z(k)))i < 0,
difference u−v and then multiplying once each by A and AT . g(k) = i
i
0, otherwise.
Since ∇F(z) = c+Bz (the gradient of the objective function
in (8)), we conclude that computation of ∇F(z) requires one We then choose the initial guess to be
multiplication each by A and AT , assuming that c, which
depends on b = AT y, is pre-computed at the start of the α F(z(k) −αg(k)),
α0 = arg min
algorithm.
which we can compute explicitly as
Another common operation in the GP algorithms described
below is to ﬁnd the scalar zT Bz for a given z = [uT , vT ]T . (g(k))T g(k)
α0 = (g(k))T Bg(k) . (13)
It is easy to see that
zT Bz = (u −v)T AT A(u −v) = ∥A(u −v)∥2 To protect against values of α0 that are too small or too large,
2,
we conﬁne it to the interval [αmin, αmax], where 0 < αmin <
indicating that this quantity can be calculated using only a αmax. (In this connection, we deﬁne the operator mid(a, b, c)
single multiplication by A. Since F(z) = (1/2)zTBz + cT z,
to be the middle value of its three scalar arguments.) This
it follows that evaluation of F(z) also requires only one technique for setting α0 is apparently novel, and produces an
multiplication by A. acceptable step much more often than the earlier choice of
α0 as the minimizer of F along the direction −∇F(z(k)),
ignoring the bounds.
C. A Note Concerning Non-negative Solutions The complete algorithm is deﬁned as follows.
It is worth pointing out that when the solution of (1) is Step 0 (initialization): Given z(0), choose parameters β ∈
known in advance to be nonnegative, we can directly rewrite (0, 1) and µ ∈(0, 1/2); set k = 0.
the problem as Step 1: Compute α0 from (13), and replace α0 by
mid(αmin, α0, αmax).
(τ 1n −AT y)T x + 12 xT AT Ax, Step 2 (backtracking line search): Choose α(k) to be the
min
x ﬁrst number in the sequence α0, βα0, β2α0, . . . such that
s.t. x ≥0. (10)
F((z(k) −α(k)∇F(z(k)))+) ≤
This problem is, as (8), a BCQP, and it can be solved with F(z(k)) −µ∇F(z(k))T (z(k) −(z(k) −α(k)∇F(z(k)))+),
the same algorithms. However the presence of the constraint
x ≥0 allows us to avoid splitting the variables into positive and set z(k+1) = (z(k) −α(k)∇F(z(k)))+.
and negative parts. Step 3: Perform convergence test and terminate with approx-
imate solution z(k+1) if it is satisﬁed; otherwise set
k ←k + 1 and return to Step 1.
III. GRADIENT PROJECTION ALGORITHMS
Termination tests used in Step 3 are discussed below in
In this section we discuss GP techniques for solving (8). In Subsection III-D.
our approaches, we move from iterate z(k) to iterate z(k+1) The computation at each iteration consists of matrix-vector
as follows. First, we choose some scalar parameter α(k) > 0 multiplications involving A and AT , together with a few
and set (less signiﬁcant) inner products involving vectors of length n.
Step 2 requires evaluation of F for each value of α(k) tried,
w(k) = (z(k) −α(k)∇F(z(k)))+.
(11)
where each such evaluation requires a single multiplication
We then choose a second scalar λ(k) ∈[0, 1] and set by A. Once the value of α(k) is determined, we can ﬁnd
z(k+1) and then ∇F(z(k+1)) with one more multiplication
z(k+1) = z(k) + λ(k)(w(k) −z(k)). by AT . Another multiplication by A sufﬁces to calculate the
(12)
denominator in (13) at the start of each iteration. In total, the
Our approaches described next differ in their choices of α(k) number of multiplications by A or AT per iteration is two
and λ(k). plus the number of values of α(k) tried in Step 2.

<!-- 第 5 页 -->
TO APPEAR IN THE IEEE JOURNAL OF SELECTED TOPICS IN SIGNAL PROCESSING, 2007. 5

Since F is quadratic, the line search parameter λ(k) in Step
B. Barzilai-Borwein Gradient Projection: The GPSR-BB Al-
gorithm 2 can be calculated simply using the following closed-form
expression:
Algorithm GPSR-Basic ensures that the objective function
F decreases at every iteration. Recently, considerable attention (0, (δ(k))T ∇F(z(k)) )
λ(k) = mid
has been paid to an approach due to Barzilai and Borwein (δ(k))T B δ(k) , 1 .
(BB) [2] that does not have this property. This approach
was originally developed in the context of unconstrained (When (δ(k))T B δ(k) = 0, we set λ(k) = 1.) The use of this
minimization of a smooth nonlinear function F. It calculates parameter λ(k) removes one of the salient properties of the
each step by the formula δ(k) = −H−1k ∇F(z(k)), where Hk
Barzilai-Borwein approach, namely, the possibility that F may
is an approximation to the Hessian of F at z(k). Barzilai
increase on some iterations. Nevertheless, in our problems,
and Borwein propose a particularly simple choice for the
it appeared to improve performance over the more standard
approximation Hk: They set it to be a multiple of the identity non-monotone variant, which sets λ(k) ≡1. We also tried
Hk = η(k)I, where η(k) is chosen so that this approximation
other variants of the Barzilai-Borwein approach, including one
has similar behavior to the true Hessian over the most recent
proposed in [15], which alternates between two deﬁnitions of
step, that is, α(k). The difference in performance were very small, so we
∇F(z(k)) −∇F(z(k−1)) ≈η(k) hz(k) −z(k−1)i focus our presentation on the method described above.
,
In earlier testing, we experimented with other variants of GP,
with η(k) chosen to satisfy this relationship in the least-squares including the GPCG approach of [43] and the proximal-point
sense. In the unconstrained setting, the update formula is approach of [59]. The GPCG approach runs into difﬁculties
because the projection of the Hessian B onto most faces of
z(k+1) = z(k) −(η(k))−1∇F(z(k));
the positive orthant deﬁned by z ≥0 is singular, so the inner
CG loop in this algorithm tends to fail.
this step is taken even if it yields an increase in F. This
strategy is proved analytically in [2] to be effective on simple
problems. Numerous variants have been proposed recently, C. Convergence
and subjected to a good deal of theoretical and computational Convergence of the methods proposed above can be de-
evaluation. rived from the analysis of Bertsekas [3] and Iusem [34], but
The BB approach has been extended to BCQPs in [15], follows most directly from the results of Birgin, Martinez,
[52]. The approach described here is simply that of [52, and Raydan [4] and Seraﬁni, Zanghirati, and Zanni [52].
Section 2.2]. We choose λk in (12) as the exact minimizer We summarize convergence properties of the two algorithms
over the interval [0, 1] and choose η(k) at each iteration in
described above, assuming that termination occurs only when
the manner described above, except that α(k) = (η(k))−1 is z(k+1) = z(k) (which indicates that z(k) is optimal).
restricted to the interval [αmin, αmax]. In deﬁning the value of Theorem 1: The sequence of iterates {z(k)} generated by
α(k+1) in Step 3 below, we make use of the fact that for F
the either the GPSR-Basic of GPSR-BB algorithms either
deﬁned in (8), we have terminates at a solution of (8), or else converges to a solution
z(k) −z(k−1) of (8) at an R-linear rate.
∇F(z(k)) −∇F(z(k−1)) = B
.
Proof: Theorem 2.1 of [52] can be used to show that
all accumulation points of {z(k)} are stationary points. (This
result applies to an algorithm in which the α(k) are chosen by
Step 0 (initialization): Given z(0), choose parameters αmin,
αmax, α(0) ∈[αmin, αmax], and set k = 0. a different scheme, but the only relevant requirement on these
Step 1: Compute step: parameters in the proof of [52, Theorem 2.1] is that they lie in
the range [αmin, αmax], as is the case here.) Since the objective
δ(k) = z(k) −α(k)∇F(z(k))+ −z(k).
(14) in (8) is clearly bounded below (by zero), we can apply [52,
Theorem 2.2] to deduce convergence to a solution of (8) at an
Step 2 (line search): Find the scalar λ(k) that minimizes
R-linear rate.
F(z(k) + λ(k) δ(k)) on the interval λ(k) ∈[0, 1], and
set z(k+1) = z(k) + λ(k) δ(k).
D. Termination
Step 3 (update α): compute
The decision about when an approximate solution is of
γ(k) = (δ(k))T B δ(k);
(15) sufﬁciently high quality to terminate the algorithms is a
if γ(k) = 0, let α(k+1) = αmax, otherwise difﬁcult one. We wish for the approximate solution z to be
reasonably close to a solution z∗and/or that the function
(αmin, ∥δ(k)∥2 ) value F(z) be reasonably close to F(z∗), but at the same
α(k+1) = mid 2
, αmax . time we wish to avoid the excessive computation involved
γ(k)
in ﬁnding an overly accurate solution. For the problem (7),
Step 4: Perform convergence test and terminate with approx- given that variable selection is the main motivation of the
imate solution z(k+1) if it is satisﬁed; otherwise set
formulation (1) and that a debiasing step may be carried out
k ←k + 1 and return to Step 1. in a postprocessing phase (see Subsection III-E), we wish the

<!-- 第 6 页 -->
TO APPEAR IN THE IEEE JOURNAL OF SELECTED TOPICS IN SIGNAL PROCESSING, 2007. 6

nonzero components of the approximate solution z to be close it does not work for general BCQPs (e.g., in which all the
to the nonzeros of a true solution z∗. components of z are nonzero at the solution) or for algorithms
These considerations motivate a number of possible termi- that generate iterates in the interior of the feasible set.
nation criteria. One simple criterion is It is difﬁcult to choose a termination criterion from among
these options that performs well on all data sets and in all
∥z −(z −¯α∇F(z))+∥≤tolP, (16)
contexts. In the tests described in Section IV, unless otherwise
where tolP is a small parameter and ¯α is a positive constant. noted, we use (17), with tolP= 10−2, which appeared to
This criterion is motivated by the fact that the left-hand side is yield fairly consistent results. We may also impose some large
continuous in z and zero if and only if z is optimal. A second, upper limit maxiter on the number of iterations.
similar criterion is motivated by perturbation results for linear
complementarity problems (LCP). There is a constant CLCP E. Debiasing
such that
Once an approximate solution has been obtained using one
dist(z, S) ≤CLCP ∥min(z, ∇F(z))∥ of the algorithms above, we optionally perform a debiasing
step. The computed solution z = [uT , vT ]T is converted to
where S denotes the solution set of (8), dist(·) is the dis-
an approximate solution xGP = u −v. The zero components
tance operator, and the min on the right-hand side is taken
of xGP are ﬁxed at zero, and the least-squares objective ∥y −
component-wise [14]. With this bound in mind, we can deﬁne Ax∥2

# 2 is then minimized subject to this restriction using a CG
a convergence criterion as follows:
algorithm (see for example [44, Chapter 5]). In our code, the
∥min(z, ∇F(z))∥≤tolP. (17) CG iteration is terminated when
∥y −Ax∥22 ≤tolD ∥y −AxGP ∥22, (21)
A third criterion proposed recently in [36] is based on
duality theory for the original formulation (1). It can be shown
where tolD is a small positive parameter. We also restrict the
that the dual of (1) is
number of CG steps in the debiasing phase to maxiterD.
−12 sT s −yT s Essentially, the problem (1) is being used to select the
max
s “explanatory” variables (components of x), while the debi-
−τ1n ≤AT s ≤τ1n.
s.t. (18) asing step chooses the optimal values for these components
according to a least-squares criterion (without the regulariza-
If s is feasible for (18), then
tion term τ∥x∥1). Similar techiques have been used in other
1 2 + τ∥x∥1 + 12 sT s + yT s ≥0, ℓ1-based algorithms, e.g., [42]. It is also worth pointing out
2∥y −Ax∥2 (19)
that debiasing is not always desirable. Shrinking the selected
with equality attained if and only if x is a solution of (1) and coefﬁcients can mitigate unusually large noise deviations [19],
s is a solution of (18). To deﬁne a termination criterion, we a desirable effect that may be undone by debiasing.
invert the transformation in (6) to obtain a candidate x, and
then construct a feasible s as follows: F. Warm Starting and Continuation
Ax −y
s ≡τ The gradient projection approach beneﬁts from a good
∥AT (Ax −y)∥∞
starting point. This suggests that we can use the solution of
(see [36]). Substituting these values into the left-hand side of (1), for a given value of τ, to initialize GPSR in solving (1) for
(19), we can declare termination when this quantity falls below a nearby value of τ. The second solve will typically take fewer
a threshold tolP. Note that this quantity is an upper bound on iterations than the ﬁrst one; the number of iterations depends
the gap between F(z) and the optimal objective value F(z∗). on the closeness of the values of τ and the closeness of the
None of the criteria discussed so far take account of the solutions. Using this warm-start technique, we can efﬁciently
nonzero indices of z or of how these have changed in recent solve for a sequence of values of τ. We note that it is important
iterations. In our fourth criterion, termination is declared when to use the non-debiased solution as starting point; debiasing
the set of nonzero indices of an iterate z(k) changes by may move the iterates away from the true minimizer of (1).
a relative amount of less than a speciﬁed threshold tolA. One motivation for solving for a range of τ values is that
Speciﬁcally, we deﬁne we often wish to obtain solutions for a range of values of τ,
possibly using some test based on the solution sparsity and
Ik = {i | z(k) = 0},
i the goodness of least-squares ﬁt to choose the “best” solution
Ck = {i | (i ∈Ik and i /∈Ik−1) or (i /∈Ik and i ∈Ik−1)}, from among these possibilities.
Another important application of warm-starting is continu-
and terminate if
ation, as recently suggested in [31]. It has been noted recently
|Ck|/|Ik| ≤tolA. (20)
that the speed of GPSR may degrade considerably for smaller
This criterion is well suited to the class of problems addressed values of the regularization parameter τ. However, if we use
in this paper (where we expect the cardinality of Ik, in later GPSR to minimize (1) for a larger value of τ, then decrease τ
stages of the algorithm, to be much less than the dimension in steps toward its desired value, running GPSR with warm-
of z), and to algorithms of the gradient projection type, which start for each successive value of τ, we are often able to
generate iterates on the boundary of the feasible set. However, identify the solution much more efﬁciently than if we just

<!-- 第 7 页 -->
TO APPEAR IN THE IEEE JOURNAL OF SELECTED TOPICS IN SIGNAL PROCESSING, 2007. 7

ran GPSR once for the desired value of τ from a “cold For the GPSR-BB algorithm, we set αmin = 10−30, αmax =
start.” We illustrate this claim with a computational example 1030; the performance is insensitive to these choices, similar
in Section IV-D. results are obtained for other small settings of αmin and large
values of αmax. We discuss results also for a nonmonotone
version of the GPSR-BB algorithm, in which λk ≡1. In
G. Analysis of Computational Cost
GPSR-Basic, we used β = 0.5 and µ = 0.1.
It is not possible to accurately predict the number of GPSR-
Basic and GPSR-BB iterations required to ﬁnd an approximate
A. Compressed Sensing (CS)
solution. We can however analyze the cost of each iteration
of these algorithms. The main computational cost per iteration In our ﬁrst experiment, we consider a typical CS scenario
is a small number of inner products, vector-scalar multiplica- (similar to the one in [36]), where the goal is to reconstruct
tions, and vector additions, each requiring n or 2n ﬂoating- a length-n sparse signal (in the canonical basis) from k
point operations, plus a modest number of multiplications by observations, where k < n. In this case, the k × n matrix
A and AT . When A = RW, these operations entail a small A is obtained by ﬁrst ﬁlling it with independent samples of a
number of multiplications by R, RT , W, and WT . The cost standard Gaussian distribution and then orthonormalizing the
of each CG iteration in the debiasing phase is similar but rows. In this example, n = 4096, k = 1024, the original
lower; just one multiplication by each of R, RT , W, and signal x contains 160 randomly placed ±1 spikes, and the
WT plus a number of vector operations. We next analyze the observation y is generated according to (2), with σ2 = 10−4.
cost of multiplications by R, RT , W, and WT for various Parameter τ is chosen as suggested in [36]:
typical problems; let us begin by recalling that A = RW is τ = 0.1 ∥AT y∥∞;
(22)
a k × n matrix, and that x ∈Rn, y ∈Rk. Thus, if R has
dimensions k × d, then W must be a d × n matrix. notice that for τ ≥∥AT y∥∞the unique minimum of (1) is
If W contains an orthogonal wavelet basis (d = n), matrix- the zero vector [29], [36].
vector products involving W or WT can be implemented
The original signal and the estimate obtained by solving
using fast wavelet transform algorithms with O(n) cost [40], (1) using the monotone version of the GPSR-BB (which is
instead of the O(n2) cost of a direct matrix-vector product. essentially the same as that produced by the nonmonotone
Thus, the cost of a product by A or AT is O(n) plus that of
GPSR-BB and GPSR-Basic) are shown in Fig. 1. Also shown
multiplying by R or RT which, with a direct implementation,
in Fig. 1 is the reconstruction obtained after the debiasing
is O(k n). When using redundant translation-invariant wavelet procedure described in Section III-E; although GPSR-BB
systems, W is d × d(log2(d) + 1), but the corresponding does an excellent job at locating the spikes, the debiased
matrix-vector products can be done with O(d log d) cost, using reconstruction exhibits a much lower mean squared error3
fast undecimated wavelet transform algorithms [40]. (MSE) with respect to the original signal. Finally, Fig. 1 also
As mentioned above, direct implementations of products depicts the solution of minimal ℓ2-norm to the undetermined
by R and RT have O(k d) cost. However, in some cases, system y = Ax, which is equal to AT (AAT )−1y.
these products can be carried out with signiﬁcantly lower In Fig. 2, we plot the evolution of the objective function
cost. For example, in image deconvolution problems [25], (without debiasing) versus iteration number and CPU time,
R is a k × k (d = k) block-Toeplitz matrix with Toeplitz for GPSR-Basic and both versions of GPSR-BB. The GPSR-
blocks (representing 2D convolutions) and these products can BB variants are slightly faster, but the performance of all three
be performed in the discrete Fourier domain using the FFT, codes is quite similar on this problem. Fig. 3 shows how the
with O(k log k) cost, instead of the O(k2) cost of a direct objective function (1) and the MSE evolve in the debiasing
implementation. If the blur kernel support is very small (say phase. Notice that the objective function (1) increases during
l pixels) these products can be done with even lower cost, the debiasing phase, since we are minizing a different function
O(kl), by implementing the corresponding convolution. Also, in this phase.
in certain applications of CS, such as MR image reconstruction
[38], R is formed from a subset of the discrete Fourier TABLE I
CPU TIMES (AVERAGE OVER 10 RUNS) OF SEVERAL ALGORITHMS ON THE
transform basis, so the cost is O(k log k) using the FFT. EXPERIMENT OF FIG. 1.
Algorithm CPU time (seconds)
IV. EXPERIMENTS
GPSR-BB monotone 0.59
This section describes some experiments testifying to the GPSR-BB nonmonotone 0.51
GPSR-Basic 0.69
very good performance of the proposed algorithms in sev-
GPSR-BB monotone + debias 0.89
eral types of problems of the form (1). These experiments GPSR-BB nonmonotone + debias 0.82
include comparisons with state-of-the-art approaches, namely GPSR-Basic + debias 0.98
l1_ls 6.56
IST [16], [25], and the recent l1_ls package, which was
IST 2.76
shown in [36] to outperform all previous methods, includ-
ing the ℓ1-magic toolbox and the homotopy method from
Table I reports average CPU times (over 10 experiments)
[21]. The algorithms discussed in Section III are written
required by the three GPSR algorithms as well as by l1_ls
in MATLAB and are freely available for download from
www.lx.it.pt/˜mtf/GPSR/. 3MSE = (1/n)∥bx −x∥22, where bx is an estimate of x.

<!-- 第 8 页 -->
TO APPEAR IN THE IEEE JOURNAL OF SELECTED TOPICS IN SIGNAL PROCESSING, 2007. 8

Original (n = 4096, number of nonzeros = 160)
1
0
−1

# 0 500 1000 1500 2000 2500 3000 3500 4000
GPSR reconstruction (k = 1024, tau =  0.08, MSE = 0.0072)
1
0
−1

# 0 500 1000 1500 2000 2500 3000 3500 4000
Debiased (MSE = 3.377e−005)
1
0
−1

# 0 500 1000 1500 2000 2500 3000 3500 4000
Minimum norm solution (MSE = 1.568)
10
5
0
−5

# 0 500 1000 1500 2000 2500 3000 3500 4000
Fig. 1. From top to bottom: original signal, reconstruction via the minimization of (1) obtained by GPSR-BB, reconstruction after debiasing, the minimum
norm solution given by AT (AAT )−1y.

and IST. To perform this comparison, we ﬁrst run the l1_ls R). For each data set, we ﬁrst run GPSR-BB (the monotone
algorithm and then each of the other algorithms until each version) and store the ﬁnal value of the residual; we then run
reaches the same value of the objective function reached by greed_omp_qr and SolveOMP until they reach the same
l1_ls. The results in this table show that, for this problem, all residual norm. Finally, we compute average MSE (with respect
GPSR variants are about one order of magnitude faster than to the true x) and average CPU time, over the 10 runs.
l1_ls and 5 times faster than IST. Fig. 4 plots the average reconstruction MSE and the av-
An indirect performance comparison with other codes on erage CPU times, as a function of the number of nonzero
this problem can be made by referring to [36, Table 1], which components in x. We observe that all methods basically obtain
shows that l1_ls outperforms the homotopy method from [21] exact reconstructions for m up to almost 200, with the OMP
(6.9 second vs 11.3 seconds). It also outperforms ℓ1-magic by solutions (which are equal up to some numerical ﬂuctuations)
about two orders of magnitude and the pdco algorithms from starting to degrade earlier and faster than those produced by
SparseLab by about one order of magnitude. solving (1). Concerning computational efﬁciency, our main
focus in this experiment, we can observed that GPSR-BB is
clearly faster than both OMP implementations, except in the
B. Comparison with OMP
case of extreme sparseness (m < 50 non-zero elements in the
Next, we compare the computational efﬁciency of GPSR
4096-vector x).
algorithms against OMP, often regarded as a highly efﬁcient
method that is especially well-suited to very sparse cases.
We use two efﬁcient MATLAB implementations of OMP: C. Scalability Assessment
the greed_omp_qr function of the Sparsify toolbox (avail- To assess how the computational cost of the GPSR algo-
able at www.see.ed.ac.uk/˜tblumens/sparsify), rithms grows with the size of matrix A, we have performed
which is based on QR factorization [5], [17], and the function an experiment similar to the one in [36, Section 5.3]. The idea
SolveOMP of the SparseLab toolbox, which is based on is to assume that the computational cost is O(nα) and obtain
the Cholesky factorization. Because greed_omp_qr requires empirical estimates of the exponent α. We consider random
each column of the matrix R to have unit norm, we use sparse matrices (with the nonzero entries normally distributed)
matrices with this property in all our comparisons. of dimensions (0.1 n) × n, with n ranging from 104 to 106.
Since OMP is not an optimization algorithm for minimizing Each matrix is generated with about 3n nonzero elements
(1) (or any other objective function), it is not obvious how and the original signal with n/4 randomly placed nonzero
to compare it with GPSR. In our experiments, we ﬁx the components. For each value of n, we generate 10 random
matrix size (1024 × 4096) and consider a range of degrees of matrices and original signals and observed data according to
sparseness: the number m of non-zeros spikes in x (randomly (2), with noise variance σ2 = 10−4. For each data set (i.e.,
located values of ±1) ranges from 5 to 250. For each value each pair A, y), τ is chosen as in (22). The results in Fig. 5
of m we generate 10 random data sets, i.e., triplets (x, y, (which are average for 10 data sets of each size) show that all

<!-- 第 9 页 -->
TO APPEAR IN THE IEEE JOURNAL OF SELECTED TOPICS IN SIGNAL PROCESSING, 2007. 9

n=4096, k=1024, tau=0.08 22

|Col1|Debiasing|
|---|---|

22

|GPSR−BB monotone<br>GPSR−BB non−monotone<br>GPSR−Basic|GPSR−BB monotone<br>GPSR−BB non−monotone<br>GPSR−Basic|Col3|
|---|---|---|

20
20
18
Objective function
Objective function 18
16
16
14
14
12

12
10

# 0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8
CPU time (seconds)
10

# 1 2 3 4 5 6 7 8 9 10 0.04

|Col1|Debiasing|
|---|---|

Iterations
n=4096, k=1024, tau=0.08 0.035
22

|GPSR−BB monotone<br>GPSR−BB non−monotone<br>GPSR−Basic|GPSR−BB monotone<br>GPSR−BB non−monotone<br>GPSR−Basic|Col3|
|---|---|---|

### 0.03

# 20 0.025
MSE 0.02
Objective function 18

### 0.015

16

### 0.01

# 14 0.005

# 0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8

# 12 CPU time (seconds)

Fig. 3. Evolution of the objective function and reconstruction MSE, vs
10
0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 CPU time, including the debiasing phase, corresponding to the experiment
CPU time (seconds) illustrated in Fig. 1.
Fig. 2. The objective function plotted against iteration number and CPU
time, for GPSR-Basic and the monotone and nonmonotone versions of the
It has been pointed out recently that the speed of GPSR
GPSR-BB, corresponding to the experiment illustrated in Fig. 1.
can degrade as the value of τ becomes small [31]. (This
observation is conﬁrmed by the CPU times of the cold-started
GPSR algorithms have empirical exponents below 0.9, thus runs of GPSR shown in Fig. 6.) The GPSR approaches can
much better than l1_ls (for which we found α = 1.21, in be improved by adding a continuation heuristic, as suggested
agreement with the value 1.2 reported in [36]); IST has an in [31] and explained in Section III-F. Our simple heuristic
exponent very close to that of GPSR algorithms, but a worse starts by setting τ = 0.8∥ATy∥∞, then decreases in τ by
constant, thus its computational complexity is approximately a constant factor in ﬁve steps until the desired value of τ is
a constant factor above GPSR. Finally, notice that, according obtained. GPSR is run from a “cold start” at the ﬁrst (largest)
to [36], ℓ1-magic has an exponent close to 1.3, while all the value of τ, then run from a warm start for each of the other
other methods considered in that paper have exponents no less ﬁve values in the sequence.
than 2. We illustrate the performance of this heuristic by using the
same test problem as in Section IV-A, but with σ2 = 0.
D. Warm Starting and Continuation In this noiseless case, CS theory states that it is possible to
reconstruct x accurately by solving (5). Since the solution of
As mentioned in Section III-F, GPSR algorithms can beneﬁt
(1) approaches that of (5), as τ goes to zero, it makes sense
from being warm-started, that is, initialized at a point close
for this problem to work with small values of τ.
to the solution. This property can be exploited to ﬁnd minima
Fig. 7 shows the average (over 10 runs) of the CPU times
(1) for a sequence of values of τ, at a modest multiple of
required by GPSR-BB and GPSR-Basic with and without
the cost of solving only for one value of τ. We illustrate this
continuation, as well as l1_ls, for several values of β, where
possibility in a problem with k = 1024, n = 8192, which we
we deﬁne β = ∥AT y∥∞/τ. Although the original versions of
wish to solve for 9 different values of τ,
the GPSR algorithms are slower than l1_ls, for β sufﬁciently
τ ∈{0.05, 0.075, 0.1, ..., 0.275} ∥ATy∥∞.
large (τ sufﬁciently small), the continuation schemes are faster
than l1_ls for the whole range of values.
As shown in Fig. 6, warm starting does indeed signiﬁcantly
reduce the CPU time required by GPSR. The total CPU time
of the 9 runs was about 6.5 seconds, less than twice that of the E. Image Deconvolution Experiments
ﬁrst run, which is about 3.7 seconds. The total time required In this subsection, we illustrate the use of the GPSR-BB al-
using a cold-start for each value of τ was about 17.5 seconds. gorithm in image deconvolution. Recall that (see Section I-A)

<!-- 第 10 页 -->
TO APPEAR IN THE IEEE JOURNAL OF SELECTED TOPICS IN SIGNAL PROCESSING, 2007. 10

|Col1|MSE versus sparseness degree<br>0.07<br>GPSR<br>0.06 Sparsify OMP<br>SparseLab OMP<br>0.05<br>0.04<br>MSE<br>0.03<br>0.02<br>0.01<br>0<br>0 50 100 150 200 250<br>Number of non−zero components|
|---|---|
|<br>0<br>50<br>100<br>150<br>200<br>250<br>0<br>5<br>10<br>15<br>20<br>25<br>Number of non−zero components<br>CPU time (seconds)<br>CPU time versus sparseness degree<br>GPSR<br>Sparsify OMP<br>SparseLab OMP|<br>|

Warm versus cold start
4

|Cold start<br>Warm start|Cold start<br>Warm start|Col3|
|---|---|---|

### 3.5

3

### 2.5

CPU time
2

### 1.5

1

### 0.5

0

## 0.005 0.01 0.015 0.02 0.025 0.03 0.035 0.04
Value of τ

Fig. 6. CPU times for a sequence of values of τ with warm starting and
without warm starting (cold starting).

103
GPSR-BB
GPSR-Basic
GPSR-BB w/ continuation

# 2 GPSR-Basic w/ continuation

# 10 l1-ls
CPU time (seconds)
101

100
Fig. 4. Average MSE and CPU times for GPSR and two implementations
of OMP, as a function of the number of non-zero components of x.
10-1

# 101 102 103 104
Empirical asymptotic exponents O(nα) β
103
Fig. 7. CPU times of the GPSR-BB and GPSR-Basic algorithms, with and
without continuation, as a function of β = ∥AT y∥∞/τ.
102

Average CPU time
image; these problems have been studied in [25], [26] (and
101
other papers). In this experiments, W represents the inverse
orthogonal wavelet transform, with Haar wavelets, and R

# 0 is a matrix representation of the blur operation; we have

# 10 GPSR−BB monotone (α = 0.861)
GPSR−BB non−monotone (α = 0.882) k = n = 2562, and the difﬁculty comes not form the
GPSR−Basic (α = 0.874)
l1−ls (α = 1.21) indeterminacy of the associated system, but from the very
IST (α = 0.891)
10−1 ill-conditioned nature of matrix RW. Parameter τ is hand-

# 104 105 106
Problem size (n) tuned for the best SNR improvement. In each case, we ﬁrst
run IST and then run the GPSR algorithms until they reach
Fig. 5. Assessment of the empirical growth exponent of the computational
the same ﬁnal value of the objective function; the ﬁnal values
complexity of several algorithms.
of MSE are essentially the same. Table III lists the CPU times
required by GPSR-BB algorithms and IST, in each of these
experiments, showing that GPSR-BB is two to three times
wavelet-based image deconvolution, under a Laplacian prior
faster than IST.
on the wavelet coefﬁcients, can be formulated as (1). We
stress that the goal of these experiments is not to assess the
performance (e.g., in terms of SNR improvement) of the crite- TABLE II
IMAGE DECONVOLUTION EXPERIMENTS.
rion form (1). Such an assessment has been comprehensively
carried out in [25], [26], and several other recent works on Experiment blur kernel σ2
this topic. Rather, our goal is to compare the speed of the 1 9 × 9 uniform 0.562

# 2 hij = 1/(i2 + j2) 2
proposed GPSR algorithms against the competing IST.

# 3 hij = 1/(i2 + j2) 8
We consider three standard benchmark problems summa-
rized in Table II, all based on the well-known Cameraman

<!-- 第 11 页 -->
TO APPEAR IN THE IEEE JOURNAL OF SELECTED TOPICS IN SIGNAL PROCESSING, 2007. 11

TABLE III
CPU TIMES (IN SECONDS) FOR THE IMAGE DECONVOLUTION [13] P. Combettes and V. Wajs, “Signal recovery by proximal forward-
EXPERIMENTS. backward splitting,” SIAM Journal on Multiscale Modeling & Simu-
lation, vol. 4, pp. 1168–1200, 2005.
Experiment GPSR-BB GPSR-BB IST [14] R. W. Cottle, J.-S. Pang, and R. E. Stone. The Linear Complementarity
monotone nonmonotone Problem, Academic Press, 1993.
1 1.69 1.04 3.82 [15] Y.-H. Dai and R. Fletcher. “Projected Barzilai-Borwein methods
2 1.11 0.84 2.63 for large-scale box-constrained quadratic programming,” Numerische

# 3 1.21 1.01 2.38 Mathematik, vol. 100, pp. 21–47, 2005.
[16] I. Daubechies, M. De Friese, and C. De Mol. “An iterative thresholding
algorithm for linear inverse problems with a sparsity constraint,” Com-
munications in Pure and Applied Mathematics, vol. 57, pp. 1413–1457,
V. CONCLUSIONS 2004.
[17] G. Davis, S. Mallat, M. Avellaneda, “Greedy adaptive approximation,”
We have proposed gradient projection algorithms for solving Journal of Constructive Approximation, vol. 12, pp. 57–98, 1997.
a quadratic programming reformulation of a class of convex [18] D. Donoho. “Compressed sensing,” IEEE Transactions on Information
Theory, vol. 52, pp. 1289-1306, 2006.
nonsmooth unconstrained optimization problems arising in [19] D. Donoho. “De-noising by soft-thresholding,” IEEE Transactions on
compressed sensing and other inverse problems in signal Information Theory, vol. 41, pp. 613–627, 1995.
processing and statistics. In experimental comparisons to state- [20] D. Donoho, M. Elad, and V. Temlyakov. “Stable recovery of sparse over-
complete representations in the presence of noise,” IEEE Transactions
of-the-art algorithms, the proposed methods are signiﬁcantly on Information Theory, vol. 52, pp. 6-18, 2006.
faster (in some cases by orders of magnitude), especially [21] D. Donoho and Y. Tsaig. “Fast solution of L1-norm minimization
in large-scale settings. Instances of poor performance have problems when the solution may be sparse,” Technical Report, Institute
for Computational and Mathematical Engineering, Stanford University,
been observed when the regularization parameter τ is small, 2006. Available at www.stanford.edu/˜tsaig
but in such cases the gradient projection methods can be [22] B. Efron, T. Hastie, I. Johnstone, and R. Tibshirani. “Least Angle
embedded in a simple continuation heuristic to recover their Regression,” Annals of Statistics, vol. 32, pp. 407–499, 2004.
[23] M. Elad, “Why simple shrinkage is still relevant for redundant represen-
efﬁcient practical performance. The new algorithms are easy tations?”, IEEE Transactions on Information Theory, vol. 52, pp. 5559-
to implement, work well across a large range of applications, 5569, 2006.
and do not appear to require application-speciﬁc tuning. Our [24] M. Elad, B. Matalon, and M. Zibulevsky, “Image denoising with shrink-
age and redundant representations”, Proceedings of the IEEE Computer
experiments also evidenced the importance of a debiasing Society Conference on Computer Vision and Pattern Recognition –
phase, in which we use a linear CG method to minimize the CVPR’2006, New York, 2006.
least squares cost of the inverse problem, under the constraint [25] M. Figueiredo and R. Nowak. “An EM algorithm for wavelet-based
image restoration,” IEEE Transactions on Image Processing, vol. 12,
that the zero components of the sparse estimate produced by pp. 906–916, 2003.
the GP algorithm remain at zero. [26] M. Figueiredo and R. Nowak. “A bound optimization approach to
wavelet-based image deconvolution,” IEEE International Conference
MATLAB implementations of the algorithms discussed in
on Image Processing – ICIP’2005, 2005.
this paper are available at www.lx.it.pt/˜mtf/GPSR. [27] M. Frank and P. Wolfe. “An algorithm for quadratic programming,”
Naval Research Logistics Quarterly, vol. 3, pp. 95–110, 1956.
[28] J. J. Fuchs. “Multipath time-delay detection and estimation,” IEEE
REFERENCES Transactions on Signal Processing, vol. 47, pp. 237–243, 1999.
[29] J. J. Fuchs. “More on sparse representations in arbitrary bases,” IEEE
[1] S. Alliney and S. Ruzinsky. “An algorithm for the minimization of Transactions on Information Theory, vol. 50, pp. 1341–1344, 2004.
mixed ℓ1 and ℓ2 norms with application to Bayesian estimation,” IEEE [30] J. Gondzio and A. Grothey. “A New unblocking technique to warmstart
Transactions on Signal Processing, vol. 42, pp. 618–627, 1994. interior point methods based on sensitivity analysis,” Technical Report
[2] J. Barzilai and J. Borwein. “Two point step size gradient methods,” IMA MS-06-005, School of Mathematics, The University of Edinburgh,
Journal of Numerical Analysis, vol. 8, pp. 141–148, 1988. Edinburgh, UK, 2006.
[3] D. P. Bertsekas. Nonlinear Programming, 2nd ed., Athena Scientiﬁc, [31] E. Hale, W. Yin, and Y. Zhang. “A ﬁxed-point continuation method for
Boston, 1999. ℓ1-regularized minimization with applications to compresses sensing,”
[4] E. G. Birgin, J. M. Martinez, and M. Raydan. “Nonmonotone spectral Technical Report TR07-07, Department of Computational and Applied
projected gradient methods on convex sets,” SIAM Journal on Optimiza- Mathematics, Rice University, Houston, TX, USA, 2007.
tion, vol. 10, pp. 1196–1211, 2000. [32] J. Haupt and R. Nowak. “Signal reconstruction from noisy random
[5] T. Blumensath and M. Davies. “Gradient pursuits”, submitted, 2007. projections,” IEEE Transactions on Information Theory, vol. 52,
Available at www.see.ed.ac.uk/˜tblumens/papers pp. 4036–4048, 2006.
[6] E. Cand`es, J. Romberg and T. Tao. “Stable signal recovery from [33] D. Hunter and K. Lange. “A Tutorial on MM Algorithms,” The American
incomplete and inaccurate information,” Communications on Pure and Statistician, vol. 58, pp. 30–37, 2004.
Applied Mathematics, vol. 59, pp. 1207–1233, 2005. [34] A. N. Iusem. “On the convergence proeperties of the projected
[7] E. Cand`es and T. Tao, “Near optimal signal recovery from random gradient method for convex optimization,” Computational and Applied
projections: universal encoding strategies,” IEEE Transactions on Mathematics, vol. 22, pp. 37–52, 2003.
Information Theory, vol. 52, pp. 5406–5425, 2004. [35] E. John and E. A. Yıldırım. “Implementation of warm-start strategies
[8] E. Cand`es and T. Tao, “The Dantzig selector: statistical estimation when in interior-point methods for linear programming in ﬁxed dimension,”
p is much larger than n,” Annals of Statistics, 2007, to appear. Available Technical Report, Department of Industrial Engineering, Bilkent Uni-
at arxiv.org/abs/math.ST/0506081 versity, Ankara, Turkey, 2006.
[9] E. Cand`es, J. Romberg, and T. Tao. “Robust uncertainty principles: Exact [36] S. Kim, K. Koh, M. Lustig, S. Boyd, and D. Gorinvesky. “A
signal reconstruction from highly incomplete frequency information,” method for large-scale ℓ1-regularized least squares problems with ap-
IEEE Transations on Information Theory, vol. 52, pp. 489–509, 2006. plications in signal processing and statistics,” Tech. Report, Dept.
[10] A. Chambolle, “An algorithm for total variation minimization and of Electrical Engineering, Stanford University, 2007. Available at
applications,” Journal of Mathematical Imaging and Vision, vol. 20, www.stanford.edu/˜boyd/l1_ls.html
pp. 89-97, 2004. [37] S. Levy and P. Fullagar. “Reconstruction of a sparse spike train from
[11] S. Chen, D. Donoho, and M. Saunders. “Atomic decomposition by basis a portion of its spectrum and application to high-resolution deconvolu-
pursuit,” SIAM Journal of Scientiﬁc Computation, vol. 20, pp. 33–61, tion,” Geophysics, vol. 46, pp. 1235–1243, 1981.
1998. [38] M. Lustig, D. Donoho, and J. Pauly. “Sparse MRI: The application of
[12] J. Claerbout and F. Muir. “Robust modelling of erratic data,” Geophysics, compressed sensing for rapid MR imaging”, submitted, 2007. Available
vol. 38, pp. 826–844, 1973. at www.stanford.edu/˜mlustig/SparseMRI.pdf

<!-- 第 12 页 -->
TO APPEAR IN THE IEEE JOURNAL OF SELECTED TOPICS IN SIGNAL PROCESSING, 2007. 12

[39] D. Malioutov, M. C¸ etin, and A. Willsky. “Homotopy continuation
for sparse signal representation,” Proceedings of the IEEE Interna-
tional Conference on Acoustics, Speech, and Signal Processing, vol. 5,
pp. 733–736, Philadelphia, PA, 2005.
[40] S. Mallat. A Wavelet Tour of Signal Processing. Academic Press, San
Diego, CA, 1998.
[41] A. Miller, Subset Selection in Regression. Chapman and Hall, London,
2002.
[42] B. Moghaddam, Y. Weiss, and S. Avidan. “Spectral bounds for sparse
PCA: exact and greedy algorithms,” Advances in Neural Information
Processing Systems 18, MIT Press, pp. 915-922, 2006.
[43] J. Mor´e and G. Toraldo. “On the solution of large quadratic program-
ming problems with bound constraints,” SIAM Journal on Optimization,
vol. 1, pp. 93–113, 1991.
[44] J. Nocedal and S. J. Wright. Numerical Optimization, 2nd ed., Springer
Verlag, New York, 2006.
[45] R. Nowak and M. Figueiredo. “Fast wavelet-based image deconvolution
using the EM algorithm”, Proceedings of the 35th Asilomar Conference
on Signals, Systems, and Computers, Monterey, CA, 2001.
[46] M. Osborne, B. Presnell, B. Turlach. “A new approach to variable
selection in least squares problems,” IMA Journal of Numerical Analysis,
vol. 20, pp. 389-403, 2000.
[47] S. Osher, L. Rudin, and E. Fatemi, “Nonlinear total variation based
noise removal algorithms,” Physica D., vol. 60, pp. 259–268, 1992.
[48] C. Paige and M. A. Saunders, “LSQR: An algorithm for sparse linear
equations and sparse least squares,” ACM Transactions on Mathematical
Software, vol. 8, pp. 43–71, 1982.
[49] R. T. Rockafellar, Convex Analysis, Princeton University Press, Prince-
ton, NJ, 1970.
[50] F. Santosa and W. Symes. “Linear invesion of band-limited reﬂection
histograms,” SIAM Journal of Scientiﬁc and Statistical Computing,
vol. 7, pp. 1307–1330, 1986.
[51] M. A. Saunders. ”PDCO: Primal-dual interior-point method for con-
vex objectives,” Systems Optimization Laboratory, Stanford University,
2002. Available at www.stanford.edu/group/SOL/
[52] T. Seraﬁni, G. Zanghirati, L. Zanni. “Gradient projection methods for
large quadratic programs and applications in training support vector
machines,” Optimization Methods and Software, vol. 20, pp. 353–378,
2004.
[53] H. Taylor, S. Bank, J. McCoy. “Deconvolution with the ℓ1 norm,”
Geophysics, vol. 44, pp. 39–52, 1979.
[54] R. Tibshirani. “Regression shrinkage and selection via the lasso,”
Journal Royal Statistical Society B, vol. 58, pp. 267-288, 1996.
[55] J. Tropp, “Just relax: Convex programming methods for identifying
sparse signals,” IEEE Transactions on Information Theory, vol. 51,
pp. 1030–1051, 2006.
[56] J. Tropp, “Greed is good: Algorithmic results for sparse approximation,”
IEEE Transactions on Information Theory, vol. 50, pp. 2231–2242, 2004.
[57] B. Turlach. “On algorithms for solving least squares problems under an
L1 penalty or an L1 constraint,” Proceedings of the American Statistical
Association; Statistical Computing Section, pp. 2572-2577, Alexandria,
VA, 2005.
[58] B. Turlach, W. N. Venables, and S. J. Wright. “Simultaneous variable
selection,” Technometrics, vol. 27, pp. 349–363, 2005.
[59] S. J. Wright. “Implementing proximal point methods for linear pro-
gramming,” Journal of Optimization Theory and Applications, vol. 65,
pp. 531–554, 1990.
[60] S. J. Wright. Primal-Dual Interior-Point Methods, SIAM Publications,
1997.
[61] E. A. Yıldırım and S. J. Wright, “Warm-start strategies in interior-
point methods for linear programming,” SIAM Journal on Optimization,
vol. 12, pp. 782–810, 2002.
