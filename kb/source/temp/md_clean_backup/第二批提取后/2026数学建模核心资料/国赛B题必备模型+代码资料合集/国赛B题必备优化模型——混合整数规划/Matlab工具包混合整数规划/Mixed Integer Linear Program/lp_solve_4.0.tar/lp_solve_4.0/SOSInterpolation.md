<!-- 第 1 页 -->

# Interpolation with GAMS

### Erwin Kalvelagen

### erwin@gams.com

### January 26, 2002

## 1 Introduction
Interpolation of tabular data and the implementation of piecewise (non)linear
functions is not straightforward in GAMS. In this paper we will discuss some

#### possible implementations using a number of examples.
Mixed-integer programming can be used to implement one-dimensional in-
terpolation using an advanced technique called Special Ordered Sets of type 2
(SOS2 sets). The advantage of using this method is that one can use a MIP
solver provided the rest of the model is linear and that one can get global solu-
tions (or a solution within a certain tolerance from the global optimum). If other
nonlinearities are present, this method is less attractive: the problem becomes
an MINLP and global solutions can only be found in special cases.

## 2 Special Ordered Sets
Suppose we have tabular data for a scalar function y = f(x) for a given interval
x ∈[xlo, xup]. Let’s denote this data by (¯xk, ¯yk). We introduce variables λk

#### with:

#### X = X λk¯xk (1)
k

#### Y = X λk¯yk (2)
k

#### X λk = 1 (3)
k

#### max 2 adjacent λ’s nonzero (4)

#### λk ≥0 (5)

#### xlo ≤X ≤xup

#### (6)

Equation (1) is called the reference row. Equation (2) is known as the function

#### row, and equation (3) is the convexity row.

<!-- 第 2 页 -->
The λk variables form a Special Order Set of Type 2. In a SOS2 set only
two adjacent variables of the set can assume non-zero values.
SOS2 variables can be implemented in GAMS using the SOS2 variable type:

#### sos2 variables lambda(k);
The exact deﬁnition of SOS2 variables is solver speciﬁc, especially in special
cases where nonzero lower bounds are used. In the above case we have added
λk ≥0, which only leaves the “max two adjacent lambda’s are nonzero” which

#### is shared by all solvers that have SOS2 facilities.

#### y

#### ¯yk
  - 444444444444444

#### 

#### 

#### 

#### ¯yk−1  ¯yk+2

#### 

#### 
-  ¯yk+1 o•

#### oo

#### oo

#### oo

#### oo

#### x

#### ¯xk−1 ¯xk ¯xk+1 ¯xk+2

#### Figure 1: Linear interpolation

### 2.1 Example: Local optima
This example will demonstrate the problem of ﬁnding local minima using a
local solver. In this case we use CONOPT2, but other local solvers show similar

#### behavior.

#### Consider the problem:

#### x6 + 4x5 −10x4 −20x3

#### P1 minimize
x

#### −5 ≤x ≤5

<!-- 第 3 页 -->
When implemented as an NLP only local solutions can found, depending on

#### the starting point.

#### Figure 2: Global minimization of problem P1

#### The GAMS model looks like:

variables z,x;
equations e;
e.. z =e= power(x,6) + 4*power(x,5) - 10*power(x,4) - 20*power(x,3);
x.lo = -5;
x.up = 5;
x.l = 0;
model m /all/;
solve m using nlp minimizing z;

#### Depending on the starting point we get diﬀerent solutions:
Table 2.2 shows the results with the NLP solver CONOPT when we use
diﬀerent starting points (denoted by x0). The columns x∗and f ∗are the optimal
solutions found. As can be seen the results are rather unpredictable. In general
starting close to a local optimum will lead the algorithm to that point, but in

<!-- 第 4 页 -->

|x0|x∗|f ∗|
|---|---|---|
|-5<br>-4<br>-3<br>-2<br>-1<br>0<br>1<br>2<br>3<br>4<br>5|-4.339<br>-4.339<br>-4.339<br>-4.339<br>2.102<br>0<br>2.102<br>2.102<br>-4.339<br>2.102<br>2.102|-1389.357<br>-1389.357<br>-1389.357<br>-1389.357<br>-130.572<br>0<br>-130.572<br>-130.572<br>-1389.357<br>-130.572<br>-130.572|

#### Table 1: Results for problem P1 for diﬀerent starting points

some cases the algorithm will not move at all (starting from x0 = 0.0) or will

#### jump over the closest local optimum (starting from x0 = 3).

### 2.2 Example: SOS2 implementation

#### Consider the problem:

#### P2 maximize y
x

#### subject to y = x4 −3x3 −1.5x2 + 10x

#### y = −20x + 100

#### −5 ≤x ≤5

The NLP model using a (default) starting point of x0 = 0.0 will cause the

#### NLP solver CONOPT to converge to x∗= 3.395, y∗= 32.105.

variables y,x;
equations e1,e2;
e1.. y =e= power(x,4) - 3*power(x,3) - 1.5*power(x,2) + 10*x;
e2.. y =e= -20*x+100;
x.lo = -5;
x.up = 5;
y.l = 0;
x.l = 0;
model m /all/;
solve m using nlp maximizing y;

<!-- 第 5 页 -->

#### Figure 3: Two feasible points in problem P2

Using a SOS2 implementation we can ﬁnd a close solution to the global
optimum. There are two sources for error: the linear approximation, and the
integer optimality tolerances as set by the options OPTCR and OPTCA. The linear
approximate solution can be reﬁned by passing the optimal integer solution to
an NLP solver. The integer solution will be close to the global optimum, so
there is good hope the NLP solver will converge to that solution.

set k /k0*k100/;

parameter xbar(k), ybar(k);

xbar(k) = -5 + (ord(k)-1)*0.1;
ybar(k) = power(xbar(k),4) - 3*power(xbar(k),3) - 1.5*power(xbar(k),2) + 10*xbar(k);

display xbar,ybar;

variables y,x;
sos2 variables lambda(k);

equations refrow, funrow, convexity, e1, e2;

refrow.. x =e= sum(k, lambda(k)*xbar(k));
funrow.. y =e= sum(k, lambda(k)*ybar(k));

<!-- 第 6 页 -->
convexity.. sum(k, lambda(k)) =e= 1;

e1.. y =e= power(x,4) - 3*power(x,3) - 1.5*power(x,2) + 10*x;
e2.. y =e= -20*x+100;

lambda.lo(k) = 0;

x.lo = -5;
x.up = 5;

option optcr=0;
option optca=0;
option mip=cplex;
option nlp=conopt2;

model m1 /refrow, funrow, convexity, e2/;
solve m1 using mip maximizing y;

model m2 /e1,e2/;
solve m2 using nlp maximizing y;

|model|x∗|y∗|
|---|---|---|
|MIP model m1<br>NLP model m2|-3.243<br>-3.244|164.851<br>164.874|

#### Table 2: Results for problem P2

Notice that it is not needed to pass an initial solution to the MIP solvers.
LP/MIP solvers are in general not capable of dealing with level values, although
for large models it may be beneﬁcial to specify an advanced basis (this can be
accomplished by setting the marginal values). For MIP models, in many cases
the time it takes to solve the initial LP is negligible, in which case using an

#### advanced basis is not beneﬁcial.
It is noted that this SOS2 implementation implements a “grid search” and
thus sharp spikes may be missed altogether if the grid is too coarse.

### 2.3 Example: a discount schedule I
In some cases a piecewise linear function results naturally from the problem
deﬁnition. A good example is a discount schedule. As a basis we use the

#### transportation model from the User’s Guide:

$Title A Transportation Problem (TRNSPORT,SEQ=1)
$Ontext

This problem finds a least cost shipping schedule that meets
requirements at markets and supplies at factories.

References: Dantzig, G B, Linear Programming and Extensions

<!-- 第 7 页 -->
Princeton University Press, Princeton, New Jersey, 1963,
Chapter 3-3.

This formulation is described in detail in Chapter 2
(by Richard E. Rosenthal) of GAMS: A Users’ Guide.
(A Brooke, D Kendrick and A Meeraus, The Scientific Press,
Redwood City, California, 1988.)

The line numbers will not match those in the book because of
these comments.
$Offtext

Sets
i canning plants / seattle, san-diego /
j markets / new-york, chicago, topeka / ;

Parameters

a(i) capacity of plant i in cases
/ seattle 350
san-diego 600 /

b(j) demand at market j in cases
/ new-york 325
chicago 300
topeka 275 / ;

Table d(i,j) distance in thousands of miles
new-york chicago topeka
seattle 2.5 1.7 1.8
san-diego 2.5 1.8 1.4 ;

Scalar f freight in dollars per case per thousand miles /90/ ;

Parameter c(i,j) transport cost in thousands of dollars per case ;

c(i,j) = f * d(i,j) / 1000 ;

Variables
x(i,j) shipment quantities in cases
z total transportation costs in thousands of dollars ;

Positive Variable x ;

Equations
cost define objective function
supply(i) observe supply limit at plant i
demand(j) satisfy demand at market j ;

cost .. z =e= sum((i,j), c(i,j)*x(i,j)) ;

supply(i) .. sum(j, x(i,j)) =l= a(i) ;

demand(j) .. sum(i, x(i,j)) =g= b(j) ;

<!-- 第 8 页 -->
Model transport /all/ ;

Solve transport using lp minimizing z ;

Display x.l, x.m ;

Now assume the shipping costs ci,j are subject to a discount, as follows:

|from|through|discount|
|---|---|---|
|0<br>100<br>200<br>500<br>_>_ 1000|100<br>200<br>500<br>1000|0%<br>20%<br>40%<br>60%<br>80%|

#### Table 3: Discount schedule

Discounts are for shipments along the same link, and are implemented for
each case in the bracket. I.e. when shipping xi,j = 110 the ﬁrst 100 cases are not
discounted and the subsequent 10 cases are discounted by 20%. I.e. the total
discount for this shipment is 1.81818...%. The advantage of this schedule is that
the cost function is continuous and piecewise linear. If we assume ci,j = 0.225
(this is the shipment cost from Seattle to New-York without discount), then the

#### total shipment cost along this link is depicted in ﬁgure 4.
The following model implements the transportation model yusing the above
discount schedule. It is noted that the order of the indices in λi,j,dp is important:

#### the last index is reserved for the SOS set.

Sets
i canning plants / seattle, san-diego /
j markets / new-york, chicago, topeka / ;

Parameters

a(i) capacity of plant i in cases
/ seattle 350
san-diego 600 /

b(j) demand at market j in cases
/ new-york 325
chicago 300
topeka 275 / ;

Table d(i,j) distance in thousands of miles
new-york chicago topeka
seattle 2.5 1.7 1.8
san-diego 2.5 1.8 1.4 ;

Scalar f freight in dollars per case per thousand miles /90/ ;

<!-- 第 9 页 -->

#### Figure 4: Shipment costs including discount

Parameter c(i,j) transport cost in thousands of dollars per case ;

c(i,j) = f * d(i,j) / 1000 ;

Variables
x(i,j) shipment quantities in cases
z total transportation costs in thousands of dollars ;

Positive Variable x ;

Equations
cost define objective function
supply(i) observe supply limit at plant i
demand(j) satisfy demand at market j ;

cost .. z =e= sum((i,j), c(i,j)*x(i,j)) ;

supply(i) .. sum(j, x(i,j)) =l= a(i) ;

demand(j) .. sum(i, x(i,j)) =g= b(j) ;

Model transport /all/ ;

Solve transport using lp minimizing z ;

<!-- 第 10 页 -->
Display x.l, x.m ;

set dp ’discount points’ /d0,d1,d2,d3,d4/;

table discount(dp,*) ’discount percentages’
from disc
d0 0 0
d1 100 20
d2 200 40
d3 500 60
d4 1000 80
;

display c;

parameter xbar(dp);
xbar(dp) = discount(dp,’from’);

parameter ybar(i,j,dp);
ybar(i,j,dp)=0;
loop(dp,
ybar(i,j,dp) = ybar(i,j,dp-1)+ [xbar(dp)-xbar(dp-1)]*(1-discount(dp-1,’disc’)/100)*c(i,j);
);

display xbar,ybar;

sos2 variables lambda(i,j,dp) ’order of indices is important’;
positive variables y(i,j) ’total shipment costs’;

equations
refrow(i,j)
funrow(i,j)
convexity(i,j)
cost2
;

refrow(i,j).. x(i,j) =e= sum(dp, lambda(i,j,dp)*xbar(dp));
funrow(i,j).. y(i,j) =e= sum(dp, lambda(i,j,dp)*ybar(i,j,dp));
convexity(i,j).. sum(dp, lambda(i,j,dp)) =e= 1;
cost2.. z =e= sum((i,j), y(i,j));

option optcr=0;

model m2 /supply, demand, refrow, funrow, convexity, cost2/;
solve m2 using mip minimizing z;

Note that in the calculation of ¯yi,j,dp we use an explicit loop. This is needed
to enforce the order in which this assignment is executed: before we can calculate

#### ¯yi,j,dp, ¯yi,j,dp−1 should be known.

<!-- 第 11 页 -->

### 2.4 Example: a discount schedule II
Although the above schedule has the advantage of having monotonically in-
creasing shipping costs, the disadvantage is that it is somewhat complicated
to compute. A simpler scheme is to have a table with discounts on the whole
shipment. I.e. if we have the discounts as shown in table 2.4, the interpretation

#### is that a shipment of 110 cases gets a discount of 10%.

|from|through|discount|
|---|---|---|
|0<br>100<br>200<br>500<br>_>_ 1000|100<br>200<br>500<br>1000|0%<br>10%<br>20%<br>30%<br>40%|

#### Table 4: Discount schedule II
The cost function is now discontinuous, as can be seen in ﬁgure 5.

#### Figure 5: Discontinuous discount function

#### This can be implemented using the fragment:

<!-- 第 12 页 -->
set dp ’discount points’ /d0*d7/;

table discount(dp,*) ’discount percentages’
from disc
d0 0 0
d1 100 0
d2 100 10
d3 200 10
d4 200 20
d5 500 20
d6 500 30
d7 1000 30
;

display c;

parameter xbar(dp);
xbar(dp) = discount(dp,’from’);

parameter ybar(i,j,dp);
ybar(i,j,dp)=xbar(dp)*c(i,j)*(1-discount(dp,’disc’)/100);

display xbar,ybar;

sos2 variables lambda(i,j,dp) ’order of indices is important’;
positive variables y(i,j) ’total shipment costs’;

equations
refrow(i,j)
funrow(i,j)
convexity(i,j)
cost2
;

refrow(i,j).. x(i,j) =e= sum(dp, lambda(i,j,dp)*xbar(dp));
funrow(i,j).. y(i,j) =e= sum(dp, lambda(i,j,dp)*ybar(i,j,dp));
convexity(i,j).. sum(dp, lambda(i,j,dp)) =e= 1;
cost2.. z =e= sum((i,j), y(i,j));

option optcr=0;

model m2 /supply, demand, refrow, funrow, convexity, cost2/;
solve m2 using mip minimizing z;

### 2.5 Solvers
Here are some results of diﬀerent solvers on the above two models. All solvers
that support SOS2 sets perform about the same on these small models.

### 2.6 The reference row weights
Many solvers allow a reference row to be linked to the SOS variables. In the
GAMS links this information is lost: a dummy reference row is used where
needed and the actual reference row is just an LP row. To see what impact this

<!-- 第 13 页 -->

|Solver|Model|Nodes|Iterations|
|---|---|---|---|
|BDMLP<br>BDMLP<br>Cplex 7<br>Cplex 7<br>OSL 1<br>OSL 1<br>OSL 2<br>OSL 2<br>OSL 3<br>XA<br>XPRESS<br>XPRESS|I<br>96<br>211<br>II<br>55<br>149<br>I<br>131<br>177<br>II<br>71<br>111<br>I<br>145<br>214<br>II<br>105<br>161<br>I<br>145<br>215<br>II<br>105<br>161<br>SOS2 not supported<br>SOS2 not supported<br>I<br>61<br>86<br>II<br>30<br>53|I<br>96<br>211<br>II<br>55<br>149<br>I<br>131<br>177<br>II<br>71<br>111<br>I<br>145<br>214<br>II<br>105<br>161<br>I<br>145<br>215<br>II<br>105<br>161<br>SOS2 not supported<br>SOS2 not supported<br>I<br>61<br>86<br>II<br>30<br>53|I<br>96<br>211<br>II<br>55<br>149<br>I<br>131<br>177<br>II<br>71<br>111<br>I<br>145<br>214<br>II<br>105<br>161<br>I<br>145<br>215<br>II<br>105<br>161<br>SOS2 not supported<br>SOS2 not supported<br>I<br>61<br>86<br>II<br>30<br>53|

#### Table 5: Results

have we write out the problem as an MPS ﬁle. I only had access to a standalone

#### Cplex 6.5.1 system, so that is what I used.
To create an MPS ﬁle, the solver MPSWRITE can be used. However that
tool does not support SOS variable. So we used Cplex to generate the MPS ﬁle

#### and the SOS ﬁle.
We ﬁrst show the MPS ﬁle for the problem, ignoring the SOS variables (the

#### SOS section is removed):

NAME
ROWS
N obj
L c1
L c2
G c3
G c4
G c5
E c6
E c7
E c8
E c9
E c10
E c11
E c12
E c13
E c14
E c15
E c16
E c17
E c18
E c19
E c20
E c21
E c22
E c23

<!-- 第 14 页 -->
E c24
COLUMNS
x1 c1 1 c3 1
x1 c6 1
x2 c1 1 c4 1
x2 c7 1
x3 c1 1 c5 1
x3 c8 1
x4 c2 1 c3 1
x4 c9 1
x5 c2 1 c4 1
x5 c10 1
x6 c2 1 c5 1
x6 c11 1
x7 obj 1 c24 1
x8 c18 1
x9 c6 -100 c12 -18
x9 c18 1
x10 c6 -200 c12 -31.5
x10 c18 1
x11 c6 -500 c12 -58.5
x11 c18 1
x12 c6 -1000 c12 -81
x12 c18 1
x13 c19 1
x14 c7 -100 c13 -12.24
x14 c19 1
x15 c7 -200 c13 -21.42
x15 c19 1
x16 c7 -500 c13 -39.78
x16 c19 1
x17 c7 -1000 c13 -55.08
x17 c19 1
x18 c20 1
x19 c8 -100 c14 -12.96
x19 c20 1
x20 c8 -200 c14 -22.68
x20 c20 1
x21 c8 -500 c14 -42.12
x21 c20 1
x22 c8 -1000 c14 -58.32
x22 c20 1
x23 c21 1
x24 c9 -100 c15 -18
x24 c21 1
x25 c9 -200 c15 -31.5
x25 c21 1
x26 c9 -500 c15 -58.5
x26 c21 1
x27 c9 -1000 c15 -81
x27 c21 1
x28 c22 1
x29 c10 -100 c16 -12.96
x29 c22 1
x30 c10 -200 c16 -22.68
x30 c22 1
x31 c10 -500 c16 -42.12

<!-- 第 15 页 -->
x31 c22 1
x32 c10 -1000 c16 -58.32
x32 c22 1
x33 c23 1
x34 c11 -100 c17 -10.08
x34 c23 1
x35 c11 -200 c17 -17.64
x35 c23 1
x36 c11 -500 c17 -32.76
x36 c23 1
x37 c11 -1000 c17 -45.36
x37 c23 1
x38 c12 1 c24 -1
x39 c13 1 c24 -1
x40 c14 1 c24 -1
x41 c15 1 c24 -1
x42 c16 1 c24 -1
x43 c17 1 c24 -1
RHS
rhs c1 350 c2 600
rhs c3 325 c4 300
rhs c5 275 c18 1
rhs c19 1 c20 1
rhs c21 1 c22 1
rhs c23 1
BOUNDS
FR bnd x7
ENDATA

#### The SOS ﬁle looks like:

NAME gamsmodel
S2
x8 1
x9 2
x10 3
x11 4
x12 5
S2
x13 6
x14 7
x15 8
x16 9
x17 10
S2
x18 11
x19 12
x20 13
x21 14
x22 15
S2
x23 16
x24 17
x25 18
x26 19
x27 20

<!-- 第 16 页 -->
S2
x28 21
x29 22
x30 23
x31 24
x32 25
S2
x33 26
x34 27
x35 28
x36 29
x37 30
ENDATA

The SOS ﬁle has for every member of each set a weight. These weights form
the reference row. A rule normally imposed, is that the reference row values
for each set are strictly increasing. For GAMS/CPLEX this is done rather
artiﬁcially by incrementing a global counter for each SOS member. A proper

#### reference row implementation would be:

NAME y.mps
S2
x8 0
x9 100
x10 200
x11 500
x12 1000
S2
x13 0
x14 100
x15 200
x16 500
x17 1000
S2
x18 0
x19 100
x20 200
x21 500
x22 1000
S2
x23 0
x24 100
x25 200
x26 500
x27 1000
S2
x28 0
x29 100
x30 200
x31 500
x32 1000
S2
x33 0
x34 100
x35 200

<!-- 第 17 页 -->
x36 500
x37 1000
ENDATA

#### The results for the two SOS ﬁles are as follows:

|Solver|Model|Nodes|Iterations|
|---|---|---|---|
|Cplex 6.5.1<br>Cplex 6.5.1|I, dummy weights<br>I, reference row weights|131<br>92|175<br>112|

#### Table 6: SOS2 weights

From the results in table 2.6 we see that the performance can increase by
using proper weights. Unfortunately, GAMS does not support any facility to
specify these. 1. Most likely the performance penalty will be small if the for an

#### evenly spaced grid.
It is noted that for model II, the weights can not be identical to the reference

#### row values, because they are not strictly increasing.

### 2.7 SOS2 variables modeled using binary variables
If a solver does not have SOS2 variables we can use binary variables. Let λ1...λk
form a SOS2 set. Then we can introduce binary variables δ1...δk−1, with:

#### λ1 ≤δ1 (7)

#### λi ≤δi−1 + δi for 2 ≤i ≤k −1 (8)

#### λk ≤δk−1 (9)

#### and
k

#### X δi = 1 (10)
i=1

#### The GAMS implementation looks like:

Sets
i canning plants / seattle, san-diego /
j markets / new-york, chicago, topeka / ;
Parameters
a(i) capacity of plant i in cases
/ seattle 350
san-diego 600 /
1An experimental implementation of a nonlinear branch-and-bound code link by the author
allowed to set SOS weights by specifying unequal priorities to set-members

<!-- 第 18 页 -->
b(j) demand at market j in cases
/ new-york 325
chicago 300
topeka 275 / ;

Table d(i,j) distance in thousands of miles
new-york chicago topeka
seattle 2.5 1.7 1.8
san-diego 2.5 1.8 1.4 ;

Scalar f freight in dollars per case per thousand miles /90/ ;

Parameter c(i,j) transport cost in thousands of dollars per case ;

c(i,j) = f * d(i,j) / 1000 ;

Variables
x(i,j) shipment quantities in cases
z total transportation costs in thousands of dollars ;

Positive Variable x ;

Equations
cost define objective function
supply(i) observe supply limit at plant i
demand(j) satisfy demand at market j ;

cost .. z =e= sum((i,j), c(i,j)*x(i,j)) ;

supply(i) .. sum(j, x(i,j)) =l= a(i) ;

demand(j) .. sum(i, x(i,j)) =g= b(j) ;

set dp ’discount points’ /d0,d1,d2,d3,d4/;

table discount(dp,*) ’discount percentages’
from disc
d0 0 0
d1 100 20
d2 200 40
d3 500 60
d4 1000 80
;

display c;

parameter xbar(dp);
xbar(dp) = discount(dp,’from’);

parameter ybar(i,j,dp);
ybar(i,j,dp)=0;
loop(dp,
ybar(i,j,dp) = ybar(i,j,dp-1)+ [xbar(dp)-xbar(dp-1)]*(1-discount(dp,’disc’)/100)*c(i,j);
);

display xbar,ybar;

<!-- 第 19 页 -->
positive variables lambda(i,j,dp);
binary variables delta(i,j,dp);
positive variables y(i,j) ’total shipment costs’;

set dp1(dp);
dp1(dp)$(ord(dp)<card(dp)) = yes;

equations
refrow(i,j)
funrow(i,j)
convexity(i,j)
cost2
sos(i,j,dp)
sumdelta(i,j)
;

refrow(i,j).. x(i,j) =e= sum(dp, lambda(i,j,dp)*xbar(dp));
funrow(i,j).. y(i,j) =e= sum(dp, lambda(i,j,dp)*ybar(i,j,dp));
convexity(i,j).. sum(dp, lambda(i,j,dp)) =e= 1;
cost2.. z =e= sum((i,j), y(i,j));
sos(i,j,dp).. lambda(i,j,dp) =l= delta(i,j,dp-1) + delta(i,j,dp)$(dp1(dp));
sumdelta(i,j).. sum(dp1, delta(i,j,dp1)) =e= 1;

option optcr=0;

model m2 /supply, demand, refrow, funrow, convexity, cost2, sos, sumdelta/;
solve m2 using mip minimizing z;

Model II can be adapted in a similar manner. Results for this model are

#### depicted in table 2.7.

|Solver|Model|Nodes|Iterations|
|---|---|---|---|
|BDMLP<br>BDMLP<br>Cplex 7<br>Cplex 7<br>OSL 1<br>OSL 1<br>OSL 2<br>OSL 2<br>OSL 3<br>OSL 3<br>XA<br>XA<br>XPRESS<br>XPRESS|I<br>II<br>I<br>II<br>I<br>II<br>I<br>II<br>I<br>II<br>I<br>II<br>I<br>II|108<br>320<br>15<br>7<br>94<br>183<br>140<br>186<br>na<br>na<br>45<br>128<br>52<br>109|566<br>2840<br>147<br>80<br>341<br>651<br>445<br>816<br>307<br>759<br>237<br>877<br>271<br>652|

#### Table 7: Results

<!-- 第 20 页 -->

### 2.8 Piecewise functions in AMPL
The modeling language AMPL has an interesting language extension to express
piecewise linear functions. If x is a variable, then the expression

#### <<{i in 1..n} b[i]; {i in 0..n} s[i]>> x
is a piecewise linear function with slope si if bi ≤x ≤bi+1. In addition AMPL
can use a .sosno and .ref suﬃx to indicate a SOS set and a breakpoint value

#### (reference row value).

## 3 Other approaches
Other approaches to implement interpolation are Least Squares Regression and
Splines. Both are discussed in http://www.gams.com/interface/fitpack.

#### pdf.
