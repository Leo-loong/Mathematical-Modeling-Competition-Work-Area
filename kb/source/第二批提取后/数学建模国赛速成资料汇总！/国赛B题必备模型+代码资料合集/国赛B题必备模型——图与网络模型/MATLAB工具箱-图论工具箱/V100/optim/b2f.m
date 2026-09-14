function [fval] = b2f(bval,bounds,bits)
scale=(bounds(:,2)-bounds(:,1))'./(2.^bits-1); %±‰¡ø∑∂Œß
numV=size(bounds,1);
cs=[0 cumsum(bits)];
for i=1:numV
  a=bval((cs(i)+1):cs(i+1));
  fval(i)=sum(2.^(size(a,2)-1:-1:0).*a)*scale(i)+bounds(i,1);
end
