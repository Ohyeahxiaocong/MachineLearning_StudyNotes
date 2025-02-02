# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 20:22:36 2019

@author: Hyomin
"""
import pandas as pd
import numpy as np
from xgboost.sklearn import XGBClassifier
from sklearn import metrics
from sklearn.model_selection import GridSearchCV, train_test_split

# 将训练集分为输入和输出
dataset = pd.read_csv('datasets/train_modified.csv')
x_colums = [x for x in dataset.columns if x not in ['Disbursed']]
X = dataset[x_colums]
y = dataset['Disbursed']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)


# 默认值模型 auc:0.8605372987016162
xgb0 = XGBClassifier(seed=10)
xgb0.fit(X_train, y_train)
y_predprob = xgb0.predict_proba(X_train)
metrics.roc_auc_score(y_train, y_predprob[:, 1])

# 迭代次数调参 {'n_estimators': 110}
#train_accuracy:0.985363
#test_accuracy:0.985635
#train_auc:0.905864
#test_auc:0.850271
xgb1 = XGBClassifier(max_depth=5,
                     learning_rate=0.1,
                     n_estimators=100,
                     min_child_weight=1,
                     gamma=0,
                     subsample=0.8,
                     colsample_bytree=0.8,
                     objective= 'binary:logistic',
                     scale_pos_weight=1,
                     n_jobs=4,
                     seed=10)
parameter1 = {'n_estimators': np.arange(60, 160, 10)}
xsearch1 = GridSearchCV(estimator=xgb1, param_grid=parameter1, scoring='roc_auc',
                        n_jobs=4, iid=False, cv=5)
xsearch1.fit(X_train, y_train)
xsearch1.best_params_

y_train_pred = xsearch1.predict(X_train)
y_test_pred = xsearch1.predict(X_test)
y_train_predprob = xsearch1.predict_proba(X_train)
y_test_predprob = xsearch1.predict_proba(X_test)
train_accuracy = metrics.accuracy_score(y_train, y_train_pred)
test_accuracy = metrics.accuracy_score(y_test, y_test_pred)
train_auc = metrics.roc_auc_score(y_train, y_train_predprob[:, 1])
test_auc = metrics.roc_auc_score(y_test, y_test_predprob[:, 1])
print('train_accuracy:%.6f' % train_accuracy)
print('test_accuracy:%.6f' % test_accuracy)
print('train_auc:%.6f' % train_auc)
print('test_auc:%.6f' % test_auc)

# 最大深度和最小子权重调优 {'max_depth': 5, 'min_child_weight': 1} 0.8524705811575599
xgb2 = XGBClassifier(max_depth=5,
                     learning_rate=0.1,
                     n_estimators=110,
                     min_child_weight=1,
                     gamma=0,
                     subsample=0.8,
                     colsample_bytree=0.8,
                     objective= 'binary:logistic',
                     scale_pos_weight=1,
                     n_jobs=4,
                     seed=10)
parameter2 = {'max_depth': range(3, 12, 2), 'min_child_weight': range(1,6,2)}
xsearch2 = GridSearchCV(estimator=xgb2, param_grid=parameter2, scoring='roc_auc',
                        n_jobs=4, iid=False, cv=5)
xsearch2.fit(X_train, y_train)
xsearch2.best_params_


# 正则化参数调优 {'gamma': 0.0} 0.8524705811575599
xgb3 = XGBClassifier(max_depth=5,
                     learning_rate=0.1,
                     n_estimators=140,
                     min_child_weight=1,
                     gamma=0,
                     subsample=0.8,
                     colsample_bytree=0.8,
                     objective= 'binary:logistic',
                     scale_pos_weight=1,
                     n_jobs=4,
                     seed=10)
parameter3 = {'gamma': np.arange(0, 0.6, 0.1)}
xsearch3 = GridSearchCV(estimator=xgb3, param_grid=parameter3, scoring='roc_auc',
                        n_jobs=4, iid=False, cv=5)
xsearch3.fit(X_train, y_train)
xsearch3.best_score_
xsearch3.best_params_

# 子采样率和每个子树的子采样率调优 {'colsample_bytree': 0.7, 'subsample': 0.9}
xgb4 = XGBClassifier(max_depth=5,
                     learning_rate=0.1,
                     n_estimators=140,
                     min_child_weight=1,
                     gamma=0,
                     subsample=0.8,
                     colsample_bytree=0.8,
                     objective= 'binary:logistic',
                     scale_pos_weight=1,
                     n_jobs=4,
                     seed=10)
parameter4 = {'subsample': np.arange(0.6, 1, 0.1), 'colsample_bytree': np.arange(0.6, 1, 0.1)}
xsearch4 = GridSearchCV(estimator=xgb4, param_grid=parameter4, scoring='roc_auc',n_jobs=4, iid=False, cv=5)
xsearch4.fit(X_train, y_train)
xsearch4.best_score_
xsearch4.best_params_

# auc:0.9040838147402178
xgb5 = XGBClassifier(max_depth=5,
                     learning_rate=0.1,
                     n_estimators=140,
                     min_child_weight=1,
                     gamma=0,
                     subsample=0.9,
                     colsample_bytree=0.7,
                     objective= 'binary:logistic',
                     scale_pos_weight=1,
                     n_jobs=4,
                     seed=10)
xgb5.fit(X_train, y_train)
y_predprob = xgb5.predict_proba(X_train)
metrics.roc_auc_score(y_train, y_predprob[:, 1])