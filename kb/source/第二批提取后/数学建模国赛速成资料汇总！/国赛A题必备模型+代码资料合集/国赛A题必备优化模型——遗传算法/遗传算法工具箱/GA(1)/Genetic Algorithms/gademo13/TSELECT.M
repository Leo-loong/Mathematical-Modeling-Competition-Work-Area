function mateset = tselect(population,scores,elite,mfun)
% TSELECT tournament mating selection
%
%
% set constants
%
[popsize,ndim] = size(population);

%
% With elistist strategy on you only need to choose a mating set with popsize - 1
% members in it b/c the last spot is save for the elite chromosome
%
if elite == 1
	popsize = popsize - 1;
end
%
% compute vector of random integers
%
randlist = [round(rand((popsize*2),1)*popsize+0.5)];
%
%  Begin tournament selection 
%
count = 0;
for i = 1:popsize
	count = count + 2;
	cmo = count - 1;
%
%	2 randomly chosen chromosomes from population
%	will compete for inclusion in mating subset
%
      if mfun == 1  
	
        if scores(randlist(count)) > scores(randlist(cmo))
		mateset(i,1:ndim) = population(randlist(count),1:ndim);
	else
		mateset(i,1:ndim) = population(randlist(cmo),1:ndim);
	end
      end
      if mfun ==2
       if scores(randlist(count)) < scores(randlist(cmo))
		mateset(i,1:ndim) = population(randlist(count),1:ndim);
	else
		mateset(i,1:ndim) = population(randlist(cmo),1:ndim);
	end
      end 
  
end
