
function Fn=DCCA(data1,data2,s,q)
      %Dividing Time Seris
       N=length(data1);
       n=floor(N/s)   
       Nf=n*s;
       y=zeros(Nf,1);
       Yn=zeros(Nf,1);
       
       coef1=zeros(n,q+1);
       coef2=zeros(n,q+1);
 
            ave1=mean(data1(1:Nf));
            ave2=mean(data2(1:Nf));
       for ii=1:Nf
           %数据去趋势
           y1(ii)=sum(data1(1:ii)-ave1);
           y2(ii)=sum(data2(1:ii)-ave2);
         
       end
       y=y';
       for jj=1:n
           %Calculating Coefficients for Linear Trend
           coef1(jj,:)=polyfit(1:s,y1(((jj-1)*s+1):jj*s),q);
           coef2(jj,:)=polyfit(1:s,y2(((jj-1)*s+1):jj*s),q);
       end
       for jj=1:n
           Yn1(((jj-1)*s+1):jj*s)=polyval(coef1(jj,:),1:s);
           Yn2(((jj-1)*s+1):jj*s)=polyval(coef2(jj,:),1:s);
       end
       
       Fn2=sum((y1-Yn1).*(y2-Yn2))/Nf;
 
       
       Fn=sqrt(Fn2);

       

          
       