function vars = decodeb(pop,nparam,maxval,minval,h2)
% DECODEB -- converts a binary coded chromosome to
% real number values for each variable
% pop:		population of binary coded chromosomes
% nvar:		number of real valued variables to be decoded
% maxval:	maximum real number value for each variable
% minval:	minimum real number value for each variable
% vars:		matrix of decoded real number variable settings (popsize,nparam)

[popsize,lchrome] = size(pop);

%
%	Split chromosome into sections for each variable
%

for u=1:nparam
 maxintval(u) = (2^h2(u))-1;

end
 range = maxval-minval;

for i = 1:popsize
	start = 1;
        fin = 0;
        tvars=0;
       	for j = 1:nparam
	  
             tvars(1:h2(j)) = pop(i,start:h2(j)+fin);
		start = start + h2(j);
                fin = fin + h2(j);
%
%		now decode binary number to real number (scale maxval to minval)

%
             
       	temp1 = 0;
        temp2 = 0;    
        temp3 = 2;
              for k = 1:h2(j)
	         	
			temp1 = temp1 +temp3^temp2 *tvars(h2(j)-k+1);
                 temp2 = temp2+1;
              end
            
%
%		Takes integer value and converts to a real number 
%	

		vars(i,j) = (range(j)*(temp1/maxintval(j))) + minval(j);	

	end
end

