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
int        Numeta, Numinv, Invnum;
constraint_name *First_constraint_name;
REAL       Infinite, Epsb, Epsel, Epsd;
REAL       Scale_factor = 1;

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
int        *Rend; /* Row end */
int        *Bas; /* basis heading list [ORC68] p.26 */
REAL       *Rhs; /* right hand side during iterations */
int        *Colno; /* Column number */
short      *Basis; /* indicates whether var is in the basis */ 
short      *Lower; /* variable at upper or lower bound */
short      Maximise; /* indicates whether we are maximising or minimising */

REAL       *Scale_factors; /* the initial scaling of rows and columns */

/* New variables for mixed integer solving */
REAL       *Solution, *Best_solution, *Best_duals; /* to store solutions */
short      *Must_be_int; /* indicates whether variable should be int */
short      Having_ints; /* indicates that problem is mixed integer (not LP) */
REAL       *Orig_upbo; /* To store original version of Upbo */
REAL       *Orig_lowbo; /* To store original version of Lowbo */
REAL       *Orig_rh; /* To store original version of Rh */
int        Level; /* the recursion level of solve */
intrec     *First_int;
short      Ignore_decl;
REAL       Epsilon;  /* to determine if float is an integer number */
short      Floorfirst;
short      Solve_dual; /* flag indicating we actually want to solve the dual
			  problem */

static void allocate_globals(void)
{
  Sum = Rows + Columns;
  Cur_eta_size = ETA_START_SIZE;

  CALLOC(Eta_value, Cur_eta_size, REAL);
  CALLOC(Eta_rownr, Cur_eta_size, int);
  CALLOC(Pcol, Rows + 1, REAL);
  CALLOC(Cend, Columns + 1, int); /* column boundaries in Mat */
  CALLOC(Endetacol, Sum + 1 + INVITER, int);
  CALLOC(Rend, Rows + 1, int);
  CALLOC(Bas, Rows + 1, int);
  CALLOC(Lowbo, Sum + 1, REAL);
  CALLOC(Orig_lowbo, Sum + 1, REAL);
  CALLOC(Upbo, Sum + 1, REAL);
  CALLOC(Orig_upbo, Sum + 1, REAL);
  CALLOC(Names, Sum + 1, nstring);
  CALLOC(Rh, Rows + 1, REAL); /* rhs for Mat */
  CALLOC(Orig_rh, Rows + 1, REAL); /* rhs for Mat */
  CALLOC(Rhs, Rows + 1, REAL);
  CALLOC(Colno, Nonnuls + 1, int);
  CALLOC(Mat, Nonnuls + 1, matrec); /* (initial) problem matrix */
  CALLOC(Relat, Rows + 1, short);
  CALLOC(Basis, Sum + 1, short);
  CALLOC(Lower, Sum + 1, short);
  CALLOC(Chsign, Rows + 1, short);

  CALLOC(Solution, Sum + 1, REAL);
  CALLOC(Best_solution, Sum + 1, REAL);
  CALLOC(Best_duals, Rows + 1, REAL);
  CALLOC(Must_be_int, Columns + 1, short);

  CALLOC(Scale_factors, Sum + 1, REAL); /* scale factors */
} /* allocate_globals */


static void signal_handler(int sig)
{
  fprintf(stderr, "Caught signal %d, will print intermediate result\n", sig);
  print_solution(stderr, Best_solution, Best_duals);
  signal(SIGINT, signal_handler);
}

static void debug_toggle(int sig)
{
  Debug = !Debug;
  signal(SIGUSR1, debug_toggle);
}

static REAL minmax_to_scale(REAL min, REAL max)
{
  REAL scale;

  scale = 1 / pow(10, (log10(min) + log10(max)) / 2);
  return(scale);
}

static void scale_columns(matrec *mat, int *cend, REAL *lowbo, REAL *upbo)
{
  int i, j;
  REAL col_max, col_min, col_scale;

  /* calculate scales */
  for(j = 1; j <= Columns; j++)
    {
      col_max = 0;
      col_min = Infinite;
      for(i = cend[j - 1]; i < cend[j]; i++)
	{
	  col_max = my_max(col_max, my_abs(mat[i].value));
	  col_min = my_min(col_min, my_abs(mat[i].value));
	}
      Scale_factors[Rows + j]  = minmax_to_scale(col_min, col_max);
      debug_print("column %s, min: %g, max: %g, scale: %g\n",
		  Names[Rows + j], col_min, col_max, Scale_factors[Rows + j]);
    }

  /* scale mat */
  for(j = 1; j <= Columns; j++)
    for(i = cend[j - 1]; i < cend[j]; i++)
      mat[i].value *= Scale_factors[Rows + j];

  /* scale bounds as well */
  for(i = Rows + 1; i < Sum; i++)
    {
      if(lowbo[i] != 0)
	lowbo[i] /= Scale_factors[i];
      if(upbo[i] != Infinite)
	upbo[i] /= Scale_factors[i];
    }
}

static void scale_rows(matrec *mat, int *cend, REAL *rhs)
{
  int i, j, rownr;
  REAL *row_max, *row_min, absval;

  CALLOC(row_max, Rows + 1, REAL);
  CALLOC(row_min, Rows + 1, REAL);

  /* initialise min and max values */
  for(i = 0; i <= Rows; i++)
    {
      row_max[i] = 0;
      row_min[i] = Infinite;
    }

  /* calculate min and max absolute values of rows */
  for(j = 0; j < Columns; j++)
    for(i = cend[j]; i < cend[j + 1]; i++)
      {
	rownr = mat[i].rownr;
	absval = my_abs(mat[i].value);
	row_max[rownr] = my_max(row_max[rownr], absval);
	row_min[rownr] = my_min(row_min[rownr], absval);
      }

  /* calculate scale factors for rows */
  for(i = 0; i <= Rows; i++)
    {
      Scale_factors[i] = minmax_to_scale(row_min[i], row_max[i]);
      debug_print("Row: %s, min: %g, max: %g, scale: %g\n",
		  Names[i], row_min[i], row_max[i], Scale_factors[i]);
    }

  /* now actually scale the matrix */
  for(j = 0; j < Columns; j++)
    for(i = cend[j]; i < cend[j + 1]; i++)
      mat[i].value *= Scale_factors[mat[i].rownr];

  /* and scale the rhs! */
  for(i = 0; i <= Rows; i++)
    rhs[i] *= Scale_factors[i];

  free(row_max);
  free(row_min);
}

static void initmilp(void)
{
  int i,j, rownr;
  int *num, *rownum;
  REAL theta;

  Orig_rh[0] = 0;
  for (i = 0; i <= Sum; i++)
    Lower[i] = TRUE;
  for (i = 0; i <= Rows; i++)
    Basis[i] = TRUE;
  for (i = 1; i <= Columns; i++)
    Basis[Rows + i] = FALSE;
  for (i = 0; i <= Rows; i++)
    Bas[i] = i;

  CALLOC(num, Rows + 1, int);
  CALLOC(rownum, Rows + 1, int);

  if (Verbose)
    printf("Init MILP\n");

  /* if we want to maximise the objective function,
     change the signs of the objective function */
  if(Maximise)
    Chsign[0] = TRUE;
  else
    Chsign[0] = FALSE;

  for (i = 1; i <= Rows; i++)
    if ((Relat[i] == GE) && (Orig_upbo[i] == Infinite))
      Chsign[i] = TRUE;
    else
      Chsign[i] = FALSE;

  /* invert values in rows with Chsign[i] == TRUE */
  for (i = 1; i <= Rows; i++)
    if (Chsign[i])
      Orig_rh[i] = -Orig_rh[i];
  for (i = 0; i < Nonnuls; i++)
    if (Chsign[Mat[i].rownr])
      Mat[i].value = -Mat[i].value;

   for (i = 1; i <= Rows; i++)
    {
      num[i] = 0;
      rownum[i] = 0;
    }
  for (i = 0; i < Nonnuls; i++)
    rownum[Mat[i].rownr]++;
  Rend[0] = 0;
  for (i = 1; i <= Rows; i++)
    Rend[i] = Rend[i - 1] + rownum[i];
  for (i = 1; i <= Columns; i++)
    for (j = Cend[i - 1]; j < Cend[i]; j++)
      {
	rownr = Mat[j].rownr;
	if (rownr != 0)
	  {
	    num[rownr]++;
	    Colno[Rend[rownr - 1] + num[rownr]] = i;
	  }
      }
  free(num);
  free(rownum);
}

int  main (int argc, char *argv[])
{
  int  i, failure, autoscale;
  REAL obj_bound;
  char *reason;
  Invnum = INVITER;

  Epsilon    = DEFAULT_EPSILON;
  Infinite   = DEFAULT_INFINITE;
  Epsb       = DEFAULT_EPSB;
  Epsel      = DEFAULT_EPSEL;
  Epsd       = DEFAULT_EPSD;
  Floorfirst = TRUE;
  Maximise   = TRUE;

  obj_bound = -Infinite;
  autoscale = FALSE;

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
      else if(strcmp(argv[i], "-scale") == 0)
	Scale_factor = atof(argv[++i]);
      else if(strcmp(argv[i], "-autoscale") == 0)
	autoscale = TRUE;

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
      else if(strcmp(argv[i], "-solve_dual") == 0)
	{
	  Solve_dual = TRUE;
	}
      else
	fprintf(stderr, "Unrecognized command line option %s, ignored\n",
		argv[i]);
    }
  /* construct basic problem */
  yyparse();
  Rows--; /* @!? MB */

  /* Don't know what the dual of a problem with integer variables looks like */
  if(Having_ints && Solve_dual)
    {
      fprintf(stderr, "Error, don't know how to solve the dual of a problem with integer variables\n");
      exit(1);
    }
  
  /* do not try to run problems with an empty matrix, i.e. just bounds */
  if(Rows == 0)
    {
      fprintf(stderr, "Error, you are trying to solve a problem without real constraints\n(see manual page)\n");
      exit(1);
    }

  /* set signal handler to toggle -d flag run time */
  signal(SIGUSR1, debug_toggle);

  if(Solve_dual) /* swap Rows and Columns values */
    {
      int tmp = Rows;
      Rows = Columns;
      Columns = tmp;
    }

  allocate_globals();

  if(Solve_dual)
    {
      readinput_dual(Cend, Orig_rh, Relat, Orig_lowbo, Orig_upbo, &Mat,
		     Names); 
    }
  else
    {
      readinput(Cend, Orig_rh, Relat, Orig_lowbo, Orig_upbo, Mat, Names); 
    }

  /* set initial scaling of rows and columns to 1 */
  for(i = 0; i < Sum + 1; i++)
    Scale_factors[i] = 1;

  /* perform auto scaling if required */
  if(autoscale)
    {
      scale_rows(Mat, Cend, Orig_rh);
      if(!Having_ints)
	scale_columns(Mat, Cend, Orig_lowbo, Orig_upbo);
    }

  /* if problem contains ints, from now on, catch interrupt signal to print
     best solution sofar */
  if(Having_ints)
    signal(SIGINT, signal_handler);

  /* set lower or upper bound of objective function */
  if(obj_bound == -Infinite && !Maximise)
    obj_bound = Infinite;
  Best_solution[0] = obj_bound;

  initmilp();

  /* solve it */
  failure = solve(Orig_upbo, Orig_lowbo, Basis, Lower, Bas);

  /* print result */
  if(failure == OPTIMAL)
    print_solution(stdout, Best_solution, Best_duals);
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
