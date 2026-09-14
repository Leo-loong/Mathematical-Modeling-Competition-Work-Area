<!-- 第 1 页 -->

# Polynomial Linear Programming

# with Gaussian Belief Propagation

### Danny Bickson, Yoav Tock Ori Shental Danny Dolev
IBM Haifa Research Lab Center for Magnetic School of Computer Science
Mount Carmel Recording Research and Engineering
Haifa 31905, Israel UCSD, San Diego Hebrew University of Jerusalem
Email: {dannybi,tock}@il.ibm.com 9500 Gilman Drive Jerusalem 91904, Israel
arXiv:0810.1631v1  [cs.IT]  9 Oct 2008 La Jolla, CA 92093, USA Email: dolev@cs.huji.ac.il
Email: oshental@ucsd.edu

Abstract—Interior-point methods are state-of-the-art al- of BP. Globerson et al. [3], [4] assume convexity
gorithms for solving linear programming (LP) problems of the problem and modify the BP update rules
with polynomial complexity. Speciﬁcally, the Karmarkar using dual-coordinate ascent algorithm. Hazan et
algorithm typically solves LP problems in time O(n3.5),
al. [5] describe an algorithm for solving a general
where n is the number of unknown variables. Karmarkar’s
convex free energy minimization. In both cases the
celebrated algorithm is known to be an instance of the
algorithm is guaranteed to converge to the global
log-barrier method using the Newton iteration. The main
computational overhead of this method is in inverting minimum as the problem is tailored to be convex.
the Hessian matrix of the Newton iteration. In this In the present work we take a different path. Un-
contribution, we propose the application of the Gaussian like most of the previous work which uses gradient-
belief propagation (GaBP) algorithm as part of an efﬁcient descent methods, we show how to use interior-point
and distributed LP solver that exploits the sparse and
methods which are shown to have strong advantages
symmetric structure of the Hessian matrix and avoids the
over gradient and steepest descent methods. (For a
need for direct matrix inversion. This approach shifts the
computation from realm of linear algebra to that of proba- comparative study see [6, §9.5,p. 496].) The main
bilistic inference on graphical models, thus applying GaBP beneﬁt of using interior point methods is their
as an efﬁcient inference engine. Our construction is general rapid convergence, which is quadratic once we are
and can be used for any interior-point algorithm which close enough to the optimal solution. Their main
uses the Newton method, including non-linear program
drawback is that they require heavier computational
solvers.
effort for forming and inverting the Hessian ma-
trix, needed for computing the Newton step. To
I. INTRODUCTION
overcome this, we propose the use of Gaussian BP
In recent years, considerable attention has been (GaBP) [7], [8], which is a variant of BP applicable
dedicated to the relation between belief propagation when the underlying distribution is Gaussian. Using
message passing and linear programming schemes. GaBP, we are able to reduce the time associated
This relation is natural since the maximum a- with the Hessian inversion task, from O(n2.5) to
posteriori (MAP) inference problem can be trans- O(nplog(ǫ)/log(γ)) at the worst case, where p < n
lated into integer linear programming (ILP) [1]. is the size of the constraint matrix A, ǫ is the
Weiss et al. [1] approximate the solution to the desired accuracy, and 1/2 < γ < 1 is a parameter
ILP problem by relaxing it to a LP problem using characterizing the matrix A. This computational
convex variational methods. In [2], tree-reweighted saving is accomplished by exploiting the sparsity
belief propagation (BP) is used to ﬁnd the global of the Hessian matrix.
minimum of a convex approximation to the free An additional beneﬁt of our GaBP-based ap-
energy. Both of these works apply discrete forms proach is that the polynomial-complexity LP solver

<!-- 第 2 页 -->
can be implemented in a distributed manner, en- ∆x = −f ′′(˜x)−1f ′(˜x). (5)
abling efﬁcient solution of large-scale problems.
We also provide what we believe is the ﬁrst Denoting the current point ˜x ≜(x, µ, y) and
theoretical analysis of the convergence speed of the the Newton step ∆x ≜(x, y, µ), we compute the
GaBP algorithm. gradient
The paper is organized as follows. In Section
II, we reduce standard linear programming to a f ′(x, µ, y) ≡(∂f(x, µ, y)/∂x, ∂f(x, µ, y)/∂µ,
least-squares problem. Section III shows how to , ∂f(x, µ, y)/∂y)
solve the least-squares problem using the GaBP
algorithm. In Section IV, we extend our construction The Lagrangian is
to the primal-dual method. We give our convergence
results for the GaBP algorithm in Section V, and L(x, µ, y) = cTx−µΣk log xk +yT(b−Ax), (7)
demonstrate our construction in Section VI using
an elementary example. We present our conclusions
in Section VII.
∂L(x, µ, y)
= c −µX−11 −yTA = 0, (8)
II. STANDARD LINEAR PROGRAMMING ∂x
Consider the standard linear program
∂2L(x, µ, y)
cTx = µX−2, (9)
minimizex (1a)
∂x
subject to Ax = b, x ≥0 (1b)
where X ≜diag(x) and 1 is the all-one column
where A ∈Rn×p with rank{A} = p < n. We
vector. Substituting (8)-(9) into (4), we get
assume the problem is solvable with an optimal
x∗assignment. We also assume that the problem c −µX−11 −yTA + µX−2x = 0, (10)
is strictly feasible, or in other words there exists
x ∈Rn that satisﬁes Ax = b and x > 0.
c −µX−11 + xµX−2 = yTA,
(11)
Using the log-barrier method [6, §11.2], one gets
minimizex,µ cTx −µΣnk=1 log xk (2a)
∂L(x, µ, y)
subject to Ax = b. (2b) = Ax = 0. (12)
∂y
This is an approximation to the original problem
(1a). The quality of the approximation improves as Now multiplying (11) by AX2, and using (12) to
the parameter µ →0. eliminate x we get
Now we would like to use the Newton method
AX2ATy = AX2c −µAX1. (13)
in for solving the log-barrier constrained objective
function (2a), described in Table I. Suppose that we
have an initial feasible point x0 for the canonical These normal equations can be recognized as gen-
linear program (1a). We approximate the objective erated from the linear least-squares problem
function (2a) around the current point ˜x using a
miny ||XATy −Xc −µAX1||22. (14)
second-order Taylor expansion
f(˜x + ∆x) ≃f(˜x) + f ′(˜x)∆x + 1/2∆xTf ′′(˜x)∆x.
Solving for y we can compute the Newton direction
(3)
x, taking a step towards the boundary and compose
Finding the optimal search direction ∆x yields the
one iteration of the Newton algorithm. Next, we will
computation of the gradient and compare it to zero
explain how to shift the deterministic LP problem to
∂f the probabilistic domain and solve it distributively
∂∆x = f ′(˜x) + f ′′(˜x)∆x = 0, (4)
using GaBP.

<!-- 第 3 页 -->
TABLE I
THE NEWTON ALGORITHM [6, §9.5.2] .
Given feasible starting point x0 and tolerance ǫ > 0, k = 1
Repeat 1 Compute the Newton step and decrement
∆x = f ′′(x)−1f ′(x), λ2 = f ′(x)T∆x

# 2 Stopping criterion. quit if λ2/2 ≤ǫ
3 Line search. Choose step size t by backtracking line search.

# 4 Update. xk := xk−1 + t∆x, k = k + 1

III. FROM LP TO PROBABILISTIC INFERENCE ψij and self-potentials (‘evidence’) φi. These graph
potentials are determined according to the follow-
We start from the least-squares problem (14),
ing pairwise factorization of the Gaussian distribu-
changing notations to
tion p(x) ∝Qni=1 φi(xi) Q{i,j} ψij(xi, xj), resulting
miny ||Fy −g||22, (15) in ψij(xi, xj) ≜exp(−xiCijxj), and φi(xi) ≜
exp bixi −Ciix2i /2. The set of edges {i, j} cor-
where F ≜XAT, g ≜Xc+µAX1. Now we deﬁne
responds to the set of non-zero entries in C (18).
a multivariate Gaussian Hence, we would like to calculate the marginal
densities, which must also be Gaussian,
p(ˆx) ≜p(x, y) ∝exp(−1/2(Fy −g)TI(Fy −g)).

#### (16) p(xi) ∼N (µi = {C−1g}i, P −1 = {C−1}ii),
i
It is clear that ˆy, the minimizing solution of (15),
is the MAP estimator of the conditional probability ∀i > p,
where µi and Pi are the marginal mean and inverse
ˆy = arg max p(y|x) =
variance (a.k.a. precision), respectively. Recall that,
y
according to [9], the inferred mean µi is identical
= N ((FTF)−1FTg, (FTF)−1). (17) to the desired solution ˆy of (17). The GaBP update
rules are summarized in Table II.
Recent results by Bickson and Shental et al. [7]–
It is known that if GaBP converges, it results in
[9] show that the pseudoinverse problem (17) can
exact inference [10]. However, in contrast to con-
be computed efﬁciently and distributively by using
ventional iterative methods for the solution of sys-
the GaBP algorithm.
tems of linear equations, for GaBP, determining the
The formulation (16) allows us to shift the least-
exact region of convergence and convergence rate
squares problem from an algebraic to a probabilistic
remain open research problems. All that is known is
domain. Instead of solving a deterministic vector-
a sufﬁcient (but not necessary) condition [11], [12]
matrix linear equation, we now solve an inference
stating that GaBP converges when the spectral ra-
problem in a graphical model describing a certain
dius satisﬁes ρ(|IK −A|) < 1. A stricter sufﬁcient
Gaussian distribution function. Following [9] we
condition [10], determines that the matrix A must
deﬁne the joint covariance matrix
be diagonally dominant (i.e. , |aii| > Pj̸=i |aij|, ∀i)
 −I F  in order for GaBP to converge. Convergence speed
C ≜ (18)
FT 0 is discussed in Section V.
and the shift vector b ≜{0T, gT}T ∈R(p+n)×1. IV. EXTENDING THE CONSTRUCTION TO THE
PRIMAL-DUAL METHOD
Given the covariance matrix C and the shift
vector b, one can write explicitly the Gaussian In the previous section we have shown how to
density function, p(ˆx) , and its corresponding graph compute one iteration of the Newton method using
G with edge potentials (‘compatibility functions’) GaBP. In this section we extend the technique for

<!-- 第 4 页 -->
TABLE II
COMPUTING x = A−1b VIA GABP [7].
# Stage Operation
1. Initialize Compute Pii = Aii and µii = bi/Aii.
Set Pki = 0 and µki = 0, ∀k̸ = i.
2. Iterate Propagate Pki and µki, ∀k̸ = i such that Aki̸ = 0.
Compute Pi\j = Pii + Pk∈N(i)\j Pki and µi\j = P −1i\j (Piiµii + Pk∈N(i)\j Pkiµki).
Compute Pij = −AijP −1i\j Aji and µij = −P −1ij Aijµi\j.
3. Check If Pij and µij did not converge, return to #2. Else, continue to #4.
4. Infer Pi = Pii + Pk∈N(i) Pki , µi = P −1(Piiµii + Pk∈N(i) Pkiµki).
i

### 5. Output xi = µi

computing the primal-dual method. This construc- The solution [x(µ), y(µ), z(µ)] of these equations
tion is attractive, since the extended technique has constitutes the central path of solutions to the log-
the same computation overhead. arithmic barrier method [6, 11.2.2]. Applying the
The dual problem ( [13]) conforming to (1a) can Newton method to this system of equations we get
be computed using the Lagrangian
 0 AT I   ∆x   b −Ax
L(x, y, z) = cTx + yT(b −Ax) −zTx, z ≥0, A 0 0 ∆y = c −ATy −z .

Z 0 X ∆z µ1 −Xz
(24)
g(y, z) = infx L(x, y, z), (19a) The solution can be computed explicitly by
subject to Ax = b, x ≥0. (19b)
∆y = (AZ−1XAT)−1·
while (AZ−1X(c −µX−11 −ATy) + b −Ax),
∂L(x, y, z) ∆x = XZ−1(AT∆y + µX−11 = c + ATy),
= c −ATy −z = 0. (20)
∂x ∆z = −AT∆y + c −ATy −z.
Substituting (20) into (19a) we get
The main computational overhead in this method
bTy is the computation of (AZ−1XAT)−1, which is
maximizey
derived from the Newton step in (5).
subject to ATy + z = c, z ≥0.
Now we would like to use GaBP for computing
Primal optimality is obtained using (8) [13] the solution. We make the following simple change
to (24) to make it symmetric: since z > 0, we can
yTA = c −µX−11. (22)
multiply the third row by Z−1 and get a modiﬁed
Substituting (22) in (21a) we get the connection symmetric system
between the primal and dual
 0 AT I   ∆x   b −Ax
µX−11 = z. A 0 0 ∆y = c −ATy −z .

I 0 Z−1X ∆z µZ−11 −X
In total, we have a primal-dual system (again we
assume that the solution is strictly feasible, namely  0 AT I
x > 0, z > 0) Deﬁning ˜A ≜ A 0 0 , and ˜b ≜

I 0 Z−1X
Ax = b, x > 0,
 b −Ax
ATy + z = c, z > 0,
c −ATy −z . one can use GaBP iterative
Xz = µ1.
µZ−11 −X
algorithm shown in Table II.

<!-- 第 5 页 -->
In general, by looking at (4) we see that the dominant, we deﬁne εi to be the non negative gap
solution of each Newton step involves inverting the
εi ≜|Aii| −Σj|Aij| > 0.
Hessian matrix f ′′(x). The state-of-the-art approach
in practical implementations of the Newton step and the following decomposition
is ﬁrst computing the Hessian inverse f ′′(x)−1 by
˜bij = Aij, ˜cij = Aij + εi/|N(i)|,
using a (sparse) decomposition method like (sparse)
Cholesky decomposition, and then multiplying the where |N(i)| is the number of graph neighbors of
result by f ′(x). In our approach, the GaBP al- node i. Following Weiss, we deﬁne γ to be
gorithm computes directly the result ∆x, without |˜bij|
|aij|
computing the full matrix inverse. Furthermore, if γ = max |˜cij| = |aij| + εi/|N(i)| =
i,j
the GaBP algorithm converges, the computation of
∆x is guaranteed to be accurate. 1
= max 1 + (εi)/(|aij||N(i)|) < 1. (25)
i,j
V. NEW CONVERGENCE RESULTS
In total, we get that for a desired accuracy of ǫ||b||∞
In this section we give an upper bound on the we need to iterate for t = ⌈log(ǫ)/log(γ)⌉rounds.
convergence rate of the GaBP algorithm. As far as Note that this is an upper bound and in practice
we know this is the ﬁrst theoretical result bounding we indeed have observed a much faster convergence
the convergence speed of the GaBP algorithm. rate.
Our upper bound is based on the work of Weiss The computation of the parameter γ can be easily
et al. [10, Claim 4], which proves the correctness done in a distributed manner: Each node locally
of the mean computation. Weiss uses the pairwise computes εi, and γi = maxj 1/(1 + |aij|εi/N(i)).
potentials form1, where
Finally, one maximum operation is performed glob-
ally, γ = maxi γi.
p(x) ∝ Πi,jψij(xi, xj)Πiψi(xi),
ψi,j(xi, xj) ≡ exp(−1/2(xi xj)TVij(xi xj)), A. Applications to Interior-Point Methods
 ˜bij  We would like to compare the running time of
˜aij
Vij ≡ . our proposed method to the Newton interior-point
˜bji ˜cij
method, utilizing our new convergence results of
Assuming the optimal solution is x∗, for a desired the previous section. As a reference we take the
accuracy ǫ||b||∞where ||b||∞≡maxi |bi|, and b is Karmarkar algorithm [14] which is known to be
the shift vector, we need to run the algorithm for at an instance of the Newton method [15]. Its running
most t = ⌈log(ǫ)/log(β)⌉rounds to get an accuracy time is composed of n rounds, where on each round
of |x∗−xt| < ǫ||b||∞where β = maxij |˜bij/˜cij|.
one Newton step is computed. The cost of comput-
The problem with applying Weiss’ result directly ing one Newton step on a dense Hessian matrix is
to our model is that we are working with different O(n2.5), so the total running time is O(n3.5).
parameterizations. We use the information form Using our approach, the total number of Newton
p(x) ∝exp(−1/2xTAx+bTx). The decomposition iterations, n, remains the same as in the Karmarkar
of the matrix A into pairwise potentials is not algorithm. However, we exploit the special structure
unique. In order to use Weiss’ result, we propose of the Hessian matrix, which is both symmetric
such a decomposition. Any decomposition from and sparse. Assuming that the size of the constraint
the canonical form to the pairwise potentials form matrix A is n × p, p < n, each iteration of
should be subject to the following constraints [10] GaBP for computing a single Newton step takes
O(np), and based on our new convergence analysis
˜bij = Aij, Σj˜cij = Aii.
for accuracy ǫ||b||∞we need to iterate for r =
We propose to initialize the pairwise potentials as ⌈log(ǫ)/log(γ)⌉rounds, where γ is deﬁned in (25).
following. Assuming the matrix A is diagonally The total computational burden for a single Newton
step is O(nplog(ǫ)/log(γ)). There are at most n
1Weiss assumes scalar variables with zero means. rounds, hence in total we get O(n2plog(ǫ)/log(γ)).

<!-- 第 6 页 -->
an iterative algorithm, the Gaussian belief propaga-

### 1.2

tion algorithm. Unlike previous approaches which
use discrete belief propagation and gradient descent
1
methods, we take a different path by using con-

## 0.8 tinuous belief propagation applied to interior-point
methods. By shifting the Hessian matrix inverse
x2 0.6 computation required by the Newton method, from
linear algebra domain to the probabilistic domain,

## 0.4 we gain a signiﬁcant speedup in performance of
the Newton method. We believe there are numerous

## 0.2 applications that can beneﬁt from our new approach.

# 0 ACKNOWLEDGEMENT

# 0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9
x1
Fig. 1. A simple example of using GaBP for solving linear O. Shental acknowledges the partial support of
programming with two variables and eleven constraints. Each red
the NSF (Grant CCF-0514859). D. Bickson would
circle shows one iteration of the Newton method.
like to thank Nati Linial from the Hebrew University
of Jerusalem for proposing this research direction.
The authors are grateful to Jack Wolf and Paul
VI. EXPERIMENTAL RESULTS
Siegel from UCSD for useful discussions and for
We demonstrate the applicability of the proposed constructive comments on the manuscript.
algorithm using the following simple linear program
borrowed from [16] REFERENCES
maximize x1 + x2 [1] C. Yanover, T. Meltzer, and Y. Weiss, “Linear programming
2px1 + x2 ≤p2 + 1 , relaxations and belief propagation – an empirical study,” in
subject to
Journal of Machine Learning Research, vol. 7. Cambridge,
p = 0.0, 0.1, · · · , 1.0 . MA, USA: MIT Press, 2006, pp. 1887–1907.
[2] Y. Weiss, C. Yanover, and T. Meltzer, “Map estimation, linear
programming and belief propagation with convex free energies,”
Fig. 1 shows execution of the afﬁne-scaling al-
in The 23th Conference on Uncertainty in Artiﬁcial Intelligence
gorithm [17], a variant of Karmarkar’s algorithm (UAI), 2007.
[14], on a small problem with two variables and [3] A. Globerson and T. Jaakkola, “Fixing max-product: Conver-
gent message passing algorithms for map lp-relaxations,” in
eleven constraints. Each circle is one Newton step.
Advances in Neural Information Processing Systems (NIPS),
The inverted Hessian is computed using the GaBP no. 21, Vancouver, Canada, 2007.
algorithm, using two computing nodes. Matlab code [4] M. Collins, A. Globerson, T. Koo, X. Carreras, and P. Bartlett,
for this example can be downloaded from [18]. “Exponentiated gradient algorithms for conditional random
ﬁelds and max-margin markov networks,” in Journal of Ma-
Regarding larger scale problems, we have ob-
chine Learning Research. Accepted for publication, 2008.
served rapid convergence (of a single Newton step [5] T. Hazan and A. Shashua, “Convergent message-passing al-
computation) on very large scale problems. For gorithms for inference over general graphs with convex free
energy,” in The 24th Conference on Uncertainty in Artiﬁcial
example, [19] demonstrates convergence of 5-10
Intelligence (UAI), Helsinki, July 2008.
rounds on sparse constraint matrices with several [6] S. Boyd and L. Vandenberghe, Convex Optimization. Cam-
millions of variables. [20] shows convergence of bridge University Press, March 2004.
[7] O. Shental, D. Bickson, P. H. Siegel, J. K. Wolf, and D. Dolev,
dense constraint matrices of size up to 150, 000 ×
“Gaussian belief propagation solver for systems of linear equa-
150, 000 in 6 rounds, where the algorithm is run in tions,” in IEEE Int. Symp. on Inform. Theory (ISIT), Toronto,
parallel using 1,024 CPUs. Empirical comparison Canada, July 2008.
[8] D. Bickson, O. Shental, P. H. Siegel, J. K. Wolf, and D. Dolev,
with other iterative algorithms is given in [8].
“Linear detection via belief propagation,” in Proc. 45th Allerton
Conf. on Communications, Control and Computing, Monticello,
VII. CONCLUSION IL, USA, Sept. 2007.
[9] ——, “Gaussian belief propagation based multiuser detection,”
In this paper we have shown how to efﬁciently
in IEEE Int. Symp. on Inform. Theory (ISIT), Toronto, Canada,
and distributively solve interior-point methods using July 2008.

<!-- 第 7 页 -->
[10] Y. Weiss and W. T. Freeman, “Correctness of belief propagation
in Gaussian graphical models of arbitrary topology,” Neural
Computation, vol. 13, no. 10, pp. 2173–2200, 2001.
[11] J. K. Johnson, D. M. Malioutov, and A. S. Willsky, “Walk-
sum interpretation and analysis of Gaussian belief propagation,”
in Advances in Neural Information Processing Systems 18,
Y. Weiss, B. Sch¨olkopf, and J. Platt, Eds. Cambridge, MA:
MIT Press, 2006, pp. 579–586.
[12] D. M. Malioutov, J. K. Johnson, and A. S. Willsky, “Walk-sums
and belief propagation in Gaussian graphical models,” Journal
of Machine Learning Research, vol. 7, Oct. 2006.
[13] S. Portnoy and R. Koenker, “The gaussian hare and the laplacian
tortoise: Computability of squared- error versus absolute-error
estimators,” in Statistical Science, vol. 12, no. 4. Institute of
Mathematical Statistics, 1997, pp. 279–296.
[14] N. Karmarkar, “A new polynomial-time algorithm for linear
programming,” in STOC ’84: Proceedings of the sixteenth
annual ACM symposium on Theory of computing. New York,
NY, USA: ACM, 1984, pp. 302–311.
[15] D. A. Bayer and J. C. Lagarias, “Karmarkar’s linear pro-
gramming algorithm and newton’s method,” in Mathematical
Programming, vol. 50, no. 1, March 1991, pp. 291–330.
[16] http://en.wikipedia.org/wiki/Karmarkar’s_algorithm.
[17] R. J. Vanderbei, M. S. Meketon, and B. A. Freedman, “A
modiﬁcation of karmarkar’s linear programming algorithm,” in
Algorithmica, vol. 1, no. 1, March 1986, pp. 395–407.
[18] http://www.cs.huji.ac.il/labs/danss/p2p/gabp/.
[19] D. Bickson and D. Malkhi, “A unifying framework for rating
users and data items in peer-to-peer and social networks,”
in Peer-to-Peer Networking and Applications (PPNA) Journal,
Springer-Verlag, April 2008.
[20] D. Bickson, D. Dolev, and E. Yom-Tov, “A gaussian belief
propagation solver for large scale support vector machines,”
in 5th European Conference on Complex Systems, Jerusalem,
Sept. 2008.
