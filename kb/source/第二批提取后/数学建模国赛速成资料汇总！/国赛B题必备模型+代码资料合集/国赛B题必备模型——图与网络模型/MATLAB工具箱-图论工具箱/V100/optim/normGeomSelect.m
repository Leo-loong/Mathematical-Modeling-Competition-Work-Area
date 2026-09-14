function[newPop] = normGeomSelect(oldPop,options)
q=options(2); 				% 选择最优的概率
e = size(oldPop,2); 			% xZome的长度, 即：numvars+fit
n = size(oldPop,1); 		% 种群中个体数目
newPop = zeros(n,e); 		% 为返回pop分配内存空间
fit = zeros(n,1); 			% 为返回选择概率分配内存
x=zeros(n,2); 			       
x(:,1) =[n:-1:1]'; 			
[y x(:,2)] = sort(oldPop(:,e)); 	
r = q/(1-(1-q)^n); 			% 分布归一化
fit(x(:,2))=r*(1-q).^(x(:,1)-1); 	% 生成选择概率 
fit = cumsum(fit); 			% 计算概率函数的累积和
rNums=sort(rand(n,1)); 		% 生成n个排序的任意数
fitIn=1; newIn=1; 			% 循环初始化
while newIn<=n 			% 生成n个新个体
  if(rNums(newIn)<fit(fitIn)) 		
    newPop(newIn,:) = oldPop(fitIn,:); 	 
    newIn = newIn+1; 		
  else
    fitIn = fitIn + 1; 		
  end
end
