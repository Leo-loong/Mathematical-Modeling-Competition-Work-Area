function pop = select(pop,g_para)
	% 以轮盘赌策略选择个体进行繁殖操作
	fit_value = pop.fit_value;
	pop_size = g_para.pop_size;
	chromosome = pop.chromosome;
	cum_prob = pop.cumulative_probability;
	for m = 1:pop_size
		pointer = rand();
		roulette = 0;
		for n = 1:pop_size
			roulette = roulette+cum_prob(n);
			if roulette >= pointer
				droppoint = n;
				break;
			end
		end
		pop.chromosome(m,:) = chromosome(droppoint,:);
		pop.fit_value(m,:) = fit_value(droppoint,:);
	end
end