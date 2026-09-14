function [ploss,mHt,vMinI]=F_JD_LDA_PLossVa(mQ,Q_lab,mCenters,vMD,dm) 
% Syntax: [ploss,mHt,vMinI]=F_JD_LDA_PLossVa(mQ,Q_lab,mCenters,vMD,dm); 
% 
% Compute pseudo-loss for AdaBoost.M2;
%
% Note: The only difference between F_JD_LDA_PLossVa() and F_JD_LDA_PLoss() is that, the
% former uses the Euclidean distance, while the latter uses the square
% distance, to get the distance-based hypothesis. The only one change
% appears in 'mDis=sqrt(mDis);'(line 41).
%
% [Input:]
% mQ: the query set.
% Q_lab: the index of the query set.
% mCenters: center or mean of each class.
% vMD: mislabel distribution of training samples.
% [Output:]
% ploss: the pseudo-loss at point (lambda,gamma).
% mHt: the hypothesis outputs.
% vMinI: sample labels assigned by current classifier.
% dm= similarity measure to be used. 1: euclidean, 2. cosine
% % 
% Author: Lu Juwei - Bell Canada Multimedia Lab, Dept. of ECE, U. of Toronto
% Created in 13 Dec 2002
% Modifed in 18 Feb 2003
% Modified in July 2007 by Tejaswini -- Option of measuring similarity by
% cosine similarity/inner product added. 

[DLdaNum,query_num]=size(mQ);
[classnum values]=array(Q_lab);

if dm==2
       temp2=sqrt(sum(mCenters.*mCenters));
end

   mDis=zeros(classnum,query_num);
   for i=1:query_num 
        test_data=mQ(:,i);
        test_data=kron(test_data,ones(1,classnum));

        if dm==1 % euclidean 
            distance = test_data - mCenters;
            t1 = sum(distance.*distance);
            mDis(:,i)=t1';
          %  mDis=sqrt(mDis); % Note here introduce a nonlinear transformation, added in 18 Feb 2003.
        end

        if dm==2 % cosine
            distance=test_data.*mCenters;
            distance=sum(distance,1);
            temp1=sqrt(sum(test_data.*test_data));
            distance=distance./temp1;
            distance=distance./temp2;
            mDis(:,i)=distance;
        end
    end

if dm==1
   mDis=sqrt(mDis); % Note here introduce a nonlinear transformation, added in 18 Feb 2003.
end

% - Normalize distance to [0,1] using linear re-scale.

[vMax,vMaxI]=max(mDis,[],1);
[vMin,vMinI]=min(mDis,[],1);
vNorm=vMax-vMin;


mHt=zeros(classnum,query_num);
for k=1:classnum
    mHt(k,:)=(vMax-mDis(k,:))./vNorm;
end

if dm==2
    mHt=1-mHt;
end
% - ********

ploss=0;
for i=1:query_num

    for k=1:classnum
            t=find(values(:,1)==Q_lab(i));
      ploss=ploss+vMD(k,i)*(1-mHt(t,i)+mHt(k,i)); % s'thg wrong here !!
    end
end

ploss=ploss/2;

vMinI=values(vMinI); 

