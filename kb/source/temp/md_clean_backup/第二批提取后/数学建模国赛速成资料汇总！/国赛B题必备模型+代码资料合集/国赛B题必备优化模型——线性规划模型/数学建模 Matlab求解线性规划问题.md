注：上机作业文件夹以自己的班级姓名学号命名，文件夹包括如下上机报告和Matlab程序。
上机报告模板如下：
佛山科学技术学院
上   机   报   告
课程名称                  数学建模
上机项目         Matlab求解线性规划问题
专业班级  15数学与应用数学   姓 名  余婷婷 学 号  20150820315

一.  上机目的
本节课我们认识了Matlab的线性规划的基础知识，主要有以下内容：
1．了解linprog等相关的命令格式。
2．学习掌握用MATLAB求解线性规划的问题。

二.  上机内容
1、用Matlab求解：

2、用Matlab求解：
 EMBED Equation.DSMT4
 EMBED Equation.DSMT4

3、用Matlab求解：
     EMBED Equation.DSMT4
4、用Matlab求解：
 EMBED Equation.DSMT4

 EMBED Equation.DSMT4
三.  上机方法与步骤
第1题：
代码：
f=[13 9 10 11 12 8];
A=[0.4 1.1 1 0 0 0;0 0 0 0.5 1.2 1.3];
b=[800;900];
Aeq=[1 0 0 1 0 0
     0 1 0 0 1 0
     0 0 1 0 0 1];
 beq=[400;600;500];
 vlb=zeros(6,1);
 vub=[];
 [x,fval]=linprog(f,A,b,Aeq,beq,vlb,vub)

第2题：
代码：
f=[6 3 4];
A=[0 1 0];
b=[50];
Aeq=[1 1 1];
 beq=[120];
 vlb=[30 0 20];
 vub=[];
 [x,fval]=linprog(f,A,b,Aeq,beq,vlb,vub)

第3题：
代码：
f=[300 180];
A=[0 7000];
b=[6000];
Aeq=[1 1];
 beq=[0.5];
 vlb=[0.1 0];
 vub=[];
 [x,fval]=linprog(f,A,b,Aeq,beq,vlb,vub)

第4题：
代码：
f=[2 3 5 3 3 6];
A=[ 1 2 3 0 0 0
    0 0 0 1 1 3
    -1 0 0 -1 0 0
    0 -1 0 0 -1 0
    0 0 -1 0 0 -1];
b=[80;100;-70;-50;-20];
Aeq=[];
 beq=[];
 vlb=zeros(6,1);
 vub=[];
 [x,fval]=linprog(f,A,b,Aeq,beq,vlb,vub)

上机结果
  学会了编写程序，运用上机语言求出问题结果，验证结果。有截图显示。
第1题：

第2题：

第3题：

第4题：
