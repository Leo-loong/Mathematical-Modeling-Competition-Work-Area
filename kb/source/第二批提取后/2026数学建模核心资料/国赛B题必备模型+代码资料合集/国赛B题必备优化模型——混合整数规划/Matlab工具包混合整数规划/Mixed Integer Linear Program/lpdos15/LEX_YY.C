/* c:\mks\bin\lexe lex.l */
#define YYNEWLINE 10
#define INITIAL 0
#define COMMENT 2
#define yy_endst 40
#define yy_nxtmax 623
#define YY_LA_SIZE 5

static unsigned short yy_la_act[] = {
 13, 15, 4, 9, 15, 4, 9, 5, 15, 10, 15, 8, 15, 15, 9, 15,
 10, 15, 11, 15, 12, 15, 13, 15, 13, 15, 14, 15, 15, 13, 10, 10,
 9, 8, 8, 8, 10, 10, 10, 7, 10, 6, 0, 2, 2, 3, 1, 0

};

static unsigned char yy_look[] = {
 0
};

static short yy_final[] = {
 0, 1, 2, 5, 7, 9, 11, 13, 14, 16, 18, 20, 22, 24, 26, 28,
 29, 30, 31, 31, 31, 32, 33, 34, 34, 34, 35, 36, 36, 37, 38, 39,
 40, 41, 42, 43, 43, 44, 45, 46, 47
};
#ifndef yy_state_t
#define yy_state_t unsigned char
#endif

static yy_state_t yy_begin[] = {
 0, 0, 35, 35, 0
};

static yy_state_t yy_next[] = {
 15, 15, 15, 15, 15, 15, 15, 15, 15, 2, 3, 15, 15, 15, 15, 15,
 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15,
 2, 15, 15, 15, 15, 15, 15, 15, 15, 15, 11, 8, 4, 8, 7, 1,
 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 10, 14, 12, 13, 12, 15,
 15, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 5, 9, 9,
 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 15, 15, 15, 15, 15,
 15, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 5, 9, 9,
 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 15, 15, 15, 15, 15,
 16, 17, 17, 17, 17, 17, 40, 40, 40, 40, 31, 33, 17, 17, 17, 17,
 17, 17, 17, 17, 17, 17, 17, 17, 34, 39, 18, 40, 40, 40, 17, 17,
 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 23, 17, 17, 17, 40, 17,
 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17,
 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 23, 17, 17, 19, 19, 19,
 19, 19, 3, 3, 40, 40, 40, 40, 19, 19, 19, 19, 19, 19, 19, 19,
 19, 19, 19, 19, 40, 40, 30, 40, 40, 3, 19, 19, 19, 19, 19, 19,
 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19,
 19, 19, 19, 19, 19, 19, 30, 19, 19, 19, 40, 19, 19, 19, 19, 19,
 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19,
 19, 19, 19, 19, 19, 19, 40, 19, 19, 19, 19, 19, 19, 19, 3, 3,
 40, 40, 40, 40, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19,
 40, 40, 32, 40, 20, 3, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19,
 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19,
 19, 19, 32, 19, 19, 19, 40, 19, 19, 19, 19, 19, 19, 19, 19, 19,
 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19,
 19, 19, 40, 19, 19, 21, 21, 22, 22, 22, 22, 22, 22, 22, 22, 22,
 22, 40, 40, 40, 40, 40, 40, 40, 24, 40, 24, 40, 21, 25, 25, 25,
 25, 25, 25, 25, 25, 25, 25, 21, 27, 21, 26, 26, 26, 26, 26, 26,
 26, 26, 26, 26, 29, 40, 40, 40, 40, 40, 40, 40, 28, 40, 40, 23,
 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40,
 40, 40, 40, 40, 29, 40, 40, 40, 40, 40, 40, 40, 28, 40, 40, 23,
 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 38, 37, 37, 37, 37, 37,
 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37,
 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 36, 37, 37, 37, 37, 37,
 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37,
 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37,
 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37,
 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37,
 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37,
 0
};

static yy_state_t yy_check[] = {
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
 12, 9, 9, 9, 9, 9, 25, 24, 25, 24, 30, 32, 9, 9, 9, 9,
 9, 9, 9, 9, 9, 9, 9, 9, 1, 36, 9, ~0, ~0, ~0, 9, 9,
 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 22, 9, 9, 9, ~0, 9,
 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 22, 9, 9, 18, 18, 18,
 18, 18, 3, 3, ~0, ~0, ~0, ~0, 18, 18, 18, 18, 18, 18, 18, 18,
 18, 18, 18, 18, ~0, ~0, 29, ~0, ~0, 3, 18, 18, 18, 18, 18, 18,
 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18,
 18, 18, 18, 18, 18, 18, 29, 18, 18, 18, ~0, 18, 18, 18, 18, 18,
 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18,
 18, 18, 18, 18, 18, 18, ~0, 18, 18, 19, 19, 19, 19, 19, 2, 2,
 ~0, ~0, ~0, ~0, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19,
 ~0, ~0, 28, ~0, 19, 2, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19,
 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19,
 19, 19, 28, 19, 19, 19, ~0, 19, 19, 19, 19, 19, 19, 19, 19, 19,
 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19,
 19, 19, ~0, 19, 19, 8, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7,
 7, ~0, ~0, ~0, ~0, ~0, ~0, ~0, 23, ~0, 23, ~0, 8, 23, 23, 23,
 23, 23, 23, 23, 23, 23, 23, 8, 6, 8, 6, 6, 6, 6, 6, 6,
 6, 6, 6, 6, 5, ~0, ~0, ~0, ~0, ~0, ~0, ~0, 5, ~0, ~0, 6,
 ~0, ~0, ~0, ~0, ~0, ~0, ~0, ~0, ~0, ~0, ~0, ~0, ~0, ~0, ~0, ~0,
 ~0, ~0, ~0, ~0, 5, ~0, ~0, ~0, ~0, ~0, ~0, ~0, 5, ~0, ~0, 6,
 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35,
 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35,
 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35,
 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35,
 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35,
 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35,
 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35,
 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35,
 0
};

static yy_state_t yy_default[] = {
 40, 40, 8, 8, 40, 9, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40,
 40, 9, 40, 40, 40, 8, 7, 40, 23, 23, 6, 7, 9, 9, 9, 40,
 9, 40, 40, 40, 40, 40, 40, 40, 0
};

static short yy_base[] = {
 0, 110, 309, 217, 624, 387, 394, 359, 396, 94, 624, 624, 67, 624, 624, 624,
 624, 624, 186, 278, 624, 624, 117, 381, 92, 91, 624, 624, 260, 158, 80, 624,
 81, 624, 624, 496, 106, 624, 624, 624, 624
};


#line 1 "c:/mks/etc/yylex.c"
/*
 * Copyright 1988, 1992 by Mortice Kern Systems Inc.  All rights reserved.
 * All rights reserved.
 *
 * $Header: /u/rd/src/lex/RCS/yylex.c,v 1.44 1993/05/26 14:47:37 ignac Exp $
 *
 */
#include <stdlib.h>
#include <stdio.h>
#if	__STDC__
#define YY_ARGS(args)	args
#else
#define YY_ARGS(args)	()
#endif

#ifdef LEX_WINDOWS
#include <windows.h>

/*
 * define, if not already defined
 * the flag YYEXIT, which will allow
 * graceful exits from yylex()
 * without resorting to calling exit();
 */

#ifndef YYEXIT
#define YYEXIT	1
#endif

/*
 * the following is the handle to the current
 * instance of a windows program. The user
 * program calling yylex must supply this!
 */

extern HANDLE hInst;	

#endif	/* LEX_WINDOWS */

/*
 * Define m_textmsg() to an appropriate function for internationalized messages
 * or custom processing.
 */
#ifndef I18N
#define	m_textmsg(id, str, cls)	(str)
#else /*I18N*/
extern	char* m_textmsg YY_ARGS((int id, const char* str, char* cls));
#endif/*I18N*/

/*
 * Include string.h to get definition of memmove() and size_t.
 * If you do not have string.h or it does not declare memmove
 * or size_t, you will have to declare them here.
 */
#include <string.h>
/* Uncomment next line if memmove() is not declared in string.h */
/*extern char * memmove();*/
/* Uncomment next line if size_t is not available in stdio.h or string.h */
/*typedef unsigned size_t;*/
/* Drop this when LATTICE provides memmove */
#ifdef LATTICE
#define memmove	memcopy
#endif

/*
 * YY_STATIC determines the scope of variables and functions
 * declared by the lex scanner. It must be set with a -DYY_STATIC
 * option to the compiler (it cannot be defined in the lex program).
 */
#ifdef	YY_STATIC
/* define all variables as static to allow more than one lex scanner */
#define	YY_DECL	static
#else
/* define all variables as global to allow other modules to access them */
#define	YY_DECL	
#endif

/*
 * You can redefine yygetc. For YACC Tracing, compile this code
 * with -DYYTRACE to get input from yt_getc
 */
#ifdef YYTRACE
extern int	yt_getc YY_ARGS((void));
#define yygetc()	yt_getc()
#else
#define	yygetc()	getc(yyin) 	/* yylex input source */
#endif

/*
 * the following can be redefined by the user.
 */
#ifdef YYEXIT
#define	YY_FATAL(msg)	{ fprintf(yyout, "yylex: %s\n", msg); yyLexFatal = 1; }
#else /* YYEXIT */
#define	YY_FATAL(msg)	{ fprintf(stderr, "yylex: %s\n", msg); exit(1); }
#endif /* YYEXIT */

#define	ECHO		fputs(yytext, yyout)
#define	output(c)	putc((c), yyout) /* yylex sink for unmatched chars */
#define	YY_INTERACTIVE	1		/* save micro-seconds if 0 */
#define	YYLMAX		100		/* token and pushback buffer size */

/*
 * If %array is used (or defaulted), yytext[] contains the token.
 * If %pointer is used, yytext is a pointer to yy_tbuf[].
 */
YY_DECL char	yytext[YYLMAX+1];

#define	BEGIN		yy_start =
#define	REJECT		goto yy_reject
#define	NLSTATE		(yy_lastc = YYNEWLINE)
#define	YY_INIT \
	(yy_start = yyleng = yy_end = 0, yy_lastc = YYNEWLINE)
#define	yymore()	goto yy_more
#define	yyless(n)	if ((n) < 0 || (n) > yy_end) ; \
			else { YY_SCANNER; yyleng = (n); YY_USER; }

YY_DECL	void	yy_reset YY_ARGS((void));
YY_DECL	int	input	YY_ARGS((void));
YY_DECL	int	unput	YY_ARGS((int c));

/* functions defined in libl.lib */
extern	int	yywrap	YY_ARGS((void));
extern	void	yyerror	YY_ARGS((char *fmt, ...));
extern	void	yycomment	YY_ARGS((char *term));
extern	int	yymapch	YY_ARGS((int delim, int escape));


#line 128 "c:/mks/etc/yylex.c"


#ifdef	YY_DEBUG
#undef	YY_DEBUG
#define	YY_DEBUG(fmt, a1, a2)	fprintf(stderr, fmt, a1, a2)
#else
#define	YY_DEBUG(fmt, a1, a2)
#endif

/*
 * The declaration for the lex scanner can be changed by
 * redefining YYLEX or YYDECL. This must be done if you have
 * more than one scanner in a program.
 */
#ifndef	YYLEX
#define	YYLEX yylex			/* name of lex scanner */
#endif

#ifndef YYDECL
#define	YYDECL	int YYLEX YY_ARGS((void))	/* declaration for lex scanner */
#endif

/*
 * stdin and stdout may not neccessarily be constants.
 * If stdin and stdout are constant, and you want to save a few cycles, then
 * #define YY_STATIC_STDIO 1 in this file or on the commandline when
 * compiling this file
 */
#ifndef YY_STATIC_STDIO
#define YY_STATIC_STDIO	0
#endif

#if YY_STATIC_STDIO
YY_DECL	FILE   *yyin = stdin;
YY_DECL	FILE   *yyout = stdout;
#else
YY_DECL	FILE   *yyin = (FILE *)0;
YY_DECL	FILE   *yyout = (FILE *)0;
#endif
YY_DECL	int	yylineno = 1;		/* line number */

/* yy_sbuf[0:yyleng-1] contains the states corresponding to yytext.
 * yytext[0:yyleng-1] contains the current token.
 * yytext[yyleng:yy_end-1] contains pushed-back characters.
 * When the user action routine is active,
 * yy_save contains yytext[yyleng], which is set to '\0'.
 * Things are different when YY_PRESERVE is defined. 
 */
static	yy_state_t yy_sbuf [YYLMAX+1];	/* state buffer */
static	int	yy_end = 0;		/* end of pushback */
static	int	yy_start = 0;		/* start state */
static	int	yy_lastc = YYNEWLINE;	/* previous char */
YY_DECL	int	yyleng = 0;		/* yytext token length */
#ifdef YYEXIT
static	int yyLexFatal;
#endif /* YYEXIT */

#ifndef YY_PRESERVE	/* the efficient default push-back scheme */

static	char yy_save;	/* saved yytext[yyleng] */

#define	YY_USER	{ /* set up yytext for user */ \
		yy_save = yytext[yyleng]; \
		yytext[yyleng] = 0; \
	}
#define	YY_SCANNER { /* set up yytext for scanner */ \
		yytext[yyleng] = yy_save; \
	}

#else		/* not-so efficient push-back for yytext mungers */

static	char yy_save [YYLMAX];
static	char *yy_push = yy_save+YYLMAX;

#define	YY_USER { \
		size_t n = yy_end - yyleng; \
		yy_push = yy_save+YYLMAX - n; \
		if (n > 0) \
			memmove(yy_push, yytext+yyleng, n); \
		yytext[yyleng] = 0; \
	}
#define	YY_SCANNER { \
		size_t n = yy_save+YYLMAX - yy_push; \
		if (n > 0) \
			memmove(yytext+yyleng, yy_push, n); \
		yy_end = yyleng + n; \
	}

#endif


#ifdef LEX_WINDOWS

/*
 * When using the windows features of lex,
 * it is necessary to load in the resources being
 * used, and when done with them, the resources must
 * be freed up, otherwise we have a windows app that
 * is not following the rules. Thus, to make yylex()
 * behave in a windows environment, create a new
 * yylex() which will call the original yylex() as
 * another function call. Observe ...
 */

/*
 * The actual lex scanner (usually yylex(void)).
 * NOTE: you should invoke yy_init() if you are calling yylex()
 * with new input; otherwise old lookaside will get in your way
 * and yylex() will die horribly.
 */
static int win_yylex();			/* prototype for windows yylex handler */

YYDECL {
	int wReturnValue;
	HANDLE hRes_table;
	unsigned short *old_yy_la_act;	/* remember previous pointer values */
	short *old_yy_final;
	yy_state_t *old_yy_begin;
	yy_state_t *old_yy_next;
	yy_state_t *old_yy_check;
	yy_state_t *old_yy_default;
	short *old_yy_base;

	/*
	 * the following code will load the required
	 * resources for a Windows based parser.
	 */

	hRes_table = LoadResource (hInst,
		FindResource (hInst, "UD_RES_yyLEX", "yyLEXTBL"));
	
	/*
	 * return an error code if any
	 * of the resources did not load
	 */

	if (hRes_table == NULL)
		return (0);
	
	/*
	 * the following code will lock the resources
	 * into fixed memory locations for the scanner
	 * (and remember previous pointer locations)
	 */

	old_yy_la_act = yy_la_act;
	old_yy_final = yy_final;
	old_yy_begin = yy_begin;
	old_yy_next = yy_next;
	old_yy_check = yy_check;
	old_yy_default = yy_default;
	old_yy_base = yy_base;

	yy_la_act = (unsigned short *)LockResource (hRes_table);
	yy_final = (short *)(yy_la_act + Sizeof_yy_la_act);
	yy_begin = (yy_state_t *)(yy_final + Sizeof_yy_final);
	yy_next = (yy_state_t *)(yy_begin + Sizeof_yy_begin);
	yy_check = (yy_state_t *)(yy_next + Sizeof_yy_next);
	yy_default = (yy_state_t *)(yy_check + Sizeof_yy_check);
	yy_base = (yy_state_t *)(yy_default + Sizeof_yy_default);


	/*
	 * call the standard yylex() code
	 */

	wReturnValue = win_yylex();

	/*
	 * unlock the resources
	 */

	UnlockResource (hRes_table);

	/*
	 * and now free the resource
	 */

	FreeResource (hRes_table);

	/*
	 * restore previously saved pointers
	 */

	yy_la_act = old_yy_la_act;
	yy_final = old_yy_final;
	yy_begin = old_yy_begin;
	yy_next = old_yy_next;
	yy_check = old_yy_check;
	yy_default = old_yy_default;
	yy_base = old_yy_base;

	return (wReturnValue);
}	/* end function */

static int win_yylex() {

#else /* LEX_WINDOWS */

/*
 * The actual lex scanner (usually yylex(void)).
 * NOTE: you should invoke yy_init() if you are calling yylex()
 * with new input; otherwise old lookaside will get in your way
 * and yylex() will die horribly.
 */
YYDECL {

#endif /* LEX_WINDOWS */

	register int c, i, yybase;
	unsigned	yyst;	/* state */
	int yyfmin, yyfmax;	/* yy_la_act indices of final states */
	int yyoldi, yyoleng;	/* base i, yyleng before look-ahead */
	int yyeof;		/* 1 if eof has already been read */

#line 342 "c:/mks/etc/yylex.c"



#if !YY_STATIC_STDIO
	if (yyin == (FILE *)0)
		yyin = stdin;
	if (yyout == (FILE *)0)
		yyout = stdout;
#endif

#ifdef YYEXIT
	yyLexFatal = 0;
#endif /* YYEXIT */

	yyeof = 0;
	i = yyleng;
	YY_SCANNER;

  yy_again:
	yyleng = i;
	/* determine previous char. */
	if (i > 0)
		yy_lastc = yytext[i-1];
	/* scan previously accepted token adjusting yylineno */
	while (i > 0)
		if (yytext[--i] == YYNEWLINE)
			yylineno++;
	/* adjust pushback */
	yy_end -= yyleng;
	memmove(yytext, yytext+yyleng, (size_t) yy_end);
	i = 0;

  yy_contin:
	yyoldi = i;

	/* run the state machine until it jams */
	yyst = yy_begin[yy_start + (yy_lastc == YYNEWLINE)];
	yy_sbuf[i] = (yy_state_t) yyst;
	do {
		YY_DEBUG(m_textmsg(1547, "<state %d, i = %d>\n", "I num1 num2"), yyst, i);
		if (i >= YYLMAX) {
			YY_FATAL(m_textmsg(1548, "Token buffer overflow", "E"));
#ifdef YYEXIT
			if (yyLexFatal)
				return -2;
#endif /* YYEXIT */
		}	/* endif */

		/* get input char */
		if (i < yy_end)
			c = yytext[i];		/* get pushback char */
		else if (!yyeof && (c = yygetc()) != EOF) {
			yy_end = i+1;
			yytext[i] = (char) c;
		} else /* c == EOF */ {
			c = EOF;		/* just to make sure... */
			if (i == yyoldi) {	/* no token */
				yyeof = 0;
				if (yywrap())
					return 0;
				else
					goto yy_again;
			} else {
				yyeof = 1;	/* don't re-read EOF */
				break;
			}
		}
		YY_DEBUG(m_textmsg(1549, "<input %d = 0x%02x>\n", "I num hexnum"), c, c);

		/* look up next state */
		while ((yybase = yy_base[yyst]+(unsigned char)c) > yy_nxtmax
		    || yy_check[yybase] != (yy_state_t) yyst) {
			if (yyst == yy_endst)
				goto yy_jammed;
			yyst = yy_default[yyst];
		}
		yyst = yy_next[yybase];
	  yy_jammed: ;
	  yy_sbuf[++i] = (yy_state_t) yyst;
	} while (!(yyst == yy_endst || YY_INTERACTIVE && yy_base[yyst] > yy_nxtmax && yy_default[yyst] == yy_endst));
	YY_DEBUG(m_textmsg(1550, "<stopped %d, i = %d>\n", "I num1 num2"), yyst, i);
	if (yyst != yy_endst)
		++i;

  yy_search:
	/* search backward for a final state */
	while (--i > yyoldi) {
		yyst = yy_sbuf[i];
		if ((yyfmin = yy_final[yyst]) < (yyfmax = yy_final[yyst+1]))
			goto yy_found;	/* found final state(s) */
	}
	/* no match, default action */
	i = yyoldi + 1;
	output(yytext[yyoldi]);
	goto yy_again;

  yy_found:
	YY_DEBUG(m_textmsg(1551, "<final state %d, i = %d>\n", "I num1 num2"), yyst, i);
	yyoleng = i;		/* save length for REJECT */
	
	/* pushback look-ahead RHS */
	if ((c = (int)(yy_la_act[yyfmin]>>9) - 1) >= 0) { /* trailing context? */
		unsigned char *bv = yy_look + c*YY_LA_SIZE;
		static unsigned char bits [8] = {
			1<<0, 1<<1, 1<<2, 1<<3, 1<<4, 1<<5, 1<<6, 1<<7
		};
		while (1) {
			if (--i < yyoldi) {	/* no / */
				i = yyoleng;
				break;
			}
			yyst = yy_sbuf[i];
			if (bv[(unsigned)yyst/8] & bits[(unsigned)yyst%8])
				break;
		}
	}

	/* perform action */
	yyleng = i;
	YY_USER;
	switch (yy_la_act[yyfmin] & 0777) {
	case 0:
#line 13 "lex.l"
	{
  BEGIN COMMENT;
} /* begin skip comment */
	break;
	case 1:
#line 17 "lex.l"
	{
  BEGIN INITIAL;
} /* end skip comment */
	break;
	case 2:
#line 21 "lex.l"
	{
}
	break;
	case 3:
#line 24 "lex.l"
	{
}
	break;
	case 4:
#line 27 "lex.l"
	{
}
	break;
	case 5:
#line 30 "lex.l"
	{
  return(COMMA);
}
	break;
	case 6:
#line 34 "lex.l"
	{
  return(MINIMISE);
}
	break;
	case 7:
#line 38 "lex.l"
	{
  return(MAXIMISE);
}
	break;
	case 8:
#line 42 "lex.l"
	{
  f = atof((char *)yytext) * Scale_factor;
  return(CONS);
} /* f contains the last float */
	break;
	case 9:
#line 47 "lex.l"
	{
  Sign=0;
  for(x=0;x<yyleng;x++)
    if(yytext[x] == '-' || yytext[x] == '+')
      Sign = (Sign == (yytext[x] == '+'));
  return (SIGN);
  /* Sign is TRUE if the sign-string
     represents a '-'. Otherwise Sign
     is FALSE */
}
	break;
	case 10:
#line 59 "lex.l"
	{
  strcpy(Last_var, (char *)yytext);
  return(VAR);
}
	break;
	case 11:
#line 64 "lex.l"
	{
  return (COLON);
}
	break;
	case 12:
#line 68 "lex.l"
	{
  return(AR_M_OP);
}
	break;
	case 13:
#line 72 "lex.l"
	{
  return(RE_OP);
}
	break;
	case 14:
#line 76 "lex.l"
	{
  return(END_C);
}
	break;
	case 15:
#line 80 "lex.l"
	{
  fprintf(stderr,"LEX ERROR : %s lineno %d \n" ,yytext,yylineno);
}
	break;

#line 463 "c:/mks/etc/yylex.c"

	}
	YY_SCANNER;
	i = yyleng;
	goto yy_again;			/* action fell though */

  yy_reject:
	YY_SCANNER;
	i = yyoleng;			/* restore original yytext */
	if (++yyfmin < yyfmax)
		goto yy_found;		/* another final state, same length */
	else
		goto yy_search;		/* try shorter yytext */

  yy_more:
	YY_SCANNER;
	i = yyleng;
	if (i > 0)
		yy_lastc = yytext[i-1];
	goto yy_contin;
}
/*
 * Safely switch input stream underneath LEX
 */
typedef struct yy_save_block_tag {
	FILE	* oldfp;
	int	oldline;
	int	oldend;
	int	oldstart;
	int	oldlastc;
	int	oldleng;
	char	savetext[YYLMAX+1];
	yy_state_t	savestate[YYLMAX+1];
} YY_SAVED;

YY_SAVED *
yySaveScan(fp)
FILE * fp;
{
	YY_SAVED * p;

	if ((p = (YY_SAVED *) malloc(sizeof(*p))) == NULL)
		return p;

	p->oldfp = yyin;
	p->oldline = yylineno;
	p->oldend = yy_end;
	p->oldstart = yy_start;
	p->oldlastc = yy_lastc;
	p->oldleng = yyleng;
	(void) memcpy(p->savetext, yytext, sizeof yytext);
	(void) memcpy((char *) p->savestate, (char *) yy_sbuf,
		sizeof yy_sbuf);

	yyin = fp;
	yylineno = 1;
	YY_INIT;

	return p;
}
/*f
 * Restore previous LEX state
 */
void
yyRestoreScan(p)
YY_SAVED * p;
{
	if (p == NULL)
		return;
	yyin = p->oldfp;
	yylineno = p->oldline;
	yy_end = p->oldend;
	yy_start = p->oldstart;
	yy_lastc = p->oldlastc;
	yyleng = p->oldleng;

	(void) memcpy(yytext, p->savetext, sizeof yytext);
	(void) memcpy((char *) yy_sbuf, (char *) p->savestate,
		sizeof yy_sbuf);
	free(p);
}
/*
 * User-callable re-initialization of yylex()
 */
void
yy_reset()
{
	YY_INIT;
	yylineno = 1;		/* line number */
}
/* get input char with pushback */
YY_DECL int
input()
{
	int c;
#ifndef YY_PRESERVE
	if (yy_end > yyleng) {
		yy_end--;
		memmove(yytext+yyleng, yytext+yyleng+1,
			(size_t) (yy_end-yyleng));
		c = yy_save;
		YY_USER;
#else
	if (yy_push < yy_save+YYLMAX) {
		c = *yy_push++;
#endif
	} else
		c = yygetc();
	yy_lastc = c;
	if (c == YYNEWLINE)
		yylineno++;
	return c;
}

/*f
 * pushback char
 */
YY_DECL int
unput(c)
	int c;
{
#ifndef YY_PRESERVE
	if (yy_end >= YYLMAX) {
		YY_FATAL(m_textmsg(1552, "Push-back buffer overflow", "E"));
	} else {
		if (yy_end > yyleng) {
			yytext[yyleng] = yy_save;
			memmove(yytext+yyleng+1, yytext+yyleng,
				(size_t) (yy_end-yyleng));
			yytext[yyleng] = 0;
		}
		yy_end++;
		yy_save = (char) c;
#else
	if (yy_push <= yy_save) {
		YY_FATAL(m_textmsg(1552, "Push-back buffer overflow", "E"));
	} else {
		*--yy_push = c;
#endif
		if (c == YYNEWLINE)
			yylineno--;
	}	/* endif */
	return c;
}

#line 85 "lex.l"
