function MatOut = rep(MatIn,REPN)
% 输入矩阵大小
   [N_D,N_L] = size(MatIn);
% 计算
   Ind_D = rem(0:REPN(1)*N_D-1,N_D) + 1;
   Ind_L = rem(0:REPN(2)*N_L-1,N_L) + 1;
% 生成输出矩阵
   MatOut = MatIn(Ind_D,Ind_L);
