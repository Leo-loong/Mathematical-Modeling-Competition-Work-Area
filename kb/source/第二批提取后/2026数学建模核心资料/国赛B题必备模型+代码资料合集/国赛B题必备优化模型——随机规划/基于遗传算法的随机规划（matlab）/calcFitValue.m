function fit_value = calcFitValue(x)
	if nargin < 1
		x = [0.636,0.395,0.307];
	end
	x1 = x(1);
	x2 = x(2);
	x3 = x(3);
	fit_value = sqrt(x1)+sqrt(x2)+sqrt(x3);
end