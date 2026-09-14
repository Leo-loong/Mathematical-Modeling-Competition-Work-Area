function pop = crossover(pop,g_para)
	pop_size = g_para.pop_size;
	chromosome = pop.chromosome;
	for m = 1:pop_size
		if rand() < g_para.crossover_probability/2
			crossover_label1 = randi(pop_size);
			crossover_label2 = randi(pop_size);
			meet_constraint_flag = 0;
			while meet_constraint_flag == 0
				c = rand(1,g_para.chromosome_size);
				new_chromosome1 = c.*chromosome(crossover_label1,:)...
					+(1-c).*chromosome(crossover_label2,:);
				new_chromosome2 = c.*chromosome(crossover_label2,:)...
					+(1-c).*chromosome(crossover_label1,:);
				meet_constraint_flag = all([isMeetConstraint(new_chromosome1),...
					isMeetConstraint(new_chromosome2)]);
			end
			chromosome(crossover_label1,:) = new_chromosome1;
			chromosome(crossover_label2,:) = new_chromosome2;
		end
	end
	pop.chromosome = chromosome;
end