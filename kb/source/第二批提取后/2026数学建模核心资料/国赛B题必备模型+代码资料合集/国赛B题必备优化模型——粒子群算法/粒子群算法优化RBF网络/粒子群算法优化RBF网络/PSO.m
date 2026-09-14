clear all
close all

%G为迭代次数,n为个体长度(包括12个参数),m为总群规模
%w,c1,c2为粒子群算法中的参数
G =250;
n = 12;
m = 20;
w = 0.1;
c1 = 2;
c2 = 2;

for i = 1:3
    MinX(i) = 0.1*ones(1);
    MaxX(i) = 3*ones(1);
end

for i = 4:1:9
    MinX(i) = -3*ones(1);
    MaxX(i) = 3*ones(1);
end

for i = 10:1:12
    MinX(i) = -ones(1);
    MaxX(i) = ones(1);
end

pop = rands(m,n);
for i = 1:m
    for j = 1:3
        if pop(i,j) < MinX(j)
            pop(i,j) = MinX(j);
        end
        if pop(i,j) > MaxX(j)
            pop(i,j) = MaxX(j);
        end
    end
    for j = 4:9
        if pop(i,j) < MinX(j)
            pop(i,j) = MinX(j);
        end
        if pop(i,j) > MaxX(j)
            pop(i,j) = MaxX(j);
        end
    end
    for j = 10:12
        if pop(i,j) < MinX(j)
            pop(i,j) = MinX(j);
        end
        if pop(i,j) > MaxX(j)
            pop(i,j) = MaxX(j);
        end
    end
end
        

V = 0.1*rands(m,n);
BsJ = 0;

%根据初始化的种群计算个体好坏,找出群体最优和个体最优
for s = 1:m
    indivi = pop(s,:);
    [indivi,BsJ] = chap10_3b(indivi,BsJ);
    Error(s) = BsJ;
end

[OderEr,IndexEr] = sort(Error);
Error;
Errorleast = OderEr(1);
for i = 1:m
    if Errorleast == Error(i)
        gbest = pop(i,:);
        break;
    end
end
ibest = pop;


for kg = 1:G
    kg
    for s = 1:m;
%个体有4%的变异概率        
        for j = 1:n
            for i = 1:m
                if rand(1)<0.04
                    pop(i,j) = rands(1);
                end
            end
        end
%r1,r2为粒子群算法参数        
        r1 = rand(1);
        r2 = rand(1);

%个体和速度更新        
        V(s,:) = w*V(s,:) + c1*r1*(ibest(s,:)-pop(s,:)) + c2*r2*(gbest-pop(s,:));
        pop(s,:) = pop(s,:) + 0.3*V(s,:);
        
        for j = 1:3
            if pop(s,j) < MinX(j)
                pop(s,j) = MinX(j);
            end
            if pop(s,j) > MaxX(j)
                pop(s,j) = MaxX(j);
            end
        end
        for j = 4:9
            if pop(s,j) < MinX(j)
                pop(s,j) = MinX(j);
            end
            if pop(s,j) > MaxX(j)
                pop(s,j) = MaxX(j);
            end
        end
        for j = 10:12
            if pop(s,j) < MinX(j)
                pop(s,j) = MinX(j);
            end
            if pop(s,j) > MaxX(j)
                pop(s,j) = MaxX(j);
            end
        end

%求更新后的每个个体适应度值        
        [pop(s,:),BsJ] = chap10_3b(pop(s,:),BsJ);
        error(s) = BsJ;
%根据适应度值对个体最优和群体最优进行更新        
        if error(s)<Error(s)
            ibest(s,:) = pop(s,:);
            Error(s) = error(s);
        end
        if error(s)<Errorleast
            gbest = pop(s,:);
            Errorleast = error(s);
        end
    end
    
    Best(kg) = Errorleast;
end
plot(Best);

save pfile1 gbest;
    

