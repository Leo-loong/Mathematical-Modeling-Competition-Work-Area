#include "defines.h"
#include "globals.h"

static void resize_eta(void)
{
  Cur_eta_size *= 2;
  if(Verbose)
    printf("Resizing Eta_value and Eta_rownr, new size is %d\n", Cur_eta_size);
  if(!(Eta_value = realloc(Eta_value, Cur_eta_size * sizeof(REAL))))
    {
      fprintf(stderr, "Error: cannot realloc Eta_value to size %d (entries)\n",
	      Cur_eta_size);
      exit(1);
    }
  if(!(Eta_rownr = realloc(Eta_rownr, Cur_eta_size * sizeof(int))))
    {
      fprintf(stderr, "Error: cannot realloc Eta_rownr to size %d (entries)\n",
	      Cur_eta_size);
      exit(1);
    }
} /* resize_eta */

static void condensecol(int   rownr,
			int   numc,
			REAL *pcol)
{
  int i, elnr;

  if(Verbose)
    printf("condensecol\n");
  elnr = Endetacol[numc];

  if(elnr + Rows + 1 > Cur_eta_size) /* maximum local growth of Eta */
    resize_eta();

  for(i = 0; i <= Rows; i++)
    if(i != rownr && pcol[i] != 0)
      {
	Eta_rownr[elnr] = i;
	Eta_value[elnr] = pcol[i];
	elnr++;
      }
  Eta_rownr[elnr] = rownr;
  Eta_value[elnr] = pcol[rownr];
  elnr++;
  if(numc > Sum + INVITER)
    {
      fprintf(stderr,
	      "Oops, writing to Endetacol[%d] in condensecol, out of bounds (#entries = %d)\n",
	      numc + 1, INVITER + Sum + 1 );
      fprintf(stderr, "Please contact the author michel@es.ele.tue.nl\n");
      exit(1);
    }
  Endetacol[numc + 1] = elnr;
} /* condensecol */

static void addetacol(void)
{
  int  i, j, k;
  REAL theta;

  if(Verbose)
    printf("addetacol\n");

  j = Endetacol[Numeta];
  k = Endetacol[++Numeta] - 1;
  theta = 1 / (REAL) Eta_value[k];
  Eta_value[k] = theta;
  for(i = j; i < k; i++)
    Eta_value[i] *= -theta;
} /* addetacol */

static void setpivcol(short lower,
		      int   varin,
		      REAL *pcol)
{
  int  i, colnr;
  REAL f;

  if(Verbose)
    printf("setpivcol\n");

  if(lower)
    f = 1;
  else
    f = -1;
  for(i = 0; i <= Rows; i++)
    pcol[i] = 0;
  if(varin > Rows)
    {
      colnr = varin - Rows;
      for(i = Cend[colnr - 1]; i < Cend[colnr]; i++)
	pcol[Mat[i].rownr] = Mat[i].value * f;
      pcol[0] -= Extrad * f;
    }
  else
    if(lower)
      pcol[varin] = 1;
    else
      pcol[varin] = -1;
  ftran(1, Numeta, pcol);
} /* setpivcol */

static short colprim(int   *colnr,
		     short  minit,
		     REAL  *drow)
{
  int    varnr, i, j;
  REAL   f, dpiv;

  if(Verbose)
    printf("colprim\n");

  dpiv = -Epsd;
  (*colnr) = 0;
  if(!minit)
    {
      for(i = 1; i <= Rows; i++)
	drow[i] = 0;
      drow[0] = 1;
      btran(Numeta, drow);
      for(i = 1; i <= Columns; i++)
	{
	  varnr = Rows + i;
	  if(!Basis[varnr] && (Upbo[varnr] > 0))
	    {
	      f = 0;
	      for(j = Cend[i - 1]; j < Cend[i]; j++)
		f += drow[Mat[j].rownr] * Mat[j].value;
	      drow[varnr] = f;
	    }
	}
      for(i = 1; i <= Sum; i++)
	if(my_abs(drow[i]) < Epsd)
	  drow[i] = 0;
    }
  for(i = 1; i <= Sum; i++)
    if(!Basis[i] && (Upbo[i] > 0))
      {
	if(Lower[i])
	  f = drow[i];
	else
	  f = -drow[i];
	if(f < dpiv)
	  {
	    dpiv = f;
	    (*colnr) = i;
	  }
      }
  return((*colnr) > 0);
} /* colprim */

static void minoriteration(int colnr,
			   int rownr)
{
  int  i, j, k, wk, varin, varout, elnr;
  REAL pivot, theta;

  if(Verbose)
    printf("minoriteration\n");

  varin = colnr + Rows;
  elnr = Endetacol[Numeta];
  wk = elnr;
  Numeta++;
  if(Extrad != 0)
    {
      Eta_rownr[elnr] = 0;
      Eta_value[elnr] = -Extrad;
      elnr++;
    }
  for(j = Cend[colnr - 1] ; j < Cend[colnr]; j++)
    {
      k = Mat[j].rownr;
      if(k == 0 && Extrad != 0)
	Eta_value[Endetacol[Numeta - 1]] += Mat[j].value;
      else
	if(k != rownr)
	  {
	    Eta_rownr[elnr] = k;
	    Eta_value[elnr] = Mat[j].value;
	    elnr++;
	  }
	else
	  pivot = Mat[j].value;
    }
  Eta_rownr[elnr] = rownr;
  Eta_value[elnr] = 1 / (REAL) pivot;
  elnr++;
  theta = Rhs[rownr] / (REAL) pivot;
  Rhs[rownr] = theta;
  for(i = wk; i < elnr - 1; i++)
    Rhs[Eta_rownr[i]] -= theta * Eta_value[i];
  varout = Bas[rownr];
  Bas[rownr] = varin;
  Basis[varout] = FALSE;
  Basis[varin] = TRUE;
  for(i = wk; i < elnr - 1; i++)
    Eta_value[i] /= - (REAL) pivot;
  /* printf("minoriteration: new etaindex: %d\n", elnr); */
  Endetacol[Numeta] = elnr;
} /* minoriteration */

static void rhsmincol(REAL theta,
		      int  rownr,
		      int  varin)
{
  int  i, j, k, varout;
  REAL f;

  if(Verbose)
    printf("rhsmincol\n");

  if(rownr > Rows)
    {
      fprintf(stderr, "Error: rhsmincol called with rownr: %d, Rows: %d\n",
	      rownr, Rows);
      fprintf(stderr, "This indicates numerical instability\n");
      fprintf(stderr, "If this happened with a small model, please send it to michel@es.ele.tue.nl\n");
      exit(1);
    }
  j = Endetacol[Numeta];
  k = Endetacol[Numeta + 1];
  for(i = j; i < k; i++)
    {
      f = Rhs[Eta_rownr[i]] - theta * Eta_value[i];
      if(my_abs(f) < Epsb)
	Rhs[Eta_rownr[i]] = 0;
      else
	Rhs[Eta_rownr[i]] = f;
    }
  Rhs[rownr] = theta;
  varout = Bas[rownr];
  Bas[rownr] = varin;
  Basis[varout] = FALSE;
  Basis[varin] = TRUE;
} /* rhsmincol */

static void invert(int n)
{
  int    i, j, v, wk, numit, varnr, rownr, colnr, varin;
  REAL   f, theta;
  REAL   *pcol;
  short  *frow;
  short  *fcol;
  int    *rownum, *col, *row;
  int    *colnum;

  CALLOC(rownum, Rows + 1,    int);
  CALLOC(col,    Rows + 1,    int);
  CALLOC(row,    Rows + 1,    int);
  CALLOC(pcol,   Rows + 1,    REAL);
  CALLOC(frow,   Rows + 1,    short);
  CALLOC(fcol,   Columns + 1, short);
  CALLOC(colnum, Columns + 1, int);

  if(Verbose)
    printf("a: invert:%d %d\n", Numeta, Endetacol[Numeta]);

  for(i = 0; i <= Rows; i++)
    frow[i] = TRUE;
  for(i = 0; i < n; i++)
    fcol[i] = FALSE;
  for(i = 0; i < Rows; i++)
    rownum[i] = 0;
  for(i = 1; i <= n; i++)
    colnum[i] = 0;
  for(i = 0; i <= Rows; i++)
    if(Bas[i] > Rows)
      fcol[Bas[i] - Rows - 1] = TRUE;
    else
      frow[Bas[i]] = FALSE;
  for(i = 1; i <= Rows; i++)
    if(frow[i])
      for(j = Rend[i - 1] + 1; j <= Rend[i]; j++)
	{
	  wk = Colno[j];
	  if(fcol[wk - 1])
	    {
	      colnum[wk]++;
	      rownum[i - 1]++;
	    }
	}
  for(i = 1; i <= Rows; i++)
    Bas[i] = i;
  for(i = 1; i <= Rows; i++)
    Basis[i] = TRUE;
  for(i = 1; i <= n; i++)
    Basis[i + Rows] = FALSE;
  for(i = 0; i <= Rows; i++)
    Rhs[i] = Rh[i];
  for(i = 1; i <= n; i++)
    {
      varnr = Rows + i;
      if(!Lower[varnr])
	{
	  theta = Upbo[varnr];
	  for(j = Cend[i - 1]; j < Cend[i]; j++)
	    Rhs[Mat[j].rownr] -= theta * Mat[j].value;
	}
    }
  for(i = 1; i <= Rows; i++)
    if(!Lower[i])
      Rhs[i] -= Upbo[i];
  Numeta = 0;
  v = 0;
  rownr = 0;
  Numinv = 0;
  numit = 0;
  while(v < Rows)
    {
      rownr++;
      if(rownr > Rows)
	rownr = 1;
      v++;
      if((rownum[rownr - 1] == 1) && frow[rownr])
	{
	  v = 0;
	  j = Rend[rownr - 1] + 1;
	  while(!(fcol[Colno[j] - 1]))
	    j++;
	  colnr = Colno[j];
	  fcol[colnr - 1] = FALSE;
	  colnum[colnr] = 0;
	  for(j = Cend[colnr - 1]; j < Cend[colnr]; j++)
	    if(frow[Mat[j].rownr])
	      rownum[Mat[j].rownr - 1]--;
	  frow[rownr] = FALSE;
	  minoriteration(colnr, rownr);
	}
    }
  v = 0;
  colnr = 0;
  while(v < n)
    {
      colnr++;
      if(colnr > n)
	colnr = 1;
      v++;
      if((colnum[colnr] == 1) && fcol[colnr - 1])
	{
	  v = 0;
	  j = Cend[colnr - 1] + 1;
	  while(!(frow[Mat[j - 1].rownr]))
	    j++;
	  rownr = Mat[j - 1].rownr;
	  frow[rownr] = FALSE;
	  rownum[rownr - 1] = 0;
	  for(j = Rend[rownr - 1] + 1; j <= Rend[rownr]; j++)
	    if(fcol[Colno[j] - 1])
	      colnum[Colno[j]]--;
	  fcol[colnr - 1] = FALSE;
	  numit++;
	  col[numit - 1] = colnr;
	  row[numit - 1] = rownr;
	}
    }
  for(j = 1; j <= n; j++)
    if(fcol[j - 1])
      {
	fcol[j - 1] = FALSE;
	setpivcol(Lower[Rows + j], j + Rows, pcol);
	rownr = 1;
	while(!(frow[rownr] && pcol[rownr]))
	  rownr++; /* this sometimes sets rownr to Rows + 1 and makes */
		   /* rhsmincol crash. MB */
	frow[rownr] = FALSE;
	condensecol(rownr, Numeta, pcol);
	theta = Rhs[rownr] / (REAL) pcol[rownr];
	rhsmincol(theta, rownr, Rows + j);
	addetacol();
      }
  for(i = numit - 1; i >= 0; i--)
    {
      colnr = col[i];
      rownr = row[i];
      varin = colnr + Rows;
      for(j = 0; j <= Rows; j++)
	pcol[j] = 0;
      for(j = Cend[colnr - 1]; j < Cend[colnr]; j++)
	pcol[Mat[j].rownr] = Mat[j].value;
      pcol[0] -= Extrad;
      condensecol(rownr, Numeta, pcol);
      theta = Rhs[rownr] / (REAL) pcol[rownr];
      rhsmincol(theta, rownr, varin);
      addetacol();
    }
  for(i = 1; i <= Rows; i++)
    if(my_abs(Rhs[i]) < Epsb)
      Rhs[i] = 0;

  if(Verbose)
    {
      f = 0;
      for(i = 1; i <= Rows; i++)
	if(Rhs[i] < 0)
	  f += Rhs[i];
	else
	  if(Rhs[i] > Upbo[Bas[i]])
	    f = f + Upbo[Bas[i]] - Rhs[i];
      printf("b: invert:%d %d  %12f  %12f\n", Numeta, Endetacol[Numeta],
	     (double)Rhs[0], (double)f);
    }

  free(rownum);
  free(col);
  free(row);
  free(pcol);
  free(frow);
  free(fcol);
  free(colnum);
} /* invert */

static short rowprim(int  *rownr,
		     REAL *theta,
		     REAL *pcol)
{
  int  i;
  REAL f, quot;

  if(Verbose)
    printf("rowprim\n");

  (*rownr) = 0;
  (*theta) = Infinite;
  for(i = 1; i <= Rows; i++)
    {
      f = pcol[i];
      if(f != 0)
	{
	  /* quot = (*theta) * 10; */
	  if(f > 0)
	    quot = Rhs[i] / (REAL) f;
	  else if(Upbo[Bas[i]] < Infinite)
	    quot = (Rhs[i] - Upbo[Bas[i]]) / (REAL) f;
	  else
	    continue;
	  if(quot < (*theta))
	    {
	      (*theta) = quot;
	      (*rownr) = i;
	    }
	}
    }

  if((*theta)<0)
    {
      fprintf(stderr, "Warning, quot was negative (%g) in rowprim\n", *theta);
    }

  return((*rownr) > 0);
} /* rowprim */

static void iteration(int    rownr,
		      int    varin,
		      REAL  *theta,
		      REAL   up,
		      short *minit,
		      short *low,
		      short  primal,
		      short  smotes,
		      int   *iter)
{
  int  i, k, varout;
  REAL f, pivot;

  if(Verbose)
    printf("iteration\n");

  (*iter)++;
  (*minit) = (*theta) > up;
  if((*minit))
    {
      (*theta) = up;
      (*low) = !(*low);
    }
  k = Endetacol[Numeta + 1];
  pivot = Eta_value[k - 1];
  for(i = Endetacol[Numeta]; i < k; i++)
    {
      f = Rhs[Eta_rownr[i]] - (*theta) * Eta_value[i];
      if(my_abs(f) < Epsb)
	Rhs[Eta_rownr[i]] = 0;
      else
	Rhs[Eta_rownr[i]] = f;
    }
  if(!(*minit))
    {
      Rhs[rownr] = (*theta);
      varout = Bas[rownr];
      Bas[rownr] = varin;
      Basis[varout] = FALSE;
      Basis[varin] = TRUE;
      if(primal && pivot < 0)
	Lower[varout] = FALSE;
      if(!(*low) && up != Infinite)
	{
	  (*low) = TRUE;
	  Rhs[rownr] = up - Rhs[rownr];
	  for(i = Endetacol[Numeta]; i < k; i++)
	    Eta_value[i] = -Eta_value[i];
	}
      addetacol();
      Numinv++;
    }
  if(smotes && Verbose)
    {
      printf("Iteration %d: ", (*iter));
      if((*minit))
	{
	  printf("%4d", varin);
	  if(Lower[varin])
	    printf("  ");
	  else
	    printf(" u");
	  printf("%22c", ' ');
	}
      else
	{
	  printf("%4d", varin);
	  if(Lower[varin])
	    printf("  ");
	  else
	    printf(" u");
	  printf("%4d", varout);
	  if(Lower[varout])
	    printf("  ");
	  else
	    printf(" u");
	  printf("%12.5f", (double)pivot);
	}
      printf("    %12f", (double)Pcol[0]);
      if(!primal)
	{
	  f = 0;
	  for(i = 1; i <= Rows; i++)
	    if(Rhs[i] < 0)
	      f += Rhs[i];
	    else
	      if(Rhs[i] > Upbo[Bas[i]])
		f = f + Upbo[Bas[i]] - Rhs[i];
	  printf("  %12f", (double)f);
	}
      else
	printf("    %12f", (double)Rhs[0]);
      printf("\n");
    }
} /* iteration */

static int solvelp(void)
{
  int    i, j, iter, varnr;
  REAL   f, theta;
  short  primal, doiter, doinvert, smotes;
  REAL   *drow, *prow;
  short  artif, minit;
  int    colnr, rownr;

  CALLOC(drow, Sum + 1, REAL);
  CALLOC(prow, Sum + 1, REAL);

  iter = 0;
  minit = FALSE;
  i = 0;
  smotes = TRUE;

  primal=TRUE;

  while(i != Rows && primal)
    {
      i++;
      primal = Rhs[i] >= 0 && Rhs[i] <= Upbo[Bas[i]];
    }

  if(!primal)
    {
      drow[0] = 1;
      for(i = 1; i <= Rows; i++)
	drow[i] = 0;
      Extrad = 0;
      for(i = 1; i <= Columns; i++)
	{
	  varnr = Rows + i;
	  drow[varnr] = 0;
	  for(j = Cend[i - 1]; j < Cend[i]; j++)
	    if(drow[Mat[j].rownr] != 0)
	      drow[varnr] += drow[Mat[j].rownr] * Mat[j].value;
	  if(drow[varnr] < Extrad)
	    Extrad = drow[varnr];
	}
      artif = Extrad < -Epsd;
    }
  else /* primal */
    {
      artif = FALSE;
      Extrad = 0;
    }
  if(Verbose)
    printf("artificial:%12.5f\n", (double)Extrad);
  minit = FALSE;
  do {
    doiter = FALSE;
    doinvert = FALSE;
    if(primal)
      {
	rownr = 0;
	if(colprim(&colnr, minit, drow))
	  {
	    setpivcol(Lower[colnr], colnr, Pcol);
	    if(rowprim(&rownr, &theta, Pcol))
	      {
		doiter = TRUE;
		condensecol(rownr, Numeta, Pcol);
	      }
	  }
      }
    else /* not primal */
      {
	if(!minit)
	  rowdual(&rownr);
	if(!doinvert)
	  if(rownr > 0)
	    {
	      if(coldual(rownr, &colnr, minit, prow, drow))
		{
		  doiter = TRUE;
		  setpivcol(Lower[colnr], colnr, Pcol);
		  condensecol(rownr, Numeta, Pcol);
		  f = Rhs[rownr] - Upbo[Bas[rownr]];
		  if(f > 0)
		    {
		      theta = f / (REAL) Pcol[rownr];
		      if(theta <= Upbo[colnr])
			Lower[Bas[rownr]] = !Lower[Bas[rownr]];
		    }
		  else /* f <= 0 */
		    {
		      /* getting div by zero here ... MB */
		      if(Pcol[rownr] == 0)
			{
			  fprintf(stderr,
				  "Oops, attempt to divide by zero (Pcol[%d])\n",
				  rownr);
			  fprintf(stderr,
				  "This indicates numerical instability\n");
			  fprintf(stderr,
				  "If this happened with a small model, please send it to michel@es.ele.tue.nl\n");
			  abort();
			}
		      theta = Rhs[rownr] / (REAL) Pcol[rownr];
		    }
		}
	    }
	  else /* rownr <= 0 */
	    {
              primal = TRUE;
              artif = FALSE;
	      doinvert = TRUE;
	      Extrad = 0;
	    }
      }
    if(doiter)
      iteration(rownr, colnr, &theta, Upbo[colnr], &minit, &Lower[colnr],
		primal, smotes, &iter);
    if(Numinv >= Invnum)
      doinvert = TRUE;
    if(doinvert)
      invert(Columns);
  } while(rownr && colnr || doinvert);

  free(drow);
  free(prow);

  if(rownr || colnr)
    debug_print("solvelp failed, rownr = %d, colnr = %d\n", rownr, colnr);

  /* rownr != 0 => No feasible solution */
  /* colnr != 0 => Unbounded */

  if(rownr && colnr) /* error */
    {
      fprintf(stderr,
	      "No valid solution found, but diagnostics (infeasible or unbounded) contradict\n");
      exit(1);
    }
  else if(rownr)
    return(INFEASIBLE);
  else if(colnr)
    return(UNBOUNDED);
  else
    return(OPTIMAL);
} /* solvelp */

static void construct_solution(REAL *sol)
{
  int  i, j, basi;
  REAL f;

  /* zero all results of rows */
  memset(sol, '\0', (Rows + 1) * sizeof(REAL));

  for(i = Rows + 1; i <= Sum; i++)
    sol[i] = Lowbo[i];
  for(i = 1; i <= Rows; i++)
    {
      basi = Bas[i];
      if(basi > Rows)
	sol[basi] += Rhs[i];
    }
  for(i = Rows + 1; i <= Sum; i++)
    if(!Basis[i] && !Lower[i])
      sol[i] += Upbo[i];
  for(j = 1; j <= Columns; j++)
    {
      f = sol[Rows + j];
      if(f != 0)
	for(i = Cend[j - 1]; i < Cend[j]; i++)
	  sol[Mat[i].rownr] += f * Mat[i].value;
    }

  for(i = 0; i <= Rows; i++)
    {
      if(my_abs(sol[i]) < Epsb)
	sol[i] = 0;
      else
	if(Chsign[i])
	  sol[i] = -sol[i];
    }
} /* construct_solution */

static short is_int(REAL value)
{
  REAL tmp;

  tmp = value - floor(value);
  if(tmp < Epsilon)
    return(1);
  if((tmp > 0.5) && ((1.0 - tmp) < Epsilon))
    return(1);
  return(0);
} /* is_int */

static REAL *calculate_duals(REAL *duals)
{
  int i;

 /* initialise */
  for(i = 1; i <= Rows; i++)
    duals[i] = 0;
  duals[0] = 1;
  btran(Numeta, duals);

  /* the dual values are the reduced costs of the slacks */
  /* When the slack is at its upper bound, change the sign. Can this happen? */
  for(i = 1; i <= Rows; i++)
    {
      if(Lower[i] == FALSE)
	duals[i] = -duals[i];
      if(Basis[i] == TRUE) /* to make sure */
	duals[i] = 0;
    }

  return(duals);
}

int solve(REAL  *upbo,
	  REAL  *lowbo,
          short *sbasis,
          short *slower,
          int   *sbas)
{
  int     i, j, failure, notint, is_worse;
  intrec *ptr;
  REAL    theta;

  Level++;
  debug_print("starting solve");

  /* make fresh copies of Upbo, Lowbo, Basis, Lower, Bas and Rh as solving
     changes them */
  memcpy(Upbo,  upbo,    (Sum + 1)  * sizeof(REAL));
  memcpy(Lowbo, lowbo,   (Sum + 1)  * sizeof(REAL));
  memcpy(Basis, sbasis,  (Sum + 1)  * sizeof(short));
  memcpy(Lower, slower,  (Sum + 1)  * sizeof(short));
  memcpy(Bas,   sbas,    (Rows + 1) * sizeof(int));
  memcpy(Rh,    Orig_rh, (Rows + 1) * sizeof(REAL));

  for(i = 1; i <= Columns; i++)
    if(Lowbo[Rows + i] > 0)
      {
        theta = Lowbo[ Rows + i];
	Upbo[Rows + i] -= theta;
        for(j = Cend[i - 1]; j < Cend[i]; j++)
          Rh[Mat[j].rownr] -= theta * Mat[j].value;
      }

  invert(Columns);

  failure = solvelp();

  if(failure != OPTIMAL)
    debug_print("this problem has no solution, it is %s",
		(failure == UNBOUNDED) ? "unbounded" : "infeasible");

  if(failure == OPTIMAL) /* there is a solution */
    {
      construct_solution(Solution);

      debug_print("a solution was found");
      debug_print_solution(Solution);

      /* if this solution is worse than the best sofar, this branch must die */
      if(Maximise)
	is_worse = Solution[0] <= Best_solution[0];
      else /* minimising! */
	is_worse = Solution[0] >= Best_solution[0];

      if(is_worse)
	  {
	    debug_print("but it was worse than the best sofar, discarded");
	    Level--;
	    return(MILP_FAIL);
	  }

      /* check if solution contains enough ints */
      notint = 0;
      for(ptr = First_int; !notint && ptr; ptr = ptr->next)
	if(!is_int(Solution[ptr->varnr]))
	  notint = ptr->varnr;

      if(notint) /* there is at least one value not yet int */
	{
	  /* set up two new problems */
	  REAL  *new_upbo, *new_lowbo;
	  REAL   new_bound;
          short *new_lower, *new_basis;
	  int   *new_bas, res1, res2;

	  /* allocate room for them */
	  MALLOC(new_upbo,  Sum + 1,  REAL);
	  MALLOC(new_lowbo, Sum + 1,  REAL);
          MALLOC(new_lower, Sum + 1,  short);
          MALLOC(new_basis, Sum + 1,  short);
          MALLOC(new_bas,   Rows + 1, int);
	  memcpy(new_upbo,  upbo,  (Sum + 1)  * sizeof(REAL));
          memcpy(new_lowbo, lowbo, (Sum + 1)  * sizeof(REAL));
          memcpy(new_lower, Lower, (Sum + 1)  * sizeof(short));
          memcpy(new_basis, Basis, (Sum + 1)  * sizeof(short));
          memcpy(new_bas,   Bas,   (Rows + 1) * sizeof(int));

	  debug_print("not enough ints. Selecting var %s, val: %10.3g",
		      Names[notint], (double)Solution[notint]);
	  debug_print("current bounds:\n");
	  debug_print_bounds(upbo, lowbo);

          if(Floorfirst)
            {
              new_bound = floor(Solution[notint]);
              /* this bound might conflict */
              if(new_bound < lowbo[notint])
	        {
	          debug_print("New upper bound value %g conflicts with old lower bound %g\n", (double)new_bound, (double)lowbo[notint]);
                  res1 = MILP_FAIL;
	        }
	      else /* bound feasible */
	        {
	          new_upbo[notint] = new_bound;
                  new_lower[notint]=TRUE;
                  debug_print("starting first subproblem with bounds:");
	          debug_print_bounds(new_upbo, lowbo);

	          res1 = solve(new_upbo, lowbo, new_basis, new_lower, new_bas);
	        }
              new_bound += 1;
	      if(new_bound > upbo[notint])
	        {
	          debug_print("New lower bound value %g conflicts with old upper bound %g\n", (double)new_bound, (double)upbo[notint]);
	          res2 = MILP_FAIL;
	        }
	      else /* bound feasible */
	       {
	         new_lowbo[notint] = new_bound;
                 new_lower[notint]=TRUE;
	         debug_print("starting second subproblem with bounds:");
	         debug_print_bounds(upbo, new_lowbo);

	         res2 = solve(upbo, new_lowbo, new_basis, new_lower, new_bas);
	       }
	    }
          else /* take ceiling first */
            {
              new_bound = ceil(Solution[notint]);
              /* this bound might conflict */
              if(new_bound > upbo[notint])
	        {
	          debug_print("New lower bound value %g conflicts with old upper bound %g\n", (double)new_bound, (double)upbo[notint]);
                  res1 = MILP_FAIL;
	        }
	      else /* bound feasible */
	        {
	          new_lowbo[notint] = new_bound;
                  new_lower[notint]=TRUE;
                  debug_print("starting first subproblem with bounds:");
	          debug_print_bounds(upbo, new_lowbo);

	          res1 = solve(upbo, new_lowbo, new_basis, new_lower, new_bas);
	        }
              new_bound -= 1;
	      if(new_bound < lowbo[notint])
	        {
	          debug_print("New upper bound value %g conflicts with old lower bound %g\n", (double)new_bound, (double)lowbo[notint]);
	          res2 = MILP_FAIL;
	        }
	      else /* bound feasible */
	       {
	         new_lowbo[notint] = new_bound;
                 new_lower[notint]=TRUE;
	         debug_print("starting second subproblem with bounds:");
	         debug_print_bounds(new_upbo, lowbo);

	         res2 = solve(new_upbo, lowbo, new_basis, new_lower, new_bas);
	       }
	    }

	  if(res1 && res2) /* both failed. They must have been infeasible */
	    failure = INFEASIBLE;
	  else
	    failure = OPTIMAL;

	  free(new_upbo);
	  free(new_lowbo);
          free(new_basis);
          free(new_lower);
          free(new_bas);
	}
      else /* all required values are int */
	{
	  debug_print("--> Valid solution found");

	  if(Maximise)
	    is_worse = Solution[0] < Best_solution[0];
	  else
	    is_worse = Solution[0] > Best_solution[0];

	  if(!is_worse) /* Current solution better */
	    {
	      debug_print("the best sofar. Prev: %10.3g, New: %10.3g",
			  (double)Best_solution[0], (double)Solution[0]);
	      memcpy(Best_solution, Solution, (Sum + 1) * sizeof(REAL));
	      if(Print_duals)
		calculate_duals(Best_duals);
	      if(Show_results)
		{
		  fprintf(stderr, "Intermediate solution:\n");
		  print_solution(stderr, Best_solution, Best_duals);
		}
	    }
	}
    }
  Level--;

  /* failure can have the values OPTIMAL, UNBOUNDED and INFEASIBLE. */
  return(failure);
} /* solve */
