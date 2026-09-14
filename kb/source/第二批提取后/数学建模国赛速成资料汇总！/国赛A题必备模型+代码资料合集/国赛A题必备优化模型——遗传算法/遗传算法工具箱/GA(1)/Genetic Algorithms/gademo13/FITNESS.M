function scores = fitness(pop,ffunc,maxval,minval,nparam,h2)
% FITNESS computes fitness scores for GADEMO
% scores = fitness(pop,lchrome,ffunc)
%
% scores:	column vector of fitness scores
% pop:		matrix of chromosomes
% maxval:	maximum real number value for binary to real conversion
% minval:	minimum real number value for binary to real conversion
% nparam:         number of the parameters

[popsize,lchrome] = size(pop);
if ffunc == 1
	scores = sum(pop');
elseif ffunc == 2

     vars = decodeb(pop,nparam,maxval,minval,h2);


%
%	bohachevsky function
%
	for i = 1:popsize
		scores(i) = -((vars(i,1)^2) + (2 * (vars(i,2)^2)) - (0.3 * (cos(3 * pi * vars(i,1)))) - (0.4 * (cos(4 * pi * vars(i,2)))) + 0.7);
	end

else

	vars = decodeb(pop,nparam,maxval,minval,h2);

%
%	Rosenbrock function
%

	for i = 1:popsize
		scores(i) =(100*(vars(i,2)-vars(i,1)^2)^2+(1-vars(i,1))^2);
	end
end
