function gademo(nparam,h2,psz,ngen,pm,px,xtype,elite,ffunc,mfun,maxval,minval,option )
% GADEMO
% 
% LENGTH OF INDIVIDUAL describes how many different values your each variable
% could get (in binary numbers). For example if the length of individual is 4 
% you could have 2^0+2^1+2^2+2^3=15 different values. If it is 8 you could
% have 255 different values.
%
% If your length of individual is 4, your max.value is 15 and min.value is 0
% Then your variable could values:1,2,3,4,5,6,...,15 ( (15-0)/15 =1)
%
% POPULATION SIZE The population size dictates the number of chromosomes in the
% population. Larger population sizes increase the amount of variation present
% in the initial population at the expense of requiring more fitness 
% evaluations.
%
% NUMBER OF GENERATIONS Number of generations * population size = total amount
% of function evaluations
%
% MUTATION PROBABILITY Mutation pobability determines the probability that 
% a mutation will occur. Mutation will randomly change the value of one 
% binary number in the chromosome
% 
% CROSSOVER If the parents(=chromosomes in the population) are allowed to mate,
% a recombination operator is employed to exchange genes between the two 
% parents to produce two children. In the one-point method, a crossover point 
% is selected along the chromosome and the genes up to that point are swapped 
% between the two parents. In the two-point method, two crossover points are 
% selected and the genes between the two points are swapped. In the the 
% uniform crossover method the recombination is applied to the individual 
% genes in the chromosome. If crossover is performed, the genes between the 
% parents are swapped and if no crossover is performed the genes are left 
% intact.
%
% ELITISM Best chromosome will always move to next generation. 
%
% 
% You could define more than 5 variables in the file gademo.m
%
% Demo functions are 1= simple, 2= bohachevsky, 3= rosenbrock 
%
  fig = figure('Units','Normal','Position',[.25 .25 .5 .5], ...
                'Name','GA Demo',...
                'NumberTitle','off','Tag','GA Demo');
%

%
% if you have more than 5 variables, you should define them here
% don't forget the length of each variables (bits)
%
%
if ffunc==1
  nparam=1;
end
vars=0;
for i=1:nparam
  vars=vars+h2(i);
end

 maxval = maxval(1:nparam);
 minval = minval(1:nparam);
     h2 = h2(1:nparam);

%
%
%	Initialize GA DEMO
%

%
end
%
% Start GA optimization
%
 configuration = [vars psz ngen pm px xtype elite mfun nparam];
if option == 1
	[stats,pop,bestc] = genealg(configuration,1,ffunc,maxval,minval,h2,nparam);
elseif option == 2
	[stats,pop,bestc] = genealg(configuration,2,ffunc,maxval,minval,h2,nparam);
%elseif option == 15
%	break;
end
%
%	Plot Statistical Information about the Optimization
%

if (ishold) == 1
	hold off;
end

%
% Mean and best fitness score for each generation
%
plot(stats(:,1),stats(:,4),'c',stats(:,1),stats(:,2),'g-')
title ('GA Optimization Statistics');

ylabel ('Fitness');
xlabel ('Generation #');
legend ('Best','Mean');

%
% End of GA DEMO
%
fprintf('***** Final Statistics ***** \n');
if elite ==1
fprintf('Best chromosome:  ');
 for i = 1:vars
	fprintf('%d',bestc(i));
end

fprintf('\n');
if ffunc ==1
  realvars = decodeb(bestc,nparam,maxval,minval,h2);
  fprintf('Variable # 1 = %6.4f \n',realvars(1));
end

if ((ffunc == 2) | (ffunc == 3))

       	realvars = decodeb(bestc,nparam,maxval,minval,h2);
       
	for i = 1:nparam

           	fprintf('Variable # %d = %6.4f \n',i,realvars(1,i));
	end
end
if ffunc == 4
        realvars = decodeb(bestc,nparam,maxval,minval,h2);
		for i = 1:nparam
		fprintf('Variable # %d = %6.4f \n',i,realvars(1,i));
	end
end

bestscore = fitness(bestc,ffunc,maxval,minval,nparam,h2);
fprintf('Fitness Score:  %8.4f \n', bestscore); 
end
fprintf ('End of Genetic Algorithm Demo \n');













