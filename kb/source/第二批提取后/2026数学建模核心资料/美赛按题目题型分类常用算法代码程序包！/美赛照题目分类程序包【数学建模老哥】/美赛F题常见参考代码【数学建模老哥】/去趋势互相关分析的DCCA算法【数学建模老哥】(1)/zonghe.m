data1=dlmread('E:\fMT150200.txt','\t',[1,0,3000,0])
data2=dlmread('E:\fMT150200.txt','\t',[1,1,3000,1])

  %12行-23行作用？？？

% time=input('Enter Time Length: ');
% tstep=input('Enter Time Step: ');
time=3;
tstep=0.04;
nd=length(data1);
if floor(log10(nd))>=time
    %划分时间序列
    %Sample time seris
    t=1:tstep:time;  
    %即t<N的目的
   
   n=zeros(1,length(t));
    for ii=1:length(t)
        n(ii)=10^t(ii);
    end
    n=floor(n);
    n=n';


    len=length(n);
    Fn=zeros(len,1);

    
    %Calculation of DFA, q=1.
    for ii=1:len
        Fn(ii)=DFAq(data1,n(ii),1);
    end


    p=polyfit(log10(n),log10(Fn),1);


%      plot(n,Fn(:,1),'o');

    % Curve fitting
    x=n;
    y=p(2)+p(1)*log10(x);
    for ii=1:len
        y(ii)=10^y(ii);
    end
    hold on
    plot(x,y,'b');


    xlabel('n','FontSize',14)
    ylabel('F(n)','FontSize',14)
    set(gca,'XSCALE','log');
    set(gca,'YSCALE','log');

    fprintf('Hurst Exponent1 is: %f \n',p(1))
    
    
    
    
    
     %Calculation of DFA2, q=1. 
     for ii=1:len
        Fn(ii)=DFAq(data2,n(ii),1);
    end


    p=polyfit(log10(n),log10(Fn),1);

%     plot(n,Fn(:,1),'o');

    % Curve fitting
    x=n;
    y=p(2)+p(1)*log10(x);
    for ii=1:len
        y(ii)=10^y(ii);
    end
    hold on
    plot(x,y,'b');


    xlabel('n','FontSize',14)
    ylabel('F(n)','FontSize',14)
    set(gca,'XSCALE','log');
    set(gca,'YSCALE','log');

    fprintf('Hurst Exponent2 is: %f \n',p(1))
    
    
    
    
    %计算DCCA, q=1.
    for ii=1:len
        Fn(ii)=DCCA(data1,data2,n(ii),1);
    end


    p=polyfit(log10(n),log10(Fn),1);

% 
%     plot(n,Fn,'*');
% 
%     %曲线拟合
    x=n;
    y=p(2)+p(1)*log10(x);
    for ii=1:len
        y(ii)=10^y(ii);
    end
    hold on
    plot(x,y,'k');


    xlabel('n','FontSize',14)
    ylabel('F(n)','FontSize',14)
    set(gca,'XSCALE','log');
    set(gca,'YSCALE','log');

    fprintf(' Exponent is: %f \n',p(1))
    

else
    disp('错误: time lenght 应小于log([size(data)])');
  end