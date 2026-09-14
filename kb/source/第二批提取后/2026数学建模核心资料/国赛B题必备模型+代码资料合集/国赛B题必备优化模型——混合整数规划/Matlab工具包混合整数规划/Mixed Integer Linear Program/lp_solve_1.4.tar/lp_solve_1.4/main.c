#include <signal.h>
#include "defines.h"
#include "globals.h"
#include "patchlevel.h"

/* declare all global variables here */
int        Rows, Columns, Nonnuls, Sum;
REAL       Extrad;
REAL       *Pcol;
nstring	   Probname;
int	   Totnum, Classnr, Linenr;
short	   Bounds, Ranges, Verbose, Debug, Show_results, Print_duals;
unsigned   Cur_eta_size;
REAL       *Eta_value;
int        *Eta_rownr;
constraint_name *First_constraint_name;
REAL       Infinite, Epsb, Epsel, Epsd;

/* Variables which contain the original problem statement */
matrec     *Mat; /* initial problem matrix */
REAL       *Upbo, *Lowbo; /* bounds on rows and variables */
nstring    *Names; /* contains the names of rows and columns */
int        *Cend; /* Column start indexes in Mat */
REAL       *Rh; /* Right hand side of original problem */
short      *Relat; /* Relational operators of original problem */

tmp_store_struct tmp_store;
rside      *First_rside;
hashelem   *Hash_tab[HASHSIZE];

/* Variables which are used during solving */
short      *Chsign; /* tells which row was multiplied by -1 before solving */
int        *Endetacol; /* Column start indexes in Eta */
int        *Rend; /* ?? */
int        *Bas; /* basis heading list [ORC68] p.26 */
REAL       *Rhs; /* right hand side of Eta ?? */
int        *Colno; /* ?? */
short      *Basis; /* indicates whether var is in the basis */ 
short      *Lower; /* ?? */
short      Maximise; /* indicates whether we are maximising or minimising */

/* New variables for mixed integer solving */
REAL       *Solution, *Best_solution; /* to store solutions */
short      *Must_be_int; /* indicates whether variable should be int */
short      Having_ints; /* indicates that problem is mixed integer (not LP) */
matrec     *Orig_mat; /* To store original version of Mat */
REAL       *Orig_upbo; /* To store original version of Upbo */
REAL       *Orig_lowbo; /* To store original version of Lowbo */
REAL       *Orig_rh; /* To store original version of Rh */
int        Level; /* the recursion level of solve */
intrec     *First_int;
short      Ignore_decl;
REAL       Epsilon;  /* to determine if float is an integer number */
short      Floorfirst;

static void allocate_globals(void)
{
  Sum = Rows + Columns;
  Cur_eta_size = ETA_START_SIZE;

  CALLOC(Eta_value, Cur_eta_size, REAL);
  CALLOC(Eta_rownr, Cur_eta_size, int);
  CALLOC(Pcol, Rows + 2, REAL);
  CALLOC(Cend, Columns + 2, int); /* column boundaries in Mat */
  CALLOC(Endetacol, Sum + 2, int);
  CALLOC(Rend, Rows + 2, int);
  CALLOC(Bas, Rows + 2, int);
  CALLOC(Lowbo, Sum + 2, REAL);
  CALLOC(Orig_lowbo, Sum + 2, REAL);
  CALLOC(Upbo, Sum + 2, REAL);
  CALLOC(Orig_upbo, Sum + 2, REAL);
  CALLOC(Names, Sum + 2, nstring);
  CALLOC(Rh, Rows + 2, REAL); /* rhs for Mat */
  CALLOC(Orig_rh, Rows + 2, REAL); /* rhs for Mat */
  CALLOC(Rhs, Rows + 2, REAL);
  CALLOC(Colno, Nonnuls + 2, int);
  CALLOC(Mat, Nonnuls + 1, matrec); /* (initial) problem matrix */
  CALLOC(Orig_mat, Nonnuls + 1, matrec); /* (initial) problem matrix */
  CALLOC(Relat, Rows + 2, short);
  CALLOC(Basis, Sum + 2, short);
  CALLOC(Lower, Sum + 2, short);
  CALLOC(Chsign, Rows + 2, short);

  CALLOC(Solution, Sum + 1, REAL);
  CALLOC(Best_solution, Sum + 1, REAL);
  CALLOC(Must_be_int, Columns + 1, short);
} /* allocate_globals */


static void signal_handler(int sig)
{
  fprintf(stderr, "Caught signal %d, will print intermediate result\n", sig);
  print_solution(stderr, Best_solution);
  signal(SIGINT, signal_handler);
}

static void debug_toggle(int sig)
{
  Debug = !Debug;
  signal(SIGUSR1, debug_toggle);
}


int  main (int argc, char *argv[])
{
  int i, failure;
  REAL   obj_bound;
  char *reason;

  Epsilon = DEFAULT_EPSILON;
  Infinite = DEFAULT_INFINITE;
  Epsb = DEFAULT_EPSB;
  Epsel = DEFAULT_EPSEL;
  Epsd = DEFAULT_EPSD;
  Floorfirst = 1;
  Maximise = TRUE;

  obj_bound = -Infinite;

  for(i = 1; i < argc; i++)
    {
      if(strcmp(argv[i], "-v") == 0)
	Verbose = TRUE;
      else if(strcmp(argv[i], "-d") == 0)
	Debug = TRUE;
      else if(strcmp(argv[i], "-i") == 0)
	Show_results = TRUE;
      else if(strcmp(argv[i], "-c") == 0)
	Floorfirst = FALSE;
      else if(strcmp(argv[i], "-b") == 0)
	obj_bound = atof(argv[++i]);
      else if(strcmp(argv[i], "-e") == 0)
	{
	  Epsilon = atof(argv[++i]);
	  if((Epsilon <= 0.0) || (Epsilon >= 0.5))
	    {
	      fprintf(stderr, "Invalid epsilon %g; 0 < epsilon < 0.5\n",
		      (double)Epsilon);
	      exit(1);
	    }
	}
      else if(strcmp(argv[i], "-p") == 0)
	Print_duals = TRUE;
      else if(strcmp(argv[i], "-h") == 0)
	{
	  printf("Usage of %s version %s:\n", argv[0], PATCHLEVEL);
	  printf("%s [-v] [-d] [-p] [-h] [-b <bound>] [-i] [-e <epsilon>] [-c]\"<\" <input_file>\n",
		 argv[0]);
	  printf("-h:\t\tprints this message\n");
	  printf("-v:\t\tverbose mode, gives flow through the program\n");
	  printf("-d:\t\tdebug mode, all intermediate results are printed,\n\t\tand the branch-and-bound decisions\n");
	  printf("-p:\t\tAlso print the values of the dual variables with the result\n");
	  printf("-b <bound>:\tspecify a lower bound for the value of the objective function\n\t\tto the program. If close enough, may speed up the calculations.\n");
	  printf("-i:\t\tprint all intermediate valid solutions. Can give you useful\n\t\tsolutions even if the total run time is too long\n");
	  printf("-e <number>:\tspecifies the epsilon which is used to determine whether a\n\t\tfloating point number is in fact an integer. Should be < 0.5\n");
	  printf("-c:\t\tduring branch-and-bound, take the ceiling branch first\n");
	  exit(0);
	}
      /* undocumented "expert" options */
      /* use only if you know what you are doing */
      else if(strcmp(argv[i], "-infinite") == 0)
	{
	  Infinite = atof(argv[++i]);
	  if(Infinite <= 0)
	    {
	      fprintf(stderr, "Impossible infinite value %g\n",
		      (double)Infinite);
	      exit(1);
	    }
	  if(obj_bound == -DEFAULT_INFINITE) /* not changed by user */
	    obj_bound = -Infinite;
	}
      else if(strcmp(argv[i], "-epsb") == 0)
	{
	  Epsb = atof(argv[++i]);
	  if(Epsb <= 0)
	    {
	      fprintf(stderr, "Impossible Epsb value %g\n", (double)Epsb);
	      exit(1);
	    }
	}
      else if(strcmp(argv[i], "-epsel") == 0)
	{
	  Epsel = atof(argv[++i]);
	  if(Epsel <= 0)
	    {
	      fprintf(stderr, "Impossible Epsel value %g\n", (double)Epsel);
	      exit(1);
	    }
	}
      else if(strcmp(argv[i], "-epsd") == 0)
	{
	  Epsd = atof(argv[++i]);
	  if(Epsd <= 0)
	    {
	      fprintf(stderr, "Impossible Epsd value %g\n", (double)Epsd);
	      exit(1);
	    }
	}
      else
	fprintf(stderr, "Unrecognized command line option %s, ignored\n",
		argv[i]);
    }
  /* construct basic problem */
  yyparse();
  Rows--; /* @!? MB */
  
  /* do not try to run problems with an empty matrix, i.e. just bounds */
  if(Rows == 0)
    {
      fprintf(stderr, "Error, you are trying to solve a problem without real constraints\n(see manual page)\n");
      exit(1);
    }

  /* set signal handler to toggle -d flag run time */
  signal(SIGUSR1, debug_toggle);

  allocate_globals();
  readinput(Cend, Orig_rh, Relat, Orig_lowbo, Orig_upbo, Orig_mat, Names); 


  /* if problem contains ints, from now on, catch interrupt signal to print
     best solution sofar */
  if(Having_ints)
    signal(SIGINT, signal_handler);

  /* set lower or upper bound of objective function */
  if(obj_bound == -Infinite && !Maximise)
    obj_bound = Infinite;
  Best_solution[0] = obj_bound;

  /* solve it */
  failure = solve(Orig_upbo, Orig_lowbo);

  /* print result */
  if(failure == OPTIMAL)
    print_solution(stdout, Best_solution);
  else /* no valid solution found, find out reason */
    {
      if(failure == MILP_FAIL) /* this should not occur here */
	reason = ", reason cannot be detected";
      else if(failure == UNBOUNDED)
	reason = ", problem is unbounded";
      else if(failure == INFEASIBLE)
	reason = ", problem is infeasible";

    fprintf(stderr, "%s problem has no solution%s\n",
	    Having_ints ? "(M)ILP" : "LP", reason);
    }

  return (0);
} /* main */
