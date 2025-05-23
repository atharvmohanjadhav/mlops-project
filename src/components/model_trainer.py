import pandas as pd
import numpy as np
import os,sys
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split,RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score,mean_absolute_error
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor,AdaBoostRegressor
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression,Lasso,Ridge
from catboost import CatBoostRegressor
from xgboost import XGBRegressor
from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass

from src.utils import save_object,eval_model

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts","model_trainer","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self,train_arr,test_arr):
        try:
            logging.info("Spliting train and test data")
            x_train,y_train,x_test,y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )

            models = {
                "Linear Regression":LinearRegression(),
                "Lasso":Lasso(),
                "Ridge":Ridge(),
                "K-Neighbors Regressor":KNeighborsRegressor(),
                "Decision Tree":DecisionTreeRegressor(),
                "Random Forest Regressor":RandomForestRegressor(),
                "XGB Regressor":XGBRegressor(),
                "Ada Boost Regressor":AdaBoostRegressor()
            }      

            model_report:dict = eval_model(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test,models=models)      
            best_model_score = max(sorted(model_report.values()))   
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]
            if best_model_score < 0.6:
                raise CustomException("No best model found")
            logging.info(f"best model found! {best_model}")

            save_object(file_path=self.model_trainer_config.trained_model_file_path,obj=best_model)

            predicted = best_model.predict(x_test)
            r2 = r2_score(y_test,predicted)
            return r2

        except Exception as e:
            raise CustomException(e,sys)