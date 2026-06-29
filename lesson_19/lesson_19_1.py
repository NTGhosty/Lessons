import numpy as np
import pandas as pd

data = pd.read_csv("../data/phishing.csv")
print(data.head())

print(data.columns)

X = data.drop(columns=["class"])
print(X.columns)

y = pd.DataFrame(data["class"])
print(y.columns)


from sklearn.model_selection import train_test_split

X_tr, X_tst, y_tr, y_tst = train_test_split(
X, y, test_size=0.25
)

from sklearn.tree import DecisionTreeClassifier

dt = DecisionTreeClassifier()

model = dt.fit(X_tr, y_tr)

predict = model.predict(X_tst)

from sklearn.metrics import accuracy_score

print(accuracy_score(y_tst, predict))

# Классификации: бинарные(двоичные), мультиклассовые, многометочные
# - точность (precision) - стоимость ложных срабатываний высока
# - полнота (recall) - стоимость ложноотрицательных срабатываний высока
# - специфичность (specificity) = полнота (наоборот). насколько точно определяются отрицательные образцы
# - чувствительность (sensitivity) = полнота.
# - F1-мера

# Метрики: - процент ошибок, процент правильных ответов (accuracy)
# Типы ошибочных ответов: ложноположительные (ложная тревога), ложноотрицательные (ложный пропуск)
# Типы правильных ответов: истинноположительные, истинноотрицательные