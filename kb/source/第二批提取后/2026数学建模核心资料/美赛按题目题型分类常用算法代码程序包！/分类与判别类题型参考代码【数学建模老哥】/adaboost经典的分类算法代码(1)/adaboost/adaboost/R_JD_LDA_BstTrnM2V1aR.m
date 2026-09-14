%
function [vParams,vTrn_err,vTst_err,randomlist,stTstRecord,mTstHfin]=R_JD_LDA_BstTrnM2V1aR(X,X_lab,Q,Q_lab,nTrain,T,FeaDimRate,dm,vInitTrainInx)

% Syntax: [vParams,vTrn_err,vTst_err,randomlist,stTstRecord,mTstHfin]=R_JD_LDA_BstTrnM2V1aR(X,X_lab,Q,Q_lab,nC,nT,FeaDimRate,dm,vInitTrainInx);
%
% Juwei's D-LDA (JD-LDA) with Boosting for face recognition. In the scheme, AdaBoost.M2 is used.
%
% The version uses cross-validation through partitioning X into a training set and a validation set,
% because training error is always zero without the partition so that AdaBoost cannot continue.
% Also, the version modifies the non-null space of the between-class scatter matrix based on the feedback
% from the sample distribution vD in each iteration.
%
% Note: The only difference between F_JD_LDA_BstTrnM2V1a() and F_JD_LDA_BstTrnM2V1() is that, the
% former uses the Euclidean distance, while the latter uses the square
% distance, to get the distance-based hypothesis. For only two changes, see
% F_JD_LDA_PLossVa() and F_AssignLabelM2V2a().
%
% Database partition:
%                       Total database: [A] -> randomly partitioned into [B] and [C].
%                       /                 \
%           training set: [B] or X     test set: [C]
%           /               \
%  training set: [D]    Validation set: [E]
%  Initially [B] is randomly partitioned into [D] and [E], the following partitions are based
%  on the sample distribution of the previous iteration.
%
% [Input:]
% X: the training samples [nDim,nSamples], [B].
% X_lab: the class label of each sample in X.
% Q: the test samples, [C].
% Q_lab: the labels of the test samples.
% nTrain: number of samples used per subject for training the invidual
% learner
% T: number of iterations.
% nDLdaNum: number of features used.
% vInitTrainInx: initial partition on the training set, [D].
% dm: 1- euclidean distance, 2- cosine distance/inner product 
%
% [Output:]
% vParams: parameter [beta] found in T iterations of AdaBoost.
% vTrn_err: training error rate (in [B]) in each iteration.
% vTst_err: test error rate (in [C]) in each iteration.
% randomlist: initial [D], randomly chosen from [B], for training S_btw.
% stTstRecord.IndvTstErr: test error (in [C]) of indivdual weak learner in each iteration.
% stTstRecord.vMinTrainInx: the training set [D] with minimal test error based on min(IndvTstErr).

%   
% Author: Lu Juwei - Bell Canada Multimedia Lab, Dept. of ECE, U. of Toronto
% Created in 23 Dec 2002
% Modified in 30 Jan 2003
% Modified in 18 Feb 2003 - for producing version a.
% Modified in 20 August 2003

% Edited in June 2007, by Tejaswini Ganapathi. 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%THIS IS THE MAIN FUNCTION TO BE CALLED FOR THE BOOSTING ALGORITHM
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%






%

train_smp_num=size(X,2);
[classnum values1]=array(X_lab);
values=values1(:,1)';
test_smp_num=size(Q,2);
DLdaNum=FeaDimRate;

% **********************
% AdaBoost.M2 Training
% **********************
%
if nargin<4 %if all parameters are not passed to the function
    % - samples per subject for each individual learner
    nTrain=3; 
    % - number of iterations
    T=40;
    % - number of features used
    fFeaDimRate=20;
end

% initialisation
% - Training/test error at every iteration.
vTrn_err=zeros(1,T);
vTst_err=zeros(1,T);
vIndvTst_err=zeros(1,T);
minIndvTst_err=1;

% - Boosting parameters [Beta].
vParams=zeros(1,T);

% - Final hypothesis of the training/test samples,
mTrnHfin=zeros(classnum,train_smp_num);
mTstHfin=zeros(classnum,test_smp_num);

for t=1:T
    if t==1
        if nargin==9 %if initial training set is specified
            vTrainInx=vInitTrainInx;
        else
           % Initially, randomly partition the input samples into a training set and a validation set.
            [vTrainInx,vValidInx]=F_RandPartV4(X_lab,nTrain);
        end

        % - mislabel distribution of training samples
        vMD=ones(classnum,train_smp_num)/((classnum-1)*train_smp_num);
        j=1;
        for i=1:train_smp_num
            if X_lab(i)>values(j)
                j=j+1;
            end
            if X_lab(i)==values(j)
                vMD(j,i)=0;
            end

        end

        vD=sum(vMD,1); % initial pseudo sample distribution
        mA=ones(classnum,classnum)/(classnum^2);
        randomlist=vTrainInx;


    else
        % Update the sample distribution: vD
        vD=sum(vMD,1);
        % Select hard samples based on the distribution vD of the training samples, and the remaining
        % to form the validation set.
        [vTrainInx,vValidInx]=F_PartTrainValid(X_lab,nTrain,vD); % do this one!!
        % Update the weight matrix (mA) based on current sample distribution.
        [mA,nNonzeroClass]=F_GetWgtBTW(vD,X_lab,vClsLab_t);
    end

    % The first step is to find the complement space of null space of the between-class scatter matrix, U.
    XX=double(X(:,vTrainInx)); XX_lab=X_lab(:,vTrainInx);
    vDD=vD(vTrainInx);
    [U,mCenters]=F_wJD_LDAV2(XX,XX_lab,mA,vDD,DLdaNum); % weighting within-class scatter with vD.

    % Project all training/test samples into the subspace spanned by U.
    mXwgt=U*double(X);

    mQwgt=U*double(Q);
    clear('U','XX','XX_lab');

    % Compute pseudo loss of the whole training set, [B].
    [ploss_t,mHt_t,vClsLab_t]=F_JD_LDA_PLossVa(mXwgt,X_lab,mCenters,vMD,dm); % Similarity is found using Euclidean Distance. Normalised in (0,1)

    clear('mXwgt');

    beta_t=ploss_t/(1-ploss_t); % beta_t <= 1 resulting from er_t <= 0.5
    if beta_t==0 % abortion of the boosting loop when beta=0
        disp(['Abort loop due to er_t=0 when t=',num2str(t)]);
        iT=t-1;
        vParams=vParams(1:iT);

        vTrn_err=vTrn_err(1:iT);
        vTst_err=vTst_err(1:iT);
        stTstRecord=struct('IndvTstErr',{vIndvTst_err},'MinTrainInx',{vMinTrainInx});
        return;
    end


    for i=1:train_smp_num
        for j=1:classnum
            a=find(values==X_lab(i));
            vMD(j,i)=vMD(j,i)*beta_t^((1+mHt_t(a,i)-mHt_t(j,i))/2);
        end
    end
    vMD=vMD/sum(vMD(:));

    vParams(t)=beta_t;

    % - Compute training error based on current t iterations (learners).---

    mTrnHfin=mTrnHfin+log(1/beta_t)*mHt_t;
    [vMax,vMaxI]=max(mTrnHfin,[],1);

    vT1=values(vMaxI)-X_lab;
    vI1=find(vT1~=0);
    vTrn_err(t)=length(vI1)/train_smp_num; %% done till here !!

    % - Compute test error based on current t iterations (learners).
    [mHt,vTstClsLab]=F_AssignLabelM2V2a(mQwgt,Q_lab,mCenters); % modified in 18 Feb 2003 for ver a.
    mTstHfin=mTstHfin+log(1/beta_t)*mHt;
    [vMax,vMaxI]=max(mTstHfin,[],1);
    [temp values_p]=array(Q_lab);

    vT1=values(vMaxI)-Q_lab;
    vI1=find(vT1~=0);
    vTst_err(t)=length(vI1)/test_smp_num;

    vT1=vTstClsLab-Q_lab;
    vI1=find(vT1~=0);
    vIndvTst_err(t)=length(vI1)/test_smp_num;

    if vIndvTst_err(t)<minIndvTst_err
        minIndvTst_err=vIndvTst_err(t);
        vMinTrainInx=vTrainInx;
    end

    clear('mCenters','mQwgt','mHt','mHt_t','vTstClsLab');

    disp(['t=', num2str(t), ' iterations done !, DLdaNum=', num2str(DLdaNum),', TestCer=', num2str(vTst_err(t))]);
end

stTstRecord=struct('IndvTstErr',{vIndvTst_err},'MinTrainInx',{vMinTrainInx});
