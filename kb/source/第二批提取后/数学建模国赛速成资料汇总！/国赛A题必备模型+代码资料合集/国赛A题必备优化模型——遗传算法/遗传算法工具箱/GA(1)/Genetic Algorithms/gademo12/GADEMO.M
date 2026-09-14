function [] = gademo();
% GADEMO -- matlab demo program for a binary-coded genetic algorithm
% Ron Shaffer
% Naval Research Laboratory
% Version 1.0 2/27/96 	Original Version
% Version 1.1 5/2/96	Included option for gray-coded chromosomes
%			Renamed DECODE--DECODEB 
%			Fixed bug in DECODEB
% Version 1.2 6/24/96	Fixed bug in XOVER that was discovered by
%			Mr. Radovan Cemes (ees2rc@ee.surrey.ac.uk).
%

% default settings:
vars = 10;
psz = 20;
ngen = 10;
pm = 0.1;
px = 0.95;
xtype = 1;
elite = 1;
nopt = 9;
ffunc = 1;
gray = 1;
%
%	Initialize GA DEMO
%
clc
home
fprintf('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX \n');
fprintf('  Binary-coded Genetic Algorithm Demo \n');
fprintf('  Ron Shaffer \n');
fprintf('  Naval Research Laboratory \n');
fprintf('  Version 1.1 \n');
fprintf('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX \n');
option = 0;

while option <= nopt
%
%	Display Current Settings
%
	prconfg(vars,psz,ngen,pm,px,xtype,elite,ffunc,gray);

	option = input('Enter Option (1-11) > ');
	if option < 1
		option = 10;
	end
	if option > 12
		option = 12;
	end
%
%	User choices
%
	if option == 1
		vars = input('Enter new chromosome length (5-30) > ');
		if vars < 5
			vars = 5;
		end
		if vars > 30
			vars = 30
		end
	elseif option == 2
		psz = input('Enter new population size (5-100) > ');
		if psz < 5
			psz = 5;
		end
		if psz > 100
			psz = 100;
		end
	elseif option == 3
		ngen = input('Enter maximum number of generations (1-100) > ');
		if ngen < 1
			ngen = 1;
		end
		if ngen > 100
			ngen = 100
		end
	elseif option == 4
		pm = input('Enter mutuation probability (0-1) > ');
		if pm < 0
			pm = 0;
		end
		if pm > 1
			pm = 1;
		end
	elseif option == 5
		px = input('Enter crossover probability (0-1) > ');
		if px < 0
			px = 0;
		end
		if px > 1
			px = 1;
		end
	elseif option == 6
		fprintf ('1  Single-point crossover \n');
		fprintf ('2  Two-point crossover \n');
		fprintf ('3  Uniform crossover \n');
		xtype = input('Enter crossover type (1-3) > ');
		if xtype < 0
			xtype = 1;
		end
		if xtype > 3
			xtype = 1;
		end
	elseif option == 7
		fprintf ('1  Elitist strategy On \n');
		fprintf ('2  Elitist strategy Off \n');
		elite = input('Enter choice (1 or 2) > ');
		if elite < 1
			elite = 1;
		end
		if elite > 2
			elite = 1;
		end
	elseif option == 8
		fprintf ('1 Simple summation function \n');
		fprintf ('2 Bohachevsky function \n');
		ffunc = input('Enter choice (1 or 2) > ');
		if ffunc < 1
			ffunc = 1;
		end
		if ffunc > 2
			ffunc = 2;
		end
	elseif option == 9
		fprintf ('1 Gray coding OFF \n');
		fprintf ('2 Gray coding ON \n');
		gray = input('Enter choice (1 or 2) > ');
		if gray < 1
			gray = 1;
		end
		if gray > 2
			gray = 2;
		end
	end
	clc
	home
end
%
% Start GA optimization
%
configuration = [vars psz ngen pm px xtype elite gray];
if option == 10
	[stats,pop,bestc] = genealg(configuration,1,ffunc);
elseif option == 11
	[stats,pop,bestc] = genealg(configuration,2,ffunc);
elseif option == 12
	break;
end
%
%	Plot Statistical Information about the Optimization
%

if (ishold) == 1
	hold off;
end
clf
%
% Mean and best fitness score for each generation
%

plot(stats(:,1),stats(:,4),'c',stats(:,1),stats(:,2),'g-')
title ('GA Optimization Statistics');
ylabel ('Fitness');
xlabel ('Generation #');
legend ('Best','Mean');
%
% Plot the frequency of the genes in the final population
%
figure
frq = sum(pop);
genenum = 1:vars;
bar(genenum,frq,'r');
title ('Frequency of Genes in Final Population');
xlabel ('Gene Number');
ylabel ('Frequency');
%
% End of GA DEMO
%
fprintf('***** Final Statistics ***** \n');
fprintf('Best chromosome:  ');
for i = 1:vars
	fprintf('%d',bestc(i));
end
fprintf('\n');
if ffunc == 2
	if gray == 1
		realvar = decodeb(bestc,2,1,-1);
	else
		realvar = decodeg(bestc,2,1,-1);
	end
		for i = 1:2
		fprintf('Variable # %d = %6.4f \n',i,realvar(i));
	end
end
bestscore = fitness(bestc,ffunc,1,-1,gray);
fprintf('Fitness Score:  %8.4f \n', bestscore); 
fprintf ('End of Genetic Algorithm Demo \n');
