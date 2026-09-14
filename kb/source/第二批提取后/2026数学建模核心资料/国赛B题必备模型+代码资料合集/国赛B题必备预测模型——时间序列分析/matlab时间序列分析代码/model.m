function [dev1,dev2,dev3,R1,R2,sigma1,sigma2] = model(data1,pairid,nearid,m)
    mthrehold = 0;
    [n1,t,~] = size(data1);
    dev1 = nan(n1,t);
    dev2 = nan(n1,t);
    dev3 = nan(n1,t);
    R1 = zeros(n1,t);
    R2 = zeros(n1,t);
    sigma1 = zeros(n1,1);
    sigma2 = zeros(n1,1);
    for i = 1:n1
        [b,bint,r,~,stats] = regress(data1(i,:,4)',[ones(t,1),data1(i,[1,1:(end-1)],4)',...
                                                       data1(nearid(i,1:4),:,4)',...
                                                       ]);
        R1(i,:) = r;
        sigma1(i) = std(r,'omitnan');%stats(4);
        temp1 = find(abs(r)>(3*sqrt(stats(4))));
%         if ~isempty(temp1)
%                 for j = [i,pairid(i,1:2),nearid(i,1:2)]
%                     temp1(isnan(data1(j,min(max(temp1,1),119),4))) = [];
%                     temp1(isnan(data1(j,min(max(temp1-1,1),119),4))) = [];
%                     temp1(isnan(data1(j,min(max(temp1+1,1),119),4))) = [];
%                 end
%         end

        [b,bint,r,~,stats] = regress(data1(i,:,4)',[ones(t,1),data1(i,[1,1:(end-1)],4)']);
        R2(i,:) = r;
        sigma2(i) = std(r,'omitnan');%stats(4);
        temp2 = find(abs(r)>(3*sqrt(stats(4))));
%         if ~isempty(temp2)
%                 temp2(isnan(data1(i,min(max(temp2,1),119),4))) = [];
%                 temp2(isnan(data1(i,min(max(temp2-1,1),119),4))) = [];
%                 temp2(isnan(data1(i,min(max(temp2+1,1),119),4))) = [];
%         end
        temp3 = temp2;
        temp2 = temp2(ismember(temp2,temp1));

        dev1(i,1:length(temp1)) = temp1;
        dev2(i,1:length(temp2)) = temp2;
        dev3(i,1:length(temp3)) = temp3;
    end
    dev1(m<mthrehold,:) = nan;
    sum(sum(dev1>0))

    dev2(m<mthrehold,:) = nan;
    sum(sum(dev2>0))
    
    dev3(m<mthrehold,:) = nan;
    sum(sum(dev3>0))
end