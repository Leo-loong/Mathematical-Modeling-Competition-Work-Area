function [parent] = nonUnifMutate(parent,bounds,Ops)
cg=Ops(1); 				% 当前代
mg=Ops(3);               %代的最大数目
b=Ops(4);                    % 形状参数
df = bounds(:,2) - bounds(:,1); 	%变量范围
numVar = size(parent,2)-1; 		%变量数目
% Pick a variable to mutate randomly from 1 to number of vars
mPoint = round(rand * (numVar-1)) + 1;
md = round(rand); 			% 选择变异方向
if md 					%向上界变异
  newValue=parent(mPoint)+delta(cg,mg,bounds(mPoint,2)-parent(mPoint),b);
else 					%向下界变异
  newValue=parent(mPoint)-delta(cg,mg,parent(mPoint)-bounds(mPoint,1),b);
end
parent(mPoint) = newValue; 	% 得到一个子代个体
