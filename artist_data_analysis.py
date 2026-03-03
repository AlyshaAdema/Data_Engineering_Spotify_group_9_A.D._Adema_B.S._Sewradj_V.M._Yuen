import ast
import pandas as pd
import statsmodels.api as sm
import numpy as np

def unique_artists(database):
    df = pd.read_sql_query("SELECT name FROM artist_data", database)
    return df['name'].nunique()

def correlation_followers_popularity(database):
    df = pd.read_sql_query("SELECT followers, artist_popularity FROM artist_data", database)
    return df['followers'].corr(df['artist_popularity'])

def correlation_followers_genres(database):
    df = pd.read_sql_query("SELECT artist_genres, followers FROM artist_data", database)
    df['artist_genres'] = df['artist_genres'].apply(ast.literal_eval)
    df['number_of_genres'] = df['artist_genres'].apply(len)
    return df['number_of_genres'].corr(df['followers'])

def correlation_popularity_genres(database):
    df = pd.read_sql_query("SELECT artist_genres, artist_popularity FROM artist_data", database)
    df['artist_genres'] = df['artist_genres'].apply(ast.literal_eval)
    df['number_of_genres'] = df['artist_genres'].apply(len)
    return df['number_of_genres'].corr(df['artist_popularity'])

def linear_regression_set_up(database):
    df = pd.read_sql_query("SELECT artist_popularity, followers FROM artist_data", database)
    popularity = df['artist_popularity']
    log_followers = np.log1p(df['followers'])
    followers = sm.add_constant(log_followers)
    return sm.OLS(popularity, followers).fit()

def find_legacy_artists(database):
    model = linear_regression_set_up(database)
    df = pd.read_sql_query("SELECT name, followers, artist_popularity FROM artist_data", database)
    df['predicted_popularity'] = model.predict(sm.add_constant(np.log1p(df['followers'])))
    df['residual'] = df['artist_popularity'] - df['predicted_popularity']
    return df.nsmallest(10, 'residual')['name']

def find_over_performers(database):
    model = linear_regression_set_up(database)
    df = pd.read_sql_query("SELECT name, followers, artist_popularity FROM artist_data", database)
    df['predicted_popularity'] = model.predict(sm.add_constant(np.log1p(df['followers'])))
    df['residual'] = df['artist_popularity'] - df['predicted_popularity']
    return df.largest(10, 'residual')['name']

def top10_followers_artists_genre(database, genre):
    df = pd.read_sql_query("SELECT name, followers, artist_genres FROM artist_data", database)
    df['artist_genres'] = df['artist_genres'].apply(ast.literal_eval)
    return df[df['artist_genres'].apply(lambda x: genre in x)].nlargest(10, 'followers')['name']

def top10_popularity_artists_genre(database, genre):
    df = pd.read_sql_query("SELECT name, artist_popularity, artist_genres FROM artist_data", database)
    df['artist_genres'] = df['artist_genres'].apply(ast.literal_eval)
    return df[df['artist_genres'].apply(lambda x: genre in x)].nlargest(10, 'artist_popularity')['name']

# hoeveel artiesten heeft een bepaalde genre
def artists_per_genre(database, genre):
    df = pd.read_sql_query("SELECT artist_genres FROM artist_data", database)
    df['artist_genres'] = df['artist_genres'].apply(ast.literal_eval)
    return len(df[df['artist_genres'].apply(lambda x: genre in x)])

# hoeveel volgers heeft een bepaalde genre
def total_followers_per_genre(database, genre):
    df = pd.read_sql_query("SELECT followers, artist_genres FROM artist_data", database)
    df['artist_genres'] = df['artist_genres'].apply(ast.literal_eval)
    return df[df['artist_genres'].apply(lambda x: genre in x)].sum()

# gemiddelde volgers van een genre
def average_followers_per_genre(database, genre):
    df = pd.read_sql_query("SELECT followers, artist_genres FROM artist_data", database)
    df['artist_genres'] = df['artist_genres'].apply(ast.literal_eval)
    return int(df[df['artist_genres'].apply(lambda x: genre in x)].mean() + 0.5)

# gemiddelde popularity van een genre
def average_popularity_per_genre(database, genre):
    df = pd.read_sql_query("SELECT artist_popularity, artist_genres FROM artist_data", database)
    df['artist_genres'] = df['artist_genres'].apply(ast.literal_eval)
    return int(df[df['artist_genres'].apply(lambda x: genre in x)].mean() + 0.5)

# hoeveel artists hebben bepaalde popularity rating
def artists_per_popularity_rating(database, popularity):
    df = pd.read_sql_query("SELECT artist_popularity FROM arist_data", database)
    return len(df[df['artist_popularity'] == popularity])

# miss iets met bepaalde artists (dus hoeveel followers die heeft)
def look_up_artist(database, artist):
    df = pd.read_sql_query("SELECT name, artist_popularity, followers, artist_genres FROM artist_data", database)
    df['artist_genres'] = df['artist_genres'].apply(ast.literal_eval)
    artist_data_frame = df[df['name'] == artist]
    print('name: %s' % artist)
    print('popularity: %d' % artist_data_frame['artist_popularity'].mean())
    print('followers: {:,.0f}'.format(artist_data_frame['followers'].mean()))
    print('genres: %s' % ', '.join(artist_data_frame.loc[artist_data_frame['name'] == artist, 'artist_genres'].iloc[0]))

# meest voorkomende genres + visualization
def data_frame_followers_all_genres(database):
    df = pd.read_sql_query("SELECT artist_genres, followers FROM artist_data", database)
    df['artist_genres'] = df['artist_genres'].apply(ast.literal_eval)
    clean_exploded_data_frame = df.explode('artist_genres').dropna()
    genres_data_frame = pd.DataFrame(columns=['genre', 'followers'])

    for genre in clean_exploded_data_frame['artist_genres'].unique():
        total_followers = clean_exploded_data_frame[
            clean_exploded_data_frame['artist_genres'] == genre
            ]['followers'].sum()
        genres_data_frame.loc[len(genres_data_frame)] = [genre, total_followers]

    return genres_data_frame

def top10_genres_by_most_followers(database):
    return data_frame_followers_all_genres(database).nlargest(10, 'followers')

# minst voorkomende genres
def top10_genres_by_least_followers(database):
    return data_frame_followers_all_genres(database).nsmallest(10, 'followers')

# van bepaalde creativiteitspunten kunnen we nog visualizations maken
#     eentje die we kunnen doen is correlation tussen aantal artiesten en aantal volgers