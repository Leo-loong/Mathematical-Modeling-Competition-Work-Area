    function [k,x,mu,val,P1]=lagsqp(x0,mu0,epsilon)
    %功能: 基于拉格朗日函数Hesse阵的SQP方法求解约束优化问题:
    %       min f(x),  s.t. h_i(x)=0,  i=1,2,...,l
    %输入: x0是初始点, mu0是乘子向量的初始值, epsilon是容许误差
    %输出: k是迭代次数, x, mu分别是近似最优解及相应的乘子向量,
    %      val是最优值, P1是罚函数的值
    maxk=500;  %最大迭代次数
    n=length(x0); l=length(mu0);
    beta=0.6; sigma=0.2; tau=1.55;
    x=x0; mu=mu0;
    k=0;
    while(k<maxk)
        P1=P(x,mu);  %计算罚函数的值
        if(P1<epsilon), break; end  %检验终止准则
        H=B(x,mu,tau);  % 计算KT矩阵
        c=df1(x);  %计算目标函数梯度
        Ae=dh1(x);  %计算约束函数的Jacobi矩阵
        be=-h1(x);  %计算约束函数
        [dx,lam]=qsubp(H,c,Ae,be);
        du=lam-mu-1.0/(2*tau)*dh1(x)*dx;
        m=0; mk=0;
        while(m<20)   %求步长
            if(P(x+beta^m*dx,mu+beta^m*du)<=(1-sigma*beta^m)*P1)
                mk=m; break;
            end
            m=m+1;
        end
        x=x+beta^mk*dx; mu=mu+beta^mk*du;
        k=k+1;
    end
    val=f1(x);
    P1=P(x,mu);
    %==========求解子问题==========================%
    function [x,mu1]=qsubp(H,c,Ae,be)
    ginvH=pinv(H);
    [m,n]=size(Ae);
    if(m>0)
        rb=Ae*ginvH*c + be;
        mu1=pinv(Ae*ginvH*Ae')*rb;
        x=ginvH*(Ae'*mu1-c);
    else
        x=-ginvH*c;
        mu1=zeros(m,1);
    end
    %==========拉格朗日函数L(x,mu)=====================%
    function l=la(x,mu)
    f=f1(x);                  %调用目标函数文件
    h=h1(x);                  %调用约束函数文件
    l=f-mu'*h;                % 计算乘子函数
    %==========拉格朗日函数的梯度======================%
    function dl=dla(x,mu)
    df=df1(x);                %调用目标函数梯度文件
    h=h1(x);                  %调用约束函数文件
    dh=dh1(x);                %调用约束函数Jacobi矩阵文件
    dl=[df-dh'*mu; -h];       %计算乘子函数梯度文件
    %==========罚函数P(x,mu)=========================%
    function s=P(x,mu)
    dl=dla(x,mu);
    s=norm(dl)^2;
    %==========拉格朗日函数的Hesse阵===================%
    function d2l=d2la(x,mu)
    d2f=d2f1(x);              %调用目标函数Hesse阵文件
    d2h=d2h1(x);              %调用约束函数二阶导数文件
    d2l=d2f-mu*d2h;
    %==========KKT矩阵B(x,mu)========================%
    function H=B(x,mu,tau)    %计算KKT矩阵
    d2l=d2la(x,mu);           %计算Hesse阵
    dh=dh1(x);                %约束函数的Jacobi矩阵
    H=d2l+1.0/(2*tau)*dh'*dh;
    %==============目标函数f(x)=======================%
    function f=f1(x)
    s=-x(1)-x(2);
    f=1-x(1)^2+exp(s)+x(2)^2-2*x(1)*x(2)+exp(x(1))-3*x(2);
    %==============约束函数h(x)=======================%
    function h=h1(x)
    h=x(1)^2+x(2)^2-5;
    %==============目标函数f(x)的梯度===================%
    function df=df1(x)
    s=-x(1)-x(2);
    df(1)=-2*x(1)-exp(s)-2*x(2)+exp(x(1));
    df(2)=-exp(s)+2*x(2)-2*x(1)-3;
    df=df(:);
    %==============约束函数h(x)的Jacobi矩阵A(x)=============%
    function dh=dh1(x)
    dh=[2*x(1),2*x(2)];
    %==============目标函数f(x)的Hesse阵=================%
    function d2f=d2f1(x)
    s=-x(1)-x(2);
    d2f=[-2+exp(s)+exp(x(1)),exp(s)-2; exp(s)-2,exp(s)+2];
    %==============约束函数h(x)的Hesse阵==================%
    function d2h =d2h1(x)
    d2h=[2 0 ; 0 2 ];