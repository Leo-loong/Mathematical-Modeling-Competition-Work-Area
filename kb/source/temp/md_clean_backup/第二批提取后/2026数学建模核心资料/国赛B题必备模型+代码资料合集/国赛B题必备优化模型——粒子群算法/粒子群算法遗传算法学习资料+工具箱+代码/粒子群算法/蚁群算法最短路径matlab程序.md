蚁群算法最短路径通用Matlab程序
下面的程序是蚁群算法在最短路中的应用，稍加扩展即可应用于机器人路径规划
function [ROUTES,PL,Tau]=ACASP(G,Tau,K,M,S,E,Alpha,Beta,Rho,Q)
%% ---------------------------------------------------------------
%  ACASP.m
%  蚁群算法动态寻路算法
% ChengAihua,PLA Information Engineering University,ZhengZhou,China
%  Email:aihuacheng@gmail.com
%  All rights reserved
%% ---------------------------------------------------------------
%  输入参数列表
%  G        地形图为01矩阵，如果为1表示障碍物
%  Tau      初始信息素矩阵（认为前面的觅食活动中有残留的信息素）
%  K        迭代次数（指蚂蚁出动多少波）
%  M        蚂蚁个数（每一波蚂蚁有多少个）
%  S        起始点（最短路径的起始点）
%  E        终止点（最短路径的目的点）
%  Alpha    表征信息素重要程度的参数
%  Beta     表征启发式因子重要程度的参数
%  Rho      信息素蒸发系数
%  Q        信息素增加强度系数
%
%  输出参数列表
%  ROUTES   每一代的每一只蚂蚁的爬行路线
%  PL       每一代的每一只蚂蚁的爬行路线长度
%  Tau      输出动态修正过的信息素
%% --------------------变量初始化----------------------------------
%load
D=G2D(G);
N=size(D,1);%N表示问题的规模（象素个数）
MM=size(G,1);
a=1;%小方格象素的边长
Ex=a*(mod(E,MM)-0.5);%终止点横坐标
if Ex==-0.5
    Ex=MM-0.5;
end
Ey=a*(MM+0.5-ceil(E/MM));%终止点纵坐标
Eta=zeros(1,N);%启发式信息，取为至目标点的直线距离的倒数
%下面构造启发式信息矩阵
for i=1:N
    if ix==-0.5
        ix=MM-0.5;
    end
    iy=a*(MM+0.5-ceil(i/MM));
    if i~=E
        Eta(1,i)=1/((ix-Ex)^2+(iy-Ey)^2)^0.5;
    else
        Eta(1,i)=100;
    end
end
ROUTES=cell(K,M);%用细胞结构存储每一代的每一只蚂蚁的爬行路线
PL=zeros(K,M);%用矩阵存储每一代的每一只蚂蚁的爬行路线长度
%% -----------启动K轮蚂蚁觅食活动，每轮派出M只蚂蚁--------------------
for k=1:K
    disp(k);
    for m=1:M
%%     第一步：状态初始化
        W=S;%当前节点初始化为起始点
        Path=S;%爬行路线初始化
        PLkm=0;%爬行路线长度初始化
        TABUkm=ones(1,N);%禁忌表初始化
        TABUkm(S)=0;%已经在初始点了，因此要排除
        DD=D;%邻接矩阵初始化
%%     第二步：下一步可以前往的节点
        DW=DD(W,:);
        DW1=find(DW
        for j=1:length(DW1)
            if TABUkm(DW1(j))==0
                DW(j)=inf;
            end
        end
        LJD=find(DW
        Len_LJD=length(LJD);%可选节点的个数
%%     觅食停止条件：蚂蚁未遇到食物或者陷入死胡同
        while W~=E&&Len_LJD>=1
%%         第三步：转轮赌法选择下一步怎么走
            PP=zeros(1,Len_LJD);
            for i=1:Len_LJD
                PP(i)=(Tau(W,LJD(i))^Alpha)*(Eta(LJD(i))^Beta);
            end
            PP=PP/(sum(PP));%建立概率分布
            Pcum=cumsum(PP);
            Select=find(Pcum>=rand);
%%         第四步：状态更新和记录
            Path=[Path,to_visit];%路径增加
            PLkm=PLkm+DD(W,to_visit);%路径长度增加
            W=to_visit;%蚂蚁移到下一个节点
            for kk=1:N
                if TABUkm(kk)==0
                    DD(W,kk)=inf;
                    DD(kk,W)=inf;
                end
            end
            TABUkm(W)=0;%已访问过的节点从禁忌表中删除
            for j=1:length(DW1)
                if TABUkm(DW1(j))==0
                    DW(j)=inf;
                end
            end
            LJD=find(DW
            Len_LJD=length(LJD);%可选节点的个数
        end
%%     第五步：记下每一代每一只蚂蚁的觅食路线和路线长度
        ROUTES{k,m}=Path;
        if Path(end)==E
            PL(k,m)=PLkm;
        else
            PL(k,m)=inf;
        end
    end
%% 第六步：更新信息素
    Delta_Tau=zeros(N,N);%更新量初始化
    for m=1:M
        if PL(k,m)            ROUT=ROUTES{k,m};
            TS=length(ROUT)-1;%跳数
            PL_km=PL(k,m);
            for s=1:TS
        ؀ࠦ࡬࡮คฆ ☀㩢㪘㪚㭈㭊㭌㭎㭐㭜㭞㮒㮖㮚㮨㮪����볍벲베鏍瞃鎃幥ᔌ뉨頄ᘀ뉨頄ᘣ뉨頄䈀Ī䩃䩏䩑䩞䩡桰㌳3ᘖ뉨頄㰀脈⩂愁ᕊ瀀≨∢̟jᘀ뉨頄㰀脈⩂唁Ĉ䩡桰∢"ᘙ뉨頄㰀脈⩂愁ᕊ漀Ĩ桰∢"̢jᔀ뉨頄ᘀ뉨頄䈀Īࡕ愁ᕊ瀀≨∢ᘓ뉨頄䈀Ī䩡桰∢"̜jᘀ뉨頄䈀Īࡕ愁ᕊ瀀≨∢唃Ĉᘖ뉨頄䈀Ī䩡⡯瀁≨∢ᘢ뉨頄䈀Ī䩏䩑䩞䩡⡯瀁≨∢ᔨ뉨頄ᘀ뉨頄䈀Ī䩃 䩏䩐䩡 ⡯瀁㍨㌳ᘀ؀ࠦ࡮ฆ㩤㪘㭐㮚㮦㮨㮪î�Ô퐀Ô퐀Î뼀º렀ĀЀ␃愀$฀␃ഀᇆԀỲἲᾂῒ•愀$嬀Ĥ摧ҲЀ摧Ҳ̀$萏ﺙ萑Ļ␱嘁啄埿附帀馄惾㮄愁$摧Ҳ̀Ĥ萏ﺛꐔĸ␱夁摄帀鮄懾Ĥ摧Ҳ਀؀㮪ýЄĀā        x=ROUT(s);
                Delta_Tau(x,y)=Delta_Tau(x,y)+Q/PL_km;
                Delta_Tau(y,x)=Delta_Tau(y,x)+Q/PL_km;
            end
        end
    end
    Tau=(1-Rho).*Tau+Delta_Tau;%信息素挥发一部分，新增加一部分
end
%% ---------------------------绘图--------------------------------
plotif=1;%是否绘图的控制参数
if plotif==1
    %绘收敛曲线
    meanPL=zeros(1,K);
    minPL=zeros(1,K);
    for i=1:K
        PLK=PL(i,:);
        Nonzero=find(PLK
        PLKPLK=PLK(Nonzero);
        meanPL(i)=mean(PLKPLK);
        minPL(i)=min(PLKPLK);
    end
    figure(1)
    plot(minPL);
    hold on
    plot(meanPL);
    grid on
    title('收敛曲线（平均路径长度和最小路径长度）');
    xlabel('迭代次数');
    ylabel('路径长度');
    %绘爬行图
    figure(2)
    axis([0,MM,0,MM])
    for i=1:MM
        for j=1:MM
            if G(i,j)==1
                x1=j-1;y1=MM-i;
                x2=j;y2=MM-i;
                x3=j;y3=MM-i+1;
                x4=j-1;y4=MM-i+1;
                fill([x1,x2,x3,x4],[y1,y2,y3,y4],[0.2,0.2,0.2]);
                hold on
            else
                x1=j-1;y1=MM-i;
                x2=j;y2=MM-i;
                x3=j;y3=MM-i+1;
                x4=j-1;y4=MM-i+1;
                fill([x1,x2,x3,x4],[y1,y2,y3,y4],[1,1,1]);
                hold on
            end
        end
    end
    hold on
    ROUT=ROUTES{K,M};
    LENROUT=length(ROUT);
    Rx=ROUT;
    Ry=ROUT;
    for ii=1:LENROUT
        Rx(ii)=a*(mod(ROUT(ii),MM)-0.5);
        if Rx(ii)==-0.5
            Rx(ii)=MM-0.5;
        end
        Ry(ii)=a*(MM+0.5-ceil(ROUT(ii)/MM));
    end
    plot(Rx,Ry)
end
plotif2=1;%绘各代蚂蚁爬行图
if plotif2==1
    figure(3)
    axis([0,MM,0,MM])
    for i=1:MM
        for j=1:MM
            if G(i,j)==1
                x1=j-1;y1=MM-i;
                x2=j;y2=MM-i;
                x3=j;y3=MM-i+1;
                x4=j-1;y4=MM-i+1;
                fill([x1,x2,x3,x4],[y1,y2,y3,y4],[0.2,0.2,0.2]);
                hold on
            else
                x1=j-1;y1=MM-i;
                x2=j;y2=MM-i;
                x3=j;y3=MM-i+1;
                x4=j-1;y4=MM-i+1;
                fill([x1,x2,x3,x4],[y1,y2,y3,y4],[1,1,1]);
                hold on
            end
        end
    end
    for k=1:K
        PLK=PL(k,:);
        minPLK=min(PLK);
        pos=find(PLK==minPLK);
        m=pos(1);
        ROUT=ROUTES{k,m};
        LENROUT=length(ROUT);
        Rx=ROUT;
        Ry=ROUT;
        for ii=1:LENROUT
            Rx(ii)=a*(mod(ROUT(ii),MM)-0.5);
            if Rx(ii)==-0.5
                Rx(ii)=MM-0.5;
            end
            Ry(ii)=a*(MM+0.5-ceil(ROUT(ii)/MM));
        end
        plot(Rx,Ry)
        hold on
    end
end
将上述算法应用于机器人路径规划，优化效果如下图所示
 INCLUDEPICTURE "http://s11.album.sina.com.cn/pic/4b42544302000o9m" \* MERGEFORMATINET
文章引用自： HYPERLINK "" \t "_blank"
