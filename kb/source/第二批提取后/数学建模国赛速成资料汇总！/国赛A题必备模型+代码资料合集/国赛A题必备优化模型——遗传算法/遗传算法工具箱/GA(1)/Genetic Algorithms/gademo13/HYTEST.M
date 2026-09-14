function cost=hytest(vars,i)
w1=vars(i,1);
w2=vars(i,2);
w3=vars(i,3);
w4=vars(i,4);
w5=vars(i,5);
[t,x,y]=gear('cluluc1',12);
a1=0.3;
a2=0.3;
a3=0.2;
a4=0.1;
a5=0.1;
e1;
e2;
e3;
e4;
e5;
cost=(1./(a1*sum(abs(e1))+a2*sum(abs(e2))+a3*sum(abs(e3))+a4*sum(abs(e4))+a5*sum(abs(e5))));
