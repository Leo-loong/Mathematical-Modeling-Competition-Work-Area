function scores = fitness(pop,ffunc,maxval,minval,gray)
% FITNESS computes fitness scores for GADEMO
% scores = fitness(pop,lchrome,ffunc)
% Author:	Ron Shaffer
%		Naval Research Laboratory
% Revisions:	2/27/96 Version 1.0 (original code) 
%		3/14/96 Version 1.1 Ron Shaffer
%		Modifications to binary to real conversion
%		5/2/96	Version 1.2 Ron Shaffer
%		DECODE renamed DECODEB
%		Included Option for Gray decoding DECODEG
%
% scores:	column vector of fitness scores
% pop:		matrix of chromosomes
% maxval:	maximum real number value for binary to real conversion
% minval:	minimum real number value for binary to real conversion
% gray:		1=regular binary 2 = gray coded binary


[popsize,lchrome] = size(pop);
%
% if ffunc = 1 simple function
% if ffunc = 2 bohachevsky function
%
if ffunc == 1
	scores = sum(pop');
else
	nvar = 2;
	if gray == 1
		vars = decodeb(pop,nvar,maxval,minval);
	else
		vars = decodeg(pop,nvar,maxval,minval);
	end
%
%	bohachevsky function
%
	for i = 1:popsize
		scores(i) = -((vars(i,1)^2) + (2 * (vars(i,2)^2)) - (0.3 * (cos(3 * pi * vars(i,1)))) - (0.4 * (cos(4 * pi * vars(i,2)))) + 0.7);
	end
end
