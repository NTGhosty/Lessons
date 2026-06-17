#Bagging

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

iris = sns.load_dataset("iris")

print (iris.head())

species_int = []
for row in iris.values:
    match row[4]:
        case "setosa":
            species_int.append(1)
        case "versicolor":
            species_int.append(2)
        case "virginica":
            species_int.append(3)

species_int_df = pd.DataFrame(species_int)
print(species_int_df.head())

data = iris[["sepal_length", "petal_length"]]
data["species"] = species_int

print(data.head())
print(data.shape)

data_df = data[(data["species"] == 3) | (data["species"] == 2)]
print(data_df.shape)

data_of_setosa = data[data["species"] == 3]
data_of_versicolor = data[data["species"] == 2]

plt.scatter(data_of_setosa["sepal_length"], data_of_setosa["petal_length"])
plt.scatter(data_of_versicolor["sepal_length"], data_of_versicolor["petal_length"])


X = data_df[["sepal_length", "petal_length"]]
y = data_df["species"]



x1_p = np.linspace(min(data_df["sepal_length"]), max(data_df["sepal_length"]), 100)
x2_p = np.linspace(min(data_df["petal_length"]), max(data_df["petal_length"]), 100)

X1_p, X2_p = np.meshgrid(x1_p, x2_p)

print(X1_p.shape)

X_p = pd.DataFrame(np.vstack([X1_p.ravel(), X2_p.ravel()]).T, columns=["sepal_length", "petal_length"] )

print (X_p.head())

from sklearn.tree import DecisionTreeClassifier

max_depth = [[1, 2, 3, 4], [5, 6, 7, 8]]

fig, ax = plt.subplots(2, 4, sharex="col", sharey="row")

for i in range(2):
    j = 0
    for md in max_depth[i]:

        model = DecisionTreeClassifier()
        model.fit(X, y)


        y_p = model.predict(X_p)

        ax[i, j].scatter(data_of_setosa["sepal_length"], data_of_setosa["petal_length"])
        ax[i, j].scatter(data_of_versicolor["sepal_length"], data_of_versicolor["petal_length"])

        ax[i, j].contourf(X1_p, X2_p, y_p.reshape(X1_p.shape), alpha=0.3, levels=[0, 2.5, 3.5])
        j += 1


plt.show()

