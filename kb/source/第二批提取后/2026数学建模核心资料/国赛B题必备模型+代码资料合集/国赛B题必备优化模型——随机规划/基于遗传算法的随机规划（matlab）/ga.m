function ga
	clc
	g_para = setGlobalParameter();
	pop = initPop(g_para);
	best_fit_value = -inf;
	for k = 1:g_para.max_iter
		g_para.k = k;
		pop = evaluateChromosome(pop,g_para);
		[best_fit_value_,best_chromosome_label] = max(pop.fit_value);
		fprintf('%d:%.3f\n',k,best_fit_value_);
		if best_fit_value_ > best_fit_value
			best_fit_value = best_fit_value_;
			best_x = pop.chromosome(best_chromosome_label,:);
		end
		pop = select(pop,g_para);
		pop = crossover(pop,g_para);
		pop = mutate(pop,g_para);
	end
	disp(best_x);
	disp(best_fit_value);
end