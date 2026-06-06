import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.decomposition import PCA

iris = datasets.load_iris()
X = iris.data
y = iris.target

mask = (y == 0) | (y == 1)
X_filtered = X[mask]
y_filtered = y[mask]

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_filtered)

plt.figure(figsize=(8, 6))
plt.scatter(X_pca[y_filtered == 0, 0], X_pca[y_filtered == 0, 1],
            color='red', label='Setosa', alpha=0.8, edgecolors='k')
plt.scatter(X_pca[y_filtered == 1, 0], X_pca[y_filtered == 1, 1],
            color='blue', label='Versicolor', alpha=0.8, edgecolors='k')

plt.title('PCA: Проекция двух сортов Iris на главные компоненты')
plt.xlabel('Главная компонента 1')
plt.ylabel('Главная компонента 2')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('plot1.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.show()