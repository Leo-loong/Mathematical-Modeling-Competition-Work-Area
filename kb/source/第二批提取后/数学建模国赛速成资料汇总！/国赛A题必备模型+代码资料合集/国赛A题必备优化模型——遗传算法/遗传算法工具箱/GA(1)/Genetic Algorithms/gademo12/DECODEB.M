function vars = decodeb(pop,nvar,maxval,minval)
% DECODEB -- converts a binary coded chromosome to
% real number values for each variable
% Author:	Ron Shaffer
%		Naval Reseach Laboratory
% Version	1.0 1/24/96
%		1.1 5/2/96 Renamed DECODEB
%		Fixed bug in conversion of binary number to integer
%
% pop:		population of binary coded chromosomes
% nvar:		number of real valued variables to be decoded
% maxval:	maximum real number value for each variable
% minval:	minimum real number value for each variable
% vars:		matrix of decoded real number variable settings (popsize,nvar)

[popsize,lchrome] = size(pop);
%
%	Split chromosome into sections for each variable
%
varchrome = lchrome/nvar;
pow_two = 2.^(0:varchrome)';
maxintval = ((2^varchrome))-1;
range = maxval-minval;
for i = 1:popsize
	start = 1;
	fin = varchrome;
	for j = 1:nvar
		tvars(1:varchrome) = pop(i,start:fin);
		start = start + varchrome;
		fin = fin + varchrome;
%
%		now decode binary number to real number (scale maxval to minval)
%
		temp1 = 0;
		for k = 1:varchrome
			temp1 = temp1 + pow_two(k)*tvars(varchrome-k+1);
		end
%
%		Takes integer value and converts to a real number 
%	
		vars(i,j) = (range*(temp1/maxintval)) + minval;	
	end
end
