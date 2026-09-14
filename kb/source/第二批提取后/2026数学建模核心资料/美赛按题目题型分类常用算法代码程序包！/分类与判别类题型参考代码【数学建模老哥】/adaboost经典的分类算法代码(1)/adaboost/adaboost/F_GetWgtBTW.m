function [mA,nNonzeroClass]=F_GetWgtBTW(vD,vD_lab,vClsLab)
%
% Syntax: [mA,nNonzeroClass]=F_GetWgtBTW(vD,vD_lab,vClsLab);
%
% This propramme update the weight matrix (mA) based on current sample distribution.
% mA will be used to weight pairwise between-class scatter matrix.
% The version is using the following equation to compute mA,
% $A_t(p,q)=\sum\limits_{j:h_t(\bfz_{pj})=q} {\hat D_t(\bfz_{pj} )}  + \sum\limits_{j:h_t(\bfz_{qj})=p } {\hat D_t(\bfz_{qj} )}$
%
% [Input:]
% vD: the sample distribution.
% vD_lab: the correct sample labels.
% vClsLab: the sample label assigned by previous weak learner.
% [Output:]
% mA: the updated weight matrix.
%
% Author: Lu Juwei - Bell Canada Multimedia Lab, Dept. of ECE, U. of Toronto
% Created in 03 Dec 2002
% 



[class_num, values]=array(vD_lab);

mB=zeros(class_num,class_num);

% Build weight matrix mA,
for p=1:class_num
    vP=find(vD_lab==values(p));
    vCls_P=vClsLab(vP);
    vD_P=vD(vP);
    for q=1:class_num
        vPQ=find(vCls_P==values(q));
        vD_PQ=vD_P(vPQ);
        mB(p,q)=sum(vD_PQ);
    end
end

mA=(mB+mB')/2;
        
nNonzeroClass=class_num;
