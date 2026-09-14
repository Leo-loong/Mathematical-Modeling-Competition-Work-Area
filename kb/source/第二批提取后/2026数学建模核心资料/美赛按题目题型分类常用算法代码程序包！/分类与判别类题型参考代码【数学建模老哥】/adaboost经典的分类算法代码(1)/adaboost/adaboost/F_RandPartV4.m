function [train_inx,test_inx,nEachClass]=F_RandPartV4(mix_dbs_lab,num_eachTrain)

% Randomly partition a database into two sets: training set and test set.
%
% Syntax: [train_inx,test_inx,nEachClass]=F_RandPartV4(mix_dbs_lab,num_eachTrain)
% 
% Input: 
% mix_dbs_lab: label of each sample, a row vector
% num_eachTrain: training sample number per subject for each individual
% learner
% Output:
% train_inx: index of training set.
% test_inx: index of test set.
% nEachClass: number of each class.
%
% The version extracts <num_eachTrain> samples as training from each object in 
% a database extracted from the FERET database.
%
% Author: Lu Juwei - Bell Canada Multimedia Lab, Dept. of ECE, U. of Toronto
% Modified in 07 Oct 2002
% Modified in 28 Nov 2002
% Edited in June 2007


samplenum=length(mix_dbs_lab);
[classnum values]=array(mix_dbs_lab);

mid=num_eachTrain;

OriginInx=[1:samplenum];
nEachClass=zeros(1,classnum);
% Random partition the mix_dbs into two parts, train_dbs and test_dbs
train_inx=[];
test_inx=[];
    for i=1:classnum
        b=find(mix_dbs_lab==values(i));
        %b=find(mix_dbs_lab==i);
        nEachClass(i)=length(b);

        tmpindex=OriginInx(:,b);
        randomlist = F_Random(nEachClass(i));
        tmpindex=tmpindex(:,randomlist);

        train_inx=[train_inx tmpindex(:,1:mid)];
        test_inx=[test_inx tmpindex(:,mid+1:nEachClass(i))];
    end
