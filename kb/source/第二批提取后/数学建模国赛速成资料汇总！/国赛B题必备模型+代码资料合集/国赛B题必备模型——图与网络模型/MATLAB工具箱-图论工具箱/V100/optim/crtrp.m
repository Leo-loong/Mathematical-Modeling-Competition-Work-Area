function Chrom = crtrp(Nind,FieldDR);
% 参数一致性检验
   if nargin < 2, error('parameter FieldDR missing'); end
   if nargin > 2, nargin = 2; end
   [mN, nN] = size(Nind);
   [mF, Nvar] = size(FieldDR);
   if (mN ~= 1 & nN ~= 1), error('Nind has to be a scalar'); end
   if mF ~= 2, error('FieldDR must be a matrix with 2 rows'); end

   Range = rep((FieldDR(2,:)-FieldDR(1,:)),[Nind 1]);
   Lower = rep(FieldDR(1,:), [Nind 1]);
% 生成初始种群
% 每行包含一个个体, 每个变量的值均匀分布在上下边界区间内
   Chrom = rand(Nind,Nvar) .* Range + Lower;
