<!-- 第 1 页 -->

# 使用python求解二次规划的问题

## 今天小编就为大家分享一篇使用python求解二次规划的问题，具有很好的参考价值，希望对大家有所帮助。一

## 起跟随小编过来看看吧
Python中支持Convex Optimization（凸规划）的模块为CVXOPT,其安装方式为：
pip install cvxopt

### 一、数学基础

二次型
二次型（quadratic form）：n个变量的二次多项式称为二次型，即在一个多项式中，未知数的个数为任意多个，但每一项的次
数都为2的多项式。其基本形式如下

亦可写作，  ，称作二次型的矩阵表示，其中A是对称矩阵。仿照如下的定义，我们可以直接在其基本形式和
矩阵表示之间相互转化。

### 2.正定矩阵

设A是n阶实对称矩阵， 如果对任意一非零实向量X，都使二次型  成立，则称f(X)为正定二次型，矩阵A称
为正定矩阵(Positive Definite)，A为正定矩阵。

相应的，如果对任意一非零实向量X，都使二次型 成立，则称f(X)为半正定二次型，A为半正定矩阵。

### 3.二次规划问题

二次规划是指，带有二次型目标函数和约束条件的最优化问题。其标准形式如下：

即在Gx<h 和Ax=b的约束下，最小化目标函数。其中，当P是正定矩阵时，目标函数存在全局唯一最优解；P是半正定矩阵
时，目标函数是凸函数，存在全局最优解（不唯一）;P是不定矩阵时，目标函数非凸，存在多个局部最小值和稳定点，为np

<!-- 第 2 页 -->
难问题。（本篇博客中我们不考虑非正定情况）。

### 二、python程序求解

工具包：Cvxopt python 凸优化包
函数原型：Cvxopt.solvers.qp(P,q,G,h,A,b)
P,q,G,h,A,b的含义参见上面的二次规划问题标准形式。
编程求解思路：

### 1.对于一个给定的二次规划问题，先转换为标准形式（参见数学基础中所讲的二次型二中形式转换）

### 2.对照标准形势，构建出矩阵P,q,G,h,A,b

### 3.调用result=Cvxopt.solvers.qp(P,q,G,h,A,b)求解

4.print（result）查看结果，其中result是一个字典，我们可直接获得其某个属性，e.g. print(result['x'])
下面我们来看一个例子

import pprint
from cvxopt import matrix, solvers
P = matrix([[4.0,1.0],[1.0,2.0]])
q = matrix([1.0,1.0])
G = matrix([[-1.0,0.0],[0.0,-1.0]])
h = matrix([0.0,0.0])
A = matrix([1.0,1.0],(1,2))#原型为cvxopt.matrix(array,dims)，等价于A = matrix([[1.0],[1.0]]）
b = matrix([1.0])
result = solvers.qp(P,q,G,h,A,b)
print('x\n',result['x'])
运行结果：

注意事项：
cvxopt.matrix与numpy.matrix的排列顺序不同，其中cvxopt.matrix是列优先，numpy.matrix是行优先。具体可见下面实例

<!-- 第 3 页 -->
import numpy as np
from cvxopt import matrix
a = np.matrix([[1,2],[3,4]])
b = matrix([[1,2],[3,4]])
print('numpy.matrix',a)
print('cvxopt.matrix',b)
运行结果：

以上这篇使用python求解二次规划的问题就是小编分享给大家的全部内容了，希望能给大家一个参考，也希望大家多多支持我
们。
