import xlrd
import numpy as np
INFINITY = 99999.0


# 打开文件
data = xlrd.open_workbook('cumcm2011B附件2_全市六区交通网路和平台设置的数据表.xls')
data.sheet_names()
print("sheets：" + str(data.sheet_names()))

# 通过文件名获得工作表,获取工作表1
table1 = data.sheet_by_name('全市交通路口节点数据')
loc = []
# 为使索引值和节点编号对应，填入一个占位数据
loc.append([0, 0])
#读入A区各节点的坐标数据
for k in range(1, 93):
    x = table1.cell(k, 1).value  #注意，excel里的计数也从0开始
    y = table1.cell(k, 2).value
    #print(x, y)
    loc.append([x, y])

table2 = data.sheet_by_name('全市交通路口的路线')
distance = np.zeros((93, 93), dtype=np.float)

for i in range(1, 93):
    for j in range(1, 93):
        if i == j :
            distance[i, j] = 0.0
        else:
            distance[i, j] = INFINITY
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

time = np.zeros((93, 93), dtype=np.float)

for i in range(1, 93):
    for j in range(1, 93):
        time[i, j] = distance[i, j]/10


filename = 'rask2.txt'
pingtai = range(1, 21)

table3 = data.sheet_by_name('全市区出入口的位置')
chukou = []
for k in range(1, 14):
    #print(int(table3.cell(k, 2).value))
    chukou.append(int(table3.cell(k, 2).value))

with open(filename, 'w') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
    for i in pingtai:
        for j in chukou:
            f.write('%.4f' % time[i, j] +"\t")
        f.write("\n")


