<!-- 第 1 页 -->
This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.

1

# Bayesian Compressive Sensing

# via Belief Propagation

### Dror Baron,1 Shriram Sarvotham,2 and Richard G. Baraniuk 3

Copyright (c) 2008 IEEE. Personal use of this material is permitted. However,
permission to use this material for any other purposes must be obtained from

### the IEEE by sending a request to pubs-permissions@ieee.org.

1Department of Electrical Engineering, Technion – Israel Institute of Technology; Haifa, Israel
2Halliburton; Houston, TX
3Department of Electrical and Computer Engineering, Rice University; Houston, TX

June 23, 2009 DRAFT
Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore.  Restrictions apply.

<!-- 第 2 页 -->
This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.

Abstract

Compressive sensing (CS) is an emerging ﬁeld based on the revelation that a small collection of lin-
ear projections of a sparse signal contains enough information for stable, sub-Nyquist signal acquisition.
When a statistical characterization of the signal is available, Bayesian inference can complement conven-
tional CS methods based on linear programming or greedy algorithms. We perform approximate Bayesian
inference using belief propagation (BP) decoding, which represents the CS encoding matrix as a graphical
model. Fast computation is obtained by reducing the size of the graphical model with sparse encoding
matrices. To decode a length-N signal containing K large coefﬁcients, our CS-BP decoding algorithm uses
O(K log(N)) measurements and O(N log2(N)) computation. Finally, although we focus on a two-state
mixture Gaussian model, CS-BP is easily adapted to other signal models.

I. INTRODUCTION

Many signal processing applications require the identiﬁcation and estimation of a few signiﬁcant coefﬁ-
cients from a high-dimensional vector. The wisdom behind this is the ubiquitous compressibility of signals:
in an appropriate basis, most of the information contained in a signal often resides in just a few large co-
efﬁcients. Traditional sensing and processing ﬁrst acquires the entire data, only to later throw away most
coefﬁcients and retain the few signiﬁcant ones [2]. Interestingly, the information contained in the few large
coefﬁcients can be captured (encoded) by a small number of random linear projections [3]. The ground-
breaking work in compressive sensing (CS) [4–6] has proved for a variety of settings that the signal can then
be decoded in a computationally feasible manner from these random projections.

A. Compressive sensing

Sparsity and random encoding: In a typical compressive sensing (CS) setup, a signal vector x ∈RN
has the form x = Ψθ, where Ψ ∈RN×N is an orthonormal basis, and θ ∈RN satisﬁes ∥θ∥0 = K ≪N.1
Owing to the sparsity of x relative to the basis Ψ, there is no need to sample all N values of x. Instead, the
CS theory establishes that x can be decoded from a small number of projections onto an incoherent set of
measurement vectors [4, 5]. To measure (encode) x, we compute M ≪N linear projections of x via the
matrix-vector multiplication y = Φx where Φ ∈RM×N is the encoding matrix.
In addition to strictly sparse signals where ∥θ∥0 ≤K, other signal models are possible. Approximately
sparse signals have K ≪N large coefﬁcients, while the remaining coefﬁcients are small but not necessarily
zero. Compressible signals have coefﬁcients that, when sorted, decay quickly according to a power law.
1We use ∥· ∥0 to denote the ℓ0 “norm” that counts the number of non-zero elements.

Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore.  Restrictions apply.

<!-- 第 3 页 -->
This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.

Similarly, both noiseless and noisy signals and measurements may be considered. We emphasize noiseless
measurement of approximately sparse signals in the paper.
Decoding via sparsity: Our goal is to decode x given y and Φ. Although decoding x from y =
Φx appears to be an ill-posed inverse problem, the prior knowledge of sparsity in x enables to decode x
from M ≪N measurements. Decoding often relies on an optimization, which searches for the sparsest
coefﬁcients θ that agree with the measurements y. If M is sufﬁciently large and θ is strictly sparse, then θ
is the solution to the ℓ0 minimization:

bθ = arg min ∥θ∥0 s.t. y = ΦΨθ.

Unfortunately, solving this ℓ0 optimization is NP-complete [7].
The revelation that supports the CS theory is that a computationally tractable optimization problem
yields an equivalent solution. We need only solve for the ℓ1-sparsest coefﬁcients that agree with the mea-
surements y [4, 5]:
bθ = arg min ∥θ∥1 s.t. y = ΦΨθ, (1)
as long as ΦΨ satisﬁes some technical conditions, which are satisﬁed with overwhelming probability when
the entries of Φ are independent and identically distributed (iid) sub-Gaussian random variables [4]. This ℓ1
optimization problem (1), also known as Basis Pursuit [8], can be solved with linear programming methods.
The ℓ1 decoder requires only M = O(K log(N/K)) projections [9, 10]. However, encoding by a dense
Gaussian Φ is slow, and ℓ1 decoding requires cubic computation in general [11].

B. Fast CS decoding

While ℓ1 decoders ﬁgure prominently in the CS literature, their cubic complexity still renders them
impractical for many applications. For example, current digital cameras acquire images with N = 106
pixels or more, and fast decoding is critical. The slowness of ℓ1 decoding has motivated a ﬂurry of research
into faster algorithms.
One line of research involves iterative greedy algorithms. The Matching Pursuit (MP) [12] algorithm,
for example, iteratively selects the vectors from the matrix ΦΨ that contain most of the energy of the mea-
surement vector y. MP has been proven to successfully decode the acquired signal with high probabil-
ity [12, 13]. Algorithms inspired by MP include OMP [12], tree matching pursuit [14], stagewise OMP [15],
CoSaMP [16], IHT [17], and Subspace Pursuit [18] have been shown to attain similar guarantees to those of
their optimization-based counterparts [19–21].

Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore.  Restrictions apply.

<!-- 第 4 页 -->
This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.

While the CS algorithms discussed above typically use a dense Φ matrix, a class of methods has
emerged that employ structured Φ. For example, subsampling an orthogonal basis that admits a fast im-
plicit algorithm also leads to fast decoding [4]. Encoding matrices that are themselves sparse can also be
used. Cormode and Muthukrishnan proposed fast streaming algorithms based on group testing [22, 23],
which considers subsets of signal coefﬁcients in which we expect at most one “heavy hitter” coefﬁcient
to lie. Gilbert et al. [24] propose the Chaining Pursuit algorithm, which works best for extremely sparse
signals.

C. Bayesian CS

CS decoding algorithms rely on the sparsity of the signal x. In some applications, a statistical character-
ization of the signal is available, and Bayesian inference offers the potential for more precise estimation of
x or a reduction in the number of CS measurements. Ji et al. [25] have proposed a Bayesian CS framework
where relevance vector machines are used for signal estimation. For certain types of hierarchical priors,
their method can approximate the posterior density of x and is somewhat faster than ℓ1 decoding. Seeger
and Nickisch [26] extend these ideas to experimental design, where the encoding matrix is designed sequen-
tially based on previous measurements. Another Bayesian approach by Schniter et al. [27] approximates
conditional expectation by extending the maximal likelihood approach to a weighted mixture of the most
likely models. There are also many related results on application of Bayesian methods to sparse inverse
problems (c.f. [28] and references therein).
Bayesian approaches have also been used for multiuser decoding (MUD) in communications. In MUD,
users modulate their symbols with different spreading sequences, and the received signals are superpositions
of sequences. Because most users are inactive, MUD algorithms extract information from a sparse super-
position in a manner analogous to CS decoding. Guo and Wang [29] perform MUD using sparse spreading
sequences and decode via belief propagation (BP) [30–35]; our paper also uses sparse encoding matrices
and BP decoding. A related algorithm for decoding low density lattice codes (LDLC) by Sommer et al. [36]
uses BP on a factor graph whose self and edge potentials are Gaussian mixtures. Convergence results for
the LDLC decoding algorithm have been derived for Gaussian noise [36].

D. Contributions

In this paper, we develop a sparse encoder matrix Φ and a belief propagation (BP) decoder to accelerate
CS encoding and decoding under the Bayesian framework. We call our algorithm CS-BP. Although we
emphasize a two-state mixture Gaussian model as a prior for sparse signals, CS-BP is ﬂexible to variations

Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore.  Restrictions apply.

<!-- 第 5 页 -->
This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.

in the signal and measurement models.
Encoding by sparse CS matrix: The dense sub-Gaussian CS encoding matrices [4, 5] are reminiscent
of Shannon’s random code constructions. However, although dense matrices capture the information content
of sparse signals, they may not be amenable to fast encoding and decoding. Low density parity check (LDPC)
codes [37, 38] offer an important insight: encoding and decoding are fast, because multiplication by a sparse
matrix is fast; nonetheless, LDPC codes achieve rates close to the Shannon limit. Indeed, in a previous
paper [39], we used an LDPC-like sparse Φ for the special case of noiseless measurement of strictly sparse
signals; similar matrices were also proposed for CS by Berinde and Indyk [40]. Although LDPC decoding
algorithms may not have provable convergence, the recent extension of LDPC to LDLC codes [36] offers
provable convergence, which may lead to similar future results for CS decoding.
We encode (measure) the signal using sparse Rademacher ({0, 1, −1}) LDPC-like Φ matrices. Because
entries of Φ are restricted to {0, 1, −1}, encoding only requires sums and differences of small subsets of
coefﬁcient values of x. The design of Φ, including characteristics such as column and row weights, is based
on the relevant signal and measurement models, as well as the accompanying decoding algorithm.
Decoding by BP: We represent the sparse Φ as a sparse bipartite graph. In addition to accelerating the
algorithm, the sparse structure reduces the number of loops in the graph and thus assists the convergence
of a message passing method that solves a Bayesian inference problem. Our estimate for x explains the
measurements while offering the best match to the prior. We employ BP in a manner similar to LDPC
channel decoding [34, 37, 38]. To decode a length-N signal containing K large coefﬁcients, our CS-BP
decoding algorithm uses M = O(K log(N)) measurements and O(N log2(N)) computation. Although
CS-BP is not guaranteed to converge, numerical results are quite favorable.
The remainder of the paper is organized as follows. Section II deﬁnes our signal model, and Section III
describes our sparse CS-LDPC encoding matrix. The CS-BP decoding algorithm is described in Section IV,
and its performance is demonstrated numerically in Section V. Variations and applications are discussed in
Section VI, and Section VII concludes.

II. MIXTURE GAUSSIAN SIGNAL MODEL

We focus on a two-state mixture Gaussian model [41–43] as a prior that succinctly captures our prior
knowledge about approximate sparsity of the signal. Bayesian inference using a two-state mixture model has
been studied well before the advent of CS, for example by George and McCulloch [44] and Geweke [45];
the model was proposed for CS in [1] and also used by He and Carin [46]. More formally, let X =
[X(1), . . . , X(N)] be a random vector in RN, and consider the signal x = [x(1), . . . , x(N)] as an outcome

Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore.  Restrictions apply.

<!-- 第 6 页 -->
This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.

Pr(Q = 0) Pr(Q = 1)
f(X)

|||||
|---|---|

## ⇒

Fig. 1. Mixture Gaussian model for signal coefﬁcients. The distribution of X conditioned on the two state variables,
Q = 0 and Q = 1, is depicted. Also shown is the overall distribution for X.

of X. Because our approximately sparse signal consists of a small number of large coefﬁcients and a large
number of small coefﬁcients, we associate each probability density function (pdf) f(X(i)) with a state
variable Q(i) that can take on two values. Large and small magnitudes correspond to zero mean Gaussian
distributions with high and low variances, which are implied by Q(i) = 1 and Q(i) = 0, respectively,

f(X(i)|Q(i) = 1) ∼N(0, σ21) and f(X(i)|Q(i) = 0) ∼N(0, σ20),

with σ21 > σ20. Let Q = [Q(1), . . . , Q(N)] be the state random vector associated with the signal; the actual
conﬁguration q = [q(1), . . . , q(N)] ∈{0, 1}N is one of 2N possible outcomes. We assume that the Q(i)’s
are iid.2 To ensure that we have approximately K large coefﬁcients, we choose the probability mass function
(pmf) of the state variable Q(i) to be Bernoulli with Pr (Q(i) = 1) = S and Pr (Q(i) = 0) = 1 −S, where
S = K/N is the sparsity rate.
The resulting model for signal coefﬁcients is a two-state mixture Gaussian distribution, as illustrated in
Figure 1. This mixture model is completely characterized by three parameters: the sparsity rate S and the
variances σ20 and σ21 of the Gaussian pdf’s corresponding to each state.
Mixture Gaussian models have been successfully employed in image processing and inference prob-
lems, because they are simple yet effective in modeling real-world signals [41–43]. Theoretical connections
have also been made between wavelet coefﬁcient mixture models and the fundamental parameters of Besov
spaces, which have proved invaluable for characterizing real-world images. Moreover, arbitrary densities
with a ﬁnite number of discontinuities can be approximated arbitrarily closely by increasing the number of
states and allowing non-zero means [47]. We leave these extensions for future work, and focus on two-state
mixture Gaussian distributions for modeling the signal coefﬁcients.
2The model can be extended to capture dependencies between coefﬁcients, as suggested by Ji et al. [25].

Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore.  Restrictions apply.

<!-- 第 7 页 -->
This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.

Prior Mixing

|Col1|Col2|Mixing|
|---|---|---|
|||Measur<br><br><br>Encoding|
||||
||||
||||
||||
||||
||||

States Coefficients
Q X
Fig. 2. Factor graph depicting the relationship between variable nodes (black) and constraint nodes (white) in CS-BP.

III. SPARSE ENCODING

Sparse CS encoding matrix: We use a sparse Φ matrix to accelerate both CS encoding and decoding.
Our CS encoding matrices are dominated by zero entries, with a small number of non-zeros in each row
and each column. We focus on CS-LDPC matrices whose non-zero entries are {−1, 1};3 each measurement
involves only sums and differences of a small subset of coefﬁcients of x. Although the coherence between
a sparse Φ and Ψ, which is the maximal inner product between rows of Φ and Ψ, may be higher than
the coherence using a dense Φ matrix [48], as long as Φ is not too sparse (see Theorem 1 below) the
measurements capture enough information about x to decode the signal. A CS-LDPC Φ can be represented
as a bipartite graph G, which is also sparse. Each edge of G connects a coefﬁcient node x(i) to an encoding
node y(j) and corresponds to a non-zero entry of Φ (Figure 2).
In addition to the core structure of Φ, we can introduce other constraints to tailor the measurement
process to the signal model. The constant row weight constraint makes sure that each row of Φ contains
exactly L non-zero entries. The row weight L can be chosen based on signal properties such as sparsity,
possible measurement noise, and details of the decoding process. Another option is to use a constant column
weight constraint, which ﬁxes the number of non-zero entries in each column of Φ to be a constant R.
Although our emphasis is on noiseless measurement of approximately sparse signals, we brieﬂy discuss
noisy measurement of a strictly sparse signal, and show that a constant row weight L ensures that the
measurements are approximated by two-state mixture Gaussians. To see this, consider a strictly sparse x
3CS-LDPC matrices are slightly different from LDPC parity check matrices, which only contain the binary entries 0 and 1. We
have observed numerically that allowing negative entries offers improved performance. At the expense of additional computation,
further minor improvement can be attained using sparse matrices with Gaussian non-zero entries.

Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore.  Restrictions apply.

<!-- 第 8 页 -->
This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.

with sparsity rate S and Gaussian variance σ21. We now have y = Φx + z, where z ∼N(0, σ2Z) is additive
white Gaussian noise (AWGN) with variance σ2Z. In our approximately sparse setting, each row of Φ picks
up ≈L(1 −S) small magnitude coefﬁcients. If L(1 −S)σ20 ≈σ2Z, then the few large coefﬁcients will be
obscured by similar noise artifacts.
Our deﬁnition of Φ relies on the implicit assumption that x is sparse in the canonical sparsifying basis,
i.e., Ψ = I. In contrast, if x is sparse in some other basis Ψ, then more complicated encoding matrices may
be necessary. We defer the discussion of these issues to Section VI, but emphasize that in many practical
situations our methods can be extended to support the sparsifying basis Ψ in a computationally tractable
manner.
Information content of sparsely encoded measurements: The sparsity of our CS-LDPC matrix may
yield measurements y that contain less information about the signal x than a dense Gaussian Φ. The follow-
ing theorem, whose proof appears in the Appendix, veriﬁes that y retains enough information to decode x
 2
well. As long as S = K/N = Ω σ0 , then M = O(K log(N)) measurements are sufﬁcient.
σ1
Theorem 1: Let x be a two-state mixture Gaussian signal with sparsity rate S = K/N and variances
σ20 and σ21, and let Φ be a CS-LDPC matrix with constant row weight L = η ln(SN1+γ)
, where η, γ > 0. If
S
(1 + 2η−1)(1 + γ) " σ0 2# !
M = O 2K + (N −K) log(N) , (2)
µ2 σ1
then x can be decoded to bx such that ∥x −bx∥∞< µσ1 with probability 1 −2N −γ.
The proof of Theorem 1 relies on a result by Wang et al. [49, Theorem 1]. Their proof partitions Φ into
M2 sub-matrices of M1 rows each, and estimates each bxi as a median of inner products with sub-matrices.
The ℓ∞performance guarantee relies on the union bound; a less stringent guarantee yields a reduction
in M2. Moreover, L can be reduced if we increase the number of measurements accordingly. Based on
numerical results, we propose the following modiﬁed values as rules of thumb,

L ≈S−1 = N/K,
M = O(K log(N)), and R = LM/N = O(log(N)). (3)

Noting that each measurement requires O(L) additions and subtractions, and using our rules of thumb for L
and M (3), the computation required for encoding is O(LM) = O(N log(N)), which is signiﬁcantly lower
than the O(MN) = O(KN log(N)) required for dense Gaussian Φ.

IV. CS-BP DECODING OF APPROXIMATELY SPARSE SIGNALS

Decoding approximately sparse random signals can be treated as a Bayesian inference problem. We
observe the measurements y = Φx, where x is a mixture Gaussian signal. Our goal is to estimate x given

Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore.  Restrictions apply.

<!-- 第 9 页 -->
This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.

Φ and y. Because the set of equations y = Φx is under-determined, there are inﬁnitely many solutions. All
solutions lie along a hyperplane of dimension N −M. We locate the solution within this hyperplane that
best matches our prior signal model. Consider the minimum mean square error (MMSE) and maximum a
posteriori (MAP) estimates,

bxMMSE = arg minx′ E∥X −x′∥2 s.t. y = Φx′,
2
bxMAP = arg max f(X = x′) s.t. y = Φx′,
x′

where the expectation is taken over the prior distribution for X. The MMSE estimate can be expressed as
the conditional mean, bxMMSE = E [X|Y = y], where Y ∈RM is the random vector that corresponds to
the measurements. Although the precise computation of bxMMSE may require the evaluation of 2N terms,
a close approximation to the MMSE estimate can be obtained using the (usually small) set of state con-
ﬁguration vectors q with dominant posterior probability [27]. Indeed, exact inference in graphical models
is NP-hard [50], because of loops in the graph induced by Φ. However, the sparse structure of Φ reduces
the number of loops and enables us to use low-complexity message-passing methods to estimate x approxi-
mately.

A. Decoding algorithm

We now employ belief propagation (BP), an efﬁcient method for solving inference problems by itera-
tively passing messages over graphical models [30–35]. Although BP has not been proved to converge, for
graphs with few loops it often offers a good approximation to the solution to the MAP inference problem.
BP relies on factor graphs, which enable fast computation of global multivariate functions by exploiting the
way in which the global function factors into a product of simpler local functions, each of which depends
on a subset of variables [51].
Factor graph for CS-BP: The factor graph shown in Figure 2 captures the relationship between the
states q, the signal coefﬁcients x, and the observed CS measurements y. The graph is bipartite and contains
two types of vertices; all edges connect variable nodes (black) and constraint nodes (white). There are three
types of variable nodes corresponding to state variables Q(i), coefﬁcient variables X(i), and measurement
variables Y (j). The factor graph also has three types of constraint nodes, which encapsulate the dependen-
cies that their neighbors in the graph (variable nodes) are subjected to. First, prior constraint nodes impose
the Bernoulli prior on state variables. Second, mixing constraint nodes impose the conditional distribution
on coefﬁcient variables given the state variables. Third, encoding constraint nodes impose the encoding
matrix structure on measurement variables.

Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore.  Restrictions apply.

<!-- 第 10 页 -->
This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.

Message passing: CS-BP approximates the marginal distributions of all coefﬁcient and state variables
in the factor graph, conditioned on the observed measurements Y , by passing messages between variable
nodes and constraint nodes. Each message encodes the marginal distributions of a variable associated with
one of the edges. Given the distributions Pr(Q(i)|Y = y) and f(X(i)|Y = y), one can extract MAP and
MMSE estimates for each coefﬁcient.
Denote the message sent from a variable node v to one of its neighbors in the bipartite graph, a constraint
node c, by µv−→c(v); a message from c to v is denoted by µc−→v(v). The message µv−→c(v) is updated by
taking the product of all messages received by v on all other edges. The message µc−→v(v) is computed in a
similar manner, but the constraint associated with c is applied to the product and the result is marginalized.
More formally,
Y
µv−→c(v) = µu−→v(v), (4)
u∈n(v)\{c}

X Y
µc−→v(v) = con(n(c)) µw−→c(w), (5)
∼{v} w∈n(c)\{v}
where n(v) and n(c) are sets of neighbors of v and c, respectively, con(n(c)) is the constraint on the set
of variable nodes n(c), and ∼{v} is the set of neighbors of c excluding v. We interpret these 2 types of
message processing as multiplication of beliefs at variable nodes (4) and convolution at constraint nodes (5).
Finally, the marginal distribution f(v) for a given variable node is obtained from the product of all the most
recent incoming messages along the edges connecting to that node,
Y
f(v) = µu−→v(v). (6)
u∈n(v)
Based on the marginal distribution, various statistical characterizations can be computed, including MMSE,
MAP, error bars, and so on.
We also need a method to encode beliefs. One method is to sample the relevant pdf’s uniformly and then
use the samples as messages. Another encoding method is to approximate the pdf by a mixture Gaussian
with a given number of components, where mixture parameters are used as messages. These two methods
offer different trade-offs between modeling ﬂexibility and computational requirements; details appear in
Sections IV-B and IV-C. We leave alternative methods such as particle ﬁlters and importance sampling for
future research.
Protecting against loopy graphs and message quantization errors: BP converges to the exact con-
ditional distribution in the ideal situation where the following conditions are met: (i) the factor graph is
cycle-free; and (ii) messages are processed and propagated without errors. In CS-BP decoding, both condi-
tions are violated. First, the factor graph is loopy — it contains cycles. Second, message encoding methods

Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore.  Restrictions apply.

<!-- 第 11 页 -->
This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.

introduce errors. These non-idealities may lead CS-BP to converge to imprecise conditional distributions,
or more critically, lead CS-BP to diverge [52–54]. To some extent these problems can be reduced by (i)
using CS-LDPC matrices, which have a relatively modest number of loops; and (ii) carefully designing our
message encoding methods (Sections IV-B and IV-C). We stabilize CS-BP against these non-idealities using
message damped belief propagation (MDBP) [55], where messages are weighted averages between old and
new estimates. Despite the damping, CS-BP is not guaranteed to converge, and yet the numerical results of
Section V demonstrate that its performance is quite promising. We conclude with a prototype algorithm;
Matlab code is available at http://dsp.rice.edu/CSBP.

CS-BP Decoding Algorithm

1) Initialization: Initialize the iteration counter i = 1. Set up data structures for factor graph messages
µv−→c(v) and µc−→v(v). Initialize messages µv−→c(v) from variable to constraint nodes with the
signal prior.
2) Convolution: For each measurement c = 1, . . . , M, which corresponds to constraint node c, compute
µc−→v(v) via convolution (5) for all neighboring variable nodes n(c). If measurement noise is present,
then convolve further with a noise prior. Apply damping methods such as MDBP [55] by weighting
the new estimates from iteration i with estimates from previous iterations.
3) Multiplication: For each coefﬁcient v = 1, . . . , N, which corresponds to a variable node v, compute
µv−→c(v) via multiplication (4) for all neighboring constraint nodes n(v). Apply damping methods
as needed. If the iteration counter has yet to reach its maximal value, then go to Step 2.
4) Output: For each coefﬁcient v = 1, . . . , N, compute MMSE or MAP estimates (or alternative statis-
tical characterizations) based on the marginal distribution f(v) (6). Output the requisite statistics.

B. Samples of the pdf as messages

Having described main aspects of the CS-BP decoding algorithm, we now focus on the two message
encoding methods, starting with samples. In this method, we sample the pdf and send the samples as
messages. Multiplication of pdf’s (4) corresponds to point-wise multiplication of messages; convolution (5)
is computed efﬁciently in the frequency domain.4
The main advantage of using samples is ﬂexibility to different prior distributions for the coefﬁcients; for
example, mixture Gaussian priors are easily supported. Additionally, both multiplication and convolution are
computed efﬁciently. However, sampling has large memory requirements and introduces quantization errors
4Fast convolution via FFT has been used in LDPC decoding over GF(2q) using BP [34].

Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore.  Restrictions apply.

<!-- 第 12 页 -->
This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.

that reduce precision and hamper the convergence of CS-BP [52]. Sampling also requires ﬁner sampling for
precise decoding; we propose to sample the pdf’s with a spacing less than σ0.
We analyze the computational requirements of this method. Let each message be a vector of p sam-
ples. Each iteration performs multiplication at coefﬁcient nodes (4) and convolution at constraint nodes (5).
Outgoing messages are modiﬁed,
Qu∈n(v) µu−→v(v) Qw∈n(c) µw−→c(w) !
X
µv−→c(v) = and µc−→v(v) = con(n(c)) , (7)
µc−→v(v) µv−→c(v)
∼{v}
where the denominators are non-zero, because mixture Gaussian pdf’s are strictly positive. The modiﬁca-
tions (7) reduce computation, because the numerators are computed once and then reused for all messages
leaving the node being processed.
Assuming that the column weight R is ﬁxed (Section III), the computation required for message pro-
cessing at a variable node is O(Rp) per iteration, because we multiply R+1 vectors of length p. With O(N)
variable nodes, each iteration requires O(NRp) computation. For constraint nodes, we perform convolution
in the frequency domain, and so the computational cost per node is O(Lp log(p)). With O(M) constraint
nodes, each iteration is O(LMp log(p)). Accounting for both variable and constraint nodes, each iteration
is O(NRp + LMp log(p)) = O(p log(p)N log(N)), where we employ our rules of thumb for L, M, and
R (3). To complete the computational analysis, we note ﬁrst that we use O(log(N)) CS-BP iterations,
which is proportional to the diameter of the graph [56]. Second, sampling the pdf’s with a spacing less than
σ0, we choose p = O(σ1/σ0) to support a maximal amplitude on the order of σ1. Therefore, our overall

computation is O σ0 logσ1 σ1 N log2(N) , which scales as O(N log2(N)) when σ0 and σ1 are constant.
σ0

C. Mixture Gaussian parameters as messages

In this method, we approximate the pdf by a mixture Gaussian with a maximum number of components,
and then send the mixture parameters as messages. For both multiplication (4) and convolution (5), the
resulting number of components in the mixture is multiplicative in the number of constituent components.
To keep the message representation tractable, we perform model reduction using the Iterative Pairwise
Replacement Algorithm (IPRA) [57], where a sequence of mixture models is computed iteratively.
The advantage of using mixture Gaussians to encode pdf’s is that the messages are short and hence
consume little memory. This method works well for mixture Gaussian priors, but could be difﬁcult to adapt
to other priors. Model order reduction algorithms such as IPRA can be computationally expensive [57],
and introduce errors in the messages, which impair the quality of the solution as well as the convergence of
CS-BP [52].

Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore.  Restrictions apply.

<!-- 第 13 页 -->
This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.

TABLE I
Computational and storage requirements of CS-BP decoding

Messages Parameter Computation Storage

Samples of pdf p = O(σ1/σ0) samples O σ1σ0 log σ1 N log2(N) O(pN log(N))
σ0
Mixture Gaussians m components O m2 NS log2(N) O(mN log(N))

Again, we analyze the computational requirements. Because it is impossible to undo the multiplica-
tion in (4) and (5), we cannot use the modiﬁed form (7). Let m be the maximum model order. Model
order reduction using IPRA [57] requires O(m2R2) computation per coefﬁcient node per iteration. With
O(N) coefﬁcient nodes, each iteration is O(m2R2N). Similarly, with O(M) constraint nodes, each iter-
ation is O(m2L2M). Accounting for O(log(N)) CS-BP iterations, overall computation is O(m2[L2M +
R2N] log(N)) = O m2 NS log2(N).

D. Properties of CS-BP decoding

We brieﬂy describe several properties of CS-BP decoding. The computational characteristics of the
two methods for encoding beliefs about conditional distributions were evaluated in Sections IV-B and IV-C.
The storage requirements are mainly for message representation of the LM = O(N log(N)) edges. For
encoding with pdf samples, the message length is p, and so the storage requirement is O(pN log(N)). For
encoding with mixture Gaussian parameters, the message length is m, and so the storage requirement is
O(mN log(N)). Computational and storage requirements are summarized in Table I.
Several additional properties are now featured. First, we have progressive decoding; more measure-
ments will improve the precision of the estimated posterior probabilities. Second, if we are only interested
in an estimate of the state conﬁguration vector q but not in the coefﬁcient values, then less information must
be extracted from the measurements. Consequently, the number of measurements can be reduced. Third, we
have robustness to noise, because noisy measurements can be incorporated into our model by convolving
the noiseless version of the estimated pdf (5) at each encoding node with the pdf of the noise.

V. NUMERICAL RESULTS

To demonstrate the efﬁcacy of CS-BP, we simulated several different settings. In our ﬁrst setting, we
considered decoding problems where N = 1000, S = 0.1, σ1 = 10, σ0 = 1, and the measurements are
noiseless. We used samples of the pdf as messages, where each message consisted of p = 525 = 3 · 52 · 7
samples; this choice of p provided fast FFT computation. Figure 3 plots the MMSE decoding error as a

Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore.  Restrictions apply.

<!-- 第 14 页 -->
This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.

|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|
|---|---|---|---|---|---|---|---|---|---|
|L=5<br>L=10<br>L=20|L=5<br>L=10<br>L=20|L=5<br>L=10<br>L=20|L=5<br>L=10<br>L=20|L=5<br>L=10<br>L=20|L=5<br>L=10<br>L=20|L=5<br>L=10<br>L=20|L=5<br>L=10<br>L=20|L=5<br>L=10<br>L=20||
|||||||||||

100

80
MMSE
60

40

20

# 100 200 300 400 500 600 700
M

Fig. 3. MMSE as a function of the number of measurements M using different matrix row weights L. The dashed
lines show the ℓ2 norms of x (top) and the small coefﬁcients (bottom). (N = 1000, S = 0.1, σ1 = 10, σ0 = 1, and
noiseless measurements.)

function of M for a variety of row weights L. The ﬁgure emphasizes with dashed lines the average ℓ2 norm
of x (top) and of the small coefﬁcients (bottom); increasing M reduces the decoding error, until it reaches
the energy level of the small coefﬁcients. A small row weight, e.g., L = 5, may miss some of the large
coefﬁcients and is thus bad for decoding; as we increase L, fewer measurements are needed to obtain the
same precision. However, there is an optimal Lopt ≈2/S = 20 beyond which any performance gains
are marginal. Furthermore, values of L > Lopt give rise to divergence in CS-BP, even with damping. An
example of the output of the CS-BP decoder and how it compares to the signal x appears in Figure 4, where
we used L = 20 and M = 400. Although N = 1000, we only plotted the ﬁrst 100 signal values x(i) for
ease of visualization.
To compare the performance of CS-BP with other CS decoding algorithms, we also simulated: (i) ℓ1
decoding (1) via linear programming; (ii) GPSR [20], an optimization method that minimizes ∥θ∥1 +µ∥y −
ΦΨθ∥22; (iii) CoSaMP [16], a fast greedy solver; and (iv) IHT [17], an iterative thresholding algorithm.
We simulated all ﬁve methods where N = 1000, S = 0.1, L = 20, σ1 = 10, σ0 = 1, p = 525, and
the measurements are noiseless. Throughout the experiment we ran the different methods using the same
CS-LDPC encoding matrix Φ, the same signal x, and therefore same measurements y. Figure 5 plots the
MMSE decoding error as a function of M for the ﬁve methods. For small to moderate M, CS-BP exploits
its knowledge about the approximately sparse structure of x, and has a smaller decoding error. CS-BP
requires 20–30% fewer measurements than the optimization methods LP and GPSR to obtain the same
MMSE decoding error; the advantage over the greedy solvers IHT and CoSaMP is even greater. However,
as M increases, the advantage of CS-BP over LP and GPSR becomes less pronounced.

Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore.  Restrictions apply.

<!-- 第 15 页 -->
This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.

20
Original x(i) 10
0
−10
−20

# 0 10 20 30 40 50 60 70 80 90 100
i
CS−BP estimate of x(i)
20
10
0
−10
−20

# 0 10 20 30 40 50 60 70 80 90 100
i

Fig. 4. Original signal x and version decoded by CS-BP. (N = 1000, S = 0.1, L = 20, M = 400, σ1 = 10, σ0 = 1,
and noiseless measurements.)

To compare the speed of CS-BP to other methods, we ran the same ﬁve methods as before. In this
experiment, we varied the signal length N from 100 to 10000, where S = 0.1, L = 20, σ1 = 10, σ0 = 1,
p = 525, and the measurements are noiseless. We mention in passing that some of the algorithms that were
evaluated can be accelerated using linear algebra routines optimized for sparse matrices; the improvement is
quite modest, and the run-times presented here do not reﬂect this optimization. Figure 6 plots the run-times
of the ﬁve methods in seconds as a function of N. It can be seen that LP scales more poorly than the other
algorithms, and so we did not simulate it for N > 3000.5 CoSaMP also seems to scale relatively poorly,
although it is possible that our conjugate gradient implementation can be improved using the pseudo-inverse
approach instead [16]. The run-times of CS-BP seem to scale somewhat better than IHT and GPSR. Al-
though the asymptotic computational complexity of CS-BP is good, for signals of length N = 10000 it
is still slower than IHT and GPSR; whereas IHT and GPSR essentially perform matrix-vector multiplica-
tions, CS-BP is slowed by FFT computations performed in each iteration for all nodes in the factor graph.

Additionally, whereas the choice p = O(σ1/σ0) yields O σ0 logσ1 σ1 N log2(N) complexity, FFT com-
σ0
putation with p = 525 samples is somewhat slow. That said, our main contribution is a computationally
feasible Bayesian approach, which allows to reduce the number of measurements (Figure 5); a comparison
between CS-BP and previous Bayesian approaches to CS [25, 26] would be favorable.
To demonstrate that CS-BP deals well with measurement noise, recall the noisy measurement setting
5Our LP solver is based on interior point methods.

Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore.  Restrictions apply.

<!-- 第 16 页 -->
This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.

|IHT<br>CoSaMP<br>GPSR<br>LP<br>CS−BP|IHT<br>CoSaMP<br>GPSR<br>LP<br>CS−BP|Col3|
|---|---|---|
|~~IHT~~<br>CoSaMP<br>GPSR<br>~~L~~P<br>CS−BP|~~IHT~~<br>CoSaMP<br>GPSR<br>~~L~~P<br>CS−BP||
||||

100

80
MMSE
60

40

20

# 100 200 300 400 500 600 700
M

Fig. 5. MMSE as a function of the number of measurements M using CS-BP, linear programming (LP), GPSR,
CoSaMP, and IHT. The dashed lines show the ℓ2 norms of x (top) and the small coefﬁcients (bottom). (N = 1000,
S = 0.1, L = 20, σ1 = 10, σ0 = 1, and noiseless measurements.)

y = Φx+z of Section III, where z ∼N(0, σ2Z) is AWGN with variance σ2Z. Our algorithm deals with noise
by convolving the noiseless version of the estimated pdf (5) with the noise pdf. We simulated decoding
problems where N = 1000, S = 0.1, L = 20, σ1 = 10, σ0 = 1, p = 525, and σ2Z ∈{0, 2, 5, 10}.
Figure 7 plots the MMSE decoding error as a function of M and σ2Z. To put things in perspective, the
average measurement picks up a Gaussian term of variance L(1 −S)σ20 = 18 from the signal. Although
the decoding error increases with σ2Z, as long as σ2Z ≪18 the noise has little impact on the decoding error;
CS-BP offers a graceful degradation to measurement noise.
Our ﬁnal experiment considers model mismatch where CS-BP has an imprecise statistical characteriza-
tion of the signal. Instead of a two-state mixture Gaussian signal model as before, where large coefﬁcients
have variance σ21 and occur with probability S, we deﬁned a C-component mixture model. In our deﬁni-
tion, σ20 is interpreted as a background signal level, which appears in all coefﬁcients. Whereas the two-state
model adds a “true signal” component of variance σ21 −σ20 to the background signal, the C −1 large com-
ponents each occur with probability S and the amplitudes of the true signals are σ2, 2σ2, . . . , (C −1)σ2,
where σ2 is chosen to preserve the total signal energy. At the same time, we did not change the signal
priors in CS-BP, and used the same two-state mixture model as before. We simulated decoding problems
where N = 1000, S = 0.1, L = 20, σ1 = 10, σ0 = 1, p = 525, the measurements are noiseless, and
C ∈{2, 3, 5}. Figure 8 plots the MMSE decoding error as a function of M and C. The ﬁgure also shows
how IHT and GPSR perform, in order to evaluate whether they are more robust than the Bayesian approach
of CS-BP. We did not simulate CoSaMP and ℓ1 decoding, since their MMSE performance is comparable to
that of IHT and GPSR. As the number of mixture components C increases, the MMSE provided by CS-BP

Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore.  Restrictions apply.

<!-- 第 17 页 -->
This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.

Time [seconds] 102
LP
CS−BP
GPSR
CoSaMP

# 0 IHT
10

# 102 103 104
N

Fig. 6. Run-time in seconds as a function of the signal length N using CS-BP, linear programming (LP) ℓ1 decoding,
GPSR, CoSaMP, and IHT. (S = 0.1, L = 20, M = 0.4N, σ1 = 10, σ0 = 1, and noiseless measurements.)

increases. However, even for C = 3 the sparsity rate effectively doubles from S to 2S, and an increase in
the required number of measurements M is expected. Interestingly, the greedy IHT method also degrades
signiﬁcantly, perhaps because it implicitly makes an assumption regarding the number of large mixture
components. GPSR, on the other hand, degrades more gracefully.

VI. VARIATIONS AND ENHANCEMENTS

Supporting arbitrary sparsifying basis Ψ: Until now, we have assumed that the canonical sparsifying
basis is used, i.e., Ψ = I. In this case, x itself is sparse. We now explain how CS-BP can be modiﬁed to
support the case where x is sparse in an arbitrary basis Ψ. In the encoder, we multiply the CS-LDPC matrix
Φ by ΨT and encode x as y = (ΦΨT)x = (ΦΨT )(Ψθ) = Φθ, where (·)T denotes the transpose operator.
In the decoder, we use BP to form the approximation bθ, and then transform via Ψ to bx = Ψbθ. In order
to construct the modiﬁed encoding matrix ΦΨT and later transform bθ to bx, extra computation is needed;
this extra cost is O(N 2) in general. Fortunately, in many practical situations Ψ is structured (e.g., Fourier
or wavelet bases) and amenable to fast computation. Therefore, extending our methods to such bases is
feasible.
Exploiting statistical dependencies: In many signal representations, the coefﬁcients are not iid. For
example, wavelet representations of natural images often contain correlations between magnitudes of parent
and child coefﬁcients [2, 43]. Consequently, it is possible to decode signals from fewer measurements
using an algorithm that allocates different distributions to different coefﬁcients [46, 58]. By modifying the
dependencies imposed by the prior constraint nodes (Section IV-A), CS-BP decoding supports different
signal models.

Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore.  Restrictions apply.

<!-- 第 18 页 -->
This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.

100

σZ2=10
80
σZ2=5
MMSE

# 60 2=2
σZ
Noiseless
40

20

# 100 200 300 400 500 600 700
M

Fig. 7. MMSE as a function of M using different noise levels σ2Z. The dashed lines show the ℓ2 norms of x (top) and
the small coefﬁcients (bottom). (N = 1000, S = 0.1, L = 20, σ1 = 10, and σ0 = 1.)

Feedback: Feedback from the decoder to the encoder can be used in applications where measurements
may be lost because of transmissions over faulty channels. In an analogous manner to a digital fountain [59],
the marginal distributions (6) enable us to identify when sufﬁcient information for signal decoding has
been received. At that stage, the decoder notiﬁes the encoder that decoding is complete, and the stream of
measurements is stopped.
Irregular CS-LDPC matrices: In channel coding, LDPC matrices that have irregular row and column
weights come closer to the Shannon limit, because a small number of rows or columns with large weights
require only modest additional computation yet greatly reduce the block error rate [38]. In an analogous
manner, we expect irregular CS-LDPC matrices to enable a further reduction in the number of measurements
required.

VII. DISCUSSION

This paper has developed a sparse encoding matrix and belief propagation decoding algorithm to ac-
celerate CS encoding and decoding under the Bayesian framework. Although we focus on decoding ap-
proximately sparse signals, CS-BP can be extended to signals that are sparse in other bases, is ﬂexible to
modiﬁcations in the signal model, and can address measurement noise.
Despite the signiﬁcant beneﬁts, CS-BP is not universal in the sense that the encoding matrix and de-
coding methods must be modiﬁed in order to apply our framework to arbitrary bases. Nonetheless, the
necessary modiﬁcations only require multiplication by the sparsifying basis Ψ or its transpose ΨT.
Our method resembles low density parity check (LDPC) codes [37, 38], which use a sparse Bernoulli
parity check matrix. Although any linear code can be represented as a bipartite graph, for LDPC codes

Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore.  Restrictions apply.

<!-- 第 19 页 -->
This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.

|IHT C=5|Col2|Col3|
|---|---|---|
|IHT C=5|IHT C=5|IHT C=5|
|IHT C=3<br>CS−BP C=5<br>IHT C=2<br>GPSR C=5<br>GPSR C=3<br>CS−BP C=3<br>GPSR C=2<br>CS−BP C=2|IHT C=3<br>CS−BP C=5<br>IHT C=2<br>GPSR C=5<br>GPSR C=3<br>CS−BP C=3<br>GPSR C=2<br>CS−BP C=2||
|IHT C=3<br>CS−BP C=5<br>IHT C=2<br>GPSR C=5<br>GPSR C=3<br>CS−BP C=3<br>GPSR C=2<br>CS−BP C=2|IHT C=3<br>CS−BP C=5<br>IHT C=2<br>GPSR C=5<br>GPSR C=3<br>CS−BP C=3<br>GPSR C=2<br>CS−BP C=2||
||||

100

90

80

70

MMSE
60

50

40

30

20

# 100 200 300 400 500 600 700 800
M

Fig. 8. MMSE as a function of the number of measurements M and the number of components C in the mixture
Gaussian signal model. Plots for CS-BP (x), GPSR (circle), and IHT (asterisk) appear for C = 2 (dotted), C = 3
(dashed), and C = 5 (solid). The horizontal dashed lines show the ℓ2 norms of x (top) and the small coefﬁcients
(bottom). (N = 1000, S = 0.1, L = 20, σ1 = 10, σ0 = 1, and noiseless measurements.)

the sparsity of the graph accelerates the encoding and decoding processes. LDPC codes are celebrated for
achieving rates close to the Shannon limit. A similar comparison of the MMSE performance of CS-BP with
information theoretic bounds on CS performance is left for future research. Additionally, although CS-BP
is not guaranteed to converge, the recent convergence proofs for LDLC codes [36] suggest that future work
on extensions of CS-BP may also yield convergence proofs.

In comparison to previous work on Bayesian aspects of CS [25, 26], our method is much faster, requiring
only O(N log2(N)) computation. At the same time, CS-BP offers signiﬁcant ﬂexibility, and should not be
viewed as merely another fast CS decoding algorithm. However, CS-BP relies on the sparsity of CS-LDPC
matrices, and future research can consider the applicability of such matrices in different applications.

APPENDIX

Outline of proof of Theorem 1: The proof begins with a derivation of probabilistic bounds on ∥x∥2

Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore.  Restrictions apply.

<!-- 第 20 页 -->
This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.

and ∥x∥∞. Next, we review a result by Wang et al. [49, Theorem 1]. The proof is completed by combining
the bounds with the result by Wang et al.
Upper bound on ∥x∥22: Consider ∥x∥22 = PNi=1 x2i , where the random variable (RV) Xi has a mixture
distribution

χ2σ2 w.p. S
 1
X2 .
i ∼
 χ2σ2 w.p. 1 −S
0
Recall the moment generating function (MGF), MX(t) = E[etx]. The MGF of a Chi-squared RV satisﬁes
Mχ2(t) = (1 −2t)−12. For the mixture RV X2
i ,
S 1 −S
MX2i (t) = + .
p1 −2tσ2 p1 −2tσ2

# 1 0
h iN
Additionally, because the Xi are iid, M∥x∥22(t) = MX2i (t) . Invoking the Chernoff bound, we have
" #N
< e−tSNσ2 S 1 −S
Pr ∥x∥22 < SNσ2 +
1

# 1 p1 −2tσ2 p1 −2tσ2

# 1 0
∥x∥22 < SNσ2 decays faster than N −γ as N is increased. To do so, let
for t < 0. We aim to show that Pr
1
t = −α1 , where α > 0. It sufﬁces to prove that there exists some α for which
σ2

S 1 −S
f1(α) = eαS  1 + 2α + < 1.
- r
 2

# 1 + 2α σ0
σ1
Let f2(α) = 1+2α and f3(α) = eα. It is easily seen via Taylor series that f2(α) = 1 −α + O(α2) and1
-
f3(α) = 1 + α + O(α2), and so
" σ0 2 σ0 4!!#
f1(α) = eαS S 1 −α + O(α2) + (1 −S) 1 −α + O α2
σ1 σ1
" σ0 2! #
= 1 + αS + O(α2S2) 1 −α S + (1 −S) + O(α2) .
σ1
 2
Because of the negative term −α(1 −S) σ0 < 0, which dominates the higher order term O(α2) for
σ1
small α, there exists α > 0, which is independent of N, for which f1(α) < 1. Using this α, the Chernoff
bound provides an upper bound on Pr ∥x∥22 < SNσ2 that decays exponentially with N. In summary,
1
Pr ∥x∥22 < SNσ2 = o(N −γ). (8)
1
Lower bound on ∥x∥22: In a similar manner, MGF’s and the Chernoff bound can be used to offer a
probabilistic bound on the number of large Gaussian mixture components
N !
X Q(i) > 3
Pr 2SN = o(N −γ). (9)
i=1

Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore.  Restrictions apply.

<!-- 第 21 页 -->
This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.

Taking into account the limited number of large components and the expected squared ℓ2 norm, E[∥x∥22] =
N[Sσ21 + (1 −S)σ20], we have
Pr ∥x∥22 > N[2Sσ21 + (1 −S)σ20] = o(N −γ). (10)
We omit the (similar) details for brevity.
Bound on ∥x∥∞: The upper bound on ∥x∥∞is obtained by ﬁrst considering large mixture components
and then small components. First, we consider the large Gaussian mixture components, and denote xL =
{x(i) : Q(i) = 1}.
N ! i 3
X Q(i) ≤3 h p 2SN
p2 ln(SN 1+γ)σ1 2 ln(SN 1+γ) (11)
Pr ∥xL∥∞< 2SN ≥ f4
i=1

# 32 SN
 p
f5 2 ln(SN 1+γ)
> 1 − (12)
p

# 2 ln(SN 1+γ)
p
f5 2 ln(SN 1+γ)

# 1 −3
> 2SN (13)
p2 ln(SN 1+γ)
e−12 2 ln(SN1+γ)
3SN
= 1 − √
2p2 ln(SN 1+γ) 2π
3N −γ
= 1 − ,
4pln(SN 1+γ)
R α−∞e−u2/2du is the cumulative distribution function of the standard normal dis-
where f4(α) = 1
-
2π
tribution, the inequality (11) relies on f4(·) < 1 and the possibility that PNi=1 Q(i) is strictly smaller
than 3 12πe−α2/2 is the pdf of the standard normal distribution, (12) relies on the bound
2SN, f5(α) =
-
f4(α) > 1 −f5(α)/α, and the inequality (13) is motivated by (1 −α)β > 1 −αβ for α, β > 0. Noting that
ln(SN 1+γ) increases with N, for large N we have
N ! > 1 −N −γ
X Q(i) ≤3
p2 ln(SN 1+γ)σ1 (14)
Pr ∥xL∥∞< 2SN .
5
i=1
Now consider the small Gaussian mixture components, and denote xS = {x(i) : Q(i) = 0}. As before,
 p2 ln(SN 1+γ)σ1 N
 p
Pr ∥xS∥∞< 2 ln(SN 1+γ)σ1 f4 (15)
≥
σ0
“ σ1 ”2
e−12 2 ln(SN1+γ)
N σ0
> 1 − √ ,
p2 ln(SN 1+γ)σ1 2π
σ0
where in (15) the number of small mixture components is often less than N. Because σ1 > σ0, for large N
we have
  > 1 −N −γ
p2 ln(SN 1+γ)σ1 (16)
Pr ∥xS∥∞< .

Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore.  Restrictions apply.

<!-- 第 22 页 -->
This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.

Combining (9), (14) and (16), for large N we have
  > 1 −N −γ
p2 ln(SN 1+γ)σ1 (17)
Pr ∥x∥∞< .
2
Result by Wang et al. [49, Theorem 1]:
Theorem 2—[49]: Consider x ∈RN that satisﬁes the condition
∥x∥∞
≤Q. (18)
∥x∥2
In addition, let V be any set of N vectors {v1, . . . , vN} ⊂RN. Suppose a sparse random matrix Φ ∈RM×N
satisﬁes
E[Φij] = 0, E[Φ2ij] = 1, E[Φ4ij] = s,
where 1s = LN is the fraction of non-zero entries in Φ. Let
  ϵ2 sQ2 log(N)
O 1+γ if sQ2 ≥Ω(1)

M = . (19)
1+γ
 O ϵ2 log(N) if sQ2 ≤O(1)
Then with probability at least 1 −N −γ, the random projections M Φx and1 M Φvi can produce an estimate1
bai for xT vi satisfying
|bai −xT vi| ≤ϵ∥x∥2∥vi∥2, ∀i ∈{1, . . . , N}.
Application of Theorem 2 to proof of Theorem 1: Combining (8), (10), and (17), the union bound
demonstrates that with probability lower bounded by 1 −N −γ we have ∥x∥∞< p2 ln(SN 1+γ)σ1 and
∥x∥22 ∈(NSσ21, N[2Sσ21 + (1 −S)σ20]).6 When these ℓ2 and ℓ∞bounds hold, we can apply Theorem 2.
To apply Theorem 2, we must specify (i) Q (18); (ii) the test vectors (vi)Ni=1; (iii) the matrix sparsity
q 2 ln(SN1+γ)
s; and (iv) the ϵ parameter. First, the bounds on ∥x∥2 and ∥x∥∞indicate that ∥x∥∞∥x∥2 ≤Q = .
SN
Second, we choose (vi)Ni=1 to be the N canonical vectors of the identity matrix IN, providing xT vi = xi.
Third, our choice of L offers s = NL = η ln(SN1+γ). Fourth, we setNS
µσ1
ϵ = .
pN[2Sσ21 + (1 −S)σ20]
Using these parameters, Theorem 2 demonstrates that all N approximations bai satisfy
|bai −xi| = |bai −xT vi| ≤ϵ∥x∥2∥vi∥2 < µσ1
6The o(·) terms (8) and (10) demonstrate that there exists some N0 such that for all N > N0 the upper and lower bounds on ∥x∥2
each hold with probability lower bounded by 1 −14N γ, resulting in a probability lower bounded by 1 −N −γ via the union bound.
Because the expression (2) for the number of measurements M is an order term, the case where N ≤N0 is inconsequential.

Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore.  Restrictions apply.

<!-- 第 23 页 -->
This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.

with probability lower bounded by 1−N −γ. Combining the probability that the ℓ2 and ℓ∞bounds hold and
the decoding probability offered by Theorem 2, we have

∥ba −x∥∞< µσ1 (20)
with probability lower bounded by 1 −2N −γ.
We complete the proof by computing the number of measurements M required (19). Because sQ2 =
K 2 ln(SN1+γ) = 2
η, we need
η ln(SN1+γ) SN
  " σ0 2# !
(1 + 2η−1)1 + γ N(1 + 2η−1)(1 + γ)
M = O log(N) = O 2S + (1 −S) log(N)
ϵ2 µ2 σ1
measurements. □

ACKNOWLEDGMENTS

Thanks to David Scott, Danny Sorensen, Yin Zhang, Marco Duarte, Michael Wakin, Mark Davenport,
Jason Laska, Matthew Moravec, Elaine Hale, Christine Kelley, and Ingmar Land for informative and inspir-
ing conversations. Thanks to Phil Schniter for bringing his related work [27] to our attention. Special thanks
to Ramesh Neelamani, Alexandre de Baynast, and Predrag Radosavljevic for providing helpful suggestions
for implementing BP; to Danny Bickson and Harel Avissar for improving our implementation; and to Marco
Duarte for wizardry with the ﬁgures. Additionally, the ﬁrst author thanks the Department of Electrical En-
gineering at the Technion for generous hospitality while parts of the work were being performed, and in
particular the support of Yitzhak Birk and Tsachy Weissman. Final thanks to the anonymous reviewers,
whose superb comments helped to greatly improve the quality of the paper.

REFERENCES

[1] S. Sarvotham, D. Baron, and R. G. Baraniuk, “Compressed sensing reconstruction via belief propagation,” Tech. Rep.
TREE0601, Rice University, Houston, TX, July 2006.
[2] R. A. DeVore, B. Jawerth, and B. J. Lucier, “Image compression through wavelet transform coding,” IEEE Trans. Inf. Theory,
vol. 38, no. 2, pp. 719–746, Mar. 1992.
[3] I. F. Gorodnitsky and B. D. Rao, “Sparse signal reconstruction from limited data using FOCUSS: A re-weighted minimum
norm algorithm,” IEEE Trans. Signal Process., vol. 45, no. 3, pp. 600–616, March 1997.
[4] E. Cand`es, J. Romberg, and T. Tao, “Robust uncertainty principles: Exact signal reconstruction from highly incomplete
frequency information,” IEEE Trans. Inf. Theory, vol. 52, no. 2, pp. 489–509, Feb. 2006.
[5] D. Donoho, “Compressed sensing,” IEEE Trans. Inf. Theory, vol. 52, no. 4, pp. 1289–1306, Apr. 2006.
[6] R. G. Baraniuk, “A lecture on compressive sensing,” IEEE Signal Process Mag., vol. 24, no. 4, pp. 118–121, 2007.

Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore.  Restrictions apply.

<!-- 第 24 页 -->
This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.

[7] E. Cand`es, M. Rudelson, T. Tao, and R. Vershynin, “Error correction via linear programming,” Found. Comp. Math., pp.
295–308, 2005.
[8] S. Chen, D. Donoho, and M. Saunders, “Atomic decomposition by basis pursuit,” SIAM J. Sci. Comp., vol. 20, no. 1, pp.
33–61, 1998.
[9] D. Donoho and J. Tanner, “Neighborliness of randomly projected simplices in high dimensions,” Proc. Nat. Academy
Sciences, vol. 102, no. 27, pp. 9452–457, 2005.
[10] D. Donoho, “High-dimensional centrally symmetric polytopes with neighborliness proportional to dimension,” Discrete
Comput. Geometry, vol. 35, no. 4, pp. 617–652, Mar. 2006.
[11] P. M. Vaidya, “An algorithm for linear programming which requires O(((m+n)n2+(m+n)1.5n)L) arithmetic operations,” in
STOC ’87: Proc. 19th ACM Symp. Theory of computing, New York, NY, USA, 1987, pp. 29–38, ACM.
[12] J. A. Tropp and A. C. Gilbert, “Signal recovery from random measurements via orthogonal matching pursuit,” IEEE Trans.
Inf. Theory, vol. 53, no. 12, pp. 4655–4666, Dec. 2007.
[13] A. Cohen, W. Dahmen, and R. A. DeVore, “Near optimal approximation of arbitrary vectors from highly incomplete mea-
surements,” 2007, Preprint.
[14] M. F. Duarte, M. B. Wakin, and R. G. Baraniuk, “Fast reconstruction of piecewise smooth signals from random projections,”
in Proc. SPARS05, Rennes, France, Nov. 2005.
[15] D. L. Donoho, Y. Tsaig, I. Drori, and J-C Starck, “Sparse solution of underdetermined linear equations by stagewise orthog-
onal matching pursuit,” Mar. 2006, Preprint.
[16] D. Needell and J. A. Tropp, “CoSaMP: Iterative signal recovery from incomplete and inaccurate samples,” Appl. Comput.
Harmonic Analysis, vol. 26, no. 3, pp. 301–321, 2008.
[17] T. Blumensath and M. E. Davies, “Iterative hard thresholding for compressed sensing,” to appear in Appl. Comput. Harmonic
Analysis, 2008.
[18] W. Dai and O. Milenkovic, “Subspace pursuit for compressive sensing: Closing the gap between performance and complex-
ity,” IEEE Trans. Inf. Theory, vol. 55, no. 5, pp. 2230–2249, May 2009.
[19] E. Hale, W. Yin, and Y. Zhang, “Fixed-point continuation for ℓ1-minimization: Methodology and convergence,” 2007,
Submitted.
[20] M. Figueiredo, R. Nowak, and S. J. Wright, “Gradient projection for sparse reconstruction: Application to compressed sensing
and other inverse problems,” Dec. 2007, IEEE J. Sel. Top. Sign. Proces.
[21] E. van den Berg and M. P. Friedlander, “Probing the Pareto frontier for basis pursuit solutions,” Tech. Rep. TR-2008-01,
Department of Computer Science, University of British Columbia, Jan. 2008, To appear in SIAM J. Sci. Comp.
[22] G. Cormode and S. Muthukrishnan, “Towards an algorithmic theory of compressed sensing,” DIMACS Technical Report TR
2005-25, 2005.
[23] G. Cormode and S. Muthukrishnan, “Combinatorial algorithms for compressed sensing,” DIMACS Technical Report TR
2005-40, 2005.
[24] A. C. Gilbert, M. J. Strauss, J. Tropp, and R. Vershynin, “Algorithmic linear dimension reduction in the ℓ1 norm for sparse
vectors,” Apr. 2006, Submitted.
[25] S. Ji, Y. Xue, and L. Carin, “Bayesian compressive sensing,” IEEE Trans. Signal Process., vol. 56, no. 6, pp. 2346–2356,
June 2008.
[26] M. W. Seeger and H. Nickisch, “Compressed sensing and Bayesian experimental design,” in ICML ’08: Proc. 25th Int. Conf.
Machine learning, 2008, pp. 912–919.

Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore.  Restrictions apply.

<!-- 第 25 页 -->
This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.

[27] P. Schniter, L. C. Potter, and J. Ziniel, “Fast Bayesian matching pursuit: Model uncertainty and parameter estimation for
sparse linear models,” IEEE Trans. Signal Process., March 2009.
[28] T. Hastie, R. Tibshirani, and J. H. Friedman, The Elements of Statistical Learning, Springer, August 2001.
[29] G. Guo and C.-C. Wang, “Multiuser detection of sparsely spread CDMA,” IEEE J. Sel. Areas Commun., vol. 26, no. 3, pp.
421–431, 2008.
[30] J. Pearl, “Probablistic reasoning in intelligent systems: Networks of plausible inference,” Morgan-Kaufmann, 1988.
[31] F. V. Jensen, “An introduction to Bayesian networks,” Springer-Verlag, 1996.
[32] B. J. Frey, “Graphical models for machine learning and digital communication,” MIT press, 1998.
[33] J. S. Yedidia, W. T. Freeman, and Y. Weiss, “Understanding belief propagation and its generalizations,” Mitsubishi Tech. Rep.
TR2001-022, Jan. 2002.
[34] D. J. C. MacKay, “Information theory, inference and learning algorithms,” Cambridge University Press, 2002.
[35] R. G. Cowell, A. P. Dawid, S. L. Lauritzen, and D. J. Spiegelhalter, “Probabilistic networks and expert systems,” Springer-
Verlag, 2003.
[36] N. Sommer, M. Feder, and O. Shalvi, “Low-density lattice codes,” IEEE Trans. Inf. Theory, vol. 54, no. 4, pp. 1561–1585,
2008.
[37] R. G. Gallager, “Low-density parity-check codes,” IEEE Trans. Inf. Theory, vol. 8, pp. 21–28, Jan. 1962.
[38] T. J. Richardson, M. A. Shokrollahi, and R. L. Urbanke, “Design of capacity-approaching irregular low-density parity-check
codes,” IEEE Trans. Inf. Theory, vol. 47, pp. 619–637, Feb. 2001.
[39] S. Sarvotham, D. Baron, and R. G. Baraniuk, “Sudocodes – Fast measurement and reconstruction of sparse signals,” in Proc.
Int. Symp. Inf. Theory (ISIT2006), Seattle, WA, July 2006.
[40] R. Berinde and P. Indyk, “Sparse recovery using sparse random matrices,” MIT-CSAIL-TR-2008-001, 2008, Technical Report.
[41] J.-C Pesquet, H. Krim, and E. Hamman, “Bayesian approach to best basis selection,” IEEE 1996 Int. Conf. Acoustics, Speech,
Signal Process. (ICASSP), pp. 2634–2637, 1996.
[42] H. Chipman, E. Kolaczyk, and R. McCulloch, “Adaptive Bayesian wavelet shrinkage,” J. Amer. Stat. Assoc., vol. 92, 1997.
[43] M. S. Crouse, R. D. Nowak, and R. G. Baraniuk, “Wavelet-based signal processing using hidden Markov models,” IEEE
Trans. Signal Process., vol. 46, pp. 886–902, April 1998.
[44] E. I. George and R. E. McCulloch, “Variable selection via Gibbs sampling,” J. Am. Stat. Assoc., vol. 88, pp. 881–889, 1993.
[45] J. Geweke, “Variable selection and model comparison in regression,” in Bayesian Statistics 5, 1996, pp. 609–620.
[46] L. He and L. Carin, “Exploiting structure in wavelet-based Bayesian compressed sensing,” to appear in IEEE Trans. Signal
Process., 2008.
[47] H. W. Sorenson and D. L. Alspach, “Recursive Bayesian estimation using Gaussian sums,” Automatica, vol. 7, pp. 465–479,
1971.
[48] J. A. Tropp, “Greed is good: Algorithmic results for sparse approximation,” IEEE Trans. Inf. Theory, vol. 50, pp. 2231–2242,
2004.
[49] W. Wang, M. Garofalakis, and K. Ramchandran, “Distributed sparse random projections for reﬁnable approximation,” in
Proc. Inf. Process. Sensor Networks (IPSN2007), 2007, pp. 331–339.
[50] G. Cooper, “The computational complexity of probabilistic inference using Bayesian belief networks,” Artiﬁcial Intelligence,
vol. 42, pp. 393–405, 1990.
[51] F. R. Kschischang, B. J. Frey, and H-A. Loeliger, “Factor graphs and the sum-product algorithm,” IEEE Trans. Inf. Theory,
vol. 47, no. 2, pp. 498–519, Feb. 2001.

Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore.  Restrictions apply.

<!-- 第 26 页 -->
This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.

[52] E. Sudderth, A. Ihler, W. Freeman, and A. S. Willsky, “Nonparametric belief propagation,” MIT LIDS Tech. Rep. 2551, Oct.
2002.
[53] B. J. Frey and D. J. C. MacKay, “A revolution: Belief propagation in graphs with cycles,” Adv. Neural Inf. Process. Systems,
M. Jordan, M. S. Kearns and S. A. Solla (Eds.), vol. 10, 1998.
[54] A. Ihler, J. Fisher, and A. S. Willsky, “Loopy belief propagation: Convergence and effects of message errors,” J. Machine
Learning Res., vol. 6, pp. 905–936, May 2005.
[55] M. Pretti, “A Message-Passing Algorithm with Damping,” J. Stat. Mech., Nov. 2005.
[56] D. J. C. MacKay, “Good error-correcting codes based on very sparse matrices,” IEEE Trans. Inf. Theory, vol. 45, pp. 399–431,
Mar. 1999.
[57] D. W. Scott and W. F. Szewczyk, “From kernels to mixtures,” Technometrics, vol. 43, pp. 323–335, Aug. 2001.
[58] R. G. Baraniuk, V. Cevher, M. F. Duarte, and C. Hegde, “Model-based compressive sensing,” 2008, Preprint.
[59] J. W. Byers, M. Luby, and M. Mitzenmacher, “A digital fountain approach to asynchronous reliable multicast,” IEEE J. Sel.
Areas Commun., vol. 20, no. 8, pp. 1528–1540, Oct. 2002.

Dror Baron received the B.Sc. (summa cum laude) and M.Sc. degrees from the Technion - Israel
Institute of Technology, Haifa, Israel, in 1997 and 1999, and the Ph.D. degree from the University of Illinois
at Urbana-Champaign in 2003, all in electrical engineering.
From 1997 to 1999, he worked at Witcom Ltd. in modem design. From 1999 to 2003, he was a research
assistant at the University of Illinois at Urbana-Champaign, where he was also a Visiting Assistant Professor
in 2003. From 2003 to 2006, he was a Postdoctoral Research Associate in the Department of Electrical and
Computer Engineering at Rice University, Houston, TX. From 2007 to 2008, he was a quantitative ﬁnancial
analyst with Menta Capital, San Francisco, CA. Since 2008 he has been a visiting scientist in the Department
of Electrical Engineering at Technion - Israel Institute of Technology, Haifa.
Dr. Baron’s research interests include information theory and signal processing. Dr. Baron was a
recipient of the 2002 M. E. Van Valkenburg Graduate Research Award, and received honorable mention
at the Robert Bohrer Memorial Student Workshop in April 2002, both at the University of Illinois. He
also participated from 1994 to 1997 in the Program for Outstanding Students, comprising the top 0.5% of
undergraduates at the Technion.
Shriram Sarvotham received his B.Tech degree from Indian Institute of Technology, Madras, India and
M.S and Ph.D. degrees from Rice University, Texas, all in Electrical Engineering. His research interests lie
in the broad areas of Compressed Sensing, non-asymptotic Information Theory and Internet Trafﬁc analysis
and modeling. Currently, he works as a Principal Research Scientist at Halliburton Energy Services, where
he investigates optimal data acquisition and processing of NMR data in oil and gas exploration.
Richard G. Baraniuk received the BSc degree in 1987 from the University of Manitoba (Canada),
the MSc degree in 1988 from the University of Wisconsin-Madison, and the PhD degree in 1992 from the

Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore.  Restrictions apply.

<!-- 第 27 页 -->
This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication.

University of Illinois at Urbana-Champaign, all in Electrical Engineering. After spending 1992–1993 with
the Signal Processing Laboratory of Ecole Normale Sup´erieure, in Lyon, France, he joined Rice University,
where he is currently the Victor E. Cameron Professor of Electrical and Computer Engineering. He spent
sabbaticals at Ecole Nationale Sup´erieure de T´el´ecommunications in Paris in 2001 and Ecole F´ed´erale Poly-
technique de Lausanne in Switzerland in 2002. His research interests lie in the area of signal and image
processing.
He has been a Guest Editor of several special issues of the IEEE Signal Processing Magazine, IEEE
Journal of Special Topics in Signal Processing, and the Proceedings of the IEEE and has served as technical
program chair or on the technical program committee for several IEEE workshops and conferences.
In 1999, Dr. Baraniuk founded Connexions (cnx.org), a non-proﬁt publishing project that invites au-
thors, educators, and learners worldwide to “create, rip, mix, and burn” free textbooks, courses, and learning
materials from a global open-access repository.
Dr. Baraniuk received a NATO postdoctoral fellowship from NSERC in 1992, the National Young
Investigator award from the National Science Foundation in 1994, a Young Investigator Award from the
Ofﬁce of Naval Research in 1995, the Rosenbaum Fellowship from the Isaac Newton Institute of Cambridge
University in 1998, the C. Holmes MacDonald National Outstanding Teaching Award from Eta Kappa Nu in
1999, the Charles Duncan Junior Faculty Achievement Award from Rice in 2000, the University of Illinois
ECE Young Alumni Achievement Award in 2000, the George R. Brown Award for Superior Teaching at
Rice in 2001, 2003, and 2006, the Hershel M. Rich Invention Award from Rice in 2007, the Wavelet Pioneer
Award from SPIE in 2008, and the Internet Pioneer Award from the Berkman Center for Internet and Society
at Harvard Law School in 2008. He was selected as one of Edutopia Magazine’s Daring Dozen educators
in 2007. Connexions received the Tech Museum Laureate Award from the Tech Museum of Innovation
in 2006. His work with Kevin Kelly on the Rice single-pixel compressive camera was selected by MIT
Technology Review Magazine as a TR10 Top 10 Emerging Technology in 2007. He was co-author on a
paper with Matthew Crouse and Robert Nowak that won the IEEE Signal Processing Society Junior Paper
Award in 2001 and another with Vinay Ribeiro and Rolf Riedi that won the Passive and Active Measurement
(PAM) Workshop Best Student Paper Award in 2003. He was elected a Fellow of the IEEE in 2001 and a
Plus Member of AAA in 1986.

Copyright (c) 2009 IEEE. Personal use is permitted. For any other purposes, Permission must be obtained from the IEEE by emailing pubs-permissions@ieee.org.
Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 9, 2009 at 20:44 from IEEE Xplore.  Restrictions apply.
