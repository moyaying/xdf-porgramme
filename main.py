"""
This program performs two different logistic regression implementations on two
different datasets of the format [float,float,boolean], one
implementation is in this file and one from the sklearn library. The program
then compares the two implementations for how well the can predict the given outcome
for each input tuple in the datasets.
@author Per Harald Borgen
"""

import json
import math
import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
# from sklearn.cross_validation import train_test_split
from sklearn.model_selection import train_test_split
from numpy import loadtxt, where
from pylab import scatter, show, legend, xlabel, ylabel
from sklearn.preprocessing import StandardScaler  # data normalization

with open('./out/titles.txt') as json_file:
    titles = json.load(json_file)
    # list(titles).remove('学员号')
    # del titles[0]
    print(titles)
# exit(0)

# scale larger positive and values to between -1,1 depending on the largest
# value in the data
min_max_scaler = preprocessing.MinMaxScaler(feature_range=(-1, 1))
df = pd.read_csv("out/tt.csv", header=0)

# for i in df.columns:
#     df[i] = df[i].astype(int)

# clean up data
# df.columns = titles
X = df[titles[0:-1]]
X = np.array(X)
print(X)

X = StandardScaler().fit(X).transform(X)  # 数据转换
# print(X)

Y = df[titles[-1]]
Y = np.asarray(Y)

# creating testing and training set
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.33)  # 建立测试和训练数据集合

# train scikit learn model
clf = LogisticRegression()  # 使用逻辑回归模型
clf.fit(X_train, Y_train)  # 训练模型
print('score Scikit learn: ', clf.score(X_test, Y_test))  # 打印正确率

# yhat = clf.predict(X_test)
# print('yhat', yhat)
# yhat_prob = clf.predict_proba(X_test)
# print('yhat_prob', yhat_prob)
