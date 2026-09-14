[x,y] = meshgrid(-1:.1:1);
z = (x.^2) + (2 .* (y.^2)) - (0.3 .* (cos(3 .* pi .* x))) - (0.4 .* (cos(4 .* pi .* y))) + 0.7;
z = -z;
surf(x,y,z)
