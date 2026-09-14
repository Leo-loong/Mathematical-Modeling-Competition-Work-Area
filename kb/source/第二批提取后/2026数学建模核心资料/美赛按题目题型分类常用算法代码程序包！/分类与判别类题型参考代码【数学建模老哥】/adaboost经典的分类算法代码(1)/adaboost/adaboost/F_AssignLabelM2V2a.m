function [mHt,vMinI]=F_AssignLabelM2V2a(mQ,Q_lab,mCenters)
%
% Syntax: [mHt,vMinI]=F_AssignLabelM2V2a(mQ,Q_lab,mCenters);
% 
% Compute hypothesis for AdaBoost.M2 with JD-LDA, and assign labels to 
% the input samples using the input learner.
%
% Note: The only difference between F_AssignLabelM2V2a() and F_AssignLabelM2V2() is that, the
% former uses the Euclidean distance, while the latter uses the square
% distance, to get the distance-based hypothesis. The only one difference
% appears in 'mDis=sqrt(mDis);'(line 38).
%
% [Input:]
% mQ: the query set.
% Q_lab: the index of the query set.
% mCenters: center or mean of each class.
% [Output:]
% mHt: the hypothesis outputs.
% vMinI: sample labels assigned by current classifier.
%
% Author: Lu Juwei - Bell Canada Multimedia Lab, Dept. of ECE, U. of Toronto
% Created in 13 Dec 2002
% Modifed in 18 Feb 2003, see where marked as "added ...".
%

[DLdaNum,query_num]=size(mQ);
classnum=size(mCenters,2);

% discriminant scores
mDis=zeros(classnum,query_num);
for i=1:query_num
   test_data=mQ(:,i);
   test_data=kron(test_data,ones(1,classnum));
   distance = test_data - mCenters;
   t1 = sum(distance.*distance);
   mDis(:,i)=t1';
end

mDis=sqrt(mDis); % Note here introduce a nonlinear transformation, added in 18 Feb 2003.

% - Normalize distance to [0,1] using linear re-scale.
[vMax,vMaxI]=max(mDis,[],1);
[vMin,vMinI]=min(mDis,[],1);

vNorm=vMax-vMin;
mHt=zeros(classnum,query_num);
for k=1:classnum
    mHt(k,:)=(vMax-mDis(k,:))./vNorm;
end

[temp,values]=array(Q_lab);
vMinI=values(vMinI);
% - *********

% - Here we rescale distance using propabilistic distance.
%mHt=exp(-0.5*mDis);
%[vMin,vMinI]=max(mHt,[],1);
%for k=1:classnum
%    mHt(k,:)=mHt(k,:)./vMin;
%end
% - *********