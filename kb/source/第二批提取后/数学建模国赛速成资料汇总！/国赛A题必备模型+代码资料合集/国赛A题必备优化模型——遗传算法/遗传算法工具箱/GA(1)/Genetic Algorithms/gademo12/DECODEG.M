function vars = decodeg(pop,nvar,maxval,minval)
% DECODE -- converts a gray-coded binary chromosome to
% real number values for each variable
% Author:	Ron Shaffer
%		Naval Research Laboratory
%		Version 1.0:  Based on DECODEB 1.1
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
%
% first compute gray conversion coefficients
%
gray(1) = maxintval;
for i = 2:varchrome
		gray(i) = (gray(i-1) - 1)/2;
end
for i = 1:popsize
	start = 1;
	fin = varchrome;
	for j = 1:nvar
		tvars(1:varchrome) = pop(i,start:fin);
		start = start + varchrome;
		fin = fin + varchrome;
%
%		now decode binary number to real number (scale maxval to minval)
%		first convert gray binary to integer
%
		temp1 = 0;
		parity = 1;
		for k = 1:varchrome
			if tvars(k) == 1
				if parity == 1
					temp1 = temp1 + (tvars(k)*gray(k));
					parity = 0;
				else
					temp1 = temp1 - (tvars(k)*gray(k));
					parity = 1;
				end
			end
		end
%
%		Takes integer value and converts to a real number 
%
		vars(i,j) = (range*(temp1/maxintval)) + minval;	
	end
end
