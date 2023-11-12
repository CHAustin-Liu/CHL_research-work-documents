'''
This file is to conduct machine learning analysis (neural network model)
to study the effect of tweets on the price change of Bitcoins.
The twitter information (twt_synchronous.csv file) is preprocessed (splitting data, selected features)
followed by neural network analysis, and RMSE calculation.
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
X, Y = pp.decomposition(dataset, x_columns=[1,2,3,4,5,6,7,8,9,10,11,12], y_columns=[14])

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

# In[] Neural Networks without HappyML's Class
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Initialize the whole Neural Networks
regressor = Sequential()

# Add the Input & First Hidden Layer
regressor.add(Dense(input_dim=X_train.shape[1], units=6, kernel_initializer="normal", activation="relu"))

# Add the Second Hidden Layer
regressor.add(Dense(units=3, kernel_initializer="normal", activation="relu"))

# Add the Output Layer
regressor.add(Dense(units=1, kernel_initializer="normal", activation="linear"))

# Compile the whole Neural Networks
regressor.compile(optimizer="adam", loss="mse", metrics=["mse"])

# Fit
regressor.fit(x=X_train, y=Y_train, batch_size=5, epochs=10)

# Predict
import pandas as pd
Y_pred = pd.DataFrame(regressor.predict(x=X_test), index=Y_test.index, columns=Y_test.columns)

# In[] Performance with RMSE
from HappyML.performance import rmse

print("The RMSE of Neural Networks: {:.4f}".format(rmse(Y_test, Y_pred)))

