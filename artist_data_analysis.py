import ast
import pandas as pd
import statsmodels.api as sm
import numpy as np

def unique_artists(database, eras):
    eras_str = ','.join([f"'{era}'" for era in eras])
    df = pd.read_sql_query(f"SELECT ar.id, al.era FROM artist_data ar JOIN albums_data al ON ar.id = al.artist_id WHERE al.era IN ({eras_str})", database)
    return df['id'].nunique()

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
    return df.nlargest(10, 'residual')['name']

def top10_followers_artists_genre(database, genre):
    df = pd.read_sql_query("SELECT name, followers, artist_genres FROM artist_data", database)
    df['artist_genres'] = df['artist_genres'].apply(ast.literal_eval)
    return df[df['artist_genres'].apply(lambda x: genre in x)].nlargest(10, 'followers')['name']

def top10_popularity_artists_genre(database, genre):
    df = pd.read_sql_query("SELECT name, artist_popularity, artist_genres FROM artist_data", database)
    df['artist_genres'] = df['artist_genres'].apply(ast.literal_eval)
    return df[df['artist_genres'].apply(lambda x: genre in x)].nlargest(10, 'artist_popularity')['name']

def artists_per_genre(database, genre):
    df = pd.read_sql_query("SELECT artist_genres FROM artist_data", database)
    df['artist_genres'] = df['artist_genres'].apply(ast.literal_eval)
    return len(df[df['artist_genres'].apply(lambda x: genre in x)])

def total_followers_per_genre(database, genre):
    df = pd.read_sql_query("SELECT followers, artist_genres FROM artist_data", database)
    df['artist_genres'] = df['artist_genres'].apply(ast.literal_eval)
    return df[df['artist_genres'].apply(lambda x: genre in x)].sum()

def average_followers_per_genre(database, genre):
    df = pd.read_sql_query("SELECT followers, artist_genres FROM artist_data", database)
    df['artist_genres'] = df['artist_genres'].apply(ast.literal_eval)
    return int(df[df['artist_genres'].apply(lambda x: genre in x)].mean() + 0.5)

def average_popularity_per_genre(database, genre):
    df = pd.read_sql_query("SELECT artist_popularity, artist_genres FROM artist_data", database)
    df['artist_genres'] = df['artist_genres'].apply(ast.literal_eval)
    return int(df[df['artist_genres'].apply(lambda x: genre in x)].mean() + 0.5)

def artists_per_popularity_rating(database, popularity):
    df = pd.read_sql_query("SELECT artist_popularity FROM arist_data", database)
    return len(df[df['artist_popularity'] == popularity])

def look_up_artist(database, artist):
    df = pd.read_sql_query("SELECT name, artist_popularity, followers, artist_genres FROM artist_data", database)
    df['artist_genres'] = df['artist_genres'].apply(ast.literal_eval)
    artist_df = df[df['name'] == artist]
    print('name: %s' % artist)
    print('popularity: %d' % artist_df['artist_popularity'].mean())
    print('followers: {:,.0f}'.format(artist_df['followers'].mean()))
    print('genres: %s' % ', '.join(artist_df.loc[artist_df['name'] == artist, 'artist_genres'].iloc[0]))

def df_followers_all_genres(database, eras):
    if not eras:
        return pd.DataFrame(columns=['genre', 'followers'])
    eras_str = ','.join([f"'{era}'" for era in eras])
    df = pd.read_sql_query(f"SELECT ar.artist_genres, ar.followers FROM artist_data ar JOIN albums_data al ON ar.id = al.artist_id WHERE era IN ({eras_str})", database)
    df['artist_genres'] = df['artist_genres'].apply(ast.literal_eval)
    clean_exploded_df = df.explode('artist_genres').dropna()
    genres_df = pd.DataFrame(columns=['genre', 'followers'])

    for genre in clean_exploded_df['artist_genres'].unique():
        total_followers = clean_exploded_df[
            clean_exploded_df['artist_genres'] == genre
            ]['followers'].sum()
        genres_df.loc[len(genres_df)] = [genre, total_followers]

    return genres_df

def top10_genres_by_most_or_least_followers(database, eras, most_followers=True):
    return df_followers_all_genres(database, eras).sort_values('followers', ascending=not most_followers).head(10)

def number_followers_artist(database, artist):
    df = pd.read_sql_query("SELECT followers FROM artist_data WHERE name = ?", database, params=(artist,))
    return df['followers'].mean()

def popularity_artist(database, artist):
    df = pd.read_sql_query("SELECT artist_popularity FROM artist_data WHERE name = ?", database, params=(artist,))
    return df['artist_popularity'].mean()


def genres_artist(database, artist):
    df = pd.read_sql_query("SELECT artist_genres FROM artist_data WHERE name = ?", database, params=(artist,))
    if df.empty:
        return []
    df['artist_genres'] = df['artist_genres'].apply(ast.literal_eval)
    return df['artist_genres'].iloc[0]
