#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>

#define HASHSIZE  10007 /* prime number is better, MB */
#define ETA_START_SIZE 10000 /* start size of array Eta. Realloced if needed */
#define FNAMLEN 64
#define NAMELEN 25
#define MAXSTRL (NAMELEN-1)
#define STD_ROW_NAME_PREFIX "r_"

#define	FALSE	0
#define	TRUE	1

#define LE      0
#define EQ      1
#define GE      2
#define OF      3

#define OPTIMAL    0
#define MILP_FAIL  1
#define INFEASIBLE 2
#define UNBOUNDED  3

#define	my_abs(x)	((x) < 0 ? -(x) : (x))
#define my_min(x, y)    ((x) < (y) ? (x) : (y))
#define my_max(x, y)    ((x) > (y) ? (x) : (y))

#define CALLOC(ptr, nr, type) if(!(ptr = calloc((size_t)(nr),\
  sizeof(type)))) { fprintf(stderr, "calloc failed\n"); exit(1); }

#define MALLOC(ptr, nr, type) if(!(ptr = malloc((size_t)((nr) * \
  sizeof(type))))) { fprintf(stderr, "malloc failed\n"); exit(1); }

#define DEFAULT_INFINITE  1.0e24 /* limit for dynamic range */
#define DEFAULT_EPSB      0.0001 /* for rounding RHS values to 0 */
#define DEFAULT_EPSEL     1.0e-8 /* for rounding other values to 0 */
#define DEFAULT_EPSD      0.0001 /* ?? MB */
#define DEFAULT_EPSILON   1e-6   /* to determine if a float value is integer */

#define INVITER 50 /* number of iterations between inversions */

#ifndef REAL /* to allow -DREAL=<float type> while compiling */
#define REAL double
#endif

typedef char    nstring[NAMELEN];

typedef struct _column
{
  int            row;
  float          value;
  struct _column *next ;
} column;

typedef struct _constraint_name
{
  char                    name[NAMELEN];
  int                     row;
  struct _constraint_name *next;
} constraint_name;

typedef struct _bound
{
  REAL          upbo;
  REAL          lowbo;
} bound;

typedef struct _hashelem
{
  nstring          colname;
  struct _hashelem *next;
  struct _column   *col;
  struct _bound    *bnd;
  int              must_be_int;
} hashelem;

typedef struct _rside /* contains relational operator and rhs value */
{
  REAL          value;
  struct _rside *next;
  short         relat;
} rside;

/* structure or final data-storage */

typedef struct  _matrec 
{
  int    rownr;
  REAL    value;
} matrec;

typedef struct _tmp_store_struct
{
  nstring name;
  int     row;
  REAL    value;
  REAL    rhs_value;
  short   relat;
} tmp_store_struct;

typedef struct _intrec
{
  int             varnr;
  struct _intrec  *next;
}
intrec;
