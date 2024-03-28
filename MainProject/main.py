import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR 
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor


df = pd.read_csv("Cars.csv")
for month in df["column_5"]:
    print(month.split(" ")[0])

