#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include "patchlevel.h"

/* defines */

#define CALLOC(ptr, nr, type) if(!(ptr = calloc((size_t)(nr),\
  sizeof(type)))) { fprintf(stderr, "calloc failed\n"); exit(1); }

#define DOLIST(ptr, init) for((ptr) = (init); (ptr); (ptr) = (ptr)->next)

#define HASHSIZE 10009 /* prime! */
#define NAMELEN  11

#define FALSE 0
#define TRUE  1

#define VARNAME    0
#define CONSTRNAME 1

#define LE 0
#define EQ 1
#define GE 2
#define OF 3

#define NAME    -1
#define ROWS    0
#define COLUMNS 1
#define RHS     2
#define BOUNDS  3
#define RANGES  4

/* typedefs */

typedef struct _hashentry
{
  struct _hashentry  *next;
  char                name[NAMELEN];
  short               type;
  short               is_int;
  struct _constraint *constr;
} hashentry;

typedef struct _constraint
{
  struct _constraint *next;
  struct _term       *lhs;
  double              rhs;
  short               relat;
  short               has_range;
  double              range_val;
  hashentry          *hash;
} constraint;

typedef struct _term
{
  struct _term *next;
  double        coef;
  hashentry     *hash;
} term;

/* globale vars */

hashentry  *Hashtab[HASHSIZE];
constraint *First_constraint, *Objective_function;
int         Debug, Having_ints, Lineno;
term       *First_upbo, *First_lowbo;

/* hash functions */

int hashval(char *string)
{
  unsigned int result = 0;

  while(*string != '\0')
    {
      result <<= 1;
      result += *string++;
    }
  return(result % HASHSIZE);
} /* hashval */


hashentry *gethash(char *name)
{
  hashentry *hp;

  DOLIST(hp, Hashtab[hashval(name)])
    if(strcmp(hp->name, name) == 0)
      return(hp);
  return(NULL);
} /* gethash */


hashentry *puthash(char *name)
{
  int index;
  hashentry *hp;

  if(!(hp = gethash(name)))
    {
      index = hashval(name);
      CALLOC(hp, 1, hashentry);
      hp->next = Hashtab[index];
      Hashtab[index] = hp;
      strcpy(hp->name, name);
    }
  return(hp);
} /* puthash */


/*
A:  MPS format was named after an early IBM LP product and has emerged
as a de facto standard ASCII medium among most of the commercial LP
codes.  Essentially all commercial LP codes accept this format, but if
you are using public domain software and have MPS files, you may need
to write your own reader routine for this.  It's not too hard.  The
main things to know about MPS format are that it is column oriented (as
opposed to entering the model as equations), and everything (variables,
rows, etc.) gets a name.  MPS format is described in more detail in
Murtagh's book, referenced in another section.

MPS is an old format, so it is set up as though you were using punch
cards, and is not free format. Fields start in column 1, 5, 15, 25, 40
and 50.  Sections of an MPS file are marked by so-called header cards,
which are distinguished by their starting in column 1.  Although it is
typical to use upper-case throughout the file (like I said, MPS has
long historical roots), many MPS-readers will accept mixed-case for
anything except the header cards, and some allow mixed-case anywhere.
The names that you choose for the individual entities (constraints or
variables) are not important to the solver; you should pick names that
are meaningful to you, or will be easy for a post-processing code to
read.

Here is a little sample model written in MPS format (explained in more
detail below):

NAME          TESTPROB
ROWS
 N  COST
 L  LIM1
 G  LIM2
 E  MYEQN
COLUMNS
    XONE      COST                 1   LIM1                 1
    XONE      LIM2                 1
    YTWO      COST                 4   LIM1                 1
    YTWO      MYEQN               -1
    ZTHREE    COST                 9   LIM2                 1
    ZTHREE    MYEQN                1
RHS
    RHS1      LIM1                 5   LIM2                10
    RHS1      MYEQN                7
BOUNDS
 UP BND1      XONE                 4
 LO BND1      YTWO                -1
 UP BND1      YTWO                 1
ENDATA

means:

Optimize
 COST:    XONE + 4 YTWO + 9 ZTHREE
Subject To
 LIM1:    XONE + YTWO <= 5
 LIM2:    XONE + ZTHREE >= 10
 MYEQN:   - YTWO + ZTHREE  = 7
Bounds
 0 <= XONE <= 4
-1 <= YTWO <= 1
End


*/

int scan_line(char* line, char *field1, char *field2, char *field3,
	      double *field4, char *field5, double *field6)
{
  int items = 0, line_len;
  char buf[15];

  line_len = strlen(line);
  
  if(line_len >= 1)
    {
      strncpy(buf, line, 4);
      sscanf(buf, "%s", field1);
      items++;
    }
  else
    field1[0] = '\0';
  line += 4;

  if(line_len >= 5)
    {
      strncpy(buf, line, 10);
      sscanf(buf, "%s", field2);
      items++;
    }
  else
    field2[0] = '\0';
  line += 10;

  if(line_len >= 14)
    {
      strncpy(buf, line, 10);
      sscanf(buf, "%s", field3);
      items++;
    }
  else
    field3[0] = '\0';
  line += 10;

  if(line_len >= 25)
    {
      strncpy(buf, line, 15);
      sscanf(buf, "%lf", field4);
      items++;
    }
  else
    *field4 = 0;
  line += 15;

  if(line_len >= 40)
    {
      strncpy(buf, line, 10);
      sscanf(buf, "%s", field5);
      items++;
    }
  else
    field5[0] = '\0';
  line += 10;

  if(line_len >= 50)
    {
      strncpy(buf, line, 15);
      sscanf(buf, "%lf", field6);
      items++;
    }
  else
    *field6 = 0;
    
  return(items);
}

void varprint(char *name, int type)
{
  if(isalpha(name[0]))
    printf("%s ", name);
  else /* does not start with letter */
    if(type == VARNAME)
      printf("v%s ", name);
    else /* must be constraint name */
      printf("c%s ", name);
}

void write_output(char *probname)
{
  constraint *cp;
  term       *tp;

  /* print title and OF */

  printf("/* MPS name: %s */\n\n/* objective function: */\nmin: ", probname);

  DOLIST(tp, Objective_function->lhs)
    {
      printf("+ %lg ", tp->coef);
      varprint(tp->hash->name, VARNAME);
    }
  printf(";\n\n/* constraints */\n");

  /* print constraints */

  DOLIST(cp, First_constraint)
    {
      if(!cp->lhs)
	{
	  fprintf(stderr, "Warning, empty constraint %s, skipping\n",
		  cp->hash->name);
	  continue;
	}
      
      varprint(cp->hash->name, CONSTRNAME);
      printf(": ");

      DOLIST(tp, cp->lhs)
	{
	  printf("+ %lg ", tp->coef);
	  varprint(tp->hash->name, VARNAME);
	}

      switch(cp->relat) {
      case LE:
	printf("<= ");
	break;
      case GE:
	printf(">= ");
	break;
      case EQ:
	/* is this correct ? */
	if(cp->has_range)
	  if(cp->range_val > 0)
	    printf(">= ");
	  else /* negative range value */
	    printf("<= ");
	else /* no range */
	  printf("= ");
	break;
      default:
	fprintf(stderr, "Unknown relat %d\n", cp->relat);
	break;
      }

      printf("%lg;\n", cp->rhs);

      /* handle RANGES */
      if(cp->has_range)
	{
	  /* I don't know what constraint name to set, so I don't */

	  DOLIST(tp, cp->lhs)
	    {
	      printf("+ %lg ", tp->coef);
	      varprint(tp->hash->name, VARNAME);
	    }

	  switch(cp->relat) {
	  case LE:
	    printf(">= ");
	    printf("%lg;\n", cp->rhs - cp->range_val);
	    break;
	  case GE:
	    printf("<= ");
	    printf("%lg;\n", cp->rhs + cp->range_val);
	    break;
	  case EQ:
	    if(cp->range_val > 0)
	      {
		printf("<= ");
		printf("%lg;\n", cp->rhs + cp->range_val);
	      }
	    else
	      {
		printf(">= ");
		printf("%lg;\n", cp->rhs + cp->range_val);
	      }
	    break;
	  default:
	    fprintf(stderr, "Unknown relat %d\n", cp->relat);
	    break;
	  }
	}
    }
  
  /* print bounds */
  if(First_lowbo || First_upbo)
    printf("\n/* Bounds: */\n");

  DOLIST(tp, First_upbo)
    {
      varprint(tp->hash->name, VARNAME);
      printf("<= %lg;\n", tp->coef);
    }

  DOLIST(tp, First_lowbo)
    {
      varprint(tp->hash->name, VARNAME);
      printf(">= %lg;\n", tp->coef);
    }

  /* print integer declarations */
  if(Having_ints)
    {
      hashentry *hp;
      int        i;

      printf("\nint ");

      for(i = 0; i < HASHSIZE; i++)
	DOLIST(hp, Hashtab[i])
	  if(hp->is_int)
	    varprint(hp->name, VARNAME);

      printf(";\n");
    }
}

hashentry *lookup_constraint_name(char *name)
{
  hashentry *hp;

  if(!(hp = gethash(name)) || !(hp->type == CONSTRNAME))
    {
      fprintf(stderr, "Unknown row name (%s) on line %d\n", name, Lineno);
      exit(1);
    }

  return(hp);
}

main(int argc, char *argv[])
{
  char field1[5], field2[10], field3[10], field5[10], line[80], tmp[15];
  char probname[25];
  double field4, field6;
  int items, section, i, int_section = FALSE;
  hashentry  *hp, *hp2;
  constraint *cp;
  term       *tp;
  
  Debug = FALSE;

  for(i = 1; i < argc; i++)
    {
      if(strcmp(argv[i], "-d") == 0)
	Debug = TRUE;
      else if(strcmp(argv[i], "-h") == 0)
	{
	  printf("This is %s patchlevel %s\n", argv[0], PATCHLEVEL);
	  printf("Usage: %s [-d] \"<\" <mps_file> \">\" <equations_file>\n",
		 argv[0]);
	  printf("-d: debug mode, print debug information during processing\n");
	  exit(0);
	}
      else
	fprintf(stderr, "Unknown command line option %s, ignored\n", argv[i]);
    }

  while(gets(line))
    {
      Lineno++;

      /* skip lines which start with "*", they are comment */
      if(line[0] == '*')
	{
	  if(Debug)
	    fprintf(stderr, "Comment: %s\n", line);
	}
      /* first check for "special" lines: NAME, ROWS, BOUNDS .... */
      /* this must start in the first position of line */
      else if(line[0] != ' ')
	{
	  sscanf(line, "%s", tmp);
	  if(strcmp(tmp, "NAME") == 0)
	    {
	      section = NAME;
	      sscanf(line, "NAME %s", probname);
	    }
	  else if(strcmp(tmp, "ROWS") == 0)
	    {
	      section = ROWS;
	      if(Debug)
		fprintf(stderr, "Switching to ROWS section\n");
	    }
	  else if(strcmp(tmp, "COLUMNS") == 0)
	    {
	      section = COLUMNS;
	      if(Debug)
		fprintf(stderr, "Switching to COLUMNS section\n");
	    }
	  else if(strcmp(tmp, "RHS") == 0)
	    {
	      section = RHS;
	      if(Debug)
		fprintf(stderr, "Switching to RHS section\n");
	    }
	  else if(strcmp(tmp, "BOUNDS") == 0)
	    {
	      section = BOUNDS;
	      if(Debug)
		fprintf(stderr, "Switching to BOUNDS section\n");
	    }
	  else if(strcmp(tmp, "RANGES") == 0)
	    {
	      section = RANGES;
	      if(Debug)
		fprintf(stderr, "Switching to RANGES section\n");
	    }
	  else if(strcmp(tmp, "ENDATA") == 0)
	    write_output(probname);
	  else /* line does not start with space and does not match above */
	    {
	      fprintf(stderr, "Unrecognized line: %s\n", line);
	      exit(1);
	    }
	}
      else /* normal line, process */
	{
	  items = scan_line(line, field1, field2, field3, &field4, field5,
			    &field6);

	  switch(section) {

	  case NAME:
	    fprintf(stderr, "Error, extra line under NAME line\n");
	    exit(1);
	    break;

	  case ROWS:
	    /* field1: rel. operator; field2: name of constraint */

	    if(Debug)
	      {
		fprintf(stderr, "Rows line: ");
		fprintf(stderr, "%s %s\n", field1, field2);
	      }

	    hp = puthash(field2);
	    hp->type = CONSTRNAME;
	    cp = First_constraint;
	    CALLOC(First_constraint, 1, constraint);
	    hp->constr = First_constraint;
	    First_constraint->next = cp;
	    First_constraint->hash = hp;
	    if(strcmp(field1, "N") == 0)
	      {
		First_constraint->relat = OF;
		/* found objective function! */
		Objective_function = First_constraint;
		/* unhook it */
		First_constraint = First_constraint->next;
	      }
	    else if(strcmp(field1, "L") == 0)
	      First_constraint->relat = LE;
	    else if(strcmp(field1, "G") == 0)
	      First_constraint->relat = GE;
	    else if(strcmp(field1, "E") == 0)
	      First_constraint->relat = EQ;
	    else
	      {
		fprintf(stderr, "Unknown relat '%s' on line %d\n", field1,
			Lineno);
		exit(1);
	      }
	    break;

	  case COLUMNS:
	    /* field2: variable; field3: constraint; field4: coef */
	    /* optional: field5: constraint; field6: coef */

	    if(Debug)
	      {
		fprintf(stderr, "Columns line: ");
		fprintf(stderr, "%s %s %lg %s %lg\n", field2, field3,
			field4, field5, field6);
	      }

	    if((items == 4) || (items == 6))
	      {
		hp = puthash(field2);

		if(int_section)
		  hp->is_int = TRUE;

		hp2 = lookup_constraint_name(field3);
		cp = hp2->constr;
		tp = cp->lhs;
		CALLOC(cp->lhs, 1, term);
		cp->lhs->next = tp;
		tp = cp->lhs;
		tp->hash = hp;
		tp->coef = field4;
	      }

	    if(items == 6)
	      {
		hp2 = lookup_constraint_name(field5);
		cp = hp2->constr;
		tp = cp->lhs;
		CALLOC(cp->lhs, 1, term);
		cp->lhs->next = tp;
		tp = cp->lhs;
		tp->hash = hp;
		tp->coef = field6;
	      }

	    if(items == 5) /* there might be an INTEND or INTORG marker */
	      /* look for "    <name>  'MARKER'                 'INTORG'" */
	      /* or "    <name>  'MARKER'                 'INTEND'" */
	      {    
		if(strcmp(field3, "'MARKER'") ==0)
		  {
		    if(strcmp(field5, "'INTORG'") == 0)
		      {
			int_section = TRUE;
			Having_ints = TRUE;
			if(Debug)
			  fprintf(stderr, "Switching to integer section\n");
		      }
		    else if(strcmp(field5, "'INTEND'") == 0)
		      {
			int_section = FALSE;
			if(Debug)
			  fprintf(stderr, "Switching to non-integer section\n");
		      }
		    else
		      fprintf(stderr, "Unknown marker (ignored) at line %d: %s\n",
			      Lineno, field5);
		  }
	      }

	    if((items != 4) && (items != 6) && (items != 5)) /* Wrong! */
	      {
		fprintf(stderr,
			"Wrong number of items (%d) in COLUMNS section (line %d)\n",
			items, Lineno);
		exit(1);
	      }
	    break;

	  case RHS:
	    /* field2: uninteresting name; field3: constraint name */
	    /* field4: value */
	    /* optional: field5: constraint name; field6: value */

	    if(Debug)
	      {
		fprintf(stderr, "RHS line: ");
		fprintf(stderr, "%s %s %lg %s %lg\n", field2, field3,
			field4, field5, field6);
	      }

	    if((items != 4) && (items != 6))
	      {
		fprintf(stderr,
			"Wrong number of items (%d) in RHS section line %d\n",
			items, Lineno);
		exit(1);
	      }

	    hp = lookup_constraint_name(field3);
	    hp->constr->rhs = field4;

	    if(items == 6)
	      {
		hp = lookup_constraint_name(field5);
		hp->constr->rhs = field6;
	      }

	    break;

	  case BOUNDS:
	    /* field1: bound type; field2: uninteresting name; */
	    /* field3: variable name; field4: value */

	    if(Debug)
	      {
		fprintf(stderr, "BOUNDS line: %s %s %s %lg\n", field1, field2,
			field3, field4);
	      }

	    if(!(hp = gethash(field3))) /* unknown variable, skip */
	      fprintf(stderr,
		      "Warning: bound for unknown variable %s on line %d (ignored)\n",
		      field3, Lineno);
	    else /* variable known */
	      {
		CALLOC(tp, 1, term);
		tp->coef = field4;
		tp->hash = hp;

		if(strcmp(field1, "UP") == 0)
		  /* upper bound */
		  {
		    tp->next = First_upbo;
		    First_upbo = tp;
		  }
		else if(strcmp(field1, "LO") == 0)
		  /* lower bound */
		  {
		    tp->next = First_lowbo;
		    First_lowbo = tp;
		  }
		else if(strcmp(field1, "FX") == 0)
		  /* fixed, upper _and_ lower  */
		  {
		    tp->next = First_lowbo;
		    First_lowbo = tp;
		    CALLOC(tp, 1, term);
		    tp->hash = hp;
		    tp->coef = field4;
		    tp->next = First_upbo;
		    First_upbo = tp;
		  }
		else if(strcmp(field1, "PL") == 0)
		  /* normal, 0 <= var <= inf, do nothing */;
		else if(strcmp(field1, "BV") == 0) /* binary variable */
		  {
		    Having_ints = TRUE;
		    /* set upper bound of 1 */
		    tp->coef = 1;
		    tp->next = First_upbo;
		    First_upbo = tp;
		    /* variable is integer */
		    hp->is_int = TRUE;
		  }
		else
		  {
		    fprintf(stderr, "BOUND type %s on line %d is not supported\n",
			    field1, Lineno);
		    exit(1);
		  }
	      }
	    break;

	  case RANGES:
	    /* field2: uninteresting name; field3: constraint name */
	    /* field4: value */
	    /* optional: field5: constraint name; field6: value */

	    if(Debug)
	      {
		fprintf(stderr, "RANGES line: ");
		fprintf(stderr, "%s %s %lg %s %lg\n", field2, field3,
			field4, field5, field6);
	      }

	    if((items != 4) && (items != 6))
	      {
		fprintf(stderr,
			"Wrong number of items (%d) in RANGES section line %d\n",
			items, Lineno);
		exit(1);
	      }

	    hp = lookup_constraint_name(field3);
	    hp->constr->range_val = field4;
	    hp->constr->has_range = TRUE;

	    if(items == 6)
	      {
		hp = lookup_constraint_name(field5);
		hp->constr->range_val = field6;
		hp->constr->has_range = TRUE;
	      }
	    break;
	  }
	}
    }
  exit(0);
}
