# Аномалии
import numpy as np
import pandas as pd

data = pd.read_csv("../data/creditcard.csv")
print(data.head())

legit = data[data["Class"] == 0]
fraud = data[data["Class"] == 1]

X = data.drop(["Time", "Class"], axis=1)
y = data["Class"]

from sklearn.model_selection import train_test_split

X_tr, X_tst, y_tr, y_tst = train_test_split(
    X, y, test_size=0.25
)

from sklearn.linear_model import LogisticRegression

model1 = LogisticRegression()
model1.fit(X_tr, y_tr)

import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay

# ConfusionMatrixDisplay.from_estimator(
#     model1,
#     X_tst,
#     y_tst,
#     display_labels=["Легитимная", "Мошенническая"],
# )
# plt.show() # 14

from sklearn.metrics import precision_score, recall_score

# Точность
y_pred = model1.predict(X_tst)
print(precision_score(y_tst, y_pred))

# Полнота
print(recall_score(y_tst, y_pred))

# Специфичность
print(recall_score(y_tst, y_pred, pos_label=0))

# from sklearn.ensemble import RandomForestClassifier

# model2 = RandomForestClassifier(n_estimators=10)
# model1.fit(X_tr, y_tr)
# ConfusionMatrixDisplay.from_estimator(
#     model2,
#     X_tst,
#     y_tst,
#     display_labels=["Легитимная", "Мошенническая"],
# )
# plt.show() # ?

from sklearn.ensemble import GradientBoostingClassifier
model3 = GradientBoostingClassifier()
model3.fit(X_tr, y_tr)
ConfusionMatrixDisplay.from_estimator(
    model3,
    X_tst,
    y_tst,
    display_labels=["Легитимная", "Мошенническая"],
)

plt.show()
