import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def popular_books(ratings_path, books_path,num=50,image_show=False):
    ratings = pd.read_csv(ratings_path)
    books = pd.read_csv(books_path)

    books_data = pd.merge(ratings, books, on='ISBN')

    if(image_show == True):
        books_data = books_data[['User-ID', 'Book-Title', 'Book-Rating','Book-Author','Year-Of-Publication','Publisher','Image-URL-S','Image-URL-M','Image-URL-L']]
    else:
        books_data = books_data[['User-ID', 'Book-Title', 'Book-Rating','Book-Author','Year-Of-Publication','Publisher']]

    books_data.dropna(inplace=True)
    books_data.drop(books_data[books_data['Book-Rating'] == 0].index, inplace=True)
    books_data['Book-Title'] = books_data['Book-Title'].apply(lambda x: re.sub("[\W_]+", " ", x).strip())

    if(image_show == True):
        book_popularity = books_data.groupby(['Book-Title', 'Book-Author','Year-Of-Publication','Publisher','Image-URL-S','Image-URL-M','Image-URL-L'])['Book-Rating'].count().reset_index(name='Popularity')
    else:
        book_popularity = books_data.groupby(['Book-Title', 'Book-Author','Year-Of-Publication','Publisher'])['Book-Rating'].count().reset_index(name='Popularity')
    
    # book_popularity = books_data.groupby('Book-Title')['Book-Rating'].count().reset_index(name='Popularity')
    book_popularity = book_popularity.sort_values('Popularity', ascending=False)
    book_popularity.index = range(1, len(book_popularity) + 1)
    return book_popularity.head(num)

def search_books(title_query, ratings_path,books_path, num_results=10):
    books = pd.read_csv(books_path)
    ratings = pd.read_csv(ratings_path)

    data = pd.merge(books, ratings, on='ISBN')

    vectorizer = CountVectorizer()
    title_matrix = vectorizer.fit_transform(data['Book-Title'])

    query_matrix = vectorizer.transform([title_query])
    similarity_scores = cosine_similarity(query_matrix, title_matrix)
    indices = np.argsort(-similarity_scores)

    results = []
    for i in range(num_results):
        index = indices[0][i]
        result = {
            'title': data.loc[index, 'Book-Title'],
            'author': data.loc[index, 'Book-Author'],
            'year': data.loc[index, 'Year-Of-Publication'],
            'publisher': data.loc[index, 'Publisher'],
            'image_url': data.loc[index, 'Image-URL-M'],
            'rating': data.loc[index, 'Book-Rating'],
            'user_id': data.loc[index, 'User-ID']
        }
        results.append(result)

    return results
