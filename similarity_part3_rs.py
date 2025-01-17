# -*- coding: utf-8 -*-
"""similarity_part3_rs.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Uu3l2J_yPY0fVEAfhwNylSrPTTrpUp22
"""

!pip install nltk
!pip install gensim
!pip install scipy==1.10
!pip install pandas
!pip install matplotlib
!pip install seaborn

# Commented out IPython magic to ensure Python compatibility.
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import gensim
import pandas as pd
import nltk as nltk

from scipy.spatial.distance import cosine
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import ngrams
from gensim import corpora

# %matplotlib inline

bows_url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-ML321EN-SkillsNetwork/labs/datasets/courses_bows.csv"
bows_df = pd.read_csv(bows_url)
bows_df = bows_df[['doc_id', 'token', 'bow']]

bows_df.head(10)

course_url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-ML321EN-SkillsNetwork/labs/datasets/course_processed.csv"
course_df = pd.read_csv(course_url)

course_df.head(10)

course_df[course_df['COURSE_ID'] == 'ML0101ENv3']

ml_course = bows_df[bows_df['doc_id'] == 'ML0101ENv3']
ml_course

ml_courseT = ml_course.pivot(index=['doc_id'], columns='token').reset_index(level=[0])
ml_courseT

def pivot_two_bows(basedoc, comparedoc):
    """
    Pivot two bag-of-words (BoW) representations for comparison.

    Parameters:
    basedoc (DataFrame): DataFrame containing the bag-of-words representation for the base document.
    comparedoc (DataFrame): DataFrame containing the bag-of-words representation for the document to compare.

    Returns:
    DataFrame: A DataFrame with pivoted BoW representations for the base and compared documents,
    facilitating direct comparison of word occurrences between the two documents.
    """

    # Create copies of the input DataFrames to avoid modifying the originals
    base = basedoc.copy()
    base['type'] = 'base'  # Add a 'type' column indicating base document
    compare = comparedoc.copy()
    compare['type'] = 'compare'  # Add a 'type' column indicating compared document

    # Concatenate the two DataFrames vertically
    join = pd.concat([base, compare])

    # Pivot the concatenated DataFrame based on 'doc_id' and 'type', with words as columns
    joinT = join.pivot(index=['doc_id', 'type'], columns='token').fillna(0).reset_index(level=[0, 1])

    # Assign meaningful column names to the pivoted DataFrame
    joinT.columns = ['doc_id', 'type'] + [t[1] for t in joinT.columns][2:]

    # Return the pivoted DataFrame for comparison
    return joinT

course1 = bows_df[bows_df['doc_id'] == 'ML0151EN']
course2 = bows_df[bows_df['doc_id'] == 'ML0101ENv3']

bow_vectors = pivot_two_bows(course1, course2)
bow_vectors

similarity = 1 - cosine(bow_vectors.iloc[0, 2:], bow_vectors.iloc[1, 2:])
similarity

course_df[course_df['COURSE_ID'] == 'ML0101ENv3']

from sklearn.metrics.pairwise import cosine_similarity

# Set a similarity threshold
similarity_threshold = 0.5

# Get the BoW for the pivot course 'ML0101ENv3'
pivot_course_bow = bows_df[bows_df['doc_id'] == 'ML0101ENv3']

# List to store similar courses
similar_courses = []

# Loop over all other courses except 'ML0101ENv3'
for course_id in bows_df['doc_id'].unique():
    if course_id != 'ML0101ENv3':
        # Get the BoW for the current course
        current_course_bow = bows_df[bows_df['doc_id'] == course_id]

        # Use the pivot_two_bows function to get the BoW vectors for both courses
        bow_vectors = pivot_two_bows(pivot_course_bow, current_course_bow)

        # Calculate the cosine similarity
        similarity = 1 - cosine(bow_vectors.iloc[0, 2:], bow_vectors.iloc[1, 2:])

        # If the similarity exceeds the threshold, add to the list
        if similarity > similarity_threshold:
            similar_courses.append({
                'course_id': course_id,
                'similarity': similarity,
                'title': course_df[course_df['COURSE_ID'] == course_id]['TITLE'].values[0],
                'description': course_df[course_df['COURSE_ID'] == course_id]['DESCRIPTION'].values[0]
            })

# Print the results
for course in similar_courses:
    print(f"Course ID: {course['course_id']}")
    print(f"Title: {course['title']}")
    print(f"Description: {course['description']}")
    print(f"Similarity: {course['similarity']:.2f}")
    print("=" * 50)









