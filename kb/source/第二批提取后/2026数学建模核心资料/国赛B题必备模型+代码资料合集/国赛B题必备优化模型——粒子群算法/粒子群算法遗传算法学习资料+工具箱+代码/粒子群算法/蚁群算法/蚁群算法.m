% 
% 
% the procedure of ant colony algorithm for VRP 
% 
% % % % % % % % % % % 

%initialize the parameters of ant colony algorithms 
load data.txt; 
d=data(:,2:3); 
g=data(:,4); 

m=31; % 蚂蚁数 
alpha=1; 
belta=4;% 决定tao和miu重要性的参数 
lmda=0; 
rou=0.9; %衰减系数 
q0=0.95; 
% 概率 
tao0=1/(31*841.04);%初始信息素 
Q=1;% 蚂蚁循环一周所释放的信息素 
defined_phrm=15.0; % initial pheromone level value 
QV=100; % 车辆容量 
vehicle_best=round(sum(g)/QV)+1; %所完成任务所需的最少车数 
V=40; 

% 计算两点的距离 
for i=1:32; 
for j=1:32; 
dist(i,j)=sqrt((d(i,1)-d(j,1))^2+(d(i,2)-d(j,2))^2); 
end; 
end; 

%给tao miu赋初值 
for i=1:32; 
for j=1:32; 
if i~=j; 
%s(i,j)=dist(i,1)+dist(1,j)-dist(i,j); 
tao(i,j)=defined_phrm; 
miu(i,j)=1/dist(i,j); 
end; 
end; 
end; 

for k=1:32; 
for k=1:32; 
deltao(i,j)=0; 
end; 
end; 

best_cost=10000; 
for n_gen=1:50; 


print_head(n_gen); 

for i=1:m; 
%best_solution=[]; 
print_head2(i); 
sumload=0; 
cur_pos(i)=1; 
rn=randperm(32); 
n=1; 
nn=1; 
part_sol(nn)=1; 
%cost(n_gen,i)=0.0; 
n_sol=0; % 由蚂蚁产生的路径数量 
M_vehicle=500; 
t=0; %最佳路径数组的元素数为0 

while sumload<=QV; 

for k=1:length(rn); 
if sumload+g(rn(k))<=QV; 
gama(cur_pos(i),rn(k))=(sumload+g(rn(k)))/QV; 
A(n)=rn(k); 
n=n+1; 
end; 
end; 

fid=fopen('out_customer.txt','a+'); 
fprintf(fid,'%s %i\t','the current position is:',cur_pos(i)); 
fprintf(fid,'\n%s','the possible customer set is:') 
fprintf(fid,'\t%i\n',A); 
fprintf(fid,'------------------------------\n'); 
fclose(fid); 

p=compute_prob(A,cur_pos(i),tao,miu,alpha,belta,gama,lmda,i); 
maxp=1e-8; 
na=length(A); 
for j=1:na; 
if p(j)>maxp 
maxp=p(j); 
index_max=j; 
end; 
end; 

old_pos=cur_pos(i); 
if rand(1)<q0 
cur_pos(i)=A(index_max); 
else 
krnd=randperm(na); 
cur_pos(i)=A(krnd(1)); 
bbb=[old_pos cur_pos(i)]; 
ccc=[1 1]; 
if bbb==ccc; 
cur_pos(i)=A(krnd(2)); 
end; 
end; 

tao(old_pos,cur_pos(i))=taolocalupdate(tao(old_pos,cur_pos(i)),rou,tao0);%对所经弧进行局部更新 

sumload=sumload+g(cur_pos(i)); 

nn=nn+1; 
part_sol(nn)=cur_pos(i); 
temp_load=sumload; 

if cur_pos(i)~=1; 
rn=setdiff(rn,cur_pos(i)); 
n=1; 
A=[]; 
end; 

if cur_pos(i)==1; % 如果当前点为车场,将当前路径中的已访问用户去掉后,开始产生新路径 
if setdiff(part_sol,1)~=[]; 
n_sol=n_sol+1; % 表示产生的路径数,n_sol=1,2,3,..5,6...,超过5条对其费用加上车辆的派遣费用 
fid=fopen('out_solution.txt','a+'); 
fprintf(fid,'%s%i%s','NO.',n_sol,'条路径是:'); 
fprintf(fid,'%i ',part_sol); 
fprintf(fid,'\n'); 
fprintf(fid,'%s','当前的用户需求量是:'); 
fprintf(fid,'%i\n',temp_load); 
fprintf(fid,'------------------------------\n'); 
fclose(fid); 

% 对所得路径进行路径内3-opt优化 
final_sol=exchange(part_sol); 

for nt=1:length(final_sol); % 将所有产生的路径传给一个数组 
temp(t+nt)=final_sol(nt); 
end; 
t=t+length(final_sol)-1; 

sumload=0; 
final_sol=setdiff(final_sol,1); 
rn=setdiff(rn,final_sol); 
part_sol=[]; 
final_sol=[]; 
nn=1; 
part_sol(nn)=cur_pos(i); 
A=[]; 
n=1; 

end; 
end; 

if setdiff(rn,1)==[];% 产生最后一条终点不为1的路径 
n_sol=n_sol+1; 
nl=length(part_sol); 
part_sol(nl+1)=1;%将路径的最后1位补1 

% 对所得路径进行路径内3-opt优化 
final_sol=exchange(part_sol); 

for nt=1:length(final_sol); % 将所有产生的路径传给一个数组 
temp(t+nt)=final_sol(nt); 
end; 

cost(n_gen,i)=cost_sol(temp,dist)+M_vehicle*(n_sol-vehicle_best); %计算由蚂蚁i产生的路径总长度 

for ki=1:length(temp)-1; 
deltao(temp(ki),temp(ki+1))=deltao(temp(ki),temp(ki+1))+Q/cost(n_gen,i); 
end; 

if cost(n_gen,i)<best_cost; 
best_cost=cost(n_gen,i); 
old_cost=best_cost; 
best_gen=n_gen; % 产生最小费用的代数 
best_ant=i; %产生最小费用的蚂蚁 
best_solution=temp; 
end; 

if i==m; %如果所有蚂蚁均完成一次循环，，则用最佳费用所对应的路径对弧进行整体更新 
for ii=1:32; 
for jj=1:32; 
tao(ii,jj)=(1-rou)*tao(ii,jj); 
end; 
end; 

for kk=1:length(best_solution)-1; 
tao(best_solution(kk),best_solution(kk+1))=tao(best_solution(kk),best_solution(kk+1))+deltao(best_solution(kk),best_solution(kk+1)); 
end; 
end; 

fid=fopen('out_solution.txt','a+'); 
fprintf(fid,'%s%i%s','NO.',n_sol,'路径是:'); 
fprintf(fid,'%i ',part_sol); 
fprintf(fid,'\n'); 
fprintf(fid,'%s %i\n','当前的用户需求量是:',temp_load); 
fprintf(fid,'%s %f\n','总费用是:',cost(n_gen,i)); 
fprintf(fid,'------------------------------\n'); 
fprintf(fid,'%s\n','最终路径是:'); 
fprintf(fid,'%i-',temp); 
fprintf(fid,'\n'); 
fclose(fid); 
temp=[]; 
break; 
end; 
end; 
end; 
end; 
