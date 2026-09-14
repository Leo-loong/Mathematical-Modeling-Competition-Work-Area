function [train_inx,test_inx,vDclass,nEachClass]=F_PartTrainValid(mix_dbs_lab,num_eachTrain,vD)

% Partition a database into two sets: training set and validation set based
% on the sample distribution produced during AdaBoosting process.
%
% Syntax: [train_inx,test_inx,vDclass,nEachClass]=F_PartTrainValid(mix_dbs_lab,num_eachTrain,vD)
% 
% Input: 
% mix_dbs_lab: label of each sample, a row vector
% num_eachTrain: training sample number per subject to be created
% vD: the sample distribution
% Output:
% train_inx: index of training set.
% test_inx: index of test set.
% vDclass: the class distribution, probility sum of each class from vD
% nEachClass: number of each class.
%
% Author: Lu Juwei - Bell Canada Multimedia Lab, Dept. of ECE, U. of Toronto
% Created in 28 Nov 2002
%


samplenum=length(mix_dbs_lab);


[classnum values]=array(mix_dbs_lab);
mid=num_eachTrain; 
disp(['mid=' num2str(mid)]);
OriginInx=[1:samplenum];
nEachClass=zeros(1,classnum);
vDclass=zeros(1,classnum);
% Random partition the mix_dbs into two parts, train_dbs and test_dbs
train_inx=[];
test_inx=[];
for i=1:classnum
   	b=find(mix_dbs_lab==values(i));
    nEachClass(i)=length(b);
    
    tmpindex=OriginInx(:,b);
    t1=vD(:,b);
    vDclass(i)=sum(t1);
    [t2,J]=sort(t1);
    tmpindex=fliplr(tmpindex(:,J));
      
    train_inx=[train_inx tmpindex(:,1:mid)];
    test_inx=[test_inx tmpindex(:,mid+1:nEachClass(i))];
end
