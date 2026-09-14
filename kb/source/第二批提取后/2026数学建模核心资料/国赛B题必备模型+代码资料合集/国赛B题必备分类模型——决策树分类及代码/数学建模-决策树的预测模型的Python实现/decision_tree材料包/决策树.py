"""
决策树的应用:对泰坦尼克号数据集成员进行预测生死
算法流程还是比较简单的,简单学习一下决策树跟着注释写即可
文章参考:https://zhuanlan.zhihu.com/p/133838427
算法种遇上sklearn的函数还是比较多的,请将sklearn函数更新到最新
更新代码如下所示:
pip install --upgrade sklearn
"""
#首先导入需要的包
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.feature_extraction import  DictVectorizer
import pandas as pd

titan= pd.read_csv(r'C:\Users\Zeng Zhong Yan\Desktop\train.csv')
# 处理数据，找出特征值和目标值
x = titan[['Pclass', 'Age', 'Sex']]
y = titan['Survived']
print(x)
# 缺失值处理
x['Age'].fillna(x['Age'].mean(), inplace=True)
# 分割数据集到训练集和测试集
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)
# 进行处理(特征工程)
dict = DictVectorizer(sparse=False)
x_train = dict.fit_transform(x_train.to_dict(orient="records"))
dict = DictVectorizer(sparse=False)
x_test = dict.fit_transform(x_test.to_dict(orient='records'))
print(dict.get_feature_names_out())
#X_test = vec.fit_transform(X_features)
print(x_train)
# 用决策树进行预测
dec = DecisionTreeClassifier()
dec.fit(x_train, y_train)
# 预测准确率
print("预测的准确率为：", dec.score(x_test, y_test))
# 导出决策树的结构
export_graphviz(dec, out_file=r"C:\Users\Zeng Zhong Yan\Desktop\py.vs\.vscode\数学建模\decision_tree.dot", feature_names=['Age', 'Pclass', 'Sex=female', 'Sex=male'])




 
        
 
         
        
 
       
