function FitnV = ranking(ObjV, RFun, SUBPOP);
% 向量大小为Nind
   [Nind,ans] = size(ObjV);
   if nargin < 2, RFun = []; end
   if nargin > 1, if isnan(RFun), RFun = []; end, end
   if prod(size(RFun)) == 2,
      if RFun(2) == 1, NonLin = 1;
      elseif RFun(2) == 0, NonLin = 0;
      else error('Parameter for ranking method must be 0 or 1'); end
      RFun = RFun(1);
      if isnan(RFun), RFun = 2; end
   elseif prod(size(RFun)) > 2,
      if prod(size(RFun)) ~= Nind, error('ObjV and RFun disagree'); end
   end
   if nargin < 3, SUBPOP = 1; end
   if nargin > 2,
      if isempty(SUBPOP), SUBPOP = 1;
      elseif isnan(SUBPOP), SUBPOP = 1;
      elseif length(SUBPOP) ~= 1, error('SUBPOP must be a scalar'); end
   end
   if (Nind/SUBPOP) ~= fix(Nind/SUBPOP), error('ObjV and SUBPOP disagree'); end
   Nind = Nind/SUBPOP;  
  % 检查等级函数。如果需要使用默认值
   if isempty(RFun),
      % 选择压力为2的等级函数
         RFun = 2*[0:Nind-1]'/(Nind-1);
   elseif prod(size(RFun)) == 1
      if NonLin == 1,
         % 非线性等级函数
         if RFun(1) < 1, error('Selective pressure must be greater than 1');
         elseif RFun(1) > Nind-2, error('Selective pressure too big'); end
         Root1 = roots([RFun(1)-Nind [RFun(1)*ones(1,Nind-1)]]);
         RFun = (abs(Root1(1)) * ones(Nind,1)) .^ [(0:Nind-1)'];
         RFun = RFun / sum(RFun) * Nind;
      else
         %线性等级函数，且SP?[1,2]
         if (RFun(1) < 1 | RFun(1) > 2),
            error('Selective pressure for linear ranking must be between 1 and 2');
         end
         RFun = 2-RFun + 2*(RFun-1)*[0:Nind-1]'/(Nind-1);
      end
   end;
   FitnV = [];
%循环
for irun = 1:SUBPOP,
   % 复制实际子代的目标值
      ObjVSub = ObjV((irun-1)*Nind+1:irun*Nind);
      
%排序
      NaNix = isnan(ObjVSub);
      Validix = find(~NaNix);
      [ans,ix] = sort(-ObjVSub(Validix));
   % 建立索引向量
      ix = [find(NaNix) ; Validix(ix)];
   % 得到ObjV的排序结果
      Sorted = ObjVSub(ix);
   % 适应度分配
      i = 1;
      FitnVSub = zeros(Nind,1);
      for j = [find(Sorted(1:Nind-1) ~= Sorted(2:Nind)); Nind]',
         FitnVSub(i:j) = sum(RFun(i:j)) * ones(j-i+1,1) / (j-i+1);
         i =j+1;
      end
   % 最后返回没有排序的向量
      [ans,uix] = sort(ix);
      FitnVSub = FitnVSub(uix);
   % 添加FitnVSub到FitnV中
      FitnV = [FitnV; FitnVSub];
End
