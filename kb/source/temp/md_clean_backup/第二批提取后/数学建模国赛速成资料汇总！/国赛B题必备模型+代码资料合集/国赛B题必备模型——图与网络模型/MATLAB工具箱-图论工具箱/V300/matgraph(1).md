<!-- 第 1 页 -->
MATGRAPH: A MATLAB TOOLBOX FOR GRAPH THEORY

EDWARD R. SCHEINERMAN

OVERVIEW
MATGRAPH is a toolbox for working with simple1 graphs
This document gives an overview of the MATGRAPH tool-
in MATLAB. The goal is to make interactive graph theory ex- box. More information can be found in the accompanying web
ploration simple and efﬁcient. pages (see §3).
In order to use this toolbox, you need a copy of MATLAB, In addition to providing a graph class, MATGRAPH also
available from The MathWorks. A few of the MATGRAPH deﬁnes helper classes for working with permutations (see §4)
functions require the additional Optimization Toolbox, also and partitions (see §5).
available from The MathWorks.

### 1. GETTING MATGRAPH

1.1. Download and install. MATGRAPH is available for free This should create a directory named matgraph. You may
from my web site. Go to move this directory to any convenient location on your hard
http://www.ams.jhu.edu/˜ers/matgraph drive.
and select the link in the sentence “You can download Mat-
graph by clicking here.”
1.2. License. This software is copyrighted by Edward
This should cause the ﬁle matgraph-X.X.tgz to be down-
R. Scheinerman and released free of charge under the GNU
loaded to your computer. (The X.X is the version number.)
General Purpose Licenses. A copy of this license can be found
This is a compressed archive. To unpack on a UNIX system,
at
give the command
http://www.gnu.org/licenses/gpl.html
tar xfz matgraph-X.X.tgz
(where X.X is replaced by the correct version number). On I would like to make this tool as useful to as many people as
other computers, double clicking on the ﬁle’s icon should serve possible. I invite you to send me improvements for the current
the same purpose. .m ﬁles as well as new .m ﬁles for added functionality.

### 2. USING MATGRAPH

2.1. Basic principles. We assume the reader is familiar with MATGRAPH functions are capable of modifying their
MATLAB. Before we discuss how to use MATGRAPH, it is arguments.
crucial that the following basic principles be understood. Most MATLAB functions use call by value seman-
tics. That is, a copy of the argument is sent to the func-
- All graphs handled by MATGRAPH are simple and tion. For example, suppose we have a function named
undirected. That is, these graphs do not have loops func deﬁned in a ﬁle func.m. In MATLAB, issuing
or multiple edges. Each pair of distinct vertices either the command func(A) does not affect the value held
is not adjacent or else is joined by a single edge. in the ordinary variable A.
- The vertex set of all graphs in MATGRAPH is always MATGRAPH, however, is designed differently.
of the form {1,2,...,n} where n ≥0 is the number of Function arguments of type graph use call by refer-
vertices in the graph. ence semantics. This means that a command such as
An important consequence of this is that when a add(g,2,4) can modify the graph g (in this case, by
vertex is deleted from a graph, all vertices with higher adding an edge joining vertices 2 and 4).
value are renumbered. Not all MATGRAPH functions modify their argu-
- All graphs in MATGRAPH are specially deﬁned graph ments, but they all use call by reference for graph ar-
objects. They do not behave in the same manner as, guments. For functions that are capable of modifying
say, matrices in MATLAB. For the sake of efﬁciency, graphs, the graph that is modiﬁed is always the ﬁrst
Date: 2006:10:01:04:49.
1Simple graphs are undirected graphs without loops or multiple edges.

<!-- 第 2 页 -->

# 2 ED SCHEINERMAN

argument to the function. For example, MATGRAPH Every time a graph variable is declared, one these slots is
provides a line_graph function. The command taken to hold the data for the graph. If a graph variable is no
line_graph(g,h) longer needed, then its slot can be released like this:
overwrites g with the line graph of h. The graph h is free(g)
not affected. For more detail, see §2.3.
If, inadvertently, a graph variable is cleared from MATLAB’s
- As a consequence of how graphs are stored in
workspace, there is no convenient way to free the slot it occu-
matgraph, the only time a graph variable should ap-
pied.
pear on the left hand side of an assignment statement
Freeing a graph’s slot is not generally necessary when
is when the variable is initialized like this:
working at MATLAB’s command prompt. Graphs can be
g = graph
modiﬁed repeatedly and one need not declare more graph vari-
At no other time should a graph variable appear to the ables than the number of graphs one is currently considering.
left of an equal sign. However, releasing the slot held by a graph is vital in .m
ﬁles. It is often useful for a function to declare a graph vari-
2.2. Starting MATGRAPH. Launch MATLAB and be sure
able temporarily. Every graph that is created using the
that the MATGRAPH directory is visible on MATLAB’s path.
g=graph constructor must be released by a matching call
This can be done with MATLAB’s addpath function. For ex-
to free(g). Otherwise, each time the function is invoked,
ample:
another slot in MATGRAPH’s hidden data structure is con-
addpath(’/home/betty/programming/matgraph/’)
sumed until no slots remain available.
assuming Betty placed the matgraph directory inside a folder To make a copy of a graph, we must not use the statement
named programming on her computer. h=g. Rather, use copy(h,g).
The next step is to initialize the MATGRAPH system. This
is done by giving the following command:
2.4. Basic graph operations. The statement g=graph creates
graph_init
a new graph with no vertices or edges. It is now possible to add
This sets up hidden data structures (see §6) used by MAT-
and to delete vertices and edges using the resize, add, and
GRAPH. MATLAB responds:
delete functions. For each of these, the graph to be modiﬁed
Graph system initialized. Number of slots = 500. is the ﬁrst argument (see the discussion of basic principles in
MATGRAPH is now ready to work with graphs. By default, §2.1).
the system can handle 500 different graphs. This should be
  - resize(g,n) changes the number of vertices in g to
adequate for most purposes. However, if you need an array
the value held in n. If n is greater than the number
of, say, 1000 graphs, then this is not sufﬁcient. Alternatively,
of vertices in g, then additional, isolated vertices are
MATGRAPH may be initialized with an explicit argument spec-
added. On the other hand, if n is less than the number
ifying the number of “slots” (place holders for graphs) like
of vertices in g, then the highest numbered vertices
this:
are deleted leaving a graph with n vertices. For ex-
graph_init(20000) ample, if g has 10 vertices and we invoke the com-
If you ever wish to delete all of the hidden data structures mand resize(g,7), then vertices 8, 9, and 10 are
(and thereby erasing all graphs held therein), use the function deleted (and all edges incident on these vertices are
graph_destroy. also deleted).
See also2 the free_all, num_available, and • add(g,u,v) adds an edge between u and v to the
max_available functions. graph. If either of these values is nonpositive, or if
they are equal, nothing happens. If either u or v is
2.3. Declaring graph objects and memory management.
greater than the number of vertices currently in g, the
Before working with graphs, it is necessary to declare vari-
graph is expanded to have max{u,v} vertices.
able(s) to be of type graph. This runs against MATLAB’s
Another way to use add is like this: add(g,elist)
philosophy that variables do not need to be declared, but is
where elist is a k×2 array of positive integers. Each
necessary for the sake of efﬁciency.
row of elist is considered an edge, and all of these
To declare a variable, say g, to be of type graph, we give
edges are added to the graph. If any end point of any
the following command:
edge is larger than the number of vertices currently in
g = graph; the graph, the graph is resized to accommodate.
It is helpful to read this as “let g be a graph.” This is the only The automatic resizing has the potential side effect
circumstance in which a graph object may appear to the of adding isolated vertices. For example, if g has 5
left of an equal sign. vertices, and we then give the command add(g,3,7)
Behind the scenes, one of the “slots” allocated for graphs the graph is resized to have 7 vertices. Vertex 6 is
(by graph_init) is set aside for the graph g. added as an isolated vertex.
2See §3 for a description of the web-based information on all MATGRAPH functions. When we direct the reader to see a particular function, we typically
mean to view that function’s documentation with a web browser or by using MATLAB’s help command.

<!-- 第 3 页 -->
MATGRAPH 3

Remember: The vertex set of all graphs in MAT- Other general graph builders include path, cycle, grid,
GRAPH are always of the form {1,2,...,n} where wheel, cube, circulant, and paley. Speciﬁc graphs can be
n ≥0. formed using these: bucky, dodecahedron, icosahedron,
- delete is used to delete vertices or edges from a octahedron, and petersen. Various random graphs
graph. can be built using these functions: random, sprandom,
– delete(g,v) deletes the vertex v from the random_bipartite, and random_regular.
graph. (If v is not a vertex of the graph, there
is no effect.)
2.6. Graph operations. MATGRAPH provides a variety of
All vertices with number greater than v have their
operations to form new graphs from old. For example,
values decreased by 1. For example, suppose g line_graph(h,g) sets h to be the line graph3 of g. Other
is a path graph with edges 1 ∼2 ∼3 ∼4 ∼5.
operations include cartesian, complement, mycielski,
When we give the command delete(g,3) ver-
induce, intersect, union, and trim.
tex 3 is deleted from the graph, and vertices 4 and
Breadth-ﬁrst and depth-ﬁrst spanning trees can be found us-

# 5 get renamed 3 and 4, respectively. Thus, af-
ing bfstree and dfstree. See also nsptrees.
ter delete(g,3) the vertex set of g is {1,2,3,4}
and the only edges are 1 ∼2 and 3 ∼4.
– delete(g,vlist) deletes an entire set of ver- 2.7. Graph inspectors. The functions nv(g) and ne(g) give
tices. In this form, vlist is a k ×1 array of pos- the number of vertices and edges of g. These two values are
itive integers. All vertices in vlist are deleted returned by size(g) in a 1×2 array.
from the graph, and then vertices are renamed so There are two ways to see if an edge is present in a graph
the vertex set remains of the form {1,2,...,n}. g. The command has(g,u,v) returns 1 (for true) if the edge
For example, if g is a cycle on 5 vertices between u and v is present in g, and 0 otherwise. Alternatively,
with edges 1 ∼2 ∼3 ∼4 ∼5 ∼1, then the same result is produced by g(u,v).
delete(g,[2;3]) deletes vertices 2 and 3 from The neighborhood of a vertex is returned by the command
the graph (leaving edges 4 ∼5 ∼1) and then neighbors(g,v); the result is a list (one-dimensional array)
renumbers vertices 4 and 5 with the new names 2 of the vertices adjacent to v. The same result is returned by
and 3, so the ﬁnal result is the path 2 ∼3 ∼1. g(v).
– delete(g,u,v) deletes the edge between u and The degree of a vertex is given by deg(g,v). With only
v from the graph. If this edge is not present in the a single argument, deg(g) returns the degree sequence of the
graph, nothing happens. graph.
– delete(g,elist) deletes a list of edges from find_path(g,u,v) ﬁnds a shortest path from u to v (re-
the graph. The variable elist must be a k × 2 turned as a list of vertices on the path); if no such path exists,
array of positive integers. an empty array is returned.
Point to notice: delete(g,[3;4]) deletes vertices isconnected(g) returns 1 (true) if g is connected and 0
3 and 4 from the graph (second argument is a column (false) otherwise.
vector) whereas delete(g,[3,4]) deletes the edge The components of a graph can be found using
3 ∼4 from the graph (second argument is a k × 2 ar- components(g). This returns a partition object (see §5) each
ray where k happens to equal 1). of whose blocks is the vertex set of a component of g.
See also the clear_edges function that deletes all The distance between vertices can be found with
edges from a graph. dist(g,u,v). The form dist(g,u) returns an array giving
See also set_matrix (described in §2.8). the distances from u to all the vertices in the graph. Calling
See also
contract. dist(g) returns a square matrix giving the distances between
all pairs of vertices. See diam.
2.5. Standard graphs. MATGRAPH provides several func-
tions for forming standard graphs. One of the more versatile is
2.8. Graph–matrix conversions. The adjacency matrix of a
the complete function for creating complete graphs, complete
graph is returned by matrix(g). This returns a square log-
bipartite graphs, and complete multipartite graphs:
ical matrix. To use this matrix arithmetically, convert it to
- complete(g) adds all possible edges to g without class double; for example, the following command returns the
changing its vertex set. eigenvalues of (the adjacency matrix of) a graph:
- complete(g,n) sets g to be the complete graph Kn.
eig(double(matrix(g)))
- complete(g,n,m) sets g to be the complete bipartite
graph Kn,m. Conversely, given a square, symmetric, zero-one, zero-
- complete(g,list) sets g to be the complete mul- diagonal matrix A, we can set g to have this matrix as its adja-
tipartite graph K(a1,a2,...,at) where the indices are cency matrix like this: set_matrix(g,A).
the entries in list. See also spy, laplacian, and incidence_matrix.
3The line graph of G is a graph L(G) whose vertex set is E(G). Two vertices e1 and e2 of L(G) are adjacent in L(G) provided, when considered as edges
of G, they are incident with a common vertex.

<!-- 第 4 页 -->

# 4 ED SCHEINERMAN

2.9. Graph invariants and partitions. In addition to basic ﬁle named in filename must be one created by MAT-
information functions described in §2.7, MATGRAPH can cal- GRAPH’s save command and not just a list of edges.
culate other invariants and features of graphs of interest to
MATGRAPH provides a function named sgf which stands
graph theorists. These include alpha (independence number),
for simple graph format. This function converts graphs to and
omega (clique number), and dom (domination number). (All
from a 2-column matrix whose rows have the following mean-
three of these use the integer programming facilities in MAT-
ings:
LAB’s Optimization Toolbox.) See also diam.
The bipartition function determines whether a graph is • The ﬁrst row is [n m] where n is the number of vertices
bipartite; if it is, it returns the bipartition as a partition and m is the number of edges in the graph.
object (see §5). Otherwise (the graph is not bipartite) • The next m rows give the edges of the graph; each row
bipartition returns an empty partition. is of the form [u v] where 1 ≤u̸ = v ≤n.
A graph coloring algorithm is available in the color func- • Optionally, an additional n rows give the locations of
tion. This returns a partition of the vertex set of a graph into the vertices. Row number m+1+i is [xi yi] and spec-
independent sets by a greedy coloring algorithm (step through iﬁes the coordinates of vertex i.
the vertices in decreasing degree order and give the ﬁrst avail-
Matrices of this form are easy to read or to write on disk, and
able color to each vertex in turn). Alas, this generally does not
this format is easy for other programs to produce.
ﬁnd a coloring with χ(G) colors.
In addition, it is possible to create .m ﬁles for saving graphs
The chromatic polynomial of a graph can be found for small
to be used by other programs. For example, MATGRAPH’s
graphs. For example:
dot command writes graphs to disk in a format that can be
>> g = graph; processed by GraphViz’s dot program. See also graffle.
>> cycle(g,5)
>> chromatic_poly(g)
ans = 2.11. Handling large graphs. Behind the scenes, graphs in
1 -5 10 -10 4 0 MATGRAPH are saved as square matrices. A graph with, say,
shows that the chromatic polynomial of C5 is ten thousand vertices would occupy an array with 100 million
x5 −5x4 +10x3 −10x2 +4x. entries. MATLAB provides the ability to handle matrices large
matrices with few nonzero entries efﬁciently. This ability is
2.10. Input-output. MATGRAPH can read and write graphs embedded into MATGRAPH.
in ﬁles on the user’s hard disk. Small graphs are best handled using full storage. By de-
Suppose the user wishes to build a graph using some other fault, a graph created by g = graph uses full storage. It is
software (such as a C program written by the user) and then easy, however, to convert a graph to use sparse storage.
read that graph into MATGRAPH. To do this, the data should • sparse(g) converts a graph’s storage method to be
be saved in a ﬁle as a list of edges. Each line of the ﬁle should sparse. This is useful for extremely large graphs with
contain exactly two integers separated by white space. These relatively few edges (i.e., small average degree).
integers should range from 1 to the number of vertices in the • full(g) converts a graph’s storage to full mode. This
graph. Let’s say that this data is saved in a ﬁle named mygraph.
is the preferred method for small graphs and graphs
The MATLAB command load mygraph reads the ﬁle
with many edges.
mygraph and saves the contents of that ﬁle in a variable that
is also named mygraph. (MATLAB’s current working direc- One can check the type of storage in use with the issparse
tory must be the same as the directory that contains the ﬁle and isfull functions.
mygraph.) The graph constructor g = graph takes an optional argu-
The variable mygraph is an m×2 array of edges. This can ment; one can write g = graph(n) where n is a nonnegative
be converted into a graph like this: integer. This creates a new graph with n vertices. If n is small,
g = graph(mygraph) full storage is used for g. If n is large, sparse storage is auto-
or if the graph g already exists, like this: matically provided. How large is “large”? See set_large.
resize(g,0)
add(g,mygraph)
2.12. Labels. Naming vertices as consecutive integers from
(The resize(g,0) clears all data from g.) 1 to n can be inconvenient. MATGRAPH provides a means
MATGRAPH also provides its own save and load com- to assign text labels to vertices. The command label can be
mands. used to assign such labels to vertices: label(g,v,string)
- save(g,filename) saves the graph g to the user’s assigns the characters in string to be a label for vertex v. If
hard drive in a ﬁle named in filename. (For example, a vertex of a graph is deleted, all higher numbered vertices
save(g,’mygraph’).) This saves all the information are renumbered, but their labels are retained. The command
about the graph and not just a list of edges. get_label is used to learn the label of an individual vertex or
- load(g,filename) reads the graph data in the ﬁle to return a list of all labels on all vertices in a graph. See also
named in filename and sets g to be that graph. The clear_labels.

<!-- 第 5 页 -->
MATGRAPH 5

2.13. Visualization. It is often useful to be able to see pic- of xy. The command randxy(g) sets the coordinates of the
tures of graphs. MATGRAPH provides a basic means to do vertices to random locations.
this. To learn the current embedding of a graph, use getxy(g).
One may associate an embedding with a graph; this is a To erase a graph’s embedding, use rmxy(g). See also hasxy.
mapping from the vertex set to points in the plane. Two MATGRAPH methods are provided to calculate embed-
The command draw draws a picture of the graph in the dings based on the graph’s structure: springxy and distxy.
plane by placing each vertex at its x,y-coordinates and join- Both of these require MATLAB’s Optimization Toolbox and
ing adjacent vertices by line segments. See also ndraw and are only useful for small graphs. Both use the graph’s current
ldraw. Note that draw simply draws the graph in the current embedding as a starting point for an optimal embedding (but
ﬁgure window without erasing the contents of that ﬁgure; to with different objective functions for the two methods).
see only the graph, ﬁrst give the MATLAB command clf. springxy ﬁnds an embedding by modeling vertices as re-
When draw is invoked for graphs without embeddings, pelling objects with edges acting as springs that attract the
a default, circular embedding is automatically constructed. nodes they join. distxy attempts to place vertices in the plane
Some graph building operations attach an embedding to the so that their Euclidean distance matches their graph theoretic
graphs they form; for example, petersen(g) sets g to be the distances; greater emphasis is given to vertices at smaller dis-
Petersen graph with vertices located at classic coordinates. tances. Of these, distxy runs faster and gives reasonable re-
It is possible to set a graph’s embedding to coordinates of sults.
your choosing with the embed command. If g has n vertices Readers are warmly encouraged to submit other embedding
and xy is an n×2 matrix of real numbers, then embed(g,xy) algorithms for incorporation into MATGRAPH.
sets the coordinates of the vertices to the corresponding rows

### 3. DOCUMENTATION

This introduction to MATGRAPH does not list every func- names are overloaded. For example, the name delete is both
tion available to the user. However, all functions (in .m a built-in MATLAB command and a MATGRAPH function.
ﬁles) are documented in the accompanying web pages. These Type help graph/delete to access the MATGRAPH version.
web pages are housed in the html subdirectory of the main For a list of all methods available for graph objects, type
matgraph folder. Double clicking on the ﬁle index.html methods graph.
opens the main documentation page in a web browser. From See also Matgraph By Example in the doc directory.
here, all the .m ﬁles can be found including descriptions, cross The web pages in the html directory were generated by by
references, and source code. This includes the supporting the m2html package created by Guillaume Flandin; this utility
classes partition and permutation. can be found on the MathWorks’ web site.
In addition, the user may get help on any MATGRAPH com-
mand with MATLAB’s usual help command. Some command

### 4. THE PERMUTATION CLASS

Included in this toolbox is a class called permutation. returned. Composition of permutations is denoted by multipli-
These objects represent permutations of the integers cation, *. Repeated composition can be achieved using the ˆ
{1,2,...,n}. Unlike graphs, these object behave accord- operator: pˆ3 is equivalent to p*p*p. The power may be zero
ing to the usual MATLAB conventions and do not need to be or negative.
specially declared. permutation objects are used by MAT- Equality and inequality of permutations can be checked
GRAPH’s renumber command. with == and ˜=, respectively.
The standard way to build a permutation p is to specify its Here are the functions deﬁned for the class permutation.
action with a vector of the form [a1,a2,...,an] where ai = p(i). Their .m ﬁles are found in the @permutation folder.
For example:
>> p = permutation( [2 1 3 5 6 4] )
  - array: convert a permutation to an array. The syntax
(1,2)(3)(4,5,6) is array(p). This returns a 1×n array whose ith en-
This assigns to p a permutation in which p(1) = 2, p(2) = 1, try if p(i). For example, if p = (1,2)(3)(4,5,6), then
p(3) = 3, p(4) = 5, p(5) = 6, and p(6) = 4. Note that p is array(p) returns the array [2,1,3,5,6,4].
displayed on the console using the standard disjoint cycle no- • cycles: determine the cycle structure of a permuta-
tation. tion. The syntax is cycles(p). This returns a cell
The basic operations of applying a permutation to an ele- array. Each member of the cell array contains the
ment and composition of permutations are implemented. Typ- elements (in order) of a cycle of p. For example, if
ing p(k) returns the action of the permutation p on the ele- p = (1,2)(3)(4,5,6), then c=cycles(p) sets c{1} to
ment k. If k is not in scope (outside the range 1 to n), then 0 is [1,2], c{2} to [3], and c{3} to [4,5,6].

<!-- 第 6 页 -->

# 6 ED SCHEINERMAN

- inv: permutation inverse. The syntax is inv(p). This [2 1 3 5 6 4], then permutation(x) gives the
returns the inverse permutation, p−1. permutation (1,2)(3)(4,5,6).
- length: number of elements permuted. The syntax • random: shufﬂe a permutation. The syntax is
is length(p). For example, if p = (1,2)(3)(4,5,6), random(p). This returns a permutation on the same
then length(p) is 6. elements as p but in a random order. Typically, to gen-
- matrix: return a permutation matrix that represents erate a random permutation on n elements, one would
the permutation. The syntax is matrix(p). For ex- type this: random(permutation(n)).
ample, if p = (1,2)(3)(4,5,6), then matrix(p) gives • sign: sign (parity) of a permutation. The syntax is
this: sign(p). This returns 1 is p is an even permutation
and −1 is p is an odd permutation.

# 0 1 0 0 0 0
  - size: give the number of elements and number of cy-

# 1 0 0 0 0 0
cles in a permutation. The syntax is size(p). This

# 0 0 1 0 0 0
returns a two-element array. The ﬁrst element is the

# 0 0 0 0 0 1
number of objects permuted by the permutation and

# 0 0 0 1 0 0
the second element is the number of cycles in the

# 0 0 0 0 1 0
disjoint-cycle representation of p.
- permutation: class constructor. This can be called MATLAB uses this when reporting on per-
two ways. If n is a positive integer, permutation(n) mutation variables in the workspace. The
returns the identity permutation on {1,2,...,n}. If permutation (1,2)(3)(4,5,6) is described as a
x is an array containing the elements 1 through <6x3 permutation>. The 6 refers to the fact that
n, then permutation(x) creates the permutation this is a permutation of the set {1,2,...,6} and the 3
speciﬁed by those elements. For example, if x is refers to the fact that this permutation has 3 cycles.

### 5. THE PARTITION CLASS

The partition class represents partitions of sets of the the parts containing j and k have been merged into a
form {1,2,...,n}. A partition can be created with the com- single part.
mand p=partition(n). This creates a partition in which all • np: number of parts. The syntax is np(p); the number
parts have size 1; that is, the partition {1},{2},...,{n} . A of parts in the partition is returned.
partition can also be created from a cell array. Each cell in the • nv: size of the ground set. The syntax is nv(p); the
array should list the elements of a block; the integers 1 through number of elements in the ground set of the partition
n should appear exactly once in each member of the cell array. is returned.
For example, if we type • partition: constructor for this type. The simple syn-
c = {[1 2 4],[3 5 6],[7:10]}; tax is partition(n) (where n is a positive integer).
p = partition(c) This builds a partition with ground set {1,2,...,n} in
which there are n parts (all of size one).
Then p is the partition {1,2,4},{3,5,6},{7,8,9,10} and
Alternatively, if c is a cell array, then
MATLAB types this:
partition(c) creates a partition based on the ar-
{ {1,2,4} {3,5,6} {7,8,9,10} }
rays in c. Each of c{1}, c{2}, and so on, is a list of
If p is a partition and k is an integer, the expression p(k) integers. Together, these lists should contain each of
returns the elements in the same part as k. For the partition the integers in [n] exactly once.
presented above, p(2) would return the array [1 2 4]. For • parts: get the parts of the partition. The syntax is
integers j and k, the expression p(j,k) returns true if j and k parts(p). This returns a cell array. Each cell con-
are in the same part of p and false otherwise. tains a list (vector) of positive integers in one of the
The meet and join of two partitions is computed using p*q parts of p.
and p+q, respectively. Equality and inequality can be checked • size: report the number of elements in the ground set
with == and ˜=. and the number of parts. The syntax is size(p). This
Partitions can be converted into cell arrays with the parts returns a 1×2 array [n m] where n is the size of the
function. ground set and m is the number of blocks.
Here is a list of the various functions deﬁned for the This is used by MATLAB when it reports the vari-
partition class; these can be found in the @partition ables in a workspace. A partition is reported like
folder. this: <10x3 partition>. This means the partition’s
- merge: combine two parts. The syntax is ground set is [10] and there are three parts in the par-
merge(p,j,k). This returns a new partition in which tition.

<!-- 第 7 页 -->
MATGRAPH 7

6. UNDER THE HOOD (STUFF YOU DON’T NEED TO KNOW)

All data about graphs are held in a hidden global data struc- 6.1.2. The private double-ended queue. The Q ﬁeld of
ture named GRAPH_MAGIC. Objects of type graph are simply GRAPH_MAGIC is a double-ended queue available for use by
indices into this structure. This enable us to simulate call- graph algorithms (e.g., bfstree). It is a structure that con-
by-reference semantics for graph objects; that is, MATLAB tains three ﬁelds:
functions can modify graph arguments. • array: a one-dimensional array that holds the
It is possible to save the entire GRAPH_MAGIC structure into stack/queue values.
another variable; this would allow multiple “graph theory uni- • first: an index pointing to the ﬁrst (front most) ele-
verses” to coexist. It’s not clear this is needed. ment of the queue.
  - last: an index pointing to the last (back most) ele-
6.1. The GRAPH MAGIC structure. The global data struc-
ment of the queue.
ture is named GRAPH_MAGIC. To access this structure directly,
There is a small suite of tools for working with the queue in
use the following line in your .m ﬁles:
the directory @graph/private. These are visible to functions
global GRAPH_MAGIC inside the @graph directory, but not generally available. Here
The GRAPH_MAGIC structure contains the following ﬁelds: they are (in alphabetical order):
- ngraphs: the number of “slots” available in • q_capacity: gives the maximum capacity of the
this structure (equal to the size of the arrays queue.
GRAPH_MAGIC.graphs and GRAPH_MAGIC.in_use). • q_get: returns a list of the elements in the queue (that
- graphs: this is a cell array containing the graphs. is, array(first:last)).
(See §6.1.1.) • q_init: called with one argument, this initializes the
- in_use: an array that indicates which slots are taken. queue with a given capacity.
A 1 in position i of this array signals that slot i is taken; • q_pop_back: pops off (and returns) the last element
a 0 means the slot is available to hold a new graph. of the queue. This is a stack-like operation.
- Q: a structure implementing a double-ended queue. • q_pop_front: pops off (and returns) the front most
(See §6.1.2.) element in the queue. This is a queue-like operation.
- large_size: a variable holding the cutoff between • q_push: called with one argument, this adds an ele-
“large” and “small” graphs. If the graph construc- ment to the back of the queue.
tor graph is fed a large argument, it creates a sparse • q_size: returns the number of elements in the queue.
graph.
6.2. The graph type. The graph type is simply a “wrap-
per” for an integer; that integer is an index into the
6.1.1. Inside GRAPH MAGIC.graphs. The cell array
GRAPH_MAGIC.graphs array. A graph object contains just one
GRAPH_MAGIC.graphs holds the graphs. Each cell in this
ﬁeld, idx, which holds that integer.
array is a structure with two ﬁelds: array and xy. The array
In many graph functions (in the @graph directory) we see
ﬁeld holds the adjacency matrix of the graph (a zero-one,
the following:
symmetric matrix). The xy ﬁeld holds the embedding for the
graph; this is an n × 2 array of real values giving the coordi- GRAPH_MAGIC.graphs{g.idx}.array
nates of the vertices. This is how we refer to the adjacency matrix of the graph g.

### 7. FUTURE PROJECTS

There are many additions I would like for this project. Here hardly fast. Both rely on the Optimization Toolbox.
are few: I’d like a better layout engine.
  - A GUI for creating and editing graphs. I’d like to
- Planarity testing and embedding. I would like an see this invoked with a command such as gui(g) or
is_planar method to test if a graph is planar and a graph_edit(g).
good planar_embed method for ﬁnding a crossing- • We need .m ﬁles for connectivity, edge connectiv-
free embedding. ity, maximum matching (in general graphs), isomor-
- The current springxy routine is extremely slow and phism, approximate isomorphism, better heuristic col-
gives lousy results. The newer distxy is better, but oring algorithms, girth, and so forth.

DEPARTMENT OF APPLIED MATHEMATICS AND STATISTICS, THE JOHNS HOPKINS UNIVERSITY, BALTIMORE, MARYLAND 21218-2682 USA
E-mail address: ers@jhu.edu
