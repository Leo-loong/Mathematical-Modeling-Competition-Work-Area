#include "defines.h"
#include "globals.h"

static void resize_eta(void)
{
  Cur_eta_size *= 2;
  if (Verbose)
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

static void condensecol(int rownr,
			int numc,
			REAL   *pcol)
{
  int  i, elnr;
  
  if (Verbose)
    printf("condensecol\n");
  elnr = Endetacol[numc];

  if (elnr + Rows + 2 > Cur_eta_size) /* maximum local growth of Eta */
    resize_eta();

  for (i = 0; i <= Rows; i++)
    if (i != rownr && pcol[i] != 0)
      {
	Eta_rownr[elnr] = i;
	Eta_value[elnr] = pcol[i];
	elnr++;
      }
  Eta_rownr[elnr] = rownr;
  Eta_value[elnr] = pcol[rownr];
  elnr++;
  Endetacol[numc + 1] = elnr;
} /* condensecol */

static void addetacol(int *numc)
{
  int    i, j, k;
  REAL   theta;
  
  if (Verbose)
    printf("addetacol\n");
  j = Endetacol[(*numc)];
  (*numc)++;
  k = Endetacol[(*numc)];
  theta = 1 / (REAL) Eta_value[k - 1];
  Eta_value[k - 1] = theta;
  for (i = j; i < k - 1; i++)
    Eta_value[i] *= -theta;
} /* addetacol */


static void presolve(void)
{
  int    i, j, rownr;
  REAL   theta;
  int    *num, *rownum;

  CALLOC(num, Rows + 2, int);
  CALLOC(rownum, Rows + 2, int);
  
  if (Verbose)
    printf("presolve\n");
  Rh[0] = 0;
  for (i = 0; i <= Sum; i++)
    Lower[i] = TRUE;
  for (i = 1; i <= Rows; i++)
    Basis[i] = TRUE;
  for (i = 1; i <= Columns; i++)
    Basis[Rows + i] = FALSE;
  for (i = 0; i <= Rows; i++)
    Bas[i] = i;

  /* if we want to maximise the objective function,
     change the signs of the objective function */
  if(Maximise)
    Chsign[0] = TRUE;
  else
    Chsign[0] = FALSE;

  for (i = 1; i <= Rows; i++)
    if ((Relat[i] == GE) && (Upbo[i] == Infinite))
      Chsign[i] = TRUE;
    else
      Chsign[i] = FALSE;

  /* invert values in rows with Chsign[i] == TRUE */
  for (i = 1; i <= Rows; i++)
    if (Chsign[i])
      Rh[i] = -Rh[i];
  for (i = 0; i < Nonnuls; i++)
    if (Chsign[Mat[i].rownr])
      Mat[i].value = -Mat[i].value;

  /* handle lower bounds by transforming to 0 */
  for (i = 1; i <= Columns; i++)
    if (Lowbo[Rows + i] > 0)
      {
	theta = Lowbo[Rows + i];
	Upbo[Rows + i] -= theta;
	for (j = Cend[i - 1]; j < Cend[i]; j++)
	  Rh[Mat[j].rownr] -= theta * Mat[j].value;
      }

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
} /* presolve */

static void setpivcol(short lower, 
		int varin,
		int numeta,
		REAL   *pcol)
{
  int    i, colnr;
  REAL   f;
  
  if (Verbose)
    printf("setpivcol\n");
  if (lower)
    f = 1;
  else
    f = -1;
  for (i = 0; i <= Rows; i++)
    pcol[i] = 0;
  if (varin > Rows)
    {
      colnr = varin - Rows;
      for (i = Cend[colnr - 1]; i < Cend[colnr]; i++)
	pcol[Mat[i].rownr] = Mat[i].value * f;
      pcol[0] -= Extrad * f;
    }
  else
    if (lower)
      pcol[varin] = 1;
    else
      pcol[varin] = -1;
  ftran(1, numeta, pcol);
} /* setpivcol */


static short colprim(int *colnr,
		     int numeta,
		     short minit,
		     REAL   *drow)
{
  int    varnr, i, j;
  REAL   f, dpiv;
  
  if (Verbose)
    printf("colprim\n");
  dpiv = -Epsd;
  (*colnr) = 0;
  if (!minit)
    {
      for (i = 1; i <= Rows; i++)
	drow[i] = 0;
      drow[0] = 1;
      btran(numeta, drow);
      for (i = 1; i <= Columns; i++)
	{
	  varnr = Rows + i;
	  if (!Basis[varnr])
	    if (Upbo[varnr] > 0)
	      {
		f = 0;
		for (j = Cend[i - 1]; j < Cend[i]; j++)
		  f += drow[Mat[j].rownr] * Mat[j].value;
		drow[varnr] = f;
	      }
	}
      for (i = 1; i <= Sum; i++)
	if (abs(drow[i]) < Epsd)
	  drow[i] = 0;
    }
  for (i = 1; i <= Sum; i++)
    if (!Basis[i])
      if (Upbo[i] > 0)
	{
	  if (Lower[i])
	    f = drow[i];
	  else
	    f = -drow[i];
	  if (f < dpiv)
	    {
	      dpiv = f;
	      (*colnr) = i;
	    }
	}
  return ((*colnr) > 0);
} /* colprim */


static void minoriteration(int colnr,
			   int rownr,
			   int *numeta)
{
  int    i, j, k, wk, varin, varout, elnr;
  REAL   pivot, theta;
  
  if (Verbose)
    printf("minoriteration\n");
  varin = colnr + Rows;
  elnr = Endetacol[(*numeta)];
  wk = elnr;
  (*numeta)++;
  if (Extrad != 0)
    {
      Eta_rownr[elnr] = 0;
      Eta_value[elnr] = -Extrad;
      elnr++;
    }
  for (j = Cend[colnr - 1] ; j < Cend[colnr]; j++)
    {
      k = Mat[j].rownr;
      if (k == 0 && Extrad != 0)
	Eta_value[Endetacol[(*numeta) - 1]] += Mat[j].value;
      else
	if (k != rownr)
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
  for (i = wk; i < elnr - 1; i++)
    Rhs[Eta_rownr[i]] -= theta * Eta_value[i];
  varout = Bas[rownr];
  Bas[rownr] = varin;
  Basis[varout] = FALSE;
  Basis[varin] = TRUE;
  for (i = wk; i < elnr - 1; i++)
    Eta_value[i] /= - (REAL) pivot;
  /* printf("minoriteration: new etaindex: %d\n", elnr); */
  Endetacol[(*numeta)] = elnr;
} /* minoriteration */


static void rhsmincol(REAL   theta,
		      int rownr,
		      int varin,
		      int numeta)
{
  int    i, j, k, varout;
  REAL   f;
  
  if (Verbose)
    printf("rhsmincol\n");
  if (rownr > Rows + 1)
    {
      fprintf(stderr, "Error: rhsmincol called with rownr: %d, Rows: %d\n",
	      rownr, Rows);
      fprintf(stderr, "This indicates numerical instability\n");
      fprintf(stderr, "If this happened with a small model, please send it to michel@es.ele.tue.nl\n");
      exit(1);
    }
  j = Endetacol[numeta];
  k = Endetacol[numeta + 1];
  for (i = j; i < k; i++)
    {
      f = Rhs[Eta_rownr[i]] - theta * Eta_value[i];
      if (abs(f) < Epsb)
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

static void invert(int n,
		   int *numeta,
		   int *numinv)
{
  int    i, j, v, wk, numit, varnr, rownr, colnr, varin;
  REAL   f, theta;
  REAL   *pcol;
  short  *frow;
  short  *fcol;
  int    *rownum, *col, *row;
  int    *colnum;
  short  *lbas;
  REAL   *rhs1;
 
  CALLOC(rownum, Rows + 1, int);
  CALLOC(col, Rows + 1, int);
  CALLOC(row, Rows + 1, int);
  CALLOC(pcol, Rows + 2, REAL);
  CALLOC(frow, Rows + 2, short);
  CALLOC(fcol, Columns + 1, short);
  CALLOC(colnum, Columns + 2, int);
  CALLOC(lbas, Sum +2, short);
  CALLOC(rhs1, Rows + 2, REAL);
 
  if (Verbose)
    printf("a: invert:%d %d  %12f\n", (*numeta), Endetacol[(*numeta)],
	   (double)Rhs[0]);
  
  for(i = 0; i <= Sum + 1; i++)
    lbas[i] = Basis[i];
  for(i = 0; i <= Rows + 1; i++)
    rhs1[i] = Rhs[i];
  for (i = 0; i <= Rows; i++)
    frow[i] = TRUE;
  for (i = 0; i < n; i++)
    fcol[i] = FALSE;
  for (i = 0; i < Rows; i++)
    rownum[i] = 0;
  for (i = 1; i <= n; i++)
    colnum[i] = 0;
  for (i = 0; i <= Rows; i++)
    if (Bas[i] > Rows)
      fcol[Bas[i] - Rows - 1] = TRUE;
    else
      frow[Bas[i]] = FALSE;
  for (i = 1; i <= Rows; i++)
    if (frow[i])
      for (j = Rend[i - 1] + 1; j <= Rend[i]; j++)
	{
	  wk = Colno[j];
	  if (fcol[wk - 1])
	    {
	      colnum[wk]++;
	      rownum[i - 1]++;
	    }
	}
  for (i = 1; i <= Rows; i++)
    Bas[i] = i;
  for (i = 1; i <= Rows; i++)
    Basis[i] = TRUE;
  for (i = 1; i <= n; i++)
    Basis[i + Rows] = FALSE;
  for (i = 0; i <= Rows; i++)
    Rhs[i] = Rh[i];
  for (i = 1; i <= n; i++)
    {
      varnr = Rows + i;
      if (!Lower[varnr])
	{
	  theta = Upbo[varnr];
	  for (j = Cend[i - 1]; j < Cend[i]; j++)
	    Rhs[Mat[j].rownr] -= theta * Mat[j].value;
	}
    }
  for (i = 1; i <= Rows; i++)
    if (!Lower[i])
      Rhs[i] -= Upbo[i];
  (*numeta) = 0;
  v = 0;
  rownr = 0;
  (*numinv) = 0;
  numit = 0;
  while (v < Rows)
    {
      rownr++;
      if (rownr > Rows)
	rownr = 1;
      v++;
      if (rownum[rownr - 1] == 1)
	if (frow[rownr])
	  {
	    v = 0;
	    j = Rend[rownr - 1] + 1;
	    while (!(fcol[Colno[j] - 1]))
	      j++;
	    colnr = Colno[j];
	    fcol[colnr - 1] = FALSE;
	    colnum[colnr] = 0;
	    for (j = Cend[colnr - 1]; j < Cend[colnr]; j++)
	      if (frow[Mat[j].rownr])
		rownum[Mat[j].rownr - 1]--;
	    frow[rownr] = FALSE;
	    minoriteration(colnr, rownr, numeta);
	  }
    }
  v = 0;
  colnr = 0;
  while (v < n)
    {
      colnr++;
      if (colnr > n)
	colnr = 1;
      v++;
      if (colnum[colnr] == 1)
	if (fcol[colnr - 1])
	  {
	    v = 0;
	    j = Cend[colnr - 1] + 1;
	    while (!(frow[Mat[j - 1].rownr]))
	      j++;
	    rownr = Mat[j - 1].rownr;
	    frow[rownr] = FALSE;
	    rownum[rownr - 1] = 0;
	    for (j = Rend[rownr - 1] + 1; j <= Rend[rownr]; j++)
	      if (fcol[Colno[j] - 1])
		colnum[Colno[j]]--;
	    fcol[colnr - 1] = FALSE;
	    numit++;
	    col[numit - 1] = colnr;
	    row[numit - 1] = rownr;
	  }
    }
  for (j = 1; j <= n; j++)
    if (fcol[j - 1])
      {
	fcol[j - 1] = FALSE;
	setpivcol(Lower[Rows + j], j + Rows, (*numeta), pcol);
	rownr = 1;
	while (!(frow[rownr] && pcol[rownr]))
	  rownr++; /* this sometimes sets rownr to Rows + 2 and makes */
		   /* rhsmincol crash. MB */
	frow[rownr] = FALSE;
	condensecol(rownr, (*numeta), pcol);
	theta = Rhs[rownr] / (REAL) pcol[rownr];
	rhsmincol(theta, rownr, Rows + j, (*numeta));
	addetacol(numeta);
      }
  for (i = numit - 1; i >= 0; i--)
    {
      colnr = col[i];
      rownr = row[i];
      varin = colnr + Rows;
      for (j = 0; j <= Rows; j++)
	pcol[j] = 0;
      for (j = Cend[colnr - 1]; j < Cend[colnr]; j++)
	pcol[Mat[j].rownr] = Mat[j].value;
      pcol[0] -= Extrad;
      condensecol(rownr, (*numeta), pcol);
      theta = Rhs[rownr] / (REAL) pcol[rownr];
      rhsmincol(theta, rownr, varin, (*numeta));
      addetacol(numeta);
    }
  for (i = 1; i <= Rows; i++)
    if (abs(Rhs[i]) < Epsb)
      Rhs[i] = 0;

  if (Verbose)
    {
      f = 0;
      for (i = 1; i <= Rows; i++)
	if (Rhs[i] < 0)
	  f += Rhs[i];
	else
	  if (Rhs[i] > Upbo[Bas[i]])
	    f = f + Upbo[Bas[i]] - Rhs[i];
      printf("b: invert:%d %d  %12f  %12f\n", (*numeta), Endetacol[(*numeta)],
	     (double)Rhs[0], (double)f);
    }

  free(rownum);
  free(col);
  free(row);
  free(pcol);
  free(frow);
  free(fcol);
  free(colnum);
  free(lbas);
  free(rhs1);
} /* invert */


static short rowprim(int *rownr,
		     REAL   *theta,
		     REAL   *pcol)
{
  int    i;
  REAL   f, quot;
  
  if (Verbose)
    printf("rowprim\n");
  (*rownr) = 0;
  (*theta) = Infinite;
  for (i = 1; i <= Rows; i++)
    {
      f = pcol[i];
      if (f != 0)
	{
	  quot = (*theta) * 10;
	  if (f > 0)
	    quot = Rhs[i] / (REAL) f;
	  else
	    if (Upbo[Bas[i]] < Infinite)
	      quot = (Rhs[i] - Upbo[Bas[i]]) / (REAL) f;
	  if (quot < (*theta))
	    {
	      (*theta) = quot;
	      (*rownr) = i;
	    }
	}
    }
  return ((*rownr) > 0);
} /* rowprim */


static void iteration(int *numc,
		      int rownr,
		      int varin,
		      REAL   *theta,
		      REAL   up,
		      short *minit,
		      short *low,
		      short primal,
		      short smotes,
		      int *iter,
		      int *numinv)
{
  int    i, k, varout;
  REAL   f, pivot;
  
  if (Verbose)
    printf("iteration\n");
  (*iter)++;
  (*minit) = (*theta) > up;
  if ((*minit))
    {
      (*theta) = up;
      (*low) = !(*low);
    }
  k = Endetacol[(*numc) + 1];
  pivot = Eta_value[k - 1];
  for (i = Endetacol[(*numc)]; i < k; i++)
    {
      f = Rhs[Eta_rownr[i]] - (*theta) * Eta_value[i];
      if (abs(f) < Epsb)
	Rhs[Eta_rownr[i]] = 0;
      else
	Rhs[Eta_rownr[i]] = f;
    }
  if (!(*minit))
    {
      Rhs[rownr] = (*theta);
      varout = Bas[rownr];
      Bas[rownr] = varin;
      Basis[varout] = FALSE;
      Basis[varin] = TRUE;
      if (primal && pivot < 0)
	Lower[varout] = FALSE;
      if (!(*low) && up != Infinite)
	{
	  (*low) = TRUE;
	  Rhs[rownr] = up - Rhs[rownr];
	  for (i = Endetacol[(*numc)]; i < k; i++)
	    Eta_value[i] = -Eta_value[i];
	}
      addetacol(numc);
      (*numinv)++;
    }
  if (smotes && Verbose)
    {
      printf("Iteration %d: ", (*iter));
      if ((*minit))
	{
	  printf("%4d", varin);
	  if (Lower[varin])
	    printf("  ");
	  else
	    printf(" u");
	  printf("%22c", ' ');
	}
      else
	{
	  printf("%4d", varin);
	  if (Lower[varin])
	    printf("  ");
	  else
	    printf(" u");
	  printf("%4d", varout);
	  if (Lower[varout])
	    printf("  ");
	  else
	    printf(" u");
	  printf("%12.5f", (double)pivot);
	}
      printf("    %12f", (double)Pcol[0]);
      if (!primal)
	{
	  f = 0;
	  for (i = 1; i <= Rows; i++)
	    if (Rhs[i] < 0)
	      f += Rhs[i];
	    else
	      if (Rhs[i] > Upbo[Bas[i]])
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
  int    numinv, invnum;
  int    numeta;
  short  artif, minit;
  int    colnr, rownr;
 
  CALLOC(drow, Sum + 2, REAL);
  CALLOC(prow, Sum + 2, REAL);
 
  numinv = 0;
  invnum = 50; /* number of iterations between inversions */
  numeta = 0;
  iter = 0;
  minit = FALSE;
  primal = TRUE;
  i = 0;
  smotes = TRUE;

  while (i != Rows && primal)
    {
      i++;
      primal = Rhs[i] >= 0 && Rhs[i] <= Upbo[Bas[i]];
    }
  
  if (!primal)
    {
      drow[0] = 1;
      for (i = 1; i <= Rows; i++)
	drow[i] = 0;
      Extrad = 0;
      for (i = 1; i <= Columns; i++)
	{
	  varnr = Rows + i;
	  drow[varnr] = 0;
	  for (j = Cend[i - 1]; j < Cend[i]; j++)
	    if (drow[Mat[j].rownr] != 0)
	      drow[varnr] += drow[Mat[j].rownr] * Mat[j].value;
	  if (drow[varnr] < Extrad)
	    Extrad = drow[varnr];
	}
      artif = Extrad < -Epsd;
    }
  else /* primal */
    {
      artif = FALSE;
      Extrad = 0;
    }
  if (Verbose)
    printf("artificial:%12.5f\n", (double)Extrad);
  minit = FALSE;
  do {
    doiter = FALSE;
    doinvert = FALSE;
    if (primal)
      {
	rownr = 0;
	if (colprim(&colnr, numeta, minit, drow))
	  {
	    setpivcol(Lower[colnr], colnr, numeta, Pcol);
	    if (rowprim(&rownr, &theta, Pcol))
	      {
		doiter = TRUE;
		condensecol(rownr, numeta, Pcol);
	      }
	  }
      }
    else /* not primal */
      {
	if (!minit)
	  rowdual(&rownr);
	if (!doinvert)
	  if (rownr > 0)
	    {
	      if (coldual(numeta, rownr, &colnr, minit, prow, drow))
		{
		  doiter = TRUE;
		  setpivcol(Lower[colnr], colnr, numeta, Pcol);
		  condensecol(rownr, numeta, Pcol);
		  f = Rhs[rownr] - Upbo[Bas[rownr]];
		  if (f > 0)
		    {
		      theta = f / (REAL) Pcol[rownr];
		      if (theta <= Upbo[colnr])
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
	    if (artif)
	      {
		primal = TRUE;
		artif = FALSE;
		if(Verbose)
		  printf("primal\n");
		doinvert = TRUE;
		Extrad = 0;
	      }
	    else /* not artif */
	      colnr = 0;
      }
    if (doiter)
      iteration(&numeta, rownr, colnr, &theta, Upbo[colnr],
		&minit, &Lower[colnr], primal, smotes, &iter, &numinv);
    if (numinv >= invnum)
      doinvert = TRUE;
    if (doinvert)
      invert(Columns, &numeta, &numinv);
  } while (rownr && colnr || doinvert);

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


static void construct_solution(REAL   *sol)
{
  int    i, j, basi;
  REAL   f;

  /* zero all results of rows */
  memset(sol, '\0', (Rows + 1) * sizeof(REAL));

  for (i = Rows + 1; i <= Sum; i++)
    sol[i] = Lowbo[i];
  for (i = 1; i <= Rows; i++)
    {
      basi = Bas[i];
      if (basi > Rows)
	sol[basi] += Rhs[i];
    }
  for (i = Rows + 1; i <= Sum; i++)
    if (!Basis[i] && !Lower[i])
      sol[i] += Upbo[i];
  for (j = 1; j <= Columns; j++)
    {
      f = sol[Rows + j];
      if (f != 0)
	for (i = Cend[j - 1]; i < Cend[j]; i++)
	  sol[Mat[i].rownr] += f * Mat[i].value;
    }
  
  for (i = 0; i <= Rows; i++)
    {
      if (abs(sol[i]) < Epsb)
	sol[i] = 0;
      else
	if (Chsign[i])
	  sol[i] = -sol[i];
    }
} /* construct_solution */


static short is_int(REAL   value)
{
  REAL   tmp;

  tmp = value - floor(value);
  if(tmp < Epsilon)
    return(1);
  if((tmp > 0.5) && ((1.0 - tmp) < Epsilon))
    return(1);
  return(0);
} /* is_int */


int solve(REAL   *upbo,
	  REAL   *lowbo)
{
  int    i, failure, notint, is_worse;
  intrec *ptr;

  Level++;
  debug_print("starting solve");

  /* make fresh copies of Mat, Rh, Upbo, Lowbo, as solving changes them */
  memcpy(Mat,   Orig_mat, (Nonnuls + 1) * sizeof(matrec));
  memcpy(Rh,    Orig_rh,  (Rows + 2)    * sizeof(REAL));
  memcpy(Upbo,  upbo,     (Sum + 2)     * sizeof(REAL));
  memcpy(Lowbo, lowbo,    (Sum + 2)     * sizeof(REAL));

  Rend[0] = 0;
  presolve();

  for (i = 0; i <= Rows; i++)
    Rhs[i] = Rh[i];

  Endetacol[0] = 0;
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
	  REAL   *new_upbo, *new_lowbo;
	  REAL   new_bound;
	  int    res1, res2;

	  /* allocate room for them */
	  MALLOC(new_upbo,  Sum + 2, REAL);
	  MALLOC(new_lowbo, Sum + 2, REAL);

	  memcpy(new_upbo,  upbo,  (Sum + 2) * sizeof(REAL));
	  memcpy(new_lowbo, lowbo, (Sum + 2) * sizeof(REAL));

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
	      
		  debug_print("starting first subproblem with bounds:");
		  debug_print_bounds(new_upbo, lowbo);
		  
		  res1 = solve(new_upbo, lowbo);
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
		  
		  debug_print("starting second subproblem with bounds:");
		  debug_print_bounds(upbo, new_lowbo);
	      
		  res2 = solve(upbo, new_lowbo);
		}
	    }
	  else /* take ceiling first */
	    {
	      new_bound = ceil(Solution[notint]);
	      if(new_bound > upbo[notint])
		{
		  debug_print("New lower bound value %g conflicts with old upper bound %g\n", (double)new_bound, (double)upbo[notint]);
		  res1 = MILP_FAIL;
		}
	      else /* bound feasible */
		{
		  new_lowbo[notint] = new_bound;
		  
		  debug_print("starting first subproblem with bounds:");
		  debug_print_bounds(upbo, new_lowbo);
	      
		  res1 = solve(upbo, new_lowbo);
		}
	      
	      new_bound -= 1;
	      if(new_bound < lowbo[notint])
		{
		  debug_print("New upper bound value %g conflicts with old lower bound %g\n", (double)new_bound, (double)lowbo[notint]);
		  res2 = MILP_FAIL;
		}
	      else /* bound feasible */
		{
		  new_upbo[notint] = new_bound;
		  
		  debug_print("starting second subproblem with bounds:");
		  debug_print_bounds(new_upbo, lowbo);
		  
		  res2 = solve(new_upbo, lowbo);
		}
	    }

	  if(res1 && res2) /* both failed. They must have been infeasible */
	    failure = INFEASIBLE;
	  else
	    failure = OPTIMAL;

	  free(new_upbo);
	  free(new_lowbo);
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
	      if(Show_results)
		{
		  fprintf(stderr, "Intermediate solution:\n");
		  print_solution(stderr, Best_solution);
		}
	    }
	}
    }
  Level--;

  /* failure can have the values OPTIMAL, UNBOUNDED and INFEASIBLE. */
  return(failure);
} /* solve */
