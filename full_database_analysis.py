import pandas as pd
import matplotlib.pyplot as plt
import ast

def number_albums_artist(database, artist):
    df = pd.read_sql_query("SELECT al.album_id FROM albums_data al JOIN artist_data ar ON al.artist_id = ar.id WHERE ar.name = ? AND al.album_type == 'album'", database, params=(artist,))
    return df['album_id'].nunique()

def number_singles_artist(database, artist):
    df = pd.read_sql_query("SELECT al.album_id FROM albums_data al JOIN artist_data ar ON al.artist_id = ar.id WHERE ar.name = ? AND al.album_type == 'single'", database, params=(artist,))
    return df['album_id'].nunique()

def number_tracks_artist(database, artist):
    df = pd.read_sql_query("SELECT al.track_id FROM albums_data al JOIN artist_data ar ON al.artist_id = ar.id WHERE ar.name = ?", database, params=(artist,))
    return df['track_id'].nunique()

def artist_features(database, artist, feature, stat):
    df = pd.read_sql_query(f"SELECT al.track_id, al.album_id, f.{feature} FROM albums_data al JOIN features_data f ON al.track_id = f.id JOIN artist_data ar ON al.artist_id = ar.id WHERE ar.name = ?", database, params=[artist])

    if stat == 'mean':
        return df[feature].mean()
    elif stat == 'max':
        return df[feature].max()
    elif stat == 'min':
        return df[feature].min()
    elif stat == 'std':
        return df[feature].std()

def album_features(database, album_id, feature, visualization=False):
    allowed_features = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms']

    if feature in allowed_features:
        df = pd.read_sql_query(f"""SELECT a.track_number, f.{feature} FROM albums_data a JOIN features_data f ON a.track_id = f.id WHERE a.album_id = ?""", database, params=[album_id])
        df = df.sort_values(by=['track_number'])

        print('Statistics for feature: %s' % feature)
        print('Mean: %f' % df[feature].mean())
        print('Standard deviation: %f' % df[feature].std())
        print('Minimum: %f' % df[feature].min())
        print('Maximum: %f' % df[feature].max())

        if visualization:
            plt.plot(df['track_number'], df[feature])

            plt.xticks(range(1, len(df) + 1, 1))
            plt.xlabel('Track number')
            plt.ylabel('%s values' % feature)
            plt.title('Results of %s' % feature)

            plt.show()

def album_features_summary(database, album_name, artist_name):
    df = pd.read_sql_query("""
        SELECT f.* 
        FROM features_data f 
        JOIN albums_data a ON f.id = a.track_id 
        WHERE LOWER(a.album_name) = LOWER(?) 
        AND LOWER(a.artist_0) = LOWER(?)""", database, params=[album_name, artist_name]
    )

    if df.empty:
        return "No data found for this album and artist."

    summary = f"""
    Here follows a summary of feature scores on the album: {album_name} by {artist_name}
    Danceability score: average: {df['danceability'].mean():.3f}, minimum: {df['danceability'].min():.3f}, maximum: {df['danceability'].max():.3f}, standard deviation: {df['danceability'].std():.3f}
    Energy score: average: {df['energy'].mean():.3f}, minimum: {df['energy'].min():.3f}, maximum: {df['energy'].max():.3f}, standard deviation: {df['energy'].std():.3f}
    Key score: average: {df['key'].mean():.3f}, minimum: {df['key'].min():.3f}, maximum: {df['key'].max():.3f}, standard deviation: {df['key'].std():.3f}
    Loudness score: average: {df['loudness'].mean():.3f}, minimum: {df['loudness'].min():.3f}, maximum: {df['loudness'].max():.3f}, standard deviation: {df['loudness'].std():.3f}
    Mode score: average: {df['mode'].mean():.3f}, minimum: {df['mode'].min():.3f}, maximum: {df['mode'].max():.3f}, standard deviation: {df['mode'].std():.3f}
    Speechiness score: average: {df['speechiness'].mean():.3f}, minimum: {df['speechiness'].min():.3f}, maximum: {df['speechiness'].max():.3f}, standard deviation: {df['speechiness'].std():.3f}
    Acousticness score: average: {df['acousticness'].mean():.3f}, minimum: {df['acousticness'].min():.3f}, maximum: {df['acousticness'].max():.3f}, standard deviation: {df['acousticness'].std():.3f}
    Instrumentalness score: average: {df['instrumentalness'].mean():.3f}, minimum: {df['instrumentalness'].min():.3f}, maximum: {df['instrumentalness'].max():.3f}, standard deviation: {df['instrumentalness'].std():.3f}
    Liveness score: average: {df['liveness'].mean():.3f}, minimum: {df['liveness'].min():.3f}, maximum: {df['liveness'].max():.3f}, standard deviation: {df['liveness'].std():.3f}
    Valence score: average: {df['valence'].mean():.3f}, minimum: {df['valence'].min():.3f}, maximum: {df['valence'].max():.3f}, standard deviation: {df['valence'].std():.3f}
    Tempo score: average: {df['tempo'].mean():.3f}, minimum: {df['tempo'].min():.3f}, maximum: {df['tempo'].max():.3f}, standard deviation: {df['tempo'].std():.3f}
    Duration (per ms): average: {df['duration_ms'].mean():.3f}, minimum: {df['duration_ms'].min():.3f}, maximum: {df['duration_ms'].max():.3f}, standard deviation: {df['duration_ms'].std():.3f}
    """
    return summary

def top10_percent_tracks(database, feature):
    allowed_features = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms']

    if feature in allowed_features:
        df = pd.read_sql_query(f"""SELECT f.{feature}, ar.name FROM albums_data al JOIN features_data f ON al.track_id = f.id JOIN artist_data ar ON al.artist_id = ar.id""", database)

        ten_percent = int(len(df) * 0.1 + 0.5)
        top_df = df.nlargest(ten_percent, feature)[['name', feature]]
        sorted_top_df = top_df['name'].value_counts()

        print("The top 10 reoccuring artists for feature: %s" % feature)
        print(sorted_top_df.nlargest(10))

def relationship_artist_album_popularity(database):
    df = pd.read_sql_query("""
        SELECT al.album_popularity, ar.artist_popularity 
        FROM albums_data al 
        JOIN artist_data ar ON al.artist_id = ar.id""", database
    )

    correlation = df["album_popularity"].corr(df["artist_popularity"])
    print('The correlation between album popularity and artist popularity is: %f' % correlation)

def explicit_tracks_popularity(database):
    df = pd.read_sql_query("SELECT explicit, track_popularity FROM tracks_data", database)

    explicit_tracks = df[df['explicit'] == 'true']
    non_explicit_tracks = df[df['explicit'] == 'false']

    average_explicit = int(explicit_tracks['track_popularity'].mean() + 0.5)
    average_non_explicit = int(non_explicit_tracks['track_popularity'].mean() + 0.5)

    print('The average popularity for explicit tracks is: %d and the average for non explicit tracks is: %d' % (average_explicit, average_non_explicit))

def top10_artist_highest_proportion_explicit(database):
    df = pd.read_sql_query("SELECT ar.name FROM tracks_data t JOIN albums_data al ON t.id = al.track_id JOIN artist_data ar ON al.artist_id = ar.id WHERE t.explicit = 'true'", database)
    sorted_df = df['name'].value_counts()

    print("The top 10 artists with the most explicit tracks is:")
    print(sorted_df.nlargest(10))

def popularity_collaboration(database):
    df = pd.read_sql_query("SELECT collaboration, track_popularity FROM tracks_data", database)

    collaborations = df[df['collaboration'] == 'true']
    non_collaborations = df[df['collaboration'] == 'false']

    mean_popularity_collabs = int(collaborations['track_popularity'].mean() + 0.5)
    mean_popularity_non_collabs = int(non_collaborations['track_popularity'].mean() + 0.5)

    print("Average popularity of collaborations is: %d \nAverage popularity of non-collaborations is: %d." % (mean_popularity_collabs, mean_popularity_non_collabs))
    if mean_popularity_collabs > mean_popularity_non_collabs:
        print("Collaborations appear to be more popular on average.")
    else:
        print("Collaborations do not appear to be more popular.")

def average_artists_per_collab(database):
    artist_cols = [f'artist_{i}' for i in range(12)]
    df = pd.read_sql_query(f"""SELECT track_name, {", ".join("al."+c for c in artist_cols)} FROM albums_data al JOIN tracks_data t ON al.track_id = t.id WHERE t.collaboration = 'true'""", database)

    df["artist_list"] = df[artist_cols].apply(lambda row: [a for a in row.dropna() if a != ''], axis=1)
    df["number_of_artists"] = df["artist_list"].apply(len)

    avg_artists_per_collab = int(df["number_of_artists"].mean() + 0.5)

    print("The average number of artists per collaboration is: %d" % avg_artists_per_collab)

def duration_explicit(database):
    df = pd.read_sql_query("""SELECT duration_sec, explicit FROM albums_data al JOIN tracks_data t ON al.track_id = t.id""", database)

    explicit_tracks = df[df['explicit'] == 'true']
    non_explicit_tracks = df[df['explicit'] == 'false']

    avg_explicit = explicit_tracks['duration_sec'].mean() / 60
    avg_non_explicit = non_explicit_tracks['duration_sec'].mean() / 60

    print("Average duration of explicit tracks in minutes is: %.2f \nAverage duration of non-explicit tracks in minutes is: %.2f" % (avg_explicit, avg_non_explicit))
    if avg_explicit > avg_non_explicit:
        print("It appears that explicit tracks are longer in duration on average.")
    else:
        print("It appears that non-explicit tracks are longer in duration on average.")

def longest_or_shortest_explicit_or_non_explicit_tracks(database, longest=True, explicit=True):
    df = pd.read_sql_query("""SELECT track_name, duration_sec, explicit FROM albums_data al JOIN tracks_data t ON al.track_id = t.id""", database)

    if explicit:
        df = df[df['explicit'] == 'true']
    else:
        df = df[df['explicit'] == 'false']

    result = df.sort_values("duration_sec", ascending=not longest).head(10)

    print(result[["track_name", "duration_sec"]])

def most_popular_tracks(database, artist):
    df = pd.read_sql_query("SELECT t.track_popularity, al.track_name FROM albums_data al JOIN artist_data ar ON al.artist_id = ar.id JOIN tracks_data t ON al.track_id = t.id WHERE ar.name = ? ", database, params=(artist,))

    if df.empty:
        return pd.DataFrame(columns=['track_name', 'track_popularity'])

    return df.nlargest(5, 'track_popularity')

def most_popular_albums(database, artist):
    df = pd.read_sql_query("SELECT al.album_name, al.album_popularity FROM albums_data al JOIN artist_data ar on al.artist_id = ar.id WHERE ar.name = ? AND al.album_type == 'album'", database, params=(artist,))

    if df.empty:
        return pd.DataFrame(columns=['album_name', 'album_popularity'])

    df = df.drop_duplicates(subset='album_name')
    return df.nlargest(5, 'album_popularity')

def top10_genres_feature_ranking(database, feature, eras, very_low=True):
    eras_str = ','.join([f"'{era}'" for era in eras])

    df = pd.read_sql_query(f"""
        SELECT f.{feature}, ar.artist_genres 
        FROM features_data f 
        JOIN albums_data al ON al.track_id = f.id 
        JOIN artist_data ar ON ar.id = al.artist_id 
        WHERE al.era IN ({eras_str})""", database
    )

    df['feature_ranking'] = pd.cut(df[feature], 5, labels=['very low', 'low', 'medium', 'high', 'very high'])
    df['artist_genres'] = df['artist_genres'].apply(ast.literal_eval)
    df = df.explode(column=['artist_genres']).dropna(subset=['artist_genres'])

    if very_low:
        low_df = df[df['feature_ranking'] == 'very low']

        genres_list = low_df['artist_genres'].value_counts().keys().tolist()
        count_list = low_df['artist_genres'].value_counts().tolist()

        new_low_df = pd.DataFrame(columns=['genres', 'count'], data={'genres': genres_list, 'count': count_list})
        return new_low_df.head(10)
    else:
        high_df = df[df['feature_ranking'] == 'very high']

        genres_list = high_df['artist_genres'].value_counts().keys().tolist()
        count_list = high_df['artist_genres'].value_counts().tolist()

        new_high_df = pd.DataFrame(columns=['genres', 'count'], data={'genres': genres_list, 'count': count_list})
        return new_high_df.head(10)

def top10_artists_feature_ranking(database, feature, eras, very_low=True):
    eras_str = ','.join([f"'{era}'" for era in eras])

    artist_cols = [f'artist_{i}' for i in range(7)]
    df = pd.read_sql_query(f"""
        SELECT f.{feature}, {", ".join("al."+c for c in artist_cols)} 
        FROM features_data f 
        JOIN albums_data al ON al.track_id = f.id 
        JOIN artist_data ar ON ar.id = al.artist_id 
        WHERE al.era IN ({eras_str})""", database
    )

    df["artist_list"] = df[artist_cols].apply(lambda row: [a for a in row.dropna() if a != ''], axis=1)
    df['feature_ranking'] = pd.cut(df[feature], 5, labels=['very low', 'low', 'medium', 'high', 'very high'])

    df = df.explode(column=['artist_list']).dropna(subset=['artist_list'])

    if very_low:
        low_df = df[df['feature_ranking'] == 'very low']

        artist_list = low_df['artist_list'].value_counts().keys().tolist()
        count_list = low_df['artist_list'].value_counts().tolist()

        new_low_df = pd.DataFrame(columns=['artist', 'count'], data={'artist': artist_list, 'count': count_list})
        return new_low_df.head(10)
    else:
        high_df = df[df['feature_ranking'] == 'very high']

        artist_list = high_df['artist_list'].value_counts().keys().tolist()
        count_list = high_df['artist_list'].value_counts().tolist()

        new_high_df = pd.DataFrame(columns=['artist', 'count'], data={'artist': artist_list, 'count': count_list})
        return new_high_df.head(10)

# The following functions were used to attempt to identify dupliates in artist_data
def look_up_certain_artist(database, artist_id):
    pd.set_option('display.max_columns', None)
    # df = pd.read_sql_query("SELECT al.track_name, al.artist_0, al.label, t.explicit FROM albums_data al JOIN tracks_data t ON t.id = al.track_id WHERE artist_id = ?", database, params=(artist_id,))
    df = pd.read_sql_query("SELECT track_name , artist_0, label FROM albums_data WHERE artist_id = ?", database, params=(artist_id,))
    print(df)

def artists_with_same_name(database, name):
    pd.set_option('display.max_columns', None)
    df = pd.read_sql_query("SELECT id, name, artist_popularity, artist_genres, followers FROM artist_data", database)
    print(df[df['name'] == name])

def check_exact_duplicates(database):
    pd.set_option('display.max_columns', None)
    df = pd.read_sql_query("""SELECT name, artist_popularity,
    artist_genres, followers, genre_0, genre_1, genre_2, genre_3, genre_4,
    genre_5, genre_6 FROM artist_data""", database)
    print(df[df.duplicated() == True])


def check_duplicates(database):
    pd.set_option('display.max_columns', None)
    df = pd.read_sql_query("""SELECT name, artist_genres FROM artist_data""", database)
    print(df[df.duplicated(keep=False) == True].sort_values('name'))

def duplicate_artists(database):
    pd.set_option('display.max_columns', None)
    # pd.set_option('display.max_rows', None)
    df = pd.read_sql_query("SELECT * FROM artist_data", database)
    duplicates = df[df['name'].duplicated(keep=False)]
    print(duplicates[['name', 'id', 'artist_genres', 'artist_popularity']].sort_values('name'))

def capitalization(database):
    pd.set_option('display.max_columns', None)
    df = pd.read_sql_query("SELECT * FROM artist_data", database)

def duplicates(database):
    pd.set_option('display.max_columns', None)
    df = pd.read_sql_query("SELECT id, name, artist_popularity, artist_genres, followers FROM artist_data", database)
    duplicates = df[df['name'].duplicated(keep=False)]
    print(duplicates)

def clean_artist_data(database):
    df = pd.read_sql_query("SELECT id, name FROM artist_data", database)

    # print(df['name'].duplicated() == True)
    print(df[df['name'].duplicated() == True].value_counts())