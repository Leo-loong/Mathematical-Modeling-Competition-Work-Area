function prconfg(vars,psz,ngen,pm,px,xtype,elite,ffunc,gray)
% prconfg -- prints current GA configuration
%

fprintf('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX \n');
fprintf('  Current GA Configuration \n');
fprintf('1  Chromsosome Length		%d \n',vars);
fprintf('2  Population Size			%d \n',psz);
fprintf('3  Number of Generations		%d \n',ngen);
fprintf('4  Mutation Rate			%1.3f \n',pm);
fprintf('5  Crossover Rate			%1.3f \n',px);
if xtype == 1
	fprintf('6  Crossover Type:			Single \n');
end
if xtype == 2
	fprintf('6  Crossover Type:			Double \n');
end
if xtype == 3
	fprintf('6  Crossover Type:			Uniform \n');
end
if elite == 1
	fprintf('7  Elitist Operator:			On \n');
else
	fprintf('7  Elitist Operator:			Off \n');
end
if ffunc == 1
	fprintf('8  Function:			Simple \n');
else
	fprintf('8  Function:			Bohachevsky \n');
end
if gray == 1
	fprintf('9  Gray Coding:			Off \n');
else
	fprintf('9  Gray Coding:			On \n');
end
fprintf('10  Start GA Optimization (Full Printout) \n');
fprintf('11  Start GA Optimization (Minimal Printout) \n');
fprintf('12  Quit GA Demo \n');
fprintf('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX \n');
