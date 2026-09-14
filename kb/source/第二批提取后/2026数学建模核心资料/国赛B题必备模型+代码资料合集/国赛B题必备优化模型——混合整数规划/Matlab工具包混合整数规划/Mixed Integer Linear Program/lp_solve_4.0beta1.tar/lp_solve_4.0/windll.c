#include <windows.h>
#include <stdio.h>

#include "lpkit.h"
#include "debug.h"

static char *buferror = NULL;
static FILE *fplogfile = NULL;

/* this will only work in the following condition:

   int = long
   REAL = double 
*/

static void freebuferror()
 {
  if (buferror != NULL) {
   free(buferror);
   buferror = NULL;
  }
 }

void __declspec(dllexport) WINAPI _lasterror(char *str, long strsz)
 {
  if (strsz) {
   *str=0;
   if (buferror != NULL)
    strncpy(str,buferror,strsz);
  }
 }

/* return lp_solve version info */
void __declspec(dllexport) WINAPI _lp_solve_version(long *majorversion, long *minorversion, long *release, long *build)
 {
  lp_solve_version(majorversion, minorversion, release, build);
 }

void __declspec(dllexport) WINAPI _set_magic(long code, long param)
 {
  set_magic(code, param);
 }

/* create and initialise a lprec structure
   defaults:
   Empty (Rows * Columns) matrix,
   Minimise the objective function
   constraints all type <=
   Upperbounds all Infinite
   no integer variables
   floor first in B&B
   no scaling
   default basis */
lprec __declspec(dllexport) * WINAPI _make_lp(long rows, long columns)
 {
  freebuferror();
  return(make_lp(rows, columns));
 }

/* create and read an .lp file from input */
lprec __declspec(dllexport) * WINAPI _read_LP(char *filename, long verbose, char *lp_name)
 {
  lprec *lp;

  freebuferror();
  lp = read_LP(filename, (short) ((verbose == 0) ? FALSE : TRUE), lp_name);
  return(lp);
 }

/* Remove problem from memory */
void __declspec(dllexport) WINAPI _delete_lp(lprec *lp)
 {
  if (lp != NULL) {
   freebuferror();
   delete_lp(lp);
  }
 }

/* copy a lp structure */
lprec __declspec(dllexport) * WINAPI _copy_lp(lprec *lp)
 {
  if (lp != NULL) {
   freebuferror();
   return(copy_lp(lp));
  }
  else
   return(NULL);
 }

/* fill in element (Row,Column) of the matrix
   Row in [0..Rows] and Column in [1..Columns] */
long __declspec(dllexport) WINAPI _set_mat(lprec *lp, long row, long column, double value)
 {
  long ret;

  if (lp != NULL) {
   freebuferror();
   ret = set_mat(lp, row, column, value);
  }
  else
   ret = 0;
  return(ret);
 }

/* set the objective function (Row 0) of the matrix */
long __declspec(dllexport) WINAPI _set_obj_fn(lprec *lp, double *row)
 {
  long ret;

  if (lp != NULL) {
   freebuferror();
   ret = set_obj_fn(lp, row);
  }
  else
   ret = 0;
  return(ret);
 }

/* set the objective function (Row 0) of the matrix with string input */
long __declspec(dllexport) WINAPI _str_set_obj_fn(lprec *lp, char *row)
 {
  long ret;

  if (lp != NULL) {
   freebuferror();
   ret = str_set_obj_fn(lp, row);
  }
  else
   ret = 0;
  return(ret);
 }

/* Add a constraint to the problem,
   row is the constraint row,
   rh is the right hand side,
   constr_type is the type of constraint (LE (<=), GE(>=), EQ(=)) */
long __declspec(dllexport) WINAPI _add_constraint(lprec *lp, double *row, long constr_type, double rh)
 {
  long ret;

  if (lp != NULL) {
   freebuferror();
   ret = add_constraint(lp, row,(short) constr_type, rh);
  }
  else
   ret = 0;
  return(ret);
 }

/* Add a constraint to the problem with string input,
   row is the constraint row,
   rh is the right hand side,
   constr_type is the type of constraint (LE (<=), GE(>=), EQ(=)) */
long __declspec(dllexport) WINAPI _str_add_constraint(lprec *lp, char *row, long constr_type, double rh)
 {
  long ret;

  if (lp != NULL) {
   freebuferror();
   ret = str_add_constraint(lp, row,(short) constr_type, rh);
  }
  else
   ret = 0;
  return(ret);
 }

/* Remove constraint nr del_row from the problem */
void __declspec(dllexport) WINAPI _del_constraint(lprec *lp, long del_row)
 {
  if (lp != NULL) {
   freebuferror();
   del_constraint(lp, del_row);
  }
 }

/* add a Lagrangian constraint of form Row' x contype Rhs */
long __declspec(dllexport) WINAPI _add_lag_con(lprec *lp, double *row, long con_type, double rhs)
 {
  long ret;

  if (lp != NULL) {
   freebuferror();
   ret = add_lag_con(lp, row, (short) con_type, rhs);
  }
  else
   ret = 0;
  return(ret);
 }

/* add a Lagrangian constraint of form Row' x contype Rhs with string input */
long __declspec(dllexport) WINAPI _str_add_lag_con(lprec *lp, char *row, long con_type, double rhs)
 {
  long ret;

  if (lp != NULL) {
   freebuferror();
   ret = str_add_lag_con(lp, row, (short) con_type, rhs);
  }
  else
   ret = -1;
  return(ret);
 }

/* Add a Column to the problem */
long __declspec(dllexport) WINAPI _add_column(lprec *lp, double *column)
 {
  long ret;

  if (lp != NULL) {
   freebuferror();
   ret = add_column(lp, column);
  }
  else
   ret = 0;
  return(ret);
 }

/* Add a Column to the problem with string input */
long __declspec(dllexport) WINAPI _str_add_column(lprec *lp, char *column)
 {
  long ret;

  if (lp != NULL) {
   freebuferror();
   ret = str_add_column(lp, column);
  }
  else
   ret = 0;
  return(ret);
 }

/* Delete a column */
void __declspec(dllexport) WINAPI _del_column(lprec *lp, long column)
 {
  if (lp != NULL) {
   freebuferror();
   del_column(lp, column);
  }
 }

/* Set the upperbound of a variable */
void __declspec(dllexport) WINAPI _set_upbo(lprec *lp, long column, double value)
 {
  if (lp != NULL) {
   freebuferror();
   set_upbo(lp, column, value);
  }
 }

/* Set the lowerbound of a variable */
void __declspec(dllexport) WINAPI _set_lowbo(lprec *lp, long column, double value)
 {
  if (lp != NULL) {
   freebuferror();
   set_lowbo(lp, column, value);
  }
 }

/* Set the upper range of a constraint */
void __declspec(dllexport) WINAPI _set_uprange(lprec *lp, long row, double value)
 {
  if (lp != NULL) {
   freebuferror();
   set_uprange(lp, row, value);
  }
 }

/* Set the lower range of a constraint */
void __declspec(dllexport) WINAPI _set_lowrange(lprec *lp, long row, double value)
 {
  if (lp != NULL) {
   freebuferror();
   set_lowrange(lp, row, value);
  }
 }

/* Set the type of variable, if must_be_int = TRUE then the variable must be integer */
void __declspec(dllexport) WINAPI _set_int(lprec *lp, long column, long must_be_int)
 {
  if (lp != NULL) {
   freebuferror();
   set_int(lp, column, (short) ((must_be_int == 0) ? FALSE : TRUE));
  }
 }

/* check if var is integer */
long __declspec(dllexport) WINAPI _is_int(lprec *lp, long column)
 {
  long ret;

  if (lp != NULL) {
   freebuferror();
   ret = is_int(lp, column);
  }
  else
   ret = 0;
  return(ret);
 }

/* set var semi-continious */
void __declspec(dllexport) WINAPI _set_semicont(lprec *lp, long column, long must_be_sc)
 {
  if (lp != NULL) {
   freebuferror();
   set_semicont(lp, column, (short) ((must_be_sc == 0) ? FALSE : TRUE));
  }
 }

/* check if var is semi-continious */
long __declspec(dllexport) WINAPI _is_semicont(lprec *lp, long column)
 {
  long ret;

  if (lp != NULL) {
   freebuferror();
   ret = is_semicont(lp, column);
  }
  else
   ret = 0;
  return(ret);
 }

/* Add SOS constraint */
long __declspec(dllexport) WINAPI _add_SOS(lprec *lp, char *name, long sostype, long priority, long count, long *sosvars, double *weights)
 {
  long ret;

  if (lp != NULL) {
   freebuferror();
   ret = add_SOS(lp, name, (short) sostype, priority, count, sosvars, weights);
  }
  else
   ret = 0;
  return(ret);
 }

/* check if var is SOS */
long __declspec(dllexport) WINAPI _is_SOS_var(lprec *lp, long column)
 {
  long ret;

  if (lp != NULL) {
   freebuferror();
   ret = is_SOS_var(lp, column);
  }
  else
   ret = 0;
  return(ret);
 }

/* Set the name of the model */
long __declspec(dllexport) WINAPI _set_lp_name(lprec *lp, char *name)
 {
  long ret;

  if (lp != NULL) {
   freebuferror();
   ret = set_lp_name(lp, name);
  }
  else
   ret = 0;
  return(ret);
 }

/* Set the right hand side of a constraint row */
void __declspec(dllexport) WINAPI _set_rh(lprec *lp, long row, double value)
 {
  if (lp != NULL) {
   freebuferror();
   set_rh(lp, row, value);
  }
 }

/* Get the right hand side of a constraint row */
double __declspec(dllexport) WINAPI _get_rh(lprec *lp, long row)
 {
  double ret;

  if (lp != NULL) {
   freebuferror();
   ret = get_rh(lp, row);
  }
  else
   ret = 0.0;
  return(ret);
 }

/* Set the right hand side vector range */
void __declspec(dllexport) WINAPI _set_rh_range(lprec *lp, long row, double deltavalue)
 {
  if (lp != NULL) {
   freebuferror();
   set_rh_range(lp, row, deltavalue);
  }
 }

/* Get the right hand side vector range */
double __declspec(dllexport) WINAPI _get_rh_range(lprec *lp, long row)
 {
  double ret;

  if (lp != NULL) {
   freebuferror();
   ret = get_rh_range(lp, row);
  }
  else
   ret = 0.0;
  return(ret);
 }

/* Set the right hand side vector */
void __declspec(dllexport) WINAPI _set_rh_vec(lprec *lp, double *rh)
 {
  if (lp != NULL) {
   freebuferror();
   set_rh_vec(lp, rh);
  }
 }

/* Set the right hand side vector with string input */
long __declspec(dllexport) WINAPI _str_set_rh_vec(lprec *lp, char *rh)
 {
  long ret;

  if (lp != NULL) {
   freebuferror();
   ret = str_set_rh_vec(lp, rh);
  }
  else
   ret = 0;
  return(ret);
 }

/* maximise the objective function */
void __declspec(dllexport) WINAPI _set_maxim(lprec *lp)
 {
  if (lp != NULL) {
   freebuferror();
   set_maxim(lp);
  }
 }

/* minimise the objective function */
void __declspec(dllexport) WINAPI _set_minim(lprec *lp)
 {
  if (lp != NULL) {
   freebuferror();
   set_minim(lp);
  }
 }

/* Set the type of constraint in row Row (LE, GE, EQ) */
void __declspec(dllexport) WINAPI _set_constr_type(lprec *lp, long row, long con_type)
 {
  if (lp != NULL) {
   freebuferror();
   set_constr_type(lp, row, (short) con_type);
  }
 }

/* Get the type of constraint in row Row (LE, GE, EQ) */
long __declspec(dllexport) WINAPI _get_constr_type(lprec *lp, long row)
 {
  long ret;

  if (lp != NULL) {
   freebuferror();
   ret = get_constr_type(lp, row);
  }
  else
   ret = 0;
  return(ret);
 }

/* Set the name of a constraint row */
long __declspec(dllexport) WINAPI _set_row_name(lprec *lp, long row, char *new_name)
 {
  long ret;

  if (lp != NULL) {
   freebuferror();
   ret = set_row_name(lp, row, new_name);
  }
  else
   ret = 0;
  return(ret);
 }

/* Get the name of a constraint row */
char __declspec(dllexport) *WINAPI _get_row_name(lprec *lp, long row)
 {
  char *ret;

  if (lp != NULL) {
   freebuferror();
   ret = get_row_name(lp, row);
  }
  else
   ret = NULL;
  return(ret);
 }

/* Set the name of a variable column */
long __declspec(dllexport) WINAPI _set_col_name(lprec *lp, long column, char *new_name)
 {
  long ret;

  if (lp != NULL) {
   freebuferror();
   ret = set_col_name(lp, column, new_name);
  }
  else
   ret = 0;
  return(ret);
 }

/* Get the name of a variable column */
char __declspec(dllexport) *WINAPI _get_col_name(lprec *lp, long column)
 {
  char *ret;

  if (lp != NULL) {
   freebuferror();
   ret = get_col_name(lp, column);
  }
  else
   ret = NULL;
  return(ret);
 }

/* scale of the problem */
double __declspec(dllexport) WINAPI _scale(lprec *lp, double *myrowscale, double *mycolscale)
 {
  double ret;

  if (lp != NULL) {
   freebuferror();
   ret = scale(lp, myrowscale, mycolscale);
  }
  else
   ret = 0.0;
  return(ret);
 }

/* Automatic scaling of the problem */
double __declspec(dllexport) WINAPI _auto_scale(lprec *lp)
 {
  double ret;

  if (lp != NULL) {
   freebuferror();
   ret = auto_scale(lp);
  }
  else
   ret = 0.0;
  return(ret);
 }

/* Curtis-Reid scaling */
long __declspec(dllexport) WINAPI _scaleCR(lprec *lp)
 {
  long ret;

  if (lp != NULL) {
   freebuferror();
   ret = scaleCR(lp);
  }
  else
   ret = 0;
  return(ret);
 }

/* Remove all scaling from the problem */
void __declspec(dllexport) WINAPI _unscale(lprec *lp)
 {
  if (lp != NULL) {
   freebuferror();
   unscale(lp);
  }
 }

/* Set the basis of a problem */
void __declspec(dllexport) WINAPI _set_basis(lprec *lp, long *bascolumn)
 {
  if (lp != NULL) {
   freebuferror();
   set_basis(lp, bascolumn);
  }
 }

/* Get the basis of a problem */
void __declspec(dllexport) WINAPI _get_basis(lprec *lp, long *bascolumn)
 {
  if (lp != NULL) {
   freebuferror();
   get_basis(lp, bascolumn);
  }
 }

/* Solve the problem */
long __declspec(dllexport) WINAPI _solve(lprec *lp)
 {
  long ret;

  if (lp != NULL) {
   freebuferror();
   ret = solve(lp);
  }
  else
   ret = FAILURE;
  return(ret);
 }

/* Do NumIter iterations with Lagrangian relaxation constraints */
long __declspec(dllexport) WINAPI _lag_solve(lprec *lp, double start_bound, long num_iter, long verbose)
 {
  long ret;

  if (lp != NULL) {
   freebuferror();
   ret = lag_solve(lp, start_bound, num_iter, (short) ((verbose == 0) ? FALSE : TRUE));
  }
  else
   ret = FAILURE;
  return(ret);
 }

/* Reset the basis of a problem, can be usefull in case of degeneracy - JD */
void __declspec(dllexport) WINAPI _reset_basis(lprec *lp)
 {
  if (lp != NULL) {
   freebuferror();
   reset_basis(lp);
  }
 }

/* get a single element from the matrix */
double __declspec(dllexport) WINAPI _mat_elm(lprec *lp, long row, long column)
 {
  double ret;

  if (lp != NULL) {
   freebuferror();
   ret = mat_elm(lp, row, column);
  }
  else
   ret = 0.0;
  return(ret);
 }

/* fill row with the row row_nr from the problem */
void __declspec(dllexport) WINAPI _get_row(lprec *lp, long row_nr, double *row)
 {
  if (lp != NULL) {
   freebuferror();
   get_row(lp, row_nr, row);
  }
 }

/* fill column with the column col_nr from the problem */
void __declspec(dllexport) WINAPI _get_column(lprec *lp, long col_nr, double *column)
 {
  if (lp != NULL) {
   freebuferror();
   get_column(lp, col_nr, column);
  }
 }

/* get the reduced costs vector */
void __declspec(dllexport) WINAPI _get_reduced_costs(lprec *lp, double *rc)
 {
  if (lp != NULL) {
   freebuferror();
   get_reduced_costs(lp, rc);
  }
 }

/* get sensitivity objective function */
void __declspec(dllexport) WINAPI _get_sensitivity_obj(lprec *lp, double *objfrom, double *objtill)
 {
  if (lp != NULL) {
   freebuferror();
   memcpy(objfrom, lp->objfrom, (lp->columns + 1) * sizeof(*objfrom));
   memcpy(objtill, lp->objtill, (lp->columns + 1) * sizeof(*objtill));
  }
 }

/* get sensitivity RHS */
void __declspec(dllexport) WINAPI _get_sensitivity_rhs(lprec *lp, double *dualsfrom, double *dualstill)
 {
  if (lp != NULL) {
   freebuferror();
   memcpy(dualsfrom, lp->dualsfrom, (lp->sum + 1) * sizeof(*dualsfrom));
   memcpy(dualstill, lp->dualstill, (lp->sum + 1) * sizeof(*dualstill));
  }
 }

/* returns TRUE if the vector in values is a feasible solution to the lp */
long __declspec(dllexport) WINAPI _is_feasible(lprec *lp, double *values)
 {
  long ret;

  if (lp != NULL) {
   freebuferror();
   ret = is_feasible(lp, values);
  }
  else
   ret = FALSE;
  return(ret);
 }

/* returns TRUE if column is already present in lp. (Does not look at bounds
   and types, only looks at matrix values */
long __declspec(dllexport) WINAPI _column_in_lp(lprec *lp, double *column)
 {
  long ret;

  if (lp != NULL) {
   freebuferror();
   ret = column_in_lp(lp, column);
  }
  else
   ret = FALSE;
  return(ret);
 }

/* read a MPS file */
lprec __declspec(dllexport) * WINAPI _read_MPS(char *filename, long verbose)
 {
  lprec *lp;

  freebuferror();
  lp = read_MPS(filename, (short) ((verbose == 0) ? FALSE : TRUE));
  return(lp);
 }

/* write a MPS file to output */
long __declspec(dllexport) WINAPI _write_mps(lprec *lp, char *filename)
 {
  long ret;

  if (lp != NULL) {
   freebuferror();
   ret = write_mps(lp, filename);
  }
  return(ret);
 }

/* write a LP file to output */
long __declspec(dllexport) WINAPI _write_lp(lprec *lp, char *filename)
 {
  long ret;

  if (lp != NULL) {
   freebuferror();
   ret = write_lp(lp, filename);
  }
  return(ret);
 }

/* Print the current problem, only usefull in very small (test) problems.
  Shows the effect of scaling */
void __declspec(dllexport) WINAPI _print_lp(lprec *lp)
 {
  if (lp != NULL) {
   freebuferror();
   print_lp(lp);
  }
 }

/* Print the objective value */
void __declspec(dllexport) WINAPI _print_objective(lprec *lp)
 {
  if (lp != NULL) {
   freebuferror();
   print_objective(lp);
  }
 }

/* Print the solution */
void __declspec(dllexport) WINAPI _print_solution(lprec *lp)
 {
  if (lp != NULL) {
   freebuferror();
   print_solution(lp);
  }
 }

/* Print the constrataints */
void __declspec(dllexport) WINAPI _print_constraints(lprec *lp)
 {
  if (lp != NULL) {
   freebuferror();
   print_constraints(lp);
  }
 }

/* Print the dual variables of the solution */
void __declspec(dllexport) WINAPI _print_duals(lprec *lp)
 {
  if (lp != NULL) {
   freebuferror();
   print_duals(lp);
  }
 }

/* If scaling is used, print the scaling factors */
void __declspec(dllexport) WINAPI _print_scales(lprec *lp)
 {
  if (lp != NULL) {
   freebuferror();
   print_scales(lp);
  }
 }

/* file where results are printed to. Default stdout. If NULL then back stdout */
long __declspec(dllexport) WINAPI _print_file(char *filename)
 {
  freebuferror();
  return(print_file(filename));
 }

/* print a string */
void __declspec(dllexport) WINAPI _print_str(char *str)
 {
  print_str(str);
 }

void EndOfPgr(i)
 int i;
 {
 }

void __declspec(dllexport) WINAPI __Fortify_EnterScope()
 {
  Fortify_EnterScope();
 }

void __declspec(dllexport) WINAPI __Fortify_LeaveScope()
 {
  Fortify_LeaveScope();
 }
