function pop = evaluateChromosome(pop,g_para)
	% º∆À„  ”¶÷µ
	for m =  1:g_para.pop_size
		pop.fit_value(m) = calcFitValue(pop.chromosome(m,:));
		eval(m) = g_para.a*(1-g_para.a)^(m-1);
	end
	
	pop.cumulative_probability = eval/sum(eval);
	
	[~,max2min_label] = sort(pop.fit_value,'descend');
	pop.chromosome = pop.chromosome(max2min_label,:);
	pop.fit_value = pop.fit_value(max2min_label,:);
end