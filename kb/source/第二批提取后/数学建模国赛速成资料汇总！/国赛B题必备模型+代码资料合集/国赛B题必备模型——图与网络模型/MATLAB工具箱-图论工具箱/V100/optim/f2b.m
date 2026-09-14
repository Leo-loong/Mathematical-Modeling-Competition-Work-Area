function [bval] = f2b(fval,bounds,bits)
scale=(2.^bits-1)./ (bounds(:,2)-bounds(:,1))'; %±‰¡ø∑∂Œß
numV=size(bounds,1);
cs=[0 cumsum(bits)];
bval=[];
for i=1:numV
  fval(i)=(fval(i)-bounds(i,1)) * scale(i);
  bval=[bval rem(floor(fval(i)*pow2(1-bits(i):0)),2)];
end
