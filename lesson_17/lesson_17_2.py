#Bagging

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

iris = sns.load_dataset("iris")

# print (iris.head())

species_int = []
for row in iris.values:
    match row[4]:
        case "setosa":
            species_int.append(1)
        case "versicolor":
            species_int.append(2)
        case "virginica":
            species_int.append(3)

# species_int_df = pd.DataFrame(species_int)
# print(species_int_df.head())

data = iris[["sepal_length", "petal_length"]]
data["species"] = species_int

print(data.head())
print(data.shape)

data_df = data[(data["species"] == 3) | (data["species"] == 2)]
print(data_df.shape)

data_of_versicolor = data[data["species"] == 2]
data_of_virginica = data[data["species"] == 3]

data_of_virginica_A = data_of_virginica.iloc[:25, :]
data_of_virginica_B = data_of_virginica.iloc[25:, :]

data_of_versicolor_А = data_of_versicolor.iloc[:25, :]
data_of_versicolor_B = data_of_versicolor.iloc[25:, :]


data_df_A = pd.concat([data_of_virginica_A, data_of_versicolor_А], ignore_index=True)
data_df_B = pd.concat([data_of_virginica_B, data_of_versicolor_B], ignore_index=True)


X = data_df[["sepal_length", "petal_length"]]
y = data_df["species"]


x1_p = np.linspace(min(data_df["sepal_length"]), max(data_df["sepal_length"]), 100)
x2_p = np.linspace(min(data_df["petal_length"]), max(data_df["petal_length"]), 100)

X1_p, X2_p = np.meshgrid(x1_p, x2_p)

print(X1_p.shape)

X_p = pd.DataFrame(np.vstack([X1_p.ravel(), X2_p.ravel()]).T, columns=["sepal_length", "petal_length"] )

print (X_p.head())


from sklearn.tree import DecisionTreeClassifier

max_depth = [1, 3, 5, 7]

fig, ax = plt.subplots(2, 4, sharex="col", sharey="row")

X = data_df_A[["sepal_length", "petal_length"]]
y = data_df_A["species"]

j = 0
for md in max_depth:

    model = DecisionTreeClassifier(max_depth=md)
    model.fit(X, y)


    y_p = model.predict(X_p)

    ax[0, j].scatter(data_of_virginica_A["sepal_length"], data_of_virginica_A["petal_length"])
    ax[0, j].scatter(data_of_versicolor_А["sepal_length"], data_of_versicolor_А["petal_length"])

    ax[0, j].contourf(X1_p, X2_p, y_p.reshape(X1_p.shape), alpha=0.3, levels=[0, 2.5, 3.5])
    j += 1


X = data_df_B[["sepal_length", "petal_length"]]
y = data_df_B["species"]

j = 0
for md in max_depth:

    model = DecisionTreeClassifier(max_depth=md)
    model.fit(X, y)


    y_p = model.predict(X_p)

    ax[1, j].scatter(data_of_virginica_B["sepal_length"], data_of_virginica_B["petal_length"])
    ax[1, j].scatter(data_of_versicolor_B["sepal_length"], data_of_versicolor_B["petal_length"])

    ax[1, j].contourf(X1_p, X2_p, y_p.reshape(X1_p.shape), alpha=0.3, levels=[0, 2.5, 3.5])
    j += 1

plt.show()



