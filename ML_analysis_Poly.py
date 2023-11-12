'''
This file is to conduct machine learning analysis
(polynomial regression model) to study the effect of tweets on the price change of Bitcoins.
The twitter information (twt_synchronous.csv file) is preprocessed
(splitting data, selected features, check for regression assumptions)
followed by polynomial analysis, RMSE calculation, and model drawing.
'''

# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 14:41:16 2023

"""
# In[] Preprocessing
import HappyML.preprocessor as pp

# Load Dataset
dataset = pp.dataset(file="twt_synchronous.csv")

# Decomposition of Variables
X, Y = pp.decomposition(dataset, x_columns=[1,2,3,4,5,6,7,8,9,10,11,12,13], y_columns=[14])

# Training / Testing Set
X_train, X_test, Y_train, Y_test = pp.split_train_test(x_ary=X, y_ary=Y, train_size=0.8)

# selected_features
from HappyML.regression import MultipleRegressor

regressor = MultipleRegressor()
selected_features = regressor.backward_elimination(X, Y, verbose=True)
Y_predict = regressor.fit(X_train, Y_train).predict(X_test)

# Feature Scaling
X = pp.feature_scaling(fit_ary=X, transform_arys=(X))
Y = pp.feature_scaling(fit_ary=Y, transform_arys=(Y))

# Add one constant column
X_train = pp.add_constant(X_train)
X_test = pp.add_constant(X_test)

# In[] Check for Assumption of Regression
from HappyML.criteria import AssumptionChecker

checker = AssumptionChecker(X_train.iloc[:, selected_features], X_test.iloc[:, selected_features], Y_train, Y_test, Y_predict)
checker.y_lim = (-4, 4)
checker.heatmap = True
checker.check_all()

# In[] Polynomial Regression with HappyML's Class
from HappyML.regression import PolynomialRegressor
import HappyML.model_drawer as md

reg_poly = PolynomialRegressor()
reg_poly.best_degree(x_train=X_train, y_train=Y_train, x_test=X_test, y_test=Y_test, verbose=True)
Y_poly = reg_poly.fit(x_train=X, y_train=Y).predict(x_test=X)

#print("Multiple Regression_Adjusted R-Squared Score):", regressor.r_score())
print("Multiple Regression_Adjusted R-Squared Score):", reg_poly.r_score())
md.sample_model(sample_data=(X, Y), model_data=(X, Y_poly))

# In[] RMSE of the model

from HappyML.performance import rmse

rmse_poly = rmse(Y, Y_poly)

print("RMSE Polynomial:{:.4f}".format(rmse_poly))
