from sklearn.cluster import kmeans
import numpy as np
import matplotlib.pyplot as plt

# list of provided ids
ids = [
    203184745, 203184750, 207243920, 203081516, 212281190, 207253583, 212034493,
    203485659, 203263077, 207418802, 207269266, 207403540, 203184734, 207262989,
    203327732, 207312200, 212160115
]

# reshaping ids for clustering
id_array = np.array(ids).reshape(-1, 1)

# histogram of ids
plt.figure(figsize=(10, 4))
plt.hist(ids, bins=30, color='blue', alpha=0.7)
plt.title('histogram of ids')
plt.xlabel('id value')
plt.ylabel('frequency')
plt.show()

kmeans = kmeans(n_clusters=3)  # assumption of 3 clusters for initial analysis
id_labels = kmeans.fit_predict(id_array)

plt.figure(figsize=(10, 4))
colors = ['red', 'green', 'blue']
for i in range(3):
    plt.scatter(id_array[id_labels == i], np.zeros_like(id_array[id_labels == i]) + i, label=f'cluster {i+1}', color=colors[i])
plt.title('clustered ids')
plt.xlabel('id value')
plt.yticks([])
plt.legend()
plt.show()

kmeans.cluster_centers_
