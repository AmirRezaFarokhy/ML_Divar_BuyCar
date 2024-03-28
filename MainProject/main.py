import pandas as pd
import numpy as np
from unidecode import unidecode

from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR 
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error
from sklearn import model_selection


df = pd.read_csv("Cars.csv")


for i, month in enumerate(df["colume_5"]):
    df["colume_5"].iloc[i] = unidecode(month.split(" ")[0].strip())


urls = df['url']
X = df[['colume_3', 'colume_4', 'colume_5', 'colume_6', 'colume_10', 'colume_11']].values
y = df['price'].values
x_train = X[:-2]
y_train = y[:-2]
x_test = X[-2:]
y_test = y[-2:]


# To find how many Neighbor we must put in variable
def TestKNNAlgo():
    rmse_lst = []
    for k in range(1, 6):
        knn = KNeighborsRegressor(n_neighbors=k)
        knn.fit(X, y)
        y_pred = knn.predict(x_test)
        error = np.sqrt(mean_squared_error(y_test, y_pred))
        rmse_lst.append(error)
        print(f'RMSE value for k= {k} is: {error}')
    # This algoritm is not good at all,


# Test another algoritms
def CreateModels():
    models = []
    models.append(("LinearModel", LinearRegression(n_jobs=5)))
    models.append(("SVM", SVR()))
    models.append(("Tree", DecisionTreeRegressor()))

    results = []
    names = []
    for name, model in models:
        kfold = model_selection.KFold(n_splits=10)
        cv_results = model_selection.cross_val_score(model, x_train, y_train, cv=kfold, scoring="neg_root_mean_squared_error")
        results.append(cv_results)
        names.append(name)
        print(f"{name} : , {cv_results.mean()} ({cv_results.std()})")
    # This is a exersise working, if we have 100 or 1000 data then we can get very better reuslt's
    

# Test an algoritm
def TestTestingData():
    mld = DecisionTreeRegressor()
    mld.fit(x_train, y_train)   
    pred = mld.predict(x_test)
    for p, r in zip(pred, y_test):
        print(f"The real price is: {r}, and the predict of model is: {p}")


# Test an algoritm
def TestTrainingData():
    mld = DecisionTreeRegressor()
    mld.fit(x_train, y_train)
    pred = mld.predict(x_train)
    for p, r in zip(pred, y_train):
        print(f"The real price is: {r}, and the predict of model is: {p}")