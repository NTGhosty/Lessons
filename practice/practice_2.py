import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import DecisionBoundaryDisplay

iris = datasets.load_iris()
X = iris.data
y = iris.target

mask = (y == 0) | (y == 1)
X_filtered = X[mask]
y_filtered = y[mask]

X_2d = X_filtered[:, :2]

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_2d, y_filtered)

fig, ax = plt.subplots(figsize=(8, 6))
DecisionBoundaryDisplay.from_estimator(
    rf, X_2d, response_method="predict", cmap=plt.cm.RdYlBu, alpha=0.8, ax=ax
)

ax.scatter(X_2d[y_filtered == 0, 0], X_2d[y_filtered == 0, 1],
           color='red', label='Setosa', edgecolor='k')
ax.scatter(X_2d[y_filtered == 1, 0], X_2d[y_filtered == 1, 1],
           color='blue', label='Versicolor', edgecolor='k')

ax.set_title('Random Forest: Граница решений для двух сортов Iris')
ax.set_xlabel(iris.feature_names[0])
ax.set_ylabel(iris.feature_names[1])
ax.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
plt.savefig('plot2.png')