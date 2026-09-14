    function [k,x,mu,val,mh]=newtlagr(x0,mu0,epsilon)
    %功能: 牛顿 - 拉格朗日法求解约束优化问题:
    %         min f(x), s.t. h_i(x)=0, i=1,2,..., l
    %输入: x0是初始点, mu0是乘子向量的初始值, epsilon是容许误差
    %输出: k是迭代次数, x, mu分别是近似最优解及相应的乘子向量,
    %        val是最优值, mh是约束函数的范数
    kmax=500;  %最大迭代次数
    n=length(x0);  l=length(mu0);
    beta=0.6;  sigma=0.2;
    x=x0;  mu=mu0;
    k=0; 
    while(k<kmax)
      dl=dla(x,mu);  %计算拉格朗日函数的梯度
      if(norm(dl)<epsilon), break; end  %检验终止准则
      N=N1(x,mu);  %计算拉格朗日矩阵
      dz=-N\dl;  %解方程组得搜索方向
      dx=dz(1:n);  du=dz(n+1:n+l);
      m=0; mk=0;
      while(m<20)   %求步长
          t1=beta^m;
          if(norm(dla(x+t1*dx,mu+t1*du))^2<=(1-sigma*t1)*norm(dl)^2)
              mk=m; break;
          end
          m=m+1;
      end
      x=x+beta^mk*dx;  mu=mu+beta^mk*du;
      k=k+1;
    end
    val=f1(x);
    mh=norm(h1(x));
    %========拉格朗日函数L(x,mu)=============%
    function l=la(x,mu)
    f=f1(x);                    %调用目标函数文件
    h=h1(x);                  %调用约束函数文件
    l=f-mu'*h;               %计算拉格朗日函数
    %========拉格朗日函数的梯度==============%
    function dl=dla(x,mu)
    df=df1(x);                %调用目标函数梯度文件
    h=h1(x);                  %调用约束函数文件
    dh=dh1(x);              %调用约束函数Jacobi矩阵文件
    dl=[df-dh'*mu; -h];  %计算拉格朗日函数梯度文件
    %========拉格朗日函数的Hesse阵============%
    function d2l=d2la(x,mu)
    d2f=d2f1(x);            %调用目标函数Hesse阵文件
    d2h=d2h1(x);          %调用约束函数二阶导数文件
    d2l=d2f-mu*d2h1;  %计算拉格朗日函数的Hesse阵
    %========拉格朗日矩阵N(x,mu)==============%
    function N=N1(x,mu)  
    l=length(mu);
    d2l=d2la(x,mu);   dh=dh1(x);
    N=[d2l, -dh'; -dh, zeros(l,l)];
    %========目标函数f(x)====================%
    function f=f1(x)
    s=-x(1)-x(2);
    f=1-x(1)^2+exp(s)+x(2)^2-2*x(1)*x(2)+exp(x(1))-3*x(2);
    %========约束函数 h(x)====================%
    function h=h1(x)
    h=x(1)^2+x(2)^2-5;
    %========目标函数f(x)的梯度================%
    function df=df1(x)
    s=-x(1)-x(2);
    df(1)=-2*x(1)-exp(s)-2*x(2)+exp(x(1));
    df(2)=-exp(s)+2*x(2)-2*x(1)-3;
    df=df(:);
    %========约束函数h(x)的Jacobi矩阵A(x)=========%
    function dh=dh1(x)
    dh=[2*x(1),2*x(2)];
    %========目标函数f(x)的Hesse阵==============%
    function d2f=d2f1(x)
    s=-x(1)-x(2);
    d2f=[-2+exp(s)+exp(x(1)), exp(s)-2;  
            exp(s)-2, exp(s)+2];
    %========约束函数h(x)的Hesse阵==============%
    function d2h =d2h1(x)
    d2h=[2 0;0 2];