#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Performed based on correlation values between rows and columns
# recommends the movies based on interest of past movies
def movie_recommender(movie_name=None):
    
    from scipy import sparse
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    movies = pd.read_csv(r'C://Users//puppa//Documents//Python Files//Basic Voice Assistant//Code//Datasets//MoviesDataset//movies.csv')
    ratings = pd.read_csv(r'C://Users//puppa//Documents//Python Files//Basic Voice Assistant//Code//Datasets//MoviesDataset//ratings.csv')
    
    # replacing the movie titles to lower case and removing special chars to match the data
    movies["title"] = movies["title"].str.replace("[)(,.:;!%$@^&*?<>{}\|/~`]","")
    movies["title"] = movies["title"].str.lower()
    
    # merging movies and ratings based on movie_Id
    dataset = pd.merge(ratings,movies,on='movieId')
    
    # grouping the data based on title with mean rating
    grp_data_mean = dataset.groupby('title')['rating'].mean()
    
    # sorting the data to fetch top-5 movies
    sorted_ratings_movie = grp_data_mean.sort_values(ascending=False)
    # grouping the data based on title with count rating
    grp_data_ct = dataset.groupby('title')['rating'].count()
    
    new_record = pd.DataFrame()
    new_record['Average_ratings'] = grp_data_mean
    new_record['count of total ratings'] = grp_data_ct
    
    # grouping data based on usedId with columns as title and values as ratings
    # fetches the movies based on ratings correlation with rows and cols of movie matrix data.
    # corrwith() is used to compute pairwise correlation between rows or columns of two DataFrame objects.
    movie_matrix = dataset.pivot_table(index='userId',columns='title',values='rating')
    if movie_name:
        rating = movie_matrix[movie_name]
        movie = movie_matrix.corrwith(rating)
        movie.dropna(inplace=True)
        movie = movie.sort_values(ascending=False)
        movie = movie.head(5)
        return movie
    
    return sorted_ratings_movie.head(5)

if __name__ == "__main__":
    movie_recommender()


# In[ ]:




