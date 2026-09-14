function pop = initPop(g_para)
	% 初始化种群
	chromosome_size = g_para.chromosome_size;
	pop_size = g_para.pop_size;
	chromosome = zeros(pop_size,chromosome_size);
	for m = 1:pop_size
		meet_constraint_flag = 0;
		while meet_constraint_flag == 0
			chromosome_ = rand(1,chromosome_size);
			meet_constraint_flag = isMeetConstraint(chromosome_);
		end
		chromosome(m,:) = chromosome_;
	end
	pop.chromosome = chromosome;
	pop.fit_value = zeros(pop_size,1);
end