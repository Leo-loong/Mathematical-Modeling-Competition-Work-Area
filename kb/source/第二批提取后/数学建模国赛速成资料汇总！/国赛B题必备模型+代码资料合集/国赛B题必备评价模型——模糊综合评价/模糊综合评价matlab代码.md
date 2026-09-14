# 附录2、各章节中编程计算的MatLab 程序
### 2.1 模糊综合评判计算程序
模糊综合评判的过程：
、灰色关联分析，求权重（程序见Relation）；
、模糊聚类分析，划分等级（程序见F_class）；
、隶属度计算，求隶属函数（程序见Subjection和subject）；
、模糊综合评判，计算各单元等级（程序见F_judge）。
各步骤的程序如下：
**（1）Relation：灰色关联分析程序**
**主程序：**
% 灰色关联分析：--母序列必须置为第一行！即x(1,:)
clear;
sq={'母指标','断层分维值','隔水层厚度','太会含水层水压','开采深度'};
m=5;n=81;
fid=fopen('data1_no E_ZH.dat','r');
  X_t=fscanf(fid,'%g',[n m]);  % 从数据文件读入数据。
fclose(fid);
x=X_t';

for i=1:m
    D(i,:)=initia_MAX(x(i,:),n);
end
for i=1:m-1
    DT(i,:)=abs(D(1,:)-D(i+1,:));
end
max=DT(1,1);min=DT(1,1);
for i=1:m-1
    for j=1:n
        if max<DT(i,j)
            max=DT(i,j);
        elseif min>DT(i,j)
            min=DT(i,j);
        end
    end
end

yita=0.5;
for i=1:m-1
    gama_t(i)=0;
    for j=1:n
        xigma(i,j)=(min+yita*max)/(abs(DT(i,j))+yita*max);
        gama_t(i)=gama_t(i)+xigma(i,j);
    end
end
gama(1)=1.0;  % 母序列对自己的关联度总是为1。
disp(strcat(sq(1),'-to-',sq(1))),disp(gama(1))
for i=1:m-1
    gama(i+1)=gama_t(i)/n;
    disp(strcat(sq(i+1),'-to-',sq(1))),disp(gama(i+1))
end
disp('归一化处理如下：')
gama_all=0;
for i=1:m
    gama_all=gama_all+gama(i);
end
for i=1:m
    weight(i)=gama(i)/gama_all;
    disp(sq(i)),disp(weight(i))
end

**子程序：initia_MAX(X,n)**
function X1=initia_MAX(X,n)
% 初始化，亦即无量纲化，对地质数据，采用最大值化为宜。
max=X(1);
for i=1:n
    if max<X(i)
        max=X(i);
    end
end
X1=X./max;
**（2）F_class：模糊聚类程序**
% 模糊聚类－－减数法或相关系数法建立F关系。
clear;
m=4;n=81;
fid=fopen('data_class.dat','r');
  X_t=fscanf(fid,'%g',[n m]);  % 从数据文件读入数据。
fclose(fid);
X=X_t;

choice=input('Input the value of choice: 1-相关系数法，2-绝对值减数法 ');
switch choice
    case 1
        for i=1:n
            for j=1:n
                xi_all=0; xj_all=0;
                for k=1:m
                    xi_all=xi_all+X(i,k);
                    xj_all=xj_all+X(j,k);
                end
                xi_ave=xi_all/m;
                xj_ave=xj_all/m;
                dt_x=0; dt_xi2=0; dt_xj2=0;
                for k=1:m
                    dt_x=dt_x+abs(X(i,k)-xi_ave)*abs(X(j,k)-xj_ave);
                    dt_xi2=dt_xi2+(X(i,k)-xi_ave)^2;
                    dt_xj2=dt_xj2+(X(j,k)-xj_ave)^2;
                end
                r(i,j)=dt_x/(sqrt(dt_xi2)*sqrt(dt_xj2));
            end
        end
    case 2
        tr0=0;
        while tr0==0
            c=input('Input the value of c;');
            for i=1:n
                for j=1:n
                    d_all=0;
                    for k=1:m
                        d_all=d_all+abs(X(i,k)-X(j,k));
                    end
                    r(i,j)=1-c*d_all;
                end
            end
            if r>zeros(n,n)
                tr0=1;
            end
        end
    otherwise
        disp('You input the wrong value!');
end
disp(r);

r_t=r;
for i=1:1000
    rr=multiply_F(r_t,r_t);
    if rr==r_t
        disp('OK!');break;
    else
        r_t=rr;
        disp('NOT OK! Cycle times is:');disp(i);
    end
end
disp(rr);

tr='y';
while tr=='Y'|tr=='y'
    nmta=input('Input the value of nmta:  ');
    for i=1:n
        for j=1:n
            if rr(i,j)>=nmta
                R(i,j)=1;
            else
                R(i,j)=0;
            end
        end
    end
    disp(R);

    for i=1:n
        k=1;
        for j=i:n
            if R(i,j)==1
                C_t(k)=j;
                k=k+1;
            end
        end
        C{i}=C_t;
        disp(C{i});
        clear C_t;
    end
    tr=input('Are you go on ? (Y/N)','s');
end

n_class=n;
for i=n:-1:1
    for j=i-1:-1:1
        x=C{i};y=C{j};
        for k=1:length(C{j})
            for l=1:length(C{i})
                if x(l)==y(k)
                   C{i}=[0];
                   n_class=n_class-1;
                   continue;
                end
            end
        end
    end
end
disp('The number of classes is:');disp(n_class);
disp('They are as follow:');
for i=1:n
    disp(C{i});
end
**（3）Subjection：隶属函数计算程序（配合子程序sugject）**
**主程序：**
% 建立隶属函数－－即某单元（i)在某项指标上（Ui）对某评语等级（Vj）的隶属度（Rij）。
clear;
M=[0.002 0.004 0.006 0.008 0.010 0.012 0.014 0.016 0.018 0.020;
   0.024 0.028 0.032 0.036 0.040 0.044 0.048 0.052 0.056 0.060;
   0.066 0.072 0.078 0.084 0.090 0.096 0.102 0.108 0.114 0.120;
   0.126 0.132 0.138 0.144 0.150 0.156 0.162 0.168 0.174 0.180];
F=[  7.5  15.0  22.5  30.0  37.5  45.0  52.5  60.0  67.5  75.0;
    82.5  90.0  97.5 105.0 112.5 120.0 127.5 135.0 142.5 150.0;
   175.0 200.0 225.0 250.0 275.0 300.0 325.0 350.0 375.0 400.0;
   440.0 480.0 520.0 560.0 600.0 640.0 680.0 720.0 760.0 800.0];
Q=[0.25 0.50 0.75 1.00 1.25 1.50 1.75 2.00 2.25 2.50;
   3.25 4.00 4.75 5.50 6.25 7.00 7.75 8.50 9.25 10.0;
   11.0 12.0 13.0 14.0 15.0 16.0 17.0 18.0 19.0 20.0;
   30.0 40.0 50.0 60.0 70.0 80.0 90.0 100. 110. 120.];
A=[ 0.5  1.0  1.5  2.0  2.5  3.0  3.5  4.0  4.5  5.0;
    5.3  5.6  5.9  6.2  6.5  6.8  7.1  7.4  7.7  8.0;
    8.4  8.8  9.2  9.6 10.0 10.4 10.8 11.2 11.6 12.0;
   13.0 14.0 15.0 16.0 17.0 18.0 19.0 20.0 21.0 22.0];
R=[0.025 0.050 0.075 0.100 0.125 0.150 0.175 0.200 0.225 0.250;
   0.265 0.280 0.295 0.310 0.325 0.340 0.355 0.370 0.385 0.400;
   0.420 0.440 0.460 0.480 0.500 0.520 0.540 0.560 0.580 0.600;
   0.620 0.640 0.660 0.680 0.700 0.720 0.740 0.760 0.780 0.800];
D=[0.20 0.40 0.60 0.80 1.00 1.20 1.40 1.60 1.80 2.00;
   2.20 2.40 2.60 2.80 3.00 3.20 3.40 3.60 3.80 4.00;
   4.40 4.80 5.20 5.60 6.00 6.40 6.80 7.20 7.60 8.00;
   8.40 8.80 9.20 9.60 10.0 10.4 10.8 11.2 11.6 12.0];
H=[  6  12  18  24  30  36  42  48  54  60;
    64  68  72  76  80  84  88  92  96 100;
   105 110 115 120 125 130 135 140 145 150;
   155 160 165 170 175 180 185 190 195 200];
S=[0.01 0.02 0.03 0.04 0.05 0.06 0.07 0.08 0.09 0.10;
   0.11 0.12 0.13 0.14 0.15 0.16 0.17 0.18 0.19 0.20;
   0.21 0.22 0.23 0.24 0.25 0.26 0.27 0.28 0.29 0.30;
   0.32 0.34 0.36 0.38 0.40 0.42 0.44 0.46 0.48 0.50];

fid=fopen('subjec_dat.dat','r');
  A_t=fscanf(fid,'%g',[8 34]);  % 从数据文件读入数据。
fclose(fid);
A=A_t'; % 各单元（行数）的各项指标（列数）统计结果（矩阵）
% 注:34个单元，每个单元8项指标，每个指标4个评语等级，故要生成34个8×4矩阵。

m0=4; % 评语集的维数；
m=34;n=8; % 指标集的维数，m－单元个数，n－指标个数；
for j=1:n  % 第一循环开始
    switch j
        case 1
            X_T=M;ver=0; % 指标值为升序时 ver=0，降序时 ver=1，下同！
        case 2
            X_T=F;ver=0;
        case 3
            X_T=Q;ver=0;
        case 4
            X_T=A;ver=0;
        case 5
            X_T=R;ver=0;
        case 6
            X_T=D;ver=0;
        case 7
            X_T=H;ver=0;
        case 8
            X_T=S;ver=0;
        otherwise
        disp('指标个数 > 8 ----修改程序！');
    end
    for i=1:m  % 第二循环开始
        for k=1:m0  % 第三循环开始
            X=[A(i,j),X_T(k,:)];
            switch ver
                case 0
                    if k==1
                        chs=1;
                    else if k==m
                            chs=3;
                        else
                            chs=2;
                        end
                    end
                case 1
                    if k==1
                        chs=3;
                    else if k==m
                            chs=1;
                        else
                            chs=2;
                        end
                    end
            end
            R_T=subject(X,length(X),chs);
            R(j,k,i)=R_T(1);
        end  % 第三循环结束
    end  % 第二循环结束
    clear X_T;
end  % 第一循环结束

% 归一化处理:
clear R_T;
R_T=R;
clear R;
for i=1:m
    for j=1:n
        all=0;
        for k=1:m0
            all=all+R_T(j,k,i);
        end
        for k=1:m0
            R(j,k,i)=R_T(j,k,i)/all;
        end
    end
end

% 输出到文件......
fid=fopen('subjec_ans.dat','w');
fprintf(fid,'\n');
for i=1:m
    fprintf(fid,'\n%s%d%s\n','R(',i,')');
    for j=1:n
        fprintf(fid,'%6.4f %6.4f %6.4f %6.4f\n',R(j,:,i));
    end,fprintf(fid,'\n');
end
fclose(fid);
disp('各单元的指标对应各评语等级的隶属度');
disp(R);

**子程序：subject**
function r=subject(x,n,choice)
% 建立隶属函数－－即某单元（i)在某项指标上（Ui）对某评语等级（Vj）的隶属度（Rij）。
x_all=0;
for i=1:n
    x_all=x_all+x(i);
end
x_ave=x_all/n;
dt_a=0;
for i=1:n
    dt_a=dt_a+(x(i)-x_ave)^2;
end
dt2=dt_a/(n-1);
% disp('Input the value of choice:');
% choice=input('1-偏小型  2-中间型 3-偏大型  ');
switch choice
    case 1
        for i=1:n
            if x(i)<=x_ave
                r(i)=1;
            else
                r(i)=exp(-(x(i)-x_ave)^2/dt2);
            end
        end
    case 2
        for i=1:n
            r(i)=exp(-(x(i)-x_ave)^2/dt2);
        end
    case 3
        for i=1:n
            if x(i)>=x_ave
                r(i)=1;
            else
                r(i)=exp(-(x(i)-x_ave)^2/dt2);
            end
        end
    otherwise
        disp('The value of "choice" is wrong !');
end
**（4）F_judge：模糊综合评判程序**
% 模糊评判－－矩阵相乘
clear
A=[0.153 0.160 0.151 0.094 0.088 0.117 0.096 0.141]; % 权重集（矩阵）

m0=4;n=8; % 评价矩阵维数，m0－评语集的维数，n－指标个数；
m=34; % 单元个数；
fid=fopen('subjec_ans.dat','r');
for i=1:m
    Tmp=fscanf(fid,'%s',1);
    R_t=fscanf(fid,'%g',[m0 n]);  % 从数据文件读入数据。
    R{i}=R_t';
end
fclose(fid);

for i=1:m
    B{i}=A*R{i};
end

fid=fopen('F_judge_ans.dat','w');
fprintf(fid,'%s\n','The answers:');
fprintf(fid,'%s\n','   Ⅰ      Ⅱ      Ⅲ      Ⅳ');
fprintf('%s\n','The answers:');
fprintf('%s\n','      Ⅰ        Ⅱ        Ⅲ        Ⅳ');
for i=1:m
    disp(B{i});
    fprintf(fid,'%6.4f  %6.4f  %6.4f  %6.4f\n',B{i});
end
fclose(fid);
