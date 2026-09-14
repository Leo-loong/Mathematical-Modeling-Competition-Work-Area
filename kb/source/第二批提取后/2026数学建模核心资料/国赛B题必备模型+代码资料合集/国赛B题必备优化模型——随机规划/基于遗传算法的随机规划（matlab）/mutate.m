function pop = mutate(pop,g_para)
	chromosome = pop.chromosome;
	M = 100*max(pop.fit_value)*ones(1,g_para.chromosome_size);
	for m = 1:g_para.pop_size
		if rand() < g_para.mutation_probability
			meet_constraint_flag = 0;
			while meet_constraint_flag == 0
				new_chromosome = chromosome(m,:)+sign(rand(1,g_para.chromosome_size)-0.5).*M;
				meet_constraint_flag = isMeetConstraint(new_chromosome);
				M = M.*rand(1,g_para.chromosome_size);
			end
			pop.chromosome(m,:) = new_chromosome;
		end
		
	end
end