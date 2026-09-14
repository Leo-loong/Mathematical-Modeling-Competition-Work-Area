function df=df1(x)  
     s=-x(1)-x(2);
     df=[-exp(s)+2*x(1)+2*x(2)+2; -exp(s)+2*x(1)+2*x(2)+6];