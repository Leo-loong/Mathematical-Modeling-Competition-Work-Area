#include "defines.h"
#include "globals.h"
#include <stdarg.h>

void print_solution(FILE *stream, REAL *sol, REAL *duals)
{
  int i;

  fprintf(stream, "Value of objective function: %16.10g\n",
	  (double)sol[0] / (Scale_factor * Scale_factors[0]));

  /* print normal variables */
  for (i = Rows + 1; i <= Sum; i++)
    fprintf(stream, "%-10s%16.5g\n", Names[i],
	    (double)sol[i] * Scale_factors[i]);

  /* print achieved constraint values */
  if(Verbose)
    {
      fprintf(stream, "\nActual values of the constraints:\n");
      for (i = 1; i <= Rows; i++)
	fprintf(stream, "%-10s%16.5g\n", Names[i],
		(double)sol[i] / (Scale_factor * Scale_factors[i]));
    }

  if(Verbose || Print_duals)
    {
      fprintf(stream, "\nDual values:\n");
      for (i = 1; i <= Rows; i++)
	fprintf(stream, "%-10s%16.5g\n", Names[i], (double)duals[i]);
    }
} /* print_solution */


static void print_indent(void)
{
  int i;

  fprintf(stderr, "%2d", Level);
  if(Level < 50) /* useless otherwise */
    for(i = Level; i > 0; i--)
      fprintf(stderr, "--");
  else
    fprintf(stderr, " *** too deep ***");
  fprintf(stderr, "> ");
} /* print_indent */


void debug_print_solution(REAL *sol)
{
  int i;

  if(Debug)
    for (i = 0; i <= Sum; i++)
      {
	print_indent();
	fprintf(stderr, "%-10s%16.5g\n", Names[i],
		(double)sol[i]);
      }
} /* debug_print_solution */


void debug_print_bounds(REAL *upbo, REAL *lowbo)
{
  int i;

  if(Debug)
    for(i = Rows + 1; i <= Sum; i++)
      {
	if(lowbo[i] != 0)
	  {
	    print_indent();
	    fprintf(stderr, "%s > %10.3g\n", Names[i], (double)lowbo[i]);
	  }
	if(upbo[i] != Infinite)
	  {
	    print_indent();
	    fprintf(stderr, "%s < %10.3g\n", Names[i], (double)upbo[i]);
	  }
      }
} /* debug_print_bounds */


void debug_print(char *format, ...)
{
  va_list ap;

  if(Debug)
    {
      va_start(ap, format);
      print_indent();
      vfprintf(stderr, format, ap);
      fputc('\n', stderr);
      va_end(ap);
    }
} /* debug_print */
