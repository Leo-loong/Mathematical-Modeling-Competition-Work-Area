MS-DOS Port of lp_solve
                            John P. Powers
                          September 6, 1995

You can solve large linear programs on your MS-DOS machine thanks to
the _Borland PowerPack for DOS_ 32-bit DPMI (Dos Protected Mode
Interface) compiler.  Extended memory is allocated as needed to
contain large program matrices.

Installation
---

Program lp_solve.exe is included in this distribution so you don't
need the Borland C++ development system to run it.

Put lp_solve.exe, 32rtm.exe, cw3211.dll, and dpmi32vm.ovl on your path.

If you need to run lp_solve from a Windows 3.x DOS box, you must have
windpmi.386 installed.  Put windpmi.386 in c:\windows\system and edit
your system.ini file to include the following lines:

  [386enh]
  device=c:\windows\system\windpmi.386

Borland grants you permission to redistribute 32rtm.exe, cw3211.dll,
dpmi32vm.ovl, and windpmi.386 according to their No Nonsense License
Statement.

Other files in the distribution
---

Files lp_solve.dsw and lp_solve.ide are used by the Borland
Integrated Development Environment. You need these files only if you
intend to do further development of this project with Borland tools.

lpkit.lib is a library of routines comprising the solver, mps <-> lp
conversion routines, and procedural interface to the solver. See
demo.c for examples of how to set up an lp and call the solver from
your own programs.

lp2mps and mps2lp are utility programs which convert between lp_solve
style files and industry standard MPS style files.

In addition, you'll find the original source and support files as I
received them in the Unix distribution. I've converted end-of-line of
most of the text files to DOS carriage return/line feed.

System requirements
---

- 386 processor or better.
- Floating point coprocessor NOT necessary but improves performance.
- Extended memory.  The more extended memory you have, the larger lp
  you can solve.

Testing
---

The example test lp files ex1.lp, ..., ex7.lp are the same as
distributed with the Unix sources.  These test programs pass.  If you
run them, remember: ex7.lp needs the -s flag for scaling (lp_solve
-s <ex7.lp >solution.out).

How I Did It
---

Tools used:

gunzip
MKS tar
Thompson Automation Toolkit (Unix-like tools and shell for DOS).
Borland C 4.02 Integrated Development Environment
MKS LEX & YACC

 1. Unzip Unix distribution with gunzip.

    gunzip lp_solve.gz

 2. Extract sources from tar archive with MKS tar.

    tar -x -f lp_solve

 3. Convert sources from Unix end-of-line to DOS end-of-line.

    unix2dos *.c *.h *.l *.y

 4. Change lex.l line 6:

from.......................................................
VR   {LT}{KR}*(<{KR}+>)?
to.........................................................
VR   {LT}{KR}*(\<{KR}+\>)?
...........................................................

This was causing a syntax error in MKS lex on line 58.

 5. Add one line at the end of lp.y just before #include "lex.c"

    #define yywrap() (1)  /* supply a default yywrap() function */

 6. Edit several occurrances of message in read.c.

from.......................................................
 "(store) Warning, variable %s has een effective coefficient of 0 on line...
to.........................................................
 "(store) Warning, variable %s has an effective coefficient of 0 on line...
...........................................................

 7. Changed definition of MALLOC in lpkit.h.

from.......................................................

#define MALLOC(ptr, nr, type) ...

to.........................................................

#ifdef __BORLANDC__
#define MALLOC(ptr, nr, type) if((ptr = (type *) \
  malloc((size_t)(((nr)==0?1:(nr)) * sizeof(type)))) == 0) \
  {fprintf(stderr, "malloc failed on line %d of file %s\n", \
  __LINE__, __FILE__); exit(FAIL); }
#else
#define MALLOC(ptr, nr, type) ...
#endif
...........................................................

My malloc returns NULL if zeros bytes are requested.

 8. Create lex.c.

    lexe -o lex.c lex.l

 9. Create ytab.c.

    yacce lp.y

10. I used the Borland IDE to create project lp_solve.ide. I added
    targets lpkit.lib, lp_solve.exe, lp2mps.exe, mps2lp.exe, and
    demo.exe. Then Project | Build All. Use the distributed
    lp_solve.ide and lp_solve.dsw files as the basis for further
    development with lpkit.h
