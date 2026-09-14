#include <string.h>
#include <time.h>
#include "lpkit.h"
#include "lpglob.h"
#include "patchlevel.h"

void print_help(char *argv[])
{
  printf("Usage of %s version %s:\n", argv[0], PATCHLEVEL);
  printf("%s [options] \"<\" <input_file>\n", argv[0]);
  printf("list of options:\n");
  printf("-h\t\tprints this message\n");
  printf("-v\t\tverbose mode, gives flow through the program\n");
  printf("-d\t\tdebug mode, all intermediate results are printed,\n\t\tand the branch-and-bound decisions\n");
  printf("-p\t\tprint the values of the dual variables\n");
  printf("-b <bound>\tspecify a lower bound for the objective function\n\t\tto the program. If close enough, may speed up the\n\t\tcalculations.\n");
  printf("-i\t\tprint all intermediate valid solutions.\n\t\tCan give you useful solutions even if the total run time\n\t\tis too long\n");
  printf("-e <number>\tspecifies the epsilon which is used to determine whether a\n\t\tfloating point number is in fact an integer.\n\t\tShould be < 0.5\n");
  printf("-c\t\tduring branch-and-bound, take the ceiling branch first\n");
  printf("-s\t\tuse automatic problem scaling.\n");  
  printf("-I\t\tprint info after reinverting\n");
  printf("-t\t\ttrace pivot selection\n");
  printf("-mps\t\tread from MPS file instead of lp file\n");
  printf("-degen\t\tuse perturbations to reduce degeneracy,\n\t\tcan increase numerical instability\n");
  printf("-time\t\tPrint CPU time to parse input and to calculate result\n");
}

void print_cpu_times(const char *info)
{
  static clock_t last_time = 0;
  clock_t new_time;

  new_time = clock();
  fprintf(stderr, "CPU Time for %s: %gs (%gs total since program start)\n",
	  info, (new_time - last_time) / (double) CLOCKS_PER_SEC,
	  new_time / (double) CLOCKS_PER_SEC);
  last_time = new_time;
}


int main(int argc, char *argv[])
{
  lprec *lp;
  int i;
  short verbose = FALSE;
  short debug = FALSE;
  short print_sol = FALSE;
  short print_duals = FALSE;
  short floor_first = TRUE;
  short scaling = FALSE;
  short print_at_invert = FALSE;
  short tracing = FALSE;
  short mps = FALSE;
  short anti_degen = FALSE;
  short print_timing = FALSE;
  short parse_only = FALSE;
  int result;
  REAL obj_bound = (REAL)DEF_INFINITE;
  REAL epsilon = (REAL)DEF_EPSILON;
  Trej = 1e-4; /* default, MB */

  /* read command line arguments */

  for(i = 1; i < argc; i++)
    {
      if(strcmp(argv[i], "-v") == 0)
	verbose = TRUE;
      else if(strcmp(argv[i], "-d") == 0)
	debug = TRUE;
      else if(strcmp(argv[i], "-i") == 0)
	print_sol = TRUE;
      else if(strcmp(argv[i], "-c") == 0)
	floor_first = FALSE;
      else if(strcmp(argv[i], "-b") == 0)
	obj_bound = atof(argv[++i]);
      else if(strcmp(argv[i], "-e") == 0)
	{
	  epsilon = atof(argv[++i]);
	  if((epsilon <= 0.0) || (epsilon >= 0.5))
	    {
	      fprintf(stderr, "Invalid epsilon %g; 0 < epsilon < 0.5\n",
		      (double)epsilon);
	      exit(EXIT_FAILURE);
	    }
	}
      else if(strcmp(argv[i], "-p") == 0)
	print_duals = TRUE;
      else if(strcmp(argv[i], "-h") == 0)
        {
           print_help(argv); 
           exit(EXIT_SUCCESS);
        }
      else if(strcmp(argv[i], "-s") == 0)
	scaling = TRUE;
      else if(strcmp(argv[i], "-I") == 0)
        print_at_invert = TRUE;
      else if(strcmp(argv[i], "-t") == 0)
        tracing = TRUE;
      else if(strcmp(argv[i],"-mps") == 0)
        mps = TRUE;
      else if(strcmp(argv[i],"-degen") == 0)
        anti_degen = TRUE;
      else if(strcmp(argv[i],"-time") == 0)
	if(clock() == -1)
	  fprintf(stderr, "CPU times not available on this machine\n");
	else
	  print_timing = TRUE;
      else if(strcmp(argv[i],"-trej") == 0)
	Trej = atof(argv[++i]);
      else if(strcmp(argv[i],"-parse_only") == 0)
	parse_only = TRUE;
      else
	{
	  fprintf(stderr, "Error, Unrecognized command line argument '%s'\n",
		  argv[i]);
	  print_help(argv);
	  exit(EXIT_FAILURE);
	}
    }

  if(mps)
    lp = read_mps(stdin, verbose);
  else /* standard lp_solve syntax expected */
    lp = read_lp_file(stdin, verbose, "lp" );

  if(print_timing)
    print_cpu_times("parsing input");

  if(parse_only)
    exit(0);

  if(lp->columns < 8 && verbose)
    print_lp(lp);

  if(scaling)
    auto_scale(lp);

  lp->print_sol = print_sol;
  lp->epsilon = epsilon;
  lp->print_duals = print_duals;
  lp->debug = debug;
  lp->floor_first = floor_first;
  lp->print_at_invert = print_at_invert;
  lp->trace = tracing;
  if(obj_bound != DEF_INFINITE)
    lp->obj_bound = obj_bound;
  lp->anti_degen = anti_degen;

  if(verbose)
    {
       printf("Solving\n");
       lp->verbose = TRUE;
    }

  result = solve(lp);

  if(print_timing)
    print_cpu_times("solving");

  if(result == OPTIMAL)
    {
       print_solution(lp);
       if(verbose)
         fprintf(stderr,
		 "Branch & Bound depth: %d\nNodes processed: %d\nSimplex pivots: %d\n",
		 lp->max_level, lp->total_nodes, lp->total_iter);
    }

  else if(result == INFEASIBLE)
    printf("This problem is infeasible\n");
  else if(result == UNBOUNDED)
    printf("This problem is unbounded\n");
  else if(result == FAILURE)
    printf("lp_solve failed\n");
  return(result);
}
