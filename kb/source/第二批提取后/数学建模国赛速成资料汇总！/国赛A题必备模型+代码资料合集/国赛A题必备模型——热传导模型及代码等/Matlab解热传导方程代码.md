Sample MATLAB codes
1.
%Newton Cooling Law
clear; close all; clc;
h = 1;
T(1) = 10; %T(0)
error = 1;
TOL = 1e-6;
k = 0;
dt = 1/10;
while error > TOL,
k = k+1;
T(k+1) = h*(1-T(k))*dt+T(k);
error = abs(T(k+1)-T(k));
end
t = linspace(0,dt*(k+1),k+1);
plot(t,T),hold on, plot(t,1,'r-.')
xlabel('Time'),ylabel('Temperature'),
title(['T_0 = ',num2str(T(1)), ',    T_\infty = 1']),
legend('Cooling Trend','Steady State')
2.
%Boltzman Cooling Law
clear; close all; clc;
h = 1;
T(1) = 10; %T(0)
error = 1;
TOL = 1e-6;
k = 0;
dt = 1/10000;
while error > TOL,
k = k+1;
T(k+1) = h*(1-(T(k))^4)*dt+T(k);
error = abs(T(k+1)-T(k));
end
t = linspace(0,dt*(k+1),k+1);
plot(t,T),hold on, plot(t,1,'r-.')
xlabel('Time'),ylabel('Temperature'),
title(['T_0 = ',num2str(T(1)), ',    T_\infty = 1']),
legend('Cooling Trend','Steady State')
3.
%Fourier Heat conduction
clear; close all; clc;
h = 1;n = 11;
T = ones(n,1); Told = T;
T(1) = 1; %Left boundary
T(n) = 10; %Right boundary
x = linspace(0,1,n);
dx = x(2)-x(1);
dt = dx^2/3; %cfl condition
error = 1;
TOL = 1e-6;
k = 0;
while error > TOL,
Told = T;
k = k+1;
for i = 2:n-1
T(i) = dt*(Told(i+1)-2*Told(i)+Told(i-1))/dx^2+Told(i);
end
error = max(abs(T-Told));
if mod(k,5)==0, out(k,:) = T; end
end
plot(x,out)
xlabel('x'),ylabel('Temperature'),
title(['Fourier Heat Conduction']),
%legend('Cooling Trend','Steady State')
4. 2D Heat Equation
%2D Heat Equation.
clear; close all; clc
n = 10;  %grid has n - 2 interior points per dimension (overlapping)
x = linspace(0,1,n); dx = x(2)-x(1); y = x; dy = dx;
TOL = 1e-6;
T = zeros(n);
T(1,1:n) = 10; %TOP
T(n,1:n) = 1;  %BOTTOM
T(1:n,1) = 1;  %LEFT
T(1:n,n) = 1;  %RIGHT
dt = dx^2/4;
error = 1; k = 0;
while error > TOL
    k = k+1;
      Told = T;
      for i = 2:n-1
          for j = 2:n-1
          T(i,j) = dt*((Told(i+1,j)-2*Told(i,j)+Told(i-1,j))/dx^2 ...
                  + (Told(i,j+1)-2*Told(i,j)+Told(i,j-1))/dy^2) ...
                  + Told(i,j);
          end
      end
      error = max(max(abs(Told-T)));
endsubplot(2,1,1),contour(x,y,T),
title('Temperature (Steady State)'),xlabel('x'),ylabel('y'),colorbar
subplot(2,1,2),pcolor(x,y,T),shading interp,
title('Temperature (Steady State)'),xlabel('x'),ylabel('y'),colorbar
5. Wave Translation
%Oscillations - translation left and right
clear; close all; clc;
for c = [1 -1]
cc = 0;
n = 261;
x = linspace(0,13,n);
u = zeros(n,1);
u(121:141) = sin(pi*x(121:141));
dx = x(2)-x(1);
dt = dx;
error = 1;
TOL = 1e-6;
k = 0;
while k < 110
uold = u;
k = k+1;
for i = 2:n-1
   if c == 1, u(i) = dt*c*(uold(i+1)-uold(i))/dx+uold(i); end %c = 1
   if c == -1, u(i) = dt*c*(uold(i)-uold(i-1))/dx+uold(i); end %c = -1
end
error = max(abs(u-uold));
if mod(k,10)==0, cc = cc+1; out(cc,:) = u;
end
end
if c == 1
subplot(2,1,1),
for hh = 1:cc
plot(x,out(hh,:)+hh),hold on,
end
u = zeros(n,1);
u(121:141) = sin(pi*x(121:141)); plot(x,u)
xlabel('u(x)'),ylabel('Time'),
title('Translation to the Left')
elseif c == -1
subplot(2,1,2),
for hh = 1:cc
plot(x,out(hh,:)+hh),hold on,
end
u = zeros(n,1);
u(121:141) = sin(pi*x(121:141)); plot(x,u)
xlabel('u(x)'),ylabel('Time'),
title('Translation to the Right')
end
end
6.%wave equation
clear; close all; clc;
c = 1;
n = 21;
x = linspace(0,1,n);
dx = 1/(n-1);
dt = dx;
u(:,1) = sin(pi*x);
u(1,2) = 0;
for i = 2:n-1
u(i,2) = 0.5*(dt^2*c^2*(u(i+1,1)-2*u(i,1)+u(i-1,1))/dx^2+2*u(i,1));
end
u(n,2) = 0;
error = 1; k = 1;
while k < 100
k = k+1;
u(1,k+1) = 0;
for i = 2:n-1
u(i,k+1) = dt^2*c^2*(u(i+1,k)-2*u(i,k)+u(i-1,k))/dx^2+2*u(i,k)-u(i,k-1);
end
u(n,k+1) = 0;
end
plot(x,u), xlabel('x'),ylabel('y')
俌	g礝Cg鲖T鹼JT鍂 Rda"宍O霳剉MT

.

.

緗罷

緗罷

.

緗罷

.

.

緗罷

緗罷

.

緗罷

.

.

緗罷

緗罷

.

緗罷

.

.

緗罷

緗罷

.

緗罷
