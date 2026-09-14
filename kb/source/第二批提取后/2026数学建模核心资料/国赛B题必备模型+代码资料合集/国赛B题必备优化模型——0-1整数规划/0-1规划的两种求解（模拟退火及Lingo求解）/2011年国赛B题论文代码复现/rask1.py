import xlrd
import numpy as np

INFINITY = 99999.0


# 打开文件
data = xlrd.open_workbook('cumcm2011B附件2_全市六区交通网路和平台设置的数据表.xls')
#print("sheets：" + str(data.sheet_names()))  #打印sheets名

table1 = data.sheet_by_name('全市交通路口节点数据')
loc = []  #节点位置列表
w = []  #发案率列表
# 为使索引值和节点编号对应，填入一个占位数据
loc.append([0, 0])  # 为使索引值和节点编号对应，填入一个占位数据
w.append(0.0)  # 同上

#读入A区各节点的坐标数据
for k in range(1, 93):
    x = table1.cell(k, 1).value  #注意，excel里的计数是从0开始的，和图像化界面里显示的不同
    y = table1.cell(k, 2).value
    loc.append([x, y])
    w.append(table1.cell(k, 4).value)

table2 = data.sheet_by_name('全市交通路口的路线')
distance = np.zeros((93, 93), dtype=np.float)

# 初始化一个二维数组，用来记录无向图
for i in range(1, 93):
    for j in range(1, 93):
        if i == j:
            distance[i, j] = 0.0
        else:
            distance[i, j] = INFINITY

# 得到距离矩阵
for k in range(1, table2.nrows):
    i = int(table2.cell(k, 0).value)
    j = int(table2.cell(k, 1).value)
    # print(i, j)
    if i <= 92 and j <= 92:
        distance[i, j] = np.sqrt((loc[i][0]-loc[j][0])**2 + (loc[i][1]-loc[j][1])**2)
        distance[j, i] = np.sqrt((loc[i][0]-loc[j][0])**2 + (loc[i][1]-loc[j][1])**2)

# floyd算法求最短距离
for k in range(1, 93):
    for i in range(1, 93):
        for j in range(1, 93):
            if distance[i, k] + distance[k, j] < distance[i, j]:
                distance[i, j] = distance[i, k] + distance[k, j]

# 考虑车速60km/h，把距离矩阵变成时间矩阵
time = np.zeros((93, 93), dtype=np.float)
for i in range(1, 93):
    for j in range(1, 93):
        time[i, j] = distance[i, j]/10

#  目标函数计算函数
def F (t, w, x):
    numerator = 0.0
    denominator = 0.0
    for i in range(1, 21):
        for j in range(1, 93):
            numerator += w[j]*t[i, j]*x[i, j]
            pass
    for j in range(1, 93):
        denominator += w[j]
    return numerator/denominator

# 约束1判断函数
def F1 (x):
    judge = True
    for j in range(1, 93):
        f = 0.0
        for i in range(1, 21):
            f += x[i, j]
        if f < 1:
            judge = False
            break
    return judge

# 约束2判断函数
def F2(t, x):
    judge = True
    flag = 0
    a = 20  # 发现原约束太强，这里用来弱化约束， 这样做也有利于找到最优解
    for i in range(1, 21):
        for j in range(1, 93):
            if t[i, j]*x[i, j] > 3+a:
                judge = False
                flag = 1
                break
        if flag == 1:
            break

    return judge


#  模拟退火参数设定
T0 = 100000
Tf = 0.0001
alpha = 0.995  #温度衰减系数
Lk = 100  #马尔可夫链长

#  初始化
T = T0  # 初始化温度
x = np.zeros((21, 93), dtype=np.int)  # 初始化当前可行解
f = INFINITY  # 初始化当前可行解目标函数值
x_best = np.zeros((21, 93), dtype=np.int)  # 初始化最优解
f_best = INFINITY  #初始化 最优目标函数值

# 设置最初解，保证每个节点都有对应的平台
for j in range(1, 93):
    id = np.random.randint(1, 21)
    x[id, j] = 1

print("开始迭代：")
iter = 0
while T >= Tf:
    print("iter = "+str(iter)+", T = "+str(T)+", f = "+str(f)+", f_best = "+str(f_best))  # 打印迭代信息，用于监控退火过程
    iter += 1
    for k in range(Lk):  # 在每个温度下，搜索Lk次

        # 尝试更新解
        x_test = x.copy()
        for j in np.random.randint(1, 93, 46):  # 随机抽取一半平台做更新
            for i in range(1, 21):
                x_test[i, j] = 0
            id = np.random.randint(1, 21)
            x_test[id, j] = 1

        # 判断是否更新解
        P = -1
        p = 0.0  # 这两个都用于表示概率
        if not (F1(x_test) and F2(time, x_test)):
            P = 0
        elif F1(x_test) and F2(time, x_test) and F(time, w, x_test) < f:
            P = 1
        else:
            p = np.exp((F(time, w, x_test) - f)/T)

        if P == 1 or np.random.rand(1) < p:  # 更新解
            x = x_test
            f = F(time, w, x_test)
            if f < f_best:
                x_best = x.copy()
                f_best = f

    T = alpha*T  # 降温


print("迭代结束")
print("f_best = "+str(f_best))

# 结果打印
for i in range(1, 21):
    print(str(i)+"号平台管辖：")
    for j in range(1, 93):
        if x_best[i, j] == 1:
            print(str(j), end=" ")
    print("\n")





















