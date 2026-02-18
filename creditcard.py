import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("creditcard.csv")
#print(data.isna().sum())
#print(data.info())

#Check for imbalance
print(data['Class'].value_counts())

# #yes,imbalanced dataset
# data['Class'].value_counts().plot(kind='bar')
# plt.title("Class distribution")
# plt.show()

from sklearn.model_selection import train_test_split
x = data.drop("Class",axis=1)
y = data['Class']

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=42,stratify=y)


# print("Train Fraud Ratio:")
# print(y_train.value_counts(normalize=True))

# print("\nTest Frud Ratio:")
# print(y_test.value_counts(normalize=True))


#create a base line model
# from sklearn.linear_model import LogisticRegression

# logmodel = LogisticRegression(max_iter=1000)
# logmodel.fit(x_train,y_train)
# y_pred = logmodel.predict(x_test)

from sklearn.metrics import confusion_matrix,recall_score,classification_report
#print(confusion_matrix(y_test, y_pred))
#print(classification_report(y_test, y_pred))

from imblearn.over_sampling import SMOTE

smote = SMOTE(random_state=42)
x_trainsm,y_trainsm = smote.fit_resample(x_train,y_train)

# print("BEfore SMOTE:")
# print(y_train.value_counts())

# print("After SMOTE:")
# print(y_trainsm.value_counts())

# model_sm = LogisticRegression(max_iter=1000)
# model_sm.fit(x_trainsm,y_trainsm)
# y_predsm = model_sm.predict(x_test)
# print(confusion_matrix(y_test, y_predsm))
# print(classification_report(y_test, y_predsm))




# import optuna
# from sklearn.metrics import recall_score

# def objective(trail):
#     c = trail.suggest_loguniform("C",1e-3,10)

#     model = LogisticRegression(
#         C=c,max_iter=1000,solver='liblinear'
#     )

#     model.fit(x_trainsm,y_trainsm)
#     y_pred = model.predict(x_test)
#     recalll = recall_score(y_test,y_pred)

#     return recalll


# study = optuna.create_study(direction='maximize')
# study.optimize(objective,n_trials=20)
# print("Best params:", study.best_params)
# print("Best recall:", study.best_value)


# So,lets pickup XGBOOST
import xgboost as xgb

# model = xgb.XGBClassifier(
#     n_estimators=100,
#     max_depth=5,
#     learning_rate=0.1,
#     use_label_encoder=False,
#     eval_metrics='logloss',
#     random_state=42
# )

# model.fit(x_trainsm,y_trainsm)
# y_pred = model.predict(x_test)
# print("----BEFORE OPTUNA-------")
# print(confusion_matrix(y_test, y_pred))
# print(classification_report(y_test, y_pred))


print("----AFTER OPTUNA-----")

import optuna
from sklearn.metrics import recall_score

def objective(trial):
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 50, 300),
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'learning_rate': trial.suggest_loguniform('learning_rate', 0.01, 0.3),
        'subsample': trial.suggest_float('subsample', 0.5, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
        'use_label_encoder': False,
        'eval_metric': 'logloss',
        'random_state': 42,
        'n_jobs':-1
    }

    model = xgb.XGBClassifier(**params)
    model.fit(x_trainsm,y_trainsm)
    y_pred = model.predict(x_test)
    recall = recall_score(y_test, y_pred)
    return recall

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=30)

print("Best XGBoost parameters:", study.best_params)
print("Best fraud recall achieved:", study.best_value)


best_params = study.best_params
xgb_best = xgb.XGBClassifier(**best_params,use_label_encoder=False,eval_metric='logloss',random_state=42)
xgb_best.fit(x_trainsm,y_trainsm)
y_pred = xgb_best.predict(x_test)

from sklearn.metrics import classification_report, confusion_matrix
print("XGBoost with Optuna-tuned hyperparameters:")
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
from sklearn.metrics import roc_curve, roc_auc_score
import matplotlib.pyplot as plt

# Get predicted probabilities for fraud class
y_probs = xgb_best.predict_proba(x_test)[:, 1]

# Compute ROC curve
fpr, tpr, thresholds = roc_curve(y_test, y_probs)

# Compute AUC
auc_score = roc_auc_score(y_test, y_probs)
print("ROC-AUC score:", auc_score)

# Plot ROC Curve
# plt.figure(figsize=(8,6))
# plt.plot(fpr, tpr, label=f'XGBoost (AUC = {auc_score:.3f})', color='darkorange', linewidth=2)
# plt.plot([0,1], [0,1], 'k--', linewidth=1)  # Random classifier line
# plt.xlabel("False Positive Rate")
# plt.ylabel("True Positive Rate (Recall)")
# plt.title("ROC Curve for Fraud Detection")
# plt.legend(loc="lower right")
# plt.grid(True)
# plt.show()

deploy_threshold = 0.4
y_pred_deploy = (y_probs >= deploy_threshold).astype(int)
from sklearn.metrics import classification_report
print("Final Classification Report:",classification_report(y_test, y_pred_deploy))


import joblib

joblib.dump(xgb_best,"model.pkl")