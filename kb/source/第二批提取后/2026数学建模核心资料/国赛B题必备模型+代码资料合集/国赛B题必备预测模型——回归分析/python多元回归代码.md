# 以下是一个简单的Python多元回归代码示例，使用sklearn库中的LinearRegression类。假设我们有一个数据集，其中包含四个特征（x1，x2，x3和x4）和一个目标变量y。
**python**

|  | from sklearn.model_selection import train_test_split |
| --- | --- |
|  | from sklearn.linear_model import LinearRegression |
|  | from sklearn import metrics |
|  | import pandas as pd |
|  | import numpy as np |
|  |  |
|  | # 加载数据集 |
|  | data = pd.read_csv('dataset.csv') |
|  |  |
|  | # 特征和目标变量 |
|  | X = data[['x1', 'x2', 'x3', 'x4']] |
|  | y = data['y'] |
|  |  |
|  | # 划分训练集和测试集 |
|  | X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0) |
|  |  |
|  | # 创建线性回归模型对象 |
|  | model = LinearRegression() |
|  |  |
|  | # 训练模型 |
|  | model.fit(X_train, y_train) |
|  |  |
|  | # 预测测试集结果 |
|  | y_pred = model.predict(X_test) |
|  |  |
|  | # 输出模型参数 |
|  | print('Coefficients: \n', model.coef_) |
|  | print('Intercept: \n', model.intercept_) |
|  |  |
|  | # 评估模型性能 |
|  | print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred)) |
|  | print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred)) |
|  | print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred))) |

在这个例子中，我们首先加载数据集，然后将其划分为特征和目标变量。接下来，我们将数据集划分为训练集和测试集，并使用训练集训练线性回归模型。然后，我们使用测试集对模型进行预测，并输出模型的参数和性能指标。
