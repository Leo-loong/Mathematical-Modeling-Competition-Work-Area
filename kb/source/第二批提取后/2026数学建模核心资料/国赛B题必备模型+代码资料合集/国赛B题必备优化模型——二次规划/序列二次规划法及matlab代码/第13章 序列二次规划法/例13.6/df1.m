function df=df1(x)  %df1.m
     s=x(1)*x(2)*x(3)*x(4)*x(5);
     df(1)=s/(x(1))*exp(s)-3*(x(1)^3+x(2)^3+1)*x(1)^2;
     df(2)=s/(x(2))*exp(s)-3*(x(1)^3+x(2)^3+1)*x(2)^2;
     df(3)=s/(x(3))*exp(s);
     df(4)=s/(x(4))*exp(s);
     df(5)=s/(x(5))*exp(s);
     df=df(:);