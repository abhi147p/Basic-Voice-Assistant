#!/usr/bin/env python
# coding: utf-8

# In[23]:


# Performed based on KNN algorithm
# recommends the books based on interest of past books
def book_recommender(book_name=None):

    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import warnings
    warnings.simplefilter(action='ignore', category=FutureWarning)

    books = pd.read_csv(r'C://Users//puppa//Documents//Python Files//Basic Voice Assistant//Code//Datasets//BooksDataset//BX-Books.csv',sep=";",error_bad_lines=False,encoding='latin-1')
    # converting the book titles to lower case
    books["Book-Title"] = books["Book-Title"].str.lower()
    books=books[['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher']]
    books.rename(columns={'Book-Title':'title','Book-Author':'author','Year-Of-Publication':'year'},inplace=True)
    
    # users and ratings
    users = pd.read_csv(r'C://Users//puppa//Documents//Python Files//Basic Voice Assistant//Code//Datasets//BooksDataset//BX-Users.csv',sep=";",error_bad_lines=False,encoding='latin-1')
    ratings = pd.read_csv(r'C://Users//puppa//Documents//Python Files//Basic Voice Assistant//Code//Datasets//BooksDataset//BX-Book-Ratings.csv',sep=";",error_bad_lines=False,encoding='latin-1')
    
    # Taking the users, who have given more than 200 ratings.
    x = ratings['User-ID'].value_counts()>200
    y = x[x].index
    ratings = ratings[ratings['User-ID'].isin(y)]
    
    ratings_books = ratings.merge(books,on='ISBN')
    
    # grouping the books ratings based on title to filter the books with count
    grp_rating = ratings_books.groupby('title')['Book-Rating'].count().reset_index()
    grp_rating.rename(columns={'Book-Rating':'no-of-rating'},inplace=True)
    final_ratings = ratings_books.merge(grp_rating,on='title')
    final_ratings.rename(columns={'Book-Rating':'BookRating','no-of-rating':'noofrating'},inplace=True)
    
    # Here we are filtering the books with ratings>=50, that we have grouped above based on title with ratings count.
    final_ratings = final_ratings[final_ratings['noofrating']>=50]
    final_ratings.drop_duplicates(['User-ID','title'],inplace=True)
    book_pivot = final_ratings.pivot_table(columns='User-ID',index='title',values='BookRating')
    book_pivot.fillna(0,inplace=True)
    
    import scipy
    from scipy.spatial.distance import correlation
    from scipy.sparse import csr_matrix
    
    book_sparse = csr_matrix(book_pivot)
    
    from sklearn.neighbors import NearestNeighbors

    # Applying KNN algorithm to find the nearest neighbors
    model = NearestNeighbors(algorithm='brute')
    model.fit(book_sparse)
    
    # getting top-5 books with paramter applied as n_neighbors=6
    distances, suggestions = model.kneighbors(book_pivot.iloc[147,:].values.reshape(1,-1),n_neighbors=6)
    np.where(book_pivot.index=='dead run')[0][0] # gives id of movie

    no_before_book = []
    sorted_ratings = final_ratings.values.tolist()
    sorted_ratings.sort(key=lambda x:x[2])
    
    # filtering out top-5 books
    ct=0
    for i in range(len(sorted_ratings)):
        value=sorted_ratings[i][3]
        if value not in no_before_book:
            no_before_book.append(value)
            ct += 1
        if ct==5:
            break
    
    if book_name:
        # Recommending the top-5 books that are nearest neighbors of the given book.
        book_id=np.where(book_pivot.index==book_name)[0][0]
       # print(book_id)
        distances, suggestions = model.kneighbors(book_pivot.iloc[book_id,:].values.reshape(1,-1),n_neighbors=6)
        final_books = []
        for i in range(1,len(suggestions[0])):
            final_books.append(book_pivot.index[suggestions[0][i]])
        return final_books
    
    # if book-name is not given, then we sort out our data based on ratings and return top-5 books
    return no_before_book

if __name__ == "__main__":
    book_recommender()


# In[ ]:




