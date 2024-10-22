# -*- coding: utf-8 -*-
"""clustering based recommendation(part6)rs.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1S6IrOj8-pmk346R7M1dVit7Q6_0GyznQ
"""

# Commented out IPython magic to ensure Python compatibility.
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# %matplotlib inline

# Importing the pandas library, which is commonly used for data manipulation and analysis
import pandas as pd

# Defining the URL of the CSV file containing user profiles
user_profile_url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-ML321EN-SkillsNetwork/labs/datasets/user_profile.csv"

# Using pandas' read_csv function to read the CSV file from the specified URL into a DataFrame
user_profile_df = pd.read_csv(user_profile_url)

# Displaying the first few rows of the DataFrame to inspect its contents
user_profile_df.head()

feature_names = list(user_profile_df.columns[1:])
feature_names

user_profile_df.describe()

# Use StandardScaler to make each feature with mean 0, standard deviation 1
# Instantiating a StandardScaler object
scaler = StandardScaler()

# Standardizing the selected features (feature_names) in the user_profile_df DataFrame
user_profile_df[feature_names] = scaler.fit_transform(user_profile_df[feature_names])

# Printing the mean and standard deviation of the standardized features
print("mean {} and standard deviation{} ".format(user_profile_df[feature_names].mean(), user_profile_df[feature_names].std()))

user_profile_df.describe()

features = user_profile_df.loc[:, user_profile_df.columns != 'user']
features

user_ids = user_profile_df.loc[:, user_profile_df.columns == 'user']
user_ids

# Import necessary libraries
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# List of potential n_clusters values to try (1 to 30)
list_k = list(range(1, 30))

# Create an empty list to store sum of squared distances (inertia)
inertia_values = []

# Set a random state for reproducibility
rs = 42

# Perform grid search to find the optimal number of clusters
for k in list_k:
    # Initialize KMeans model with k clusters and a fixed random state
    kmeans_model = KMeans(n_clusters=k, random_state=rs)

    # Fit the model to the features
    kmeans_model.fit(features)

    # Append the model's inertia (sum of squared distances) to the list
    inertia_values.append(kmeans_model.inertia_)

# Plot the sum of squared distances against the k values
plt.figure(figsize=(10, 6))
plt.plot(list_k, inertia_values, marker='o', linestyle='--')
plt.title('Elbow Method for Optimal k')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Sum of Squared Distances (Inertia)')
plt.grid(True)
plt.show()

cluster_labels = [None] * len(user_ids)

optimized_n_clusters = 5
model = KMeans(n_clusters=optimized_n_clusters, random_state=42)
model.fit(features)

# Extracting cluster labels
cluster_labels = model.labels_

# Create a DataFrame to combine user IDs and their corresponding cluster labels
user_clusters_df = pd.DataFrame({'user': user_ids.values.flatten(), 'cluster': cluster_labels})

# Display the DataFrame
print(user_clusters_df)

"""**TASK: Apply PCA on user profile feature vectors to reduce dimensionst**"""

# Extracting features from the user_profile_df DataFrame, excluding the 'user' column
features = user_profile_df.loc[:, user_profile_df.columns != 'user']

# Extracting user IDs from the user_profile_df DataFrame
user_ids = user_profile_df.loc[:, user_profile_df.columns == 'user']

# Creating a list of feature names by excluding the 'user' column name
feature_names = list(user_profile_df.columns[1:])

print(f"There are {len(feature_names)} features for each user profile.")

sns.set_theme(style="white")

# Compute the correlation matrix
corr = features.cov()

# Generate a mask for the upper triangle
mask = np.triu(np.ones_like(corr, dtype=bool))

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(230, 20, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})


plt.show()

# Create a list to hold the explained variance ratios
explained_variances = []

# Define a range for the number of components to test
n_components_list = range(1, 15)  # Testing from 1 to 14 components

for n_components in n_components_list:
    pca = PCA(n_components=n_components)
    pca.fit(features)  # Fit PCA on features
    explained_variances.append(sum(pca.explained_variance_ratio_))  # Store cumulative variance

# Plotting the explained variance to visualize the results
plt.figure(figsize=(10, 6))
plt.plot(n_components_list, explained_variances, marker='o')
plt.title('Cumulative Explained Variance by Number of Components')
plt.xlabel('Number of Components')
plt.ylabel('Cumulative Explained Variance')
plt.axhline(y=0.9, color='r', linestyle='--')  # Line at 90%
plt.xticks(n_components_list)
plt.grid()
plt.show()

# Find the minimum number of components that explains at least 90% variance
optimized_n_components = next(n for n, variance in zip(n_components_list, explained_variances) if variance >= 0.9)

print(f"The optimized number of components that explain at least 90% variance is: {optimized_n_components}")

# Finding the minimum n that explains at least 90% variance
optimal_n = next(n for n, ratio in zip(n_components_list, explained_variances) if ratio >= 0.90)

# Perform PCA with the optimal number of components
pca = PCA(n_components=optimal_n)
components = pca.fit_transform(features)

# Create a DataFrame for the transformed features
components_df = pd.DataFrame(data=components)

# Merge the user_ids with the transformed features
pca_results_df = pd.merge(user_ids, components_df, left_index=True, right_index=True)

# Display the PCA transformed DataFrame
print(pca_results_df.head(10))

"""**TASK: Perform k-means clustering on the PCA transformed feature vectors**"""

# Assuming n_clusters is already defined from previous steps
# Apply KMeans on the PCA features
n_clusters = 5
kmeans_pca = KMeans(n_clusters=n_clusters, random_state=rs)
kmeans_pca.fit(components)  # components is the PCA-transformed features

# Obtain the cluster label lists
pca_cluster_labels = kmeans_pca.labels_

# Create a DataFrame to combine user IDs and PCA cluster labels
pca_clustering_results = pd.DataFrame({
    'user': user_ids.values.flatten(),  # Flatten user_ids for merging
    'cluster_label': pca_cluster_labels
})

# Display the clustering results
print(pca_clustering_results)

"""**TASK: Generate course recommendations based on the popular courses in the same cluster**"""

test_user_url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-ML0321EN-Coursera/labs/v2/module_3/ratings.csv"

# Reading the test user data CSV file into a pandas DataFrame
# Selecting only the 'user' and 'item' columns using indexing
test_users_df = pd.read_csv(test_user_url)[['user', 'item']]

# Displaying the first few rows of the DataFrame to inspect its contents
test_users_df.head()

test_users_labelled = pd.merge(test_users_df, pca_clustering_results, left_on='user', right_on='user')
test_users_labelled

# Extracting the 'item' and 'cluster' columns from the test_users_labelled DataFrame
courses_cluster = test_users_labelled[['item', 'cluster_label']]

# Adding a new column 'count' with a value of 1 for each row in the courses_cluster DataFrame
courses_cluster['count'] = [1] * len(courses_cluster)

# Grouping the DataFrame by 'cluster' and 'item', aggregating the 'count' column with the sum function,
# and resetting the index to make the result more readable
courses_cluster_grouped = courses_cluster.groupby(['cluster_label','item']).agg(enrollments=('count','sum')).reset_index()

# Setting a threshold for popularity
popularity_threshold = 10

# Initialize a dictionary to hold recommendations for each user
recommendations = {}

# Iterate through each user in the test users DataFrame
for user_id in test_users_labelled['user'].unique():
    # Create a subset for the current user
    user_subset = test_users_labelled[test_users_labelled['user'] == user_id]

    # Get the enrolled courses for the user
    enrolled_courses = set(user_subset['item'])

    # Get the cluster label for the user (assuming all entries for a user have the same cluster)
    cluster_label = user_subset['cluster_label'].iloc[0]

    # Find all courses in the same cluster
    courses_in_cluster = set(test_users_labelled[test_users_labelled['cluster_label'] == cluster_label]['item'])

    # Find new/unseen courses by taking the set difference
    unseen_courses = courses_in_cluster.difference(enrolled_courses)

    # Filter for popular courses based on the count threshold
    popular_courses = courses_cluster_grouped[courses_cluster_grouped['enrollments'] > popularity_threshold]

    # Find unseen and popular courses
    recommended_courses = popular_courses[popular_courses['item'].isin(unseen_courses)]

    # Store the recommendations for the user
    recommendations[user_id] = recommended_courses['item'].tolist()

# Display the recommendations for each user
for user, recs in recommendations.items():
    print(f"Recommendations for User {user}: {recs}")



