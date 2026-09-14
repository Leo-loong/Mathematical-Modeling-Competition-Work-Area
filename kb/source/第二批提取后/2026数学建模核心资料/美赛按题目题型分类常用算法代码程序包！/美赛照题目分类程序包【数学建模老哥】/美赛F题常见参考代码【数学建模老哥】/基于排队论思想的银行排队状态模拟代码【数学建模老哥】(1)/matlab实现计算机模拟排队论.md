matlab实现计算机模拟排队论

%排队模型的计算机模拟
%排队论是一门研究随即服务系统工作过程的理论和方法
%m表示一个工作日内完成的服务顾客数
%t表示顾客的平均等待时间
clear
i = 2;
w = 0;
e(i - 1) = 0;
x(i) = exprnd(10);
c(i) = x(i);
b(i) = x(i);

while b(i) <= 480
    y(i) = unifrnd(4,15);
    e(i) = b(i) + y(i);
    w = w + b(i) - c(i);
    i = i + 1;
    x(i) = exprnd(10);
    c(i) = c(i - 1) + x(i);
    b(i) = max(c(i),e(i - 1));
end
i = i - 2;
t = w/i
m = i

matlab实现计算机模拟排队论(续)

%排队模型的计算机模拟
%排队论是一门研究随即服务系统工作过程的理论和方法
%pm表示100工作日内平均每天完成的服务顾客数
%t表示顾客的平均等待时间
clear
cs = 100;
for j = 1:cs
    w(j) = 0;
    i = 2;
    x(i) = exprnd(10);
    c(i) = x(i);
    b(i) = x(i);

    while b(i) <= 480
        y(i) = unifrnd(4,15);
        e(i) = b(i) + y(i);
        w(j) = w(j) + b(i) - c(i);
        i = i + 1;
        x(i) = exprnd(10);
        c(i) = c(i - 1) + x(i);
        b(i) = max(c(i),e(i - 1));
    end

    i = i - 2;
    t(j) = w(j)/i;
    m(j) = i;
end
pt = 0;
pm = 0;
for j = 1:cs
    pt = pt + t(j);
    pm = pm + m(j);
end
pt = pt/cs
pm = pm/cs
