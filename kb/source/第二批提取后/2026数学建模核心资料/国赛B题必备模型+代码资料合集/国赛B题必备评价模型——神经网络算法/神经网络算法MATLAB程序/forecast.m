function [output_fore]=forecast(w1,w2,b1,b2,input_test,inputps)
inputn_test=mapminmax('apply',input_test,inputps);
[~,L]=size(input_test);[midnum,~]=size(w1);
for i=1:L
    for j=1:midnum
        I(j)=inputn_test(:,i)'*w1(j,:)'+b1(j);
        Iout(j)=1/(1+exp(-I(j)));
    end
    
    fore(:,i)=w2'*Iout'+b2;
end
for i=1:L
    output_fore(i)=find(fore(:,i)==max(fore(:,i)));
end