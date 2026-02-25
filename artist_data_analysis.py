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

def correlation_follwers_genres(data_frame):
    return data_frame['number_of_genres'].corr(data_frame['followers'])

def correlation_popularity_genres(data_frame):
    return data_frame['number_of_genres'].corr(data_frame['artist_popularity'])

def linear_regression_set_up(data_frame):
    popularity = data_frame['artist_popularity']
    followers = data_frame['followers']
    followers = sm.add_constant(followers)
    return sm.OLS(popularity, followers).fit()

def top10_followers_artists_genre(data_frame, genre):
    genres_data_frame = data_frame[data_frame['artist_genres'].apply(lambda x: genre in x)]
    return genres_data_frame.nlargest(10, 'followers')['name']

def top10_popularity_artists_genre(data_frame, genre):
    genres_data_frame = data_frame[data_frame['artist_genres'].apply(lambda x: genre in x)]
    return genres_data_frame.nlargest(10, 'artist_popularity')['name']

artist_data = get_artist_data('artist_data.csv')
# model = linear_regression_set_up(artist_data)
# print(model.summary())
# print(correlation_popularity_genres(artist_data))
# print(correlation_followers_popularity(artist_data))
# print(unique_artists(artist_data))
# advis.top10_followers(artist_data)
# advis.top10_populartity(artist_data)
# advis.linear_regression(artist_data)
# advis.genres_histogram(artist_data)

# meest voorkomende genres
# minst voorkemende genres
# hoeveel artiesten heeft een bepaalde genre
# hoeveel volgers heeft een bepaalde genre
# hoeveel artists hebben bepaalde popularity rating
# gemiddelde popularity van een genre
# gemiddelde volgers van een genre
# miss iets met bepaalde artists (dus hoeveel followers die heeft)