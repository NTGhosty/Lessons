import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

iris = datasets.load_iris()
X = iris.data
y = iris.target

mask = (y == 0) | (y == 1)
X_filtered = X[mask]
y_filtered = y[mask]

kmeans = KMeans(n_clusters=2, random_state=42)
y_kmeans = kmeans.fit_predict(X_filtered)

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_filtered)

centroids_pca = pca.transform(kmeans.cluster_centers_)

plt.figure(figsize=(8, 6))
plt.scatter(X_pca[y_kmeans == 0, 0], X_pca[y_kmeans == 0, 1],
            color='red', label='Кластер 0', alpha=0.8, edgecolors='k')
plt.scatter(X_pca[y_kmeans == 1, 0], X_pca[y_kmeans == 1, 1],
            color='blue', label='Кластер 1', alpha=0.8, edgecolors='k')

plt.scatter(centroids_pca[:, 0], centroids_pca[:, 1],
            color='black', marker='X', s=200, label='Центроиды', zorder=10)

plt.title('K-Means: Кластеризация двух сортов Iris (в пространстве PCA)')
plt.xlabel('Главная компонента 1')
plt.ylabel('Главная компонента 2')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
plt.savefig('plot3.png')