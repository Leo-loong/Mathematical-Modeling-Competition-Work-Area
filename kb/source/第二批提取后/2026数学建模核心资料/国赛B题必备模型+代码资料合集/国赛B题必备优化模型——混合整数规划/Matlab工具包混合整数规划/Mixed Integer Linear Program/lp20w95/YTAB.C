/* c:\mks\bin\yacce lp.y */
#define VAR	257
#define CONS	258
#define SIGN	259
#define AR_M_OP	260
#define RE_OP	261
#define END_C	262
#define COMMA	263
#define COLON	264
#define MINIMISE	265
#define MAXIMISE	266
#ifdef YYTRACE
#define YYDEBUG 1
#else
#ifndef YYDEBUG
#define YYDEBUG 0
#endif
#endif
/*
 * Portable way of defining ANSI C prototypes
 */
#ifndef YY_ARGS
#if __STDC__
#define YY_ARGS(args)	args
#else
#define YY_ARGS(args)	()
#endif
#endif

void yyerror(char *fmt, ...);

#ifdef YACC_WINDOWS

#include <windows.h>

/*
 * the following is the handle to the current
 * instance of a windows program. The user
 * program calling yyparse must supply this!
 */

extern HANDLE hInst;	

#endif	/* YACC_WINDOWS */

#if YYDEBUG
typedef struct yyNamedType_tag {	/* Tokens */
	char	* name;		/* printable name */
	short	token;		/* token # */
	short	type;		/* token type */
} yyNamedType;
typedef struct yyTypedRules_tag {	/* Typed rule table */
	char	* name;		/* compressed rule string */
	short	type;		/* rule result type */
} yyTypedRules;

#endif

#line 9 "lp.y"

#include "lpkit.h" 
#include "lpglob.h"
#include "read.h"

/* globals */
char Last_var[NAMELEN];
char Constraint_name[NAMELEN];
int Lin_term_count;
REAL f;
int x;
int Sign;
int isign; 	/* internal_sign variable to make sure nothing goes wrong */
		/* with lookahead */
int make_neg;	/* is true after the relational operator is seen in order */
		/* to remember if lin_term stands before or after re_op */
extern int yychar, yyerrflag;
#ifndef YYSTYPE
#define YYSTYPE int
#endif
extern YYSTYPE yylval;
#if YYDEBUG
yyTypedRules yyRules[] = {
	{ "&00: %01 &00",  0},
	{ "%02:",  0},
	{ "%01: %02 %03 %04 %05",  0},
	{ "%04: %06",  0},
	{ "%04: %04 %06",  0},
	{ "%06: %07",  0},
	{ "%08:",  0},
	{ "%06: &02 &09 %08 %07",  0},
	{ "%10:",  0},
	{ "%07: %09 &06 %10 %09 &07",  0},
	{ "%05:",  0},
	{ "%05: %11",  0},
	{ "%11: %12",  0},
	{ "%11: %11 %12",  0},
	{ "%12: %13 %14 &07",  0},
	{ "%13: &02",  0},
	{ "%14: &02",  0},
	{ "%14: %14 &02",  0},
	{ "%14: %14 &08 &02",  0},
	{ "%09: %15",  0},
	{ "%16:",  0},
	{ "%09: &04 %16 %15",  0},
	{ "%17:",  0},
	{ "%09: %09 &04 %17 %15",  0},
	{ "%15: %18",  0},
	{ "%15: &03",  0},
	{ "%19: %18",  0},
	{ "%20:",  0},
	{ "%19: &04 %20 %18",  0},
	{ "%21:",  0},
	{ "%19: %19 &04 %21 %18",  0},
	{ "%18: &02",  0},
	{ "%18: &03 &02",  0},
	{ "%18: &03 &05 &02",  0},
	{ "%03: &11 %22",  0},
	{ "%03: &10 %22",  0},
	{ "%03: %22",  0},
	{ "%22: %19 &07",  0},
{ "$accept",  0},{ "error",  0}
};
yyNamedType yyTokenTypes[] = {
	{ "$end",  0,  0},
	{ "error",  256,  0},
	{ "VAR",  257,  0},
	{ "CONS",  258,  0},
	{ "SIGN",  259,  0},
	{ "AR_M_OP",  260,  0},
	{ "RE_OP",  261,  0},
	{ "END_C",  262,  0},
	{ "COMMA",  263,  0},
	{ "COLON",  264,  0},
	{ "MINIMISE",  265,  0},
	{ "MAXIMISE",  266,  0}

};
#endif
static short yydef[] = {

	  -1,    3,    9,   -5,   38,   -9
};
static short yyex[] = {

	   0,    0,   -1,    1,    0,   39,   -1,    1,  257,   17, 
	 259,    9,  261,    9,   -1,    1
};
static short yyact[] = {

	 -30,  -21,  -32,  -23,  -22,  266,  265,  259,  258,  257, 
	 -30,  -21,  -32,  259,  258,  257,  -29,  -18,  260,  257, 
	 -31,  -25,  262,  259,   -3,   -2,  -34,  259,  258,  257, 
	 -28,  257,  -30,  -21,  258,  257,  -33,  -40,  261,  259, 
	 -41,  264,   -6,   -2,  -34,  259,  258,  257,  -30,   -2, 
	 258,  257,  -37,  257,  -38,  257,  -30,   -2,  -34,  259, 
	 258,  257,  -36,  -50,   -7,  263,  262,  257,  -33,  -39, 
	 262,  259,  -35,  257,   -1
};
static short yypact[] = {

	  10,   18,   41,   45,   55,   41,   73,   70,   65,   59, 
	  59,   50,   53,   50,   34,   38,   34,   31,   27,   22, 
	  18,   13,   13,    5
};
static short yygo[] = {

	  -1,  -24,  -19,   -4,  -43,  -45,  -44,    3,  -47,  -46, 
	   9,  -10,   -8,  -16,   10,  -11,   -5,  -49,  -48,    4, 
	 -13,   -9,  -53,  -52,  -51,   13,   11,  -14,  -12,  -57, 
	 -56,  -55,  -55,  -55,  -54,   23,   22,   21,   16,   14, 
	 -20,  -17,  -15,  -27,  -26,  -58,   22,   21,   -1
};
static short yypgo[] = {

	   0,    0,    0,   24,   45,    2,    2,   34,   34,   34, 
	  42,   41,   28,   27,   21,   21,   21,   20,    9,   15, 
	  11,    1,    0,    3,    3,    6,    6,   16,   16,   18, 
	  13,   13,   13,   24,   40,   40,   40,    2,    4,    4,    0
};
static short yyrlen[] = {

	   0,    0,    0,    1,    2,    2,    2,    3,    2,    1, 
	   0,    0,    0,    0,    3,    2,    1,    1,    5,    0, 
	   0,    0,    4,    1,    2,    1,    4,    1,    2,    3, 
	   1,    3,    4,    1,    1,    3,    4,    1,    1,    0,    2
};
#define YYS0	41
#define YYDELTA	20
#define YYNPACT	24
#define YYNDEF	6

#define YYr38	0
#define YYr39	1
#define YYr40	2
#define YYr25	3
#define YYr37	4
#define YYr35	5
#define YYr34	6
#define YYr33	7
#define YYr32	8
#define YYr31	9
#define YYr29	10
#define YYr27	11
#define YYr22	12
#define YYr20	13
#define YYr18	14
#define YYr17	15
#define YYr16	16
#define YYr15	17
#define YYr9	18
#define YYr8	19
#define YYr6	20
#define YYr1	21
#define YYrACCEPT	YYr38
#define YYrERROR	YYr39
#define YYrLR2	YYr40
#if YYDEBUG
char * yysvar[] = {
	"$accept",
	"inputfile",
	"$1",
	"objective_function",
	"constraints",
	"int_declarations",
	"constraint",
	"real_constraint",
	"$6",
	"x_lineair_sum",
	"$8",
	"real_int_decls",
	"int_declaration",
	"int_declarator",
	"vars",
	"x_lineair_term",
	"$20",
	"$22",
	"lineair_term",
	"lineair_sum",
	"$27",
	"$29",
	"real_of",
	0
};
short yyrmap[] = {

	  38,   39,   40,   25,   37,   35,   34,   33,   32,   31, 
	  29,   27,   22,   20,   18,   17,   16,   15,    9,    8, 
	   6,    1,    2,    3,    4,    5,    7,   12,   13,   14, 
	  19,   21,   23,   24,   26,   28,   30,   36,   11,   10,    0
};
short yysmap[] = {

	   2,   19,   24,   27,   37,   38,   53,   51,   47,   45, 
	  44,   43,   35,   31,   29,   23,   18,   14,   11,    8, 
	   6,    5,    4,    1,   16,   12,   13,   28,   15,    7, 
	  17,    9,   32,   21,   57,   54,   46,   48,   56,   33, 
	  34,    0,   40,   26,   39,   25,   52,   36,   49,   55, 
	  22,   42,   50,   20,   10,   30,   41,    3
};
int yyntoken = 12;
int yynvar = 23;
int yynstate = 58;
int yynrule = 41;
#endif

#if YYDEBUG
/*
 * Package up YACC context for tracing
 */
typedef struct yyTraceItems_tag {
	int	state, lookahead, errflag, done;
	int	rule, npop;
	short	* states;
	int	nstates;
	YYSTYPE * values;
	int	nvalues;
	short	* types;
} yyTraceItems;
#endif

#line 2 "c:/mks/etc/yyparse.c"

/*
 * Copyright 1985, 1990 by Mortice Kern Systems Inc.  All rights reserved.
 * 
 * Automaton to interpret LALR(1) tables.
 *
 * Macros:
 *	yyclearin - clear the lookahead token.
 *	yyerrok - forgive a pending error
 *	YYERROR - simulate an error
 *	YYACCEPT - halt and return 0
 *	YYABORT - halt and return 1
 *	YYRETURN(value) - halt and return value.  You should use this
 *		instead of return(value).
 *	YYREAD - ensure yychar contains a lookahead token by reading
 *		one if it does not.  See also YYSYNC.
 *	YYRECOVERING - 1 if syntax error detected and not recovered
 *		yet; otherwise, 0.
 *
 * Preprocessor flags:
 *	YYDEBUG - includes debug code if 1.  The parser will print
 *		 a travelogue of the parse if this is defined as 1
 *		 and yydebug is non-zero.
 *		yacc -t sets YYDEBUG to 1, but not yydebug.
 *	YYTRACE - turn on YYDEBUG, and undefine default trace functions
 *		so that the interactive functions in 'ytrack.c' will
 *		be used.
 *	YYSSIZE - size of state and value stacks (default 150).
 *	YYSTATIC - By default, the state stack is an automatic array.
 *		If this is defined, the stack will be static.
 *		In either case, the value stack is static.
 *	YYALLOC - Dynamically allocate both the state and value stacks
 *		by calling malloc() and free().
 *	YYDYNAMIC - Dynamically allocate (and reallocate, if necessary)
 *		both the state and value stacks by calling malloc(),
 *		realloc(), and free().
 *	YYSYNC - if defined, yacc guarantees to fetch a lookahead token
 *		before any action, even if it doesnt need it for a decision.
 *		If YYSYNC is defined, YYREAD will never be necessary unless
 *		the user explicitly sets yychar = -1
 *
 * Copyright (c) 1983, by the University of Waterloo
 */
/*
 * Prototypes
 */

extern int yylex YY_ARGS((void));

#if YYDEBUG

#include <stdlib.h>		/* common prototypes */
#include <string.h>

extern char *	yyValue YY_ARGS((YYSTYPE, int));	/* print yylval */
extern void yyShowState YY_ARGS((yyTraceItems *));
extern void yyShowReduce YY_ARGS((yyTraceItems *));
extern void yyShowGoto YY_ARGS((yyTraceItems *));
extern void yyShowShift YY_ARGS((yyTraceItems *));
extern void yyShowErrRecovery YY_ARGS((yyTraceItems *));
extern void yyShowErrDiscard YY_ARGS((yyTraceItems *));

extern void yyShowRead YY_ARGS((int));
#endif

/*
 * If YYDEBUG defined and yydebug set,
 * tracing functions will be called at appropriate times in yyparse()
 * Pass state of YACC parse, as filled into yyTraceItems yyx
 * If yyx.done is set by the tracing function, yyparse() will terminate
 * with a return value of -1
 */
#define YY_TRACE(fn) { \
	yyx.state = yystate; yyx.lookahead = yychar; yyx.errflag =yyerrflag; \
	yyx.states = yys+1; yyx.nstates = yyps-yys; \
	yyx.values = yyv+1; yyx.nvalues = yypv-yyv; \
	yyx.types = yytypev+1; yyx.done = 0; \
	yyx.rule = yyi; yyx.npop = yyj; \
	fn(&yyx); \
	if (yyx.done) YYRETURN(-1); }

#ifndef I18N
#define m_textmsg(id, str, cls)	(str)
#else /*I18N*/
#include <m_nls.h>
#endif/*I18N*/

#ifndef YYSSIZE
# define YYSSIZE	150
#endif

#ifdef YYDYNAMIC
#define YYALLOC
char *getenv();
int atoi();
int yysinc = -1; /* stack size increment, <0 = double, 0 = none, >0 = fixed */
#endif

#ifdef YYALLOC
int yyssize = YYSSIZE;
#endif

#define YYERROR		goto yyerrlabel
#define yyerrok		yyerrflag = 0
#if YYDEBUG
#define yyclearin	{ if (yydebug) yyShowRead(-1); yychar = -1; }
#else
#define yyclearin	yychar = -1
#endif
#define YYACCEPT	YYRETURN(0)
#define YYABORT		YYRETURN(1)
#define YYRECOVERING()	(yyerrflag != 0)
#ifdef YYALLOC
#define YYRETURN(val)	{ retval = (val); goto yyReturn; }
#else
#define YYRETURN(val)	return(val);
#endif
#if YYDEBUG
/* The if..else makes this macro behave exactly like a statement */
# define YYREAD	if (yychar < 0) {					\
			if ((yychar = yylex()) < 0)	{		\
				if (yychar == -2) YYABORT; \
				yychar = 0;				\
			}	/* endif */			\
			if (yydebug)					\
				yyShowRead(yychar);			\
		} else
#else
# define YYREAD	if (yychar < 0) {					\
			if ((yychar = yylex()) < 0) {			\
				if (yychar == -2) YYABORT; \
				yychar = 0;				\
			}	/* endif */			\
		} else
#endif

#define YYERRCODE	256		/* value of `error' */
#define	YYQYYP	yyq[yyq-yyp]

YYSTYPE	yyval;				/* $ */
YYSTYPE	*yypvt;				/* $n */
YYSTYPE	yylval;				/* yylex() sets this */

int	yychar,				/* current token */
	yyerrflag,			/* error flag */
	yynerrs;			/* error count */

#if YYDEBUG
int yydebug = 0;		/* debug if this flag is set */
extern char	*yysvar[];	/* table of non-terminals (aka 'variables') */
extern yyNamedType yyTokenTypes[];	/* table of terminals & their types */
extern short	yyrmap[], yysmap[];	/* map internal rule/states */
extern int	yynstate, yynvar, yyntoken, yynrule;

extern int	yyGetType YY_ARGS((int));	/* token type */
extern char	*yyptok YY_ARGS((int));	/* printable token string */
extern int	yyExpandName YY_ARGS((int, int, char *, int));
				  /* expand yyRules[] or yyStates[] */
static char *	yygetState YY_ARGS((int));

#define yyassert(condition, msg, arg) \
	if (!(condition)) { \
		printf(m_textmsg(2824, "\nyacc bug: ", "E")); \
		printf(msg, arg); \
		YYABORT; }
#else /* !YYDEBUG */
#define yyassert(condition, msg, arg)
#endif

#line 196 "lp.y"
#define yywrap() (1)   /* supply a default yywrap() function */
#include "lex.c"


#ifdef YACC_WINDOWS

/*
 * the following is the yyparse() function that will be
 * callable by a windows type program. It in turn will
 * load all needed resources, obtain pointers to these
 * resources, and call a statically defined function
 * win_yyparse(), which is the original yyparse() fn
 * When win_yyparse() is complete, it will return a
 * value to the new yyparse(), where it will be stored
 * away temporarily, all resources will be freed, and
 * that return value will be given back to the caller
 * yyparse(), as expected.
 */

static int win_yyparse();			/* prototype */

yyparse() 
{
	int wReturnValue;
	HANDLE hRes_table;		/* handle of resource after loading */
	short *old_yydef;		/* the following are used for saving */
	short *old_yyex;		/* the current pointers */
	short *old_yyact;
	short *old_yypact;
	short *old_yygo;
	short *old_yypgo;
	short *old_yyrlen;

	/*
	 * the following code will load the required
	 * resources for a Windows based parser.
	 */

	hRes_table = LoadResource (hInst, 
		FindResource (hInst, "UD_RES_yyYACC", "yyYACCTBL"));
	
	/*
	 * return an error code if any
	 * of the resources did not load
	 */

	if (hRes_table == NULL)
		return (1);
	
	/*
	 * the following code will lock the resources
	 * into fixed memory locations for the parser
	 * (also, save the current pointer values first)
	 */

	old_yydef = yydef;
	old_yyex = yyex;
	old_yyact = yyact;
	old_yypact = yypact;
	old_yygo = yygo;
	old_yypgo = yypgo;
	old_yyrlen = yyrlen;

	yydef = (short *)LockResource (hRes_table);
	yyex = (short *)(yydef + Sizeof_yydef);
	yyact = (short *)(yyex + Sizeof_yyex);
	yypact = (short *)(yyact + Sizeof_yyact);
	yygo = (short *)(yypact + Sizeof_yypact);
	yypgo = (short *)(yygo + Sizeof_yygo);
	yyrlen = (short *)(yypgo + Sizeof_yypgo);

	/*
	 * call the official yyparse() function
	 */

	wReturnValue = win_yyparse();

	/*
	 * unlock the resources
	 */

	UnlockResource (hRes_table);

	/*
	 * and now free the resource
	 */

	FreeResource (hRes_table);

	/*
	 * restore previous pointer values
	 */

	yydef = old_yydef;
	yyex = old_yyex;
	yyact = old_yyact;
	yypact = old_yypact;
	yygo = old_yygo;
	yypgo = old_yypgo;
	yyrlen = old_yyrlen;

	return (wReturnValue);
}	/* end yyparse */

static int win_yyparse() 

#else /* YACC_WINDOWS */

/*
 * we are not compiling a windows resource
 * based parser, so call yyparse() the old
 * standard way.
 */

yyparse() 

#endif /* YACC_WINDOWS */

{
	register short		yyi, *yyp;	/* for table lookup */
	register short		*yyps;		/* top of state stack */
	register short		yystate;	/* current state */
	register YYSTYPE	*yypv;		/* top of value stack */
	register short		*yyq;
	register int		yyj;
#if YYDEBUG
	yyTraceItems	yyx;			/* trace block */
	short	* yytp;
	int	yyruletype = 0;
#endif
#ifdef YYSTATIC
	static short	yys[YYSSIZE + 1];
	static YYSTYPE	yyv[YYSSIZE + 1];
#if YYDEBUG
	static short	yytypev[YYSSIZE+1];	/* type assignments */
#endif
#else /* ! YYSTATIC */
#ifdef YYALLOC
	YYSTYPE *yyv;
	short	*yys;
#if YYDEBUG
	short	*yytypev;
#endif
	YYSTYPE save_yylval;
	YYSTYPE save_yyval;
	YYSTYPE *save_yypvt;
	int save_yychar, save_yyerrflag, save_yynerrs;
	int retval; 			/* return value holder */
#else
	short		yys[YYSSIZE + 1];
	static YYSTYPE	yyv[YYSSIZE + 1];	/* historically static */
#if YYDEBUG
	short	yytypev[YYSSIZE+1];		/* mirror type table */
#endif
#endif /* ! YYALLOC */
#endif /* ! YYSTATIC */
#ifdef YYDYNAMIC
	char *envp;
#endif


#ifdef YYDYNAMIC
	if ((envp = getenv("YYSTACKSIZE")) != (char *)0) {
		yyssize = atoi(envp);
		if (yyssize <= 0)
			yyssize = YYSSIZE;
	}
	if ((envp = getenv("YYSTACKINC")) != (char *)0)
		yysinc = atoi(envp);
#endif
#ifdef YYALLOC
	yys = (short *) malloc((yyssize + 1) * sizeof(short));
	yyv = (YYSTYPE *) malloc((yyssize + 1) * sizeof(YYSTYPE));
#if YYDEBUG
	yytypev = (short *) malloc((yyssize + 1) * sizeof(short));
#endif
	if (yys == (short *)0 || yyv == (YYSTYPE *)0
#if YYDEBUG
		|| yytypev == (short *) 0
#endif
	) {
		yyerror("Not enough space for parser stacks");
		return 1;
	}
	save_yylval = yylval;
	save_yyval = yyval;
	save_yypvt = yypvt;
	save_yychar = yychar;
	save_yyerrflag = yyerrflag;
	save_yynerrs = yynerrs;
#endif

	yynerrs = 0;
	yyerrflag = 0;
	yyclearin;
	yyps = yys;
	yypv = yyv;
	*yyps = yystate = YYS0;		/* start state */
#if YYDEBUG
	yytp = yytypev;
	yyi = yyj = 0;			/* silence compiler warnings */
#endif

yyStack:
	yyassert((unsigned)yystate < yynstate, m_textmsg(587, "state %d\n", ""), yystate);
#ifdef YYDYNAMIC
	if (++yyps > &yys[yyssize]) {
		int yynewsize;
		int yysindex = yyps - yys;
		int yyvindex = yypv - yyv;
#if YYDEBUG
		int yytindex = yytp - yytypev;
#endif
		if (yysinc == 0) {		/* no increment */
			yyerror("Parser stack overflow");
			YYABORT;
		} else if (yysinc < 0)		/* binary-exponential */
			yynewsize = yyssize * 2;
		else				/* fixed increment */
			yynewsize = yyssize + yysinc;
		if (yynewsize < yyssize) {
			yyerror("Not enough space for parser stacks");
			YYABORT;
		}
		yyssize = yynewsize;
		yys = (short *) realloc(yys, (yyssize + 1) * sizeof(short));
		yyps = yys + yysindex;
		yyv = (YYSTYPE *) realloc(yyv, (yyssize + 1) * sizeof(YYSTYPE));
		yypv = yyv + yyvindex;
#if YYDEBUG
		yytypev = (short *)realloc(yytypev,(yyssize + 1)*sizeof(short));
		yytp = yytypev + yytindex;
#endif
		if (yys == (short *)0 || yyv == (YYSTYPE *)0
#if YYDEBUG
			|| yytypev == (short *) 0
#endif
		) {
			yyerror("Not enough space for parser stacks");
			YYABORT;
		}
	}
#else
	if (++yyps > &yys[YYSSIZE]) {
		yyerror("Parser stack overflow");
		YYABORT;
	}
#endif /* !YYDYNAMIC */
	*yyps = yystate;	/* stack current state */
	*++yypv = yyval;	/* ... and value */
#if YYDEBUG
	*++yytp = yyruletype;	/* ... and type */

	if (yydebug)
		YY_TRACE(yyShowState)
#endif

	/*
	 *	Look up next action in action table.
	 */
yyEncore:
#ifdef YYSYNC
	YYREAD;
#endif

#ifdef YACC_WINDOWS
	if (yystate >= Sizeof_yypact) 	/* simple state */
#else /* YACC_WINDOWS */
	if (yystate >= sizeof yypact/sizeof yypact[0]) 	/* simple state */
#endif /* YACC_WINDOWS */
		yyi = yystate - YYDELTA;	/* reduce in any case */
	else {
		if(*(yyp = &yyact[yypact[yystate]]) >= 0) {
			/* Look for a shift on yychar */
#ifndef YYSYNC
			YYREAD;
#endif
			yyq = yyp;
			yyi = yychar;
			while (yyi < *yyp++)
				;
			if (yyi == yyp[-1]) {
				yystate = ~YYQYYP;
#if YYDEBUG
				if (yydebug) {
					yyruletype = yyGetType(yychar);
					YY_TRACE(yyShowShift)
				}
#endif
				yyval = yylval;	/* stack what yylex() set */
				yyclearin;		/* clear token */
				if (yyerrflag)
					yyerrflag--;	/* successful shift */
				goto yyStack;
			}
		}

		/*
	 	 *	Fell through - take default action
	 	 */

#ifdef YACC_WINDOWS
		if (yystate >= Sizeof_yydef)
#else /* YACC_WINDOWS */
		if (yystate >= sizeof yydef /sizeof yydef[0])
#endif /* YACC_WINDOWS */
			goto yyError;
		if ((yyi = yydef[yystate]) < 0)	 { /* default == reduce? */
			/* Search exception table */
#ifdef YACC_WINDOWS
			yyassert((unsigned)~yyi < Sizeof_yyex,
				m_textmsg(2825, "exception %d\n", "I num"), yystate);
#else /* YACC_WINDOWS */
			yyassert((unsigned)~yyi < sizeof yyex/sizeof yyex[0],
				m_textmsg(2825, "exception %d\n", "I num"), yystate);
#endif /* YACC_WINDOWS */
			yyp = &yyex[~yyi];
#ifndef YYSYNC
			YYREAD;
#endif
			while((yyi = *yyp) >= 0 && yyi != yychar)
				yyp += 2;
			yyi = yyp[1];
			yyassert(yyi >= 0,
				 m_textmsg(2826, "Ex table not reduce %d\n", "I num"), yyi);
		}
	}

	yyassert((unsigned)yyi < yynrule, m_textmsg(2827, "reduce %d\n", "I num"), yyi);
	yyj = yyrlen[yyi];
#if YYDEBUG
	if (yydebug)
		YY_TRACE(yyShowReduce)
	yytp -= yyj;
#endif
	yyps -= yyj;		/* pop stacks */
	yypvt = yypv;		/* save top */
	yypv -= yyj;
	yyval = yypv[1];	/* default action $ = $1 */
#if YYDEBUG
	yyruletype = yyRules[yyrmap[yyi]].type;
#endif

	switch (yyi) {		/* perform semantic action */
		
case YYr1: {	/* inputfile :  */
#line 33 "lp.y"

  init_read();
  isign = 0;
  make_neg = 0;
  Sign = 0;

} break;

case YYr6: {	/* constraint :  VAR COLON */
#line 51 "lp.y"

  add_constraint_name(Last_var, Rows);

} break;

case YYr8: {	/* real_constraint :  x_lineair_sum RE_OP */
#line 60 "lp.y"

  store_re_op();
  make_neg = 1; 

} break;

case YYr9: {	/* real_constraint :  x_lineair_sum RE_OP $8 x_lineair_sum END_C */
#line 66 "lp.y"

  if(Lin_term_count == 0)
    {
      fprintf(stderr, "WARNING line %d: constraint contains no variables\n",
	      yylineno);
      null_tmp_store();
    }

  if(Lin_term_count  > 1)
    Rows++;

  if(Lin_term_count == 1)
    store_bounds();

  Lin_term_count = 0;
  isign = 0 ;
  make_neg = 0;
  Constraint_name[0] = '\0';

} break;

case YYr15: {	/* int_declarator :  VAR */
#line 98 "lp.y"

} break;

case YYr16: {	/* vars :  VAR */
#line 101 "lp.y"
add_int_var((char *)yytext);
} break;

case YYr17: {	/* vars :  vars VAR */
#line 102 "lp.y"
add_int_var((char *)yytext);
} break;

case YYr18: {	/* vars :  vars COMMA VAR */
#line 103 "lp.y"
add_int_var((char *)yytext);
} break;

case YYr20: {	/* x_lineair_sum :  SIGN */
#line 108 "lp.y"

  isign = Sign; 

} break;

case YYr22: {	/* x_lineair_sum :  x_lineair_sum SIGN */
#line 114 "lp.y"

  isign = Sign; 

} break;

case YYr25: {	/* x_lineair_term :  CONS */
#line 122 "lp.y"

  if (    (isign || !make_neg)
      && !(isign && !make_neg)) 
    f = -f;
  rhs_store(f);
  isign = 0;

} break;

case YYr27: {	/* lineair_sum :  SIGN */
#line 133 "lp.y"

  isign = Sign;

} break;

case YYr29: {	/* lineair_sum :  lineair_sum SIGN */
#line 139 "lp.y"

  isign = Sign;

} break;

case YYr31: {	/* lineair_term :  VAR */
#line 146 "lp.y"

  if (    (isign || make_neg)
      && !(isign && make_neg)) 
    var_store(Last_var, Rows, (REAL) - 1);
  else
    var_store(Last_var, Rows, (REAL)1);
  isign = 0;

} break;

case YYr32: {	/* lineair_term :  CONS VAR */
#line 156 "lp.y"

  if (    (isign || make_neg)
      && !(isign && make_neg)) 
    f = -f;
  var_store(Last_var, Rows, f);
  isign = 0;

} break;

case YYr33: {	/* lineair_term :  CONS AR_M_OP VAR */
#line 166 "lp.y"

  if (    (isign || make_neg)
      && !(isign && make_neg)) 
    f = -f;
  var_store(Last_var, Rows, f);
  isign = 0;

} break;

case YYr34: {	/* objective_function :  MAXIMISE real_of */
#line 176 "lp.y"

  Maximise = TRUE;

} break;

case YYr35: {	/* objective_function :  MINIMISE real_of */
#line 180 "lp.y"

  Maximise = FALSE;

} break;

case YYr37: {	/* real_of :  lineair_sum END_C */
#line 188 "lp.y"

  Rows++;
  Lin_term_count  =  0;
  isign = 0;
  make_neg = 0;

} break;
#line 314 "c:/mks/etc/yyparse.c"
	case YYrACCEPT:
		YYACCEPT;
	case YYrERROR:
		goto yyError;
	}

	/*
	 *	Look up next state in goto table.
	 */

	yyp = &yygo[yypgo[yyi]];
	yyq = yyp++;
	yyi = *yyps;
	while (yyi < *yyp++)
		;

	yystate = ~(yyi == *--yyp? YYQYYP: *yyq);
#if YYDEBUG
	if (yydebug)
		YY_TRACE(yyShowGoto)
#endif
	goto yyStack;

yyerrlabel:	;		/* come here from YYERROR	*/
/*
#pragma used yyerrlabel
 */
	yyerrflag = 1;
	if (yyi == YYrERROR) {
		yyps--;
		yypv--;
#if YYDEBUG
		yytp--;
#endif
	}

yyError:
	switch (yyerrflag) {

	case 0:		/* new error */
		yynerrs++;
		yyi = yychar;
		yyerror("Syntax error");
		if (yyi != yychar) {
			/* user has changed the current token */
			/* try again */
			yyerrflag++;	/* avoid loops */
			goto yyEncore;
		}

	case 1:		/* partially recovered */
	case 2:
		yyerrflag = 3;	/* need 3 valid shifts to recover */
			
		/*
		 *	Pop states, looking for a
		 *	shift on `error'.
		 */

		for ( ; yyps > yys; yyps--, yypv--
#if YYDEBUG
					, yytp--
#endif
		) {
#ifdef YACC_WINDOWS
			if (*yyps >= Sizeof_yypact)
#else /* YACC_WINDOWS */
			if (*yyps >= sizeof yypact/sizeof yypact[0])
#endif /* YACC_WINDOWS */
				continue;
			yyp = &yyact[yypact[*yyps]];
			yyq = yyp;
			do
				;
			while (YYERRCODE < *yyp++);

			if (YYERRCODE == yyp[-1]) {
				yystate = ~YYQYYP;
				goto yyStack;
			}
				
			/* no shift in this state */
#if YYDEBUG
			if (yydebug && yyps > yys+1)
				YY_TRACE(yyShowErrRecovery)
#endif
			/* pop stacks; try again */
		}
		/* no shift on error - abort */
		break;

	case 3:
		/*
		 *	Erroneous token after
		 *	an error - discard it.
		 */

		if (yychar == 0)  /* but not EOF */
			break;
#if YYDEBUG
		if (yydebug)
			YY_TRACE(yyShowErrDiscard)
#endif
		yyclearin;
		goto yyEncore;	/* try again in same state */
	}
	YYABORT;

#ifdef YYALLOC
yyReturn:
	yylval = save_yylval;
	yyval = save_yyval;
	yypvt = save_yypvt;
	yychar = save_yychar;
	yyerrflag = save_yyerrflag;
	yynerrs = save_yynerrs;
	free((char *)yys);
	free((char *)yyv);
#if YYDEBUG
	free((char *)yytypev);
#endif
	return(retval);
#endif
}

		
#if YYDEBUG
/*
 * Return type of token
 */
int
yyGetType(tok)
int tok;
{
	yyNamedType * tp;
	for (tp = &yyTokenTypes[yyntoken-1]; tp > yyTokenTypes; tp--)
		if (tp->token == tok)
			return tp->type;
	return 0;
}
/*
 * Print a token legibly.
 */
char *
yyptok(tok)
int tok;
{
	yyNamedType * tp;
	for (tp = &yyTokenTypes[yyntoken-1]; tp > yyTokenTypes; tp--)
		if (tp->token == tok)
			return tp->name;
	return "";
}

/*
 * Read state 'num' from YYStatesFile
 */
#ifdef YYTRACE

static char *
yygetState(num)
int num;
{
	int	size;
	static FILE *yyStatesFile = (FILE *) 0;
	static char yyReadBuf[YYMAX_READ+1];

	if (yyStatesFile == (FILE *) 0
	 && (yyStatesFile = fopen(YYStatesFile, "r")) == (FILE *) 0)
		return "yyExpandName: cannot open states file";

	if (num < yynstate - 1)
		size = (int)(yyStates[num+1] - yyStates[num]);
	else {
		/* length of last item is length of file - ptr(last-1) */
		if (fseek(yyStatesFile, 0L, 2) < 0)
			goto cannot_seek;
		size = (int) (ftell(yyStatesFile) - yyStates[num]);
	}
	if (size < 0 || size > YYMAX_READ)
		return "yyExpandName: bad read size";
	if (fseek(yyStatesFile, yyStates[num], 0) < 0) {
	cannot_seek:
		return "yyExpandName: cannot seek in states file";
	}

	(void) fread(yyReadBuf, 1, size, yyStatesFile);
	yyReadBuf[size] = '\0';
	return yyReadBuf;
}
#endif /* YYTRACE */
/*
 * Expand encoded string into printable representation
 * Used to decode yyStates and yyRules strings.
 * If the expansion of 's' fits in 'buf', return 1; otherwise, 0.
 */
int
yyExpandName(num, isrule, buf, len)
int num, isrule;
char * buf;
int len;
{
	int	i, n, cnt, type;
	char	* endp, * cp;
	char	*s;

	if (isrule)
		s = yyRules[num].name;
	else
#ifdef YYTRACE
		s = yygetState(num);
#else
		s = "*no states*";
#endif

	for (endp = buf + len - 8; *s; s++) {
		if (buf >= endp) {		/* too large: return 0 */
		full:	(void) strcpy(buf, " ...\n");
			return 0;
		} else if (*s == '%') {		/* nonterminal */
			type = 0;
			cnt = yynvar;
			goto getN;
		} else if (*s == '&') {		/* terminal */
			type = 1;
			cnt = yyntoken;
		getN:
			if (cnt < 100)
				i = 2;
			else if (cnt < 1000)
				i = 3;
			else
				i = 4;
			for (n = 0; i-- > 0; )
				n = (n * 10) + *++s - '0';
			if (type == 0) {
				if (n >= yynvar)
					goto too_big;
				cp = yysvar[n];
			} else if (n >= yyntoken) {
			    too_big:
				cp = "<range err>";
			} else
				cp = yyTokenTypes[n].name;

			if ((i = strlen(cp)) + buf > endp)
				goto full;
			(void) strcpy(buf, cp);
			buf += i;
		} else
			*buf++ = *s;
	}
	*buf = '\0';
	return 1;
}
#ifndef YYTRACE
/*
 * Show current state of yyparse
 */
void
yyShowState(tp)
yyTraceItems * tp;
{
	short * p;
	YYSTYPE * q;

	printf(
	    m_textmsg(2828, "state %d (%d), char %s (%d)\n", "I num1 num2 char num3"),
	      yysmap[tp->state], tp->state,
	      yyptok(tp->lookahead), tp->lookahead);
}
/*
 * show results of reduction
 */
void
yyShowReduce(tp)
yyTraceItems * tp;
{
	printf("reduce %d (%d), pops %d (%d)\n",
		yyrmap[tp->rule], tp->rule,
		tp->states[tp->nstates - tp->npop],
		yysmap[tp->states[tp->nstates - tp->npop]]);
}
void
yyShowRead(val)
int val;
{
	printf(m_textmsg(2829, "read %s (%d)\n", "I token num"), yyptok(val), val);
}
void
yyShowGoto(tp)
yyTraceItems * tp;
{
	printf(m_textmsg(2830, "goto %d (%d)\n", "I num1 num2"), yysmap[tp->state], tp->state);
}
void
yyShowShift(tp)
yyTraceItems * tp;
{
	printf(m_textmsg(2831, "shift %d (%d)\n", "I num1 num2"), yysmap[tp->state], tp->state);
}
void
yyShowErrRecovery(tp)
yyTraceItems * tp;
{
	short	* top = tp->states + tp->nstates - 1;

	printf(
	m_textmsg(2832, "Error recovery pops state %d (%d), uncovers %d (%d)\n", "I num1 num2 num3 num4"),
		yysmap[*top], *top, yysmap[*(top-1)], *(top-1));
}
void
yyShowErrDiscard(tp)
yyTraceItems * tp;
{
	printf(m_textmsg(2833, "Error recovery discards %s (%d), ", "I token num"),
		yyptok(tp->lookahead), tp->lookahead);
}
#endif	/* ! YYTRACE */
#endif	/* YYDEBUG */

