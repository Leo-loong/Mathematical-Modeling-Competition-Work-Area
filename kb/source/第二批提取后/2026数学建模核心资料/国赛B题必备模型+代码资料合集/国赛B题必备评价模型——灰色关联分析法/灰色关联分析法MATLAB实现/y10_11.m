high=xlsread('yumi.xlsx','Sheet1','B2:B727');
low=xlsread('yumi.xlsx','Sheet1','C2:C727');
close=xlsread('yumi.xlsx','Sheet1','D2:D727');
open=xlsread('yumi.xlsx','Sheet1','E2:E727');
average=xlsread('yumi.xlsx','Sheet1','F2:F727');
volume=xlsread('yumi.xlsx','Sheet1','G2:G727');
positions=xlsread('yumi.xlsx','Sheet1','H2:H727');
date=xlsread('yumi.xlsx','Sheet1','A2:A727');

for i=1:2
    stop=30;
    for j=1:length(r{i})
        if r{i}(j)<-stop
            r{i}(j)=-stop;
        end
    end
    cumr{i}=cumsum(r{i});
    benchmark{i}=close(window{i}+2:end,1);
    x{i}=1:length(close(window{i}+2:end,1));
    ret{i}=cumr{i}+1000*ones(length(cumr{i}),1);
    [Maxdrawdown{i},dd{i}]=maxdrawdown(ret{i},'return');
end
for i=1:2
    r1=r{i};
    r2=r{i};
    for j=1:length(r{i})
        if r1(j)<0
            r1(j)=0;
        end
    end
    for j=1:length(r{i})
        if r2(j)>0
            r2(j)=0;
        end
    end
end
for i=1:2
    createfigure(x{i},cumr{i},benchmark{i},dd{i})
    hold off
end
    