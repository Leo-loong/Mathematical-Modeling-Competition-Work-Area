function [stats,pop,elitechrome] = genealg(configuration,prnlevel,ffunc,maxval,minval,h2,nparam);
% GENEALG  implements simple genetic algorithm
%
%
% [stats,pop] = genealg(configuration)
% stats:	fitness statistics for each generation
% pop:		final population of chromosomes
% elitechrome:	chromosome in current population with highest fitness score
% configuration:GA configuration in the following order
%		length of chromsome, population size, number of generations,
%		mutation rate, crossover rate, crossover type, elistist, gray 

%
% set GA configuration
%

fprintf('** Starting GA Optimization ** \n');
fprintf('# \t   Mean \t     Stdev \t    Best \n');
ndim = configuration(1);
popsize = configuration(2);
numgen = configuration(3);
pm = configuration(4);
px = configuration(5);
xtype = configuration(6);
elite = configuration(7);
mfun = configuration(8);
numxover = 0;
nummut = 0;
nstat = 7;
%
%	For bohachevsky function set minimum and maximum values
%
%
% To use elitist strategy popsize must a odd integer
% If elitist strategy off popsize must be an even integer
%
test = rem(popsize,2);
if elite == 1
	if (test == 0)
		popsize = popsize + 1;
	end
else
	if (test ~= 0)
		popsize = popsize + 1;
	end
end
%
% initialize population randomly
%
pop = [(rand(popsize,ndim)<0.5)];
%
% Optimize for a given number of generations
%

tnumgen = numgen + 1;
for cgn = 1:tnumgen
%
% 	compute fitness function for each member of population
%
	scores = fitness(pop,ffunc,maxval,minval,nparam,h2);
%

	if prnlevel == 1
		for j = 1:popsize
			fprintf('%d',pop(j,1:ndim));
			fprintf('\t %8.5f',scores(j));
			fprintf('\n');
		end
	end
%	
         if mfun == 1
           [topfit,topi] = max(scores);
         end

         if mfun == 2
	   [topfit,topi] = min(scores);
        end

	ms = mean(scores);
	sd = std(scores);
	fprintf('%i \t %8.2f \t %8.2f \t %8.2f \n',cgn,ms,sd,topfit);
	stats(cgn,1:nstat) = [cgn ms sd topfit pm nummut numxover];

%
%	find best chromosome based on fitness score
%
	if elite == 1
		elitechrome = pop(topi,:);
	end

%

%
%	Stop optimization after fixed number of generations
%
	if (cgn == numgen) 
		break;
	end
%
%	select most fit members of population for mating subset
%	using tournament selection and elitist strategy (if turned on)
%	
	mate = tselect(pop,scores,elite,mfun);

%
%	perform crossover if required
%
	[child,txnum] = xover(mate,px,xtype);
	numxover = numxover + txnum;
%
%	perform mutation
%
	[child,tnmut] = mutate(child,pm);
	nummut = nummut + tnmut;
%
% 	Children + elite chromosome (if elitism turned on) form the new generation
%
	pop = child;
	if elite == 1
		pop(popsize,:) = elitechrome;
	end
%
end
