Borland C++ 4.02 Port of lp_solve 1.5

You can solve large linear programs on your MS-DOS machine thanks to
the _Borland PowerPack for DOS_ 32-bit DPMI (Dos Protected Mode
Interface) compiler.  Extended memory is allocated as needed to
contain large program matrices.

Installation
---

Program lp_solve.exe is included in this distribution so you don't
need the Borland C++ development system to run it.

Put lp_solve.exe, 32rtm.exe, cw3211.dll, and dpmi32vm.ovl on your path.

If you to run lp_solve from a Windows 3.x DOS box, you must have
windpmi.386 installed.  Put windpmi.386 in c:\windows\system and edit
your system.ini file to include the following lines:

  [386enh]
  device=c:\windows\system\windpmi.386

Borland grants you permission to redistribute 32rtm.exe, cw3211.dll,
dpmi32vm.ovl, and windpmi.386 according to their No Nonsense Licence
Statement.

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
run them, remember: ex7.lp needs the -autoscale flag (lp_solve
-autoscale <ex7.lp >solution.out).

I've also included a labor/shift assignment program I wrote.  A perl
program feeds workers' preferences for work site and shift into
lp_solve.  Another perl program formats the solution as a shift
assignment table.  This program grew out of a need to assign student
workers to run four on-campus computer centers.  Four 4-hour shifts a
day had to be staffed.  Each student can work up to five shifts a
week.  No student works more than one shift per day. Only one student
works each shift/site at a time.

The input begins with a list of works sites, each on a separate line,
and terminated by a blank line.

Next are blocks of student worker preferences.  Each block starts
with the student's name and preference for each work site on one
line.  1=prefer, 2=don't care, 3=avoid, 9=conflict.  Next are the
student's day/shift preferences:  a cost for each of four shifts for
Sunday on one line, followed by shift preferences for the remaining
days of the week.
