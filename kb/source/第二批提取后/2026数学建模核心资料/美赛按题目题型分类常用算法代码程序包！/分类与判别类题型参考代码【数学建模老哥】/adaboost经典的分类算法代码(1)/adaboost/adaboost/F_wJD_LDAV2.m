function [DFLD_Trans,mWgtMeans,mTrnWgt]=F_wJD_LDAV2(TrainData,Train_lab,mA,vDD,DLdaNum)
%
% Syntax: [DFLD_Trans,mWgtMeans,mTrnWgt]=F_wJD_LDAV2(TrainData,Train_lab,mA,vDD,DLdaNum);
%
% This propramme implement weighted Juwei's D-LDA (wJD-LDA), which uses weighted 
% between-class scatter matrix, the weights (mA) are from the sample distribution vD.
%
% Difference from F_wJD_LDA(): the version weights within-class scatter matrix with
% vD as well.
%
% [Input:]
% TrainData: Input training data, should be a matrix, col number should be
%            the number of samples.
% Train_lab: label of each training sample.
% mA: the current weight matrix.
% vDD: the sample distribution on [D], a subset of vD (on [B]).
% DLdaNum[option]: number of d-lda features required.
% [Output:]
% DFLD_Trans: the feature space derived by wJD-LDA.
% mWgtMeans: Projection of class centers on DFLD_Trans.
% mTrnWgt: projection of TrainData on DFLD_Trans.
%
% Author: Lu Juwei - Bell Canada Multimedia Lab, Dept. of ECE, U. of Toronto
% Created in 13 Dec 2002
% Modified in 15 Dec 2002
% Edited in June 2007




VERY_SMALL=1e-3;

% We use vD for normalized vDD, but please NOTE that the vD here is different from the 
% the sample distribution vD on the training set: [B]. The vD here can be considered
% the sample distribution on the training set: [D]. See F_JD_LDA_BstTrnM2V1() for detail
% explaination on the database partitions.
vD=vDD/sum(vDD);

[sample_dim,sample_num]=size(TrainData);

[class_num values]=array(Train_lab);


mean_class=mean(TrainData,2);
eachclass_num=zeros(1,class_num);
mean_eachclass=zeros(sample_dim,class_num);
for j=1:class_num
    b=find(Train_lab==values(j));
    eachclass_num(j)=length(b);
    a=TrainData(:,b);
 	mean_eachclass(:,j)=mean(a,2);
end
clear('a');

% The first m_b eigenvectors corresponding to largest eigenvalues will be extracted
% from eigenvectors of Sb
m_b=class_num-1;

mSqrA=sqrt(mA);

%-- Added 05 Dec 2002, but may not be necessary.
a=find(mSqrA~=0);
mSqrA=mSqrA+min(mSqrA(a))*0.001;
%**

% - The first step is to extract features from weighted between-class scatter matrix.
% To calculate weighted between-class scatter matrix


for i=1:class_num
    m=kron(mean_eachclass(:,i),ones(1,class_num));
    t_b=m-mean_eachclass;
    vA=mSqrA(:,i);
    Phi_b(:,i)=(t_b*vA)*sqrt(eachclass_num(i)/sample_num);
end



clear('t_b');

Sb_t=Phi_b'*Phi_b; % evaluation of the Sb matrix

m_b=min([m_b rank(Sb_t)]);
[eigvec,eigval]=eig(Sb_t);
clear('Sb_t');
eigval=abs(diag(eigval)');		% changed in 14 May 2001, original: eigval=diag(eigval)';
[eigval,I]=sort(eigval);
eigval_Sb_t=fliplr(eigval); 
eigvec_Sb_t=fliplr(eigvec(:,I));
clear('eigvec','eigval');

% discard those with eigenvalues sufficient close to 0 and 
% extract first m_b eigenvectors corresponding to largest eigenvalues
%[x,J]=find(eigval_Sb_t<VERY_SMALL);
%eigvec_Sb(:,J)=[];

eigvec_Sb_t=eigvec_Sb_t(:,1:m_b);
eigval_Sb_t=eigval_Sb_t(:,1:m_b);

% eigenvectors of Sb
eigvec_Sb=Phi_b*eigvec_Sb_t;
clear('Phi_b','eigvec_Sb_t');


D_b=eigval_Sb_t.^(-1);
Z=eigvec_Sb*diag(D_b);
clear('eigvec_Sb','D_b','eigval_Sb_t');

% - The second step is to extract features from within-class scatter matrix.

mY=Z'*TrainData;
mMeans=Z'*mean_eachclass;
mU_Sw_U=zeros(m_b,m_b);
% Sw : the within-class scatter covariance matrix 
% Sw=zeros(rowTrain,rowTrain);
% Sw=Phi_w*Phi_w';
%Phi_w=zeros(sample_dim,sample_num);
j=1;
for i=1:class_num
    t=mY(:,j:j+eachclass_num(i)-1);
    m=kron(mMeans(:,i),ones(1,eachclass_num(i)));
    dt=sqrt(vD(j:j+eachclass_num(i)-1));
    b=(t-m)*diag(dt);
  	mU_Sw_U=mU_Sw_U+b*b'; 
 	j=j+eachclass_num(i); 
end 
clear('m','b','t','dt'); 
%mU_Sw_U=mU_Sw_U/sample_num;

%rankSw=rank(mU_Sw_U);
%if rankSw<m_b % If mU_Sw_U is singular, we use the total scatter
%   mU_St_U=mU_Sw_U+eye(m_b,m_b);
%   St_0EigVal_Num=m_b-rankSw;
%else % otherwise we use within-class scatter
%   mU_St_U=mU_Sw_U;
%   St_0EigVal_Num=0;
%end
mU_St_U=mU_Sw_U+eye(m_b,m_b);
clear('mU_Sw_U');

[eigvec,eigval]=eig(mU_St_U);
clear('mU_St_U');
eigval=abs(diag(eigval)');		% changed in 14 May 2001, original: eigval=diag(eigval)';
[eigval,I]=sort(eigval);
U_vec=eigvec(:,I);
clear('eigvec');

% extract first m_s eigenvectors corresponding to smallest eigenvalues
if nargin==5
    m_s=min([m_b DLdaNum]);
    U_vec=U_vec(:,1:m_s);
    eigval=eigval(1:m_s);
end
D_w=eigval.^(-1/2);

A=U_vec*diag(D_w);
DFLD_Trans=(Z*A)';

%A=(Z*U_vec)';
clear('Z','U_vec');

mWgtMeans=A'*mMeans;
mTrnWgt=A'*mY;
%DFLD_Trans=diag(D_w)*A;
%mWgtMeans=DFLD_Trans*mean_eachclass;
