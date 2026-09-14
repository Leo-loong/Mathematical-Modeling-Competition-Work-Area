#include "defines.h"
#include "globals.h"


void ftran(int start,
	   int end,
	   REAL *pcol)
{
  int  i, j, k, r;
  REAL theta;

  if (Verbose)
    printf("ftran\n");
  for (i = start; i <= end; i++)
    {
      k = Endetacol[i] - 1;
      r = Eta_rownr[k];
      theta = pcol[r];
      if (theta != 0)
	for (j = Endetacol[i - 1]; j < k; j++)
	  pcol[Eta_rownr[j]] += theta * Eta_value[j]; /* cpu expensive line */
      pcol[r] *= Eta_value[k];
    }
  /* round small values to zero */
  for (i = 0; i <= Rows; i++)
    if (my_abs(pcol[i]) < Epsel)
      pcol[i] = 0;
} /* ftran */

void btran(int numc,
	   REAL *row)
{
  int  i, j, k;
  REAL f;

  if (Verbose)
    printf("btran\n");
  for (i = numc; i >= 1; i--)
    {
      f = 0;
      k = Endetacol[i] - 1;
      for (j = Endetacol[i - 1]; j <= k; j++)
	f += row[Eta_rownr[j]] * Eta_value[j];
      if (my_abs(f) < Epsel)
	row[Eta_rownr[k]] = 0;
      else
	row[Eta_rownr[k]] = f;
    }
} /* btran */
