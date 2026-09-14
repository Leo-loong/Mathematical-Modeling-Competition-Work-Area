function meet_contraint_flag = isMeetConstraint(x)
	if nargin < 1
		x = [0.636,0.395,0.307];
	end
	meet_contraint_flag = 0;
	x1 = x(1);
	x2 = x(2);
	x3 = x(3);
	if all([x>=0,x<=1,x1*x1+2*x2*x2+3*x3*x3<=1])
		meet_contraint_flag = 1;
	end
end