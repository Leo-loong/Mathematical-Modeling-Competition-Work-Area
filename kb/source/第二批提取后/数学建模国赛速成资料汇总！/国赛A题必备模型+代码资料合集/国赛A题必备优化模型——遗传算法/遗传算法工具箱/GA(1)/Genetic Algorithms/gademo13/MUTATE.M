function [new,nmut] = mutate(pop,pm)
% MUTATE perform mutation on population of chromsomes
% new = mutate(pop,pm)
% 
% set constants
%
[popsize,ndim] = size(pop);
nmut = 0;
%
% loop through population testing whether to mutate
%
for i = 1:popsize
	for j = 1:ndim
		test = rand;
		if test < pm
			pop(i,j) = abs(pop(i,j)-1);
			nmut = nmut + 1;
		end
	end
end
%
% return new population
%
new = pop;

		
