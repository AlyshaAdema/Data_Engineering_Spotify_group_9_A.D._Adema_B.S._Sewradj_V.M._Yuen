import ast
import pandas as pd
import statsmodels.api as sm
import numpy as np

# importing own files
import artist_data_visualization as advis

def get_artist_data(file_name):
    artist_data = pd.read_csv(file_name)
    artist_data['id'] = artist_data['id'].astype(str)
    artist_data['name'] = artist_data['name'].astype(str)
    artist_data['artist_popularity'] = artist_data['artist_popularity'].astype(int)
    artist_data['artist_genres'] = artist_data['artist_genres'].apply(ast.literal_eval)
    artist_data['followers'] = artist_data['followers'].astype(int)
    artist_data['genre_0'] = artist_data['genre_0'].astype(str)
    artist_data['genre_1'] = artist_data['genre_1'].astype(str)
    artist_data['genre_2'] = artist_data['genre_2'].astype(str)
    artist_data['genre_3'] = artist_data['genre_3'].astype(str)
    artist_data['genre_4'] = artist_data['genre_4'].astype(str)
    artist_data['genre_5'] = artist_data['genre_5'].astype(str)
    artist_data['genre_6'] = artist_data['genre_6'].astype(str)
    artist_data['number_of_genres'] = artist_data['artist_genres'].apply(len)
    return artist_data

def unique_artists(data_frame):
    return data_frame['name'].nunique()

def correlation_followers_popularity(data_frame):
    return data_frame['followers'].corr(data_frame['artist_popularity'])

def linear_regression(data_frame):
    # linear regression model still needs to be implemented
    return

def top10_artists_genre(data_frame, genre):
    genres_data_frame = data_frame[data_frame['artist_genres'].apply(lambda x: genre in x)]
    return genres_data_frame.nlargest(10, 'followers')['name']

artist_data = get_artist_data('artist_data.csv')
# print(unique_artists(artist_data))
# advis.top10_followers(artist_data)
# advis.top10_populartity(artist_data)

