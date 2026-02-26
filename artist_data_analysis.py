import ast
import pandas as pd
import statsmodels.api as sm
import numpy as np

import artist_data_visualization
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

def correlation_followers_genres(data_frame):
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
# advis.top10_popularity(artist_data)
# advis.linear_regression(artist_data)
# advis.genres_histogram(artist_data)

# hoeveel artiesten heeft een bepaalde genre
def artists_per_genre(data_frame, genre):
    genres_data_frame = data_frame[data_frame['artist_genres'].apply(lambda x: genre in x)]
    return len(genres_data_frame)
# hoeveel volgers heeft een bepaalde genre
def total_followers_per_genre(data_frame, genre):
    genres_data_frame = data_frame[data_frame['artist_genres'].apply(lambda x: genre in x)]
    return genres_data_frame['followers'].sum()
# gemiddelde volgers van een genre
def average_followers_per_genre(data_frame, genre):
    genres_data_frame = data_frame[data_frame['artist_genres'].apply(lambda x: genre in x)]
    return int(genres_data_frame['followers'].mean() + 0.5)
# gemiddelde popularity van een genre
def average_popularity_per_genre(data_frame, genre):
    genres_data_frame = data_frame[data_frame['artist_genres'].apply(lambda x: genre in x)]
    return int(genres_data_frame['artist_popularity'].mean() + 0.5)
# hoeveel artists hebben bepaalde popularity rating
def artists_per_popularity_rating(data_frame, popularity):
    popularity_data_frame = data_frame[data_frame['artist_popularity'] == popularity]
    return len(popularity_data_frame)

# miss iets met bepaalde artists (dus hoeveel followers die heeft)
def look_up_artist(data_frame, artist):
    artist_data_frame = data_frame[data_frame['name'] == artist]
    print('name: %s' % artist)
    print('popularity: %d' % artist_data_frame['artist_popularity'].mean())
    print('followers: {:,.0f}'.format(artist_data_frame['followers'].mean()))
    print('genres: %s' % ', '.join(artist_data_frame.loc[artist_data_frame['name'] == artist, 'artist_genres'].iloc[0]))

# meest voorkomende genres + visualization
def data_frame_followers_all_genres(data_frame):
    clean_exploded_data_frame = data_frame.explode('artist_genres').dropna()
    genre_list = []
    genres_data_frame = pd.DataFrame(columns=['genre', 'followers'])

    for genre in clean_exploded_data_frame['artist_genres']:
        if genre not in genre_list:
            genre_list.append(genre)

    for genre in genre_list:
        total_followers = total_followers_per_genre(data_frame, genre)
        genres_data_frame.loc[len(genres_data_frame)] = [genre, total_followers]

    return genres_data_frame

def top10_genres_by_most_followers(data_frame):
    return data_frame_followers_all_genres(data_frame).nlargest(10, 'followers')

# minst voorkomende genres
def top10_genres_by_least_followers(data_frame):
    return data_frame_followers_all_genres(data_frame).nsmallest(10, 'followers')

# van bepaalde creativiteitspunten kunnen we nog visualizations maken
#     eentje die we kunnen doen is correlation tussen aantal artiesten en aantal volgers