import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import silhouette_score

# Load the data
data = pd.read_csv('master_train.csv')

# Encode categorical variable 'zip'
label_encoder = LabelEncoder()
data['zip'] = label_encoder.fit_transform(data['zip'])

# Standardize numerical features
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data.drop('zip', axis=1))

# Define the ground truth labels for KNN
labels = data['zip'].values

# Define the range of k values for KNN
k_values = range(2, 10)

# Initialize lists to store silhouette scores for each algorithm
knn_scores = []
kmeans_scores = []
hierarchical_scores = []

# Initialize lists to store predicted labels for KNN
knn_predicted_labels = []

# Initialize lists to store cluster centers for K-means
kmeans_cluster_centers = []

# Initialize lists to store predicted labels for hierarchical clustering
hierarchical_predicted_labels = []

# Apply KNN
for k in k_values:
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(data_scaled, labels)
    knn_predicted = knn.predict(data_scaled)
    knn_predicted_labels.append(knn_predicted)
    knn_scores.append(silhouette_score(data_scaled, knn_predicted))

# Apply K-means
for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(data_scaled)
    kmeans_predicted = kmeans.labels_
    kmeans_cluster_centers.append(kmeans.cluster_centers_)
    kmeans_scores.append(silhouette_score(data_scaled, kmeans_predicted))

# Apply hierarchical clustering
for k in k_values:
    hierarchical = AgglomerativeClustering(n_clusters=k)
    hierarchical.fit(data_scaled)
    hierarchical_predicted = hierarchical.labels_
    hierarchical_predicted_labels.append(hierarchical_predicted)
    hierarchical_scores.append(silhouette_score(data_scaled, hierarchical_predicted))

# Plot the silhouette scores
plt.plot(k_values, knn_scores, label='KNN')
plt.plot(k_values, kmeans_scores, label='K-means')
plt.plot(k_values, hierarchical_scores, label='Hierarchical')
plt.xlabel('Number of clusters (k)')
plt.ylabel('Silhouette Score')
plt.title('Comparison of Clustering Algorithms')
plt.legend()
plt.show()
