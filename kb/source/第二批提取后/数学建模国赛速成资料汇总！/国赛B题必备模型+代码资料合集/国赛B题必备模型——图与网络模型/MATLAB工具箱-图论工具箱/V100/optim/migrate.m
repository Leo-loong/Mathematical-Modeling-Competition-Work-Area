function [Chrom, ObjV] = migrate(Chrom, SUBPOP, MigOpt, ObjV);
% 参数一致性检验
   if nargin < 2, error('Input parameter SUBPOP missing'); end
   if (nargout == 2 & nargin < 4), error('Input parameter ObjV missing'); end
   [Nind, Nvar] = size(Chrom);
   if length(SUBPOP) ~= 1, error('SUBPOP must be a scalar'); end
   if SUBPOP == 1, return; end
   if (Nind/SUBPOP) ~= fix(Nind/SUBPOP), error('Chrom and SUBPOP disagree'); end
   NIND = Nind/SUBPOP;  
   if nargin > 3, 
      [mO, nO] = size(ObjV);
      if nO ~= 1, error('ObjV must be a column vector'); end
      if Nind ~= mO, error('Chrom and ObjV disagree'); end
      IsObjV = 1;
   else IsObjV = 0; ObjV = [];
   end
   if nargin < 3, MIGR = 0.2; Select = 0; Structure = 0; end   
   if nargin > 2,
      if isempty(MigOpt), MIGR = 0.2; Select = 0; Structure = 0;
      elseif isnan(MigOpt), MIGR = 0.2; Select = 0; Structure = 0;
      else
         MIGR = NaN; Select = NaN; Structure = NaN;
         if length(MigOpt) > 3, error('Parameter MigOpt is too long'); end
         if length(MigOpt) >= 1, MIGR = MigOpt(1); end
         if length(MigOpt) >= 2, Select = MigOpt(2); end
         if length(MigOpt) >= 3, Structure = MigOpt(3); end
         if isnan(MIGR), MIGR =0.2; end
         if isnan(Select), Select = 0; end
         if isnan(Structure), Structure = 0; end
      end
   end
   
   if (MIGR < 0 | MIGR > 1), error('Parameter for migration rate must be a scalar in [0 1]'); end
   if (Select ~= 0 & Select ~= 1), error('Parameter for selection method must be 0 or 1'); end
   if (Structure < 0 | Structure > 2), error ('Parameter for structure must be 0, 1 or 2'); end
   if (Select == 1 & IsObjV == 0), error('ObjV for fitness-based migration needed');end

   if MIGR == 0, return; end
   MigTeil = max(floor(NIND * MIGR), 1);    % 迁移的个体数目

%子代之间进行迁移 
% 在每个子种群中根据最好的个体生成迁移矩阵
   % 清除存储矩阵
      ChromMigAll = [];
      if IsObjV == 1, ObjVAll = []; end
   % 由所有子种群的最优个体生成矩阵
      for irun = 1:SUBPOP
         % 排序ObjV
            if Select == 1,              
               [Dummy, IndMigSo]=sort(ObjV((irun-1)*NIND+1:irun*NIND));
            else       
               [Dummy, IndMigSo]=sort(rand(NIND, 1));
            end
         % 取出MigTeil个最优个体, 复制这些个体及其对应的目标函数值
            IndMigTeil=IndMigSo(1:MigTeil)+(irun-1)*NIND;
            ChromMigAll = [ChromMigAll; Chrom(IndMigTeil,:)];
            if IsObjV == 1, ObjVAll = [ObjVAll; ObjV(IndMigTeil,:)]; end
      end
   % 迁移
      for irun = 1:SUBPOP
        ChromMig = ChromMigAll;
        if IsObjV == 1, ObjVMig = ObjVAll; end
        if Structure == 1,       
        % 选择邻近子代的个体得到ChromMig 和ObjVMig
            popnum = [SUBPOP 1:SUBPOP 1];
            ins1 = popnum(irun); ins2 = popnum(irun + 2);
            InsRows = [(ins1-1)*MigTeil+1:ins1*MigTeil (ins2-1)*MigTeil+1:ins2*MigTeil];
            ChromMig = ChromMig(InsRows,:);
            if IsObjV == 1, ObjVMig = ObjVMig(InsRows,:); end
            elseif Structure == 2,   
               % 选择当代子代的个体得到ChromMig和ObjVMig
               popnum = [SUBPOP 1:SUBPOP 1];
               ins1 = popnum(irun);
               InsRows = (ins1-1)*MigTeil+1:ins1*MigTeil;
               ChromMig = ChromMig(InsRows,:);
               if IsObjV == 1, ObjVMig = ObjVMig(InsRows,:); end
            else                     
               % 从ChromMig和ObjVMig中删除当代子代的个体
               DelRows = (irun-1)*MigTeil+1:irun*MigTeil;
               ChromMig(DelRows,:) = [];
               if IsObjV == 1, ObjVMig(DelRows,:) = []; end
            end
         % 根据任意数目的排序向量生成索引   
            [Dummy,IndMigRa]=sort(rand(size(ChromMig,1),1));
         % 从任意向量中取出MigTeil个数
            IndMigN=IndMigRa((1:MigTeil)');
         % 复制MigTeil的个体到Chrom 和ObjV
            Chrom((1:MigTeil)+(irun-1)*NIND,:) = ChromMig(IndMigN,:);
            if IsObjV == 1, ObjV((1:MigTeil)+(irun-1)*NIND,:) = ObjVMig(IndMigN,:); end
end
