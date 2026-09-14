function [new,xcount] = xover(old,px,xtype)
% XOVER performs crossover with a given probability
% Version 1.0 1/23/96 Ron Shaffer
% Version 1.1 2/27/96 Ron Shaffer
%	added options for two-point and uniform crossover
% Version 1.2 6/24/96 Ron Shaffer
%	fixed bug in 2-point crossover discovered by 
%	Mr. Radovan Cemes (ee2rc@ee.surrey.ac.uk).  Crossover
%	points are now sorted before swapping is performed.
%
% new	-- new population of chromosomes
% xcount-- # of times crossover was performed
% old	-- input population of chromosomes
% px	-- crossover probability
% xtype	-- type of crossover
%	-- 1) 1-point crossover
%	-- 2) 2-point crossover
%	-- 3) Uniform crossover

%
% set constants
%
[popsize,ndim] = size(old);
halfpop = popsize/2;
xcount = 0;
%
% loop through chromosomes determining whether xover should be performed
% and if so performing single-point crossover.
%

if xtype == 1
	randlist = rand((halfpop),1);
	for i = 1:halfpop
		x = (i*2) - 1;
		xpo = x + 1;
		new(x,1:ndim) = old(x,1:ndim);
		new(xpo,1:ndim) = old(xpo,1:ndim);
		if (randlist(i) < px) 
			xcount = xcount + 1;
			xpoint = round((rand * ndim)+0.5);
			new(xpo,1:xpoint)=old(x,1:xpoint);
			new(x,1:xpoint) = old(xpo,1:xpoint);	
		end
	end
end
%
% two-point crossover
%

if xtype == 2
	randlist = rand((halfpop),1);
	for i = 1:halfpop
		x = (i*2)-1;
		xpo = x+1;
		new(x,1:ndim) = old(x,1:ndim);
		new(xpo,1:ndim) = old(xpo,1:ndim);
		if (randlist(i) < px)
			xcount = xcount + 1;
 			[xpoint] = sort(round((rand(1,2) * ndim)+0.5));
			new(xpo,xpoint(1):xpoint(2)) = old(x,xpoint(1):xpoint(2));
			new(x,xpoint(1):xpoint(2)) = old(xpo,xpoint(1):xpoint(2));
		end
	end
end
%
% uniform crossover
%

if xtype == 3
	for i = 1:halfpop
		x = (i*2)-1;
		xpo = x+1;
		new(x,1:ndim) = old(x,1:ndim);
		new(xpo,1:ndim) = old(xpo,1:ndim);
		for j = 1:ndim
			test = rand;
			if test < px
				xcount = xcount + 1;
				new(xpo,j) = old(x,j);
				new(x,j) = old(xpo,j);
			end
		end
	end
end

