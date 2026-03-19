import ast
import pandas as pd

# def v(database, artist_id): # look up certain artist
#     pd.set_option('display.max_columns', None)
#     # df = pd.read_sql_query("SELECT al.track_name, al.artist_0, al.label, t.explicit FROM albums_data al JOIN tracks_data t ON t.id = al.track_id WHERE artist_id = ?", database, params=(artist_id,))
#     df = pd.read_sql_query("SELECT track_name , artist_0, label FROM albums_data WHERE artist_id = ?", database, params=(artist_id,))
#     print(df)
#
# def w(database, name): # show all artist with same name
#     pd.set_option('display.max_columns', None)
#     df = pd.read_sql_query("SELECT id, name, artist_popularity, artist_genres, followers FROM artist_data", database)
#     print(df[df['name'] == name])
#
# def clean_artist_data(database):
#     df = pd.read_sql_query("SELECT id, name FROM artist_data", database)
#
#     # print(df['name'].duplicated() == True)
#     print(df[df['name'].duplicated() == True].value_counts())
#
# def duplicates(database):
#     pd.set_option('display.max_columns', None)
#     df = pd.read_sql_query("SELECT id, name, artist_popularity, artist_genres, followers FROM artist_data", database)
#     duplicates = df[df['name'].duplicated(keep=False)]
#     print(duplicates)
#
# def duplicate_artists(database):
#     pd.set_option('display.max_columns', None)
#     # pd.set_option('display.max_rows', None)
#     df = pd.read_sql_query("SELECT * FROM artist_data", database)
#     duplicates = df[df['name'].duplicated(keep=False)]
#     print(duplicates[['name', 'id', 'artist_genres', 'artist_popularity']].sort_values('name'))
# def capitalization(database):
#     pd.set_option('display.max_columns', None)
#     df = pd.read_sql_query("SELECT * FROM artist_data", database)
#
# def all_genres(database):
#     df = pd.read_sql_query("SELECT artist_genres FROM artist_data", database)
#     df['artist_genres'] = df['artist_genres'].apply(ast.literal_eval)
#     df = df['artist_genres'].explode().dropna()
#
#     print(sorted(df.unique()))
#
# def check_exact_duplicates(database):
#     pd.set_option('display.max_columns', None)
#     df = pd.read_sql_query("""SELECT name, artist_popularity,
#     artist_genres, followers, genre_0, genre_1, genre_2, genre_3, genre_4,
#     genre_5, genre_6 FROM artist_data""", database)
#     print(df[df.duplicated() == True])
#
# def check_duplicates(database):
#     pd.set_option('display.max_columns', None)
#     df = pd.read_sql_query("""SELECT name, artist_genres FROM artist_data""", database)
#     print(df[df.duplicated(keep=False) == True].sort_values('name'))

def most_frequent_genre_combinations(database):
    df = pd.read_sql_query("SELECT artist_genres FROM artist_data", database)
    df['artist_genres'] = df['artist_genres'].apply(ast.literal_eval)

    for i in range(len(df)):
        df.loc[i, 'number_of_genres'] = len(df['artist_genres'][i])

    df['number_of_genres'] = df['number_of_genres'].astype('Int64')
    new_df = df[df['number_of_genres'] != 1]
    new_df = new_df[new_df['number_of_genres'] != 0]

    print(new_df['artist_genres'].value_counts().head(10))
# bar plot? tabel?

def top10_genres_feature_ranking(database, feature, very_low=True):
    pd.set_option('display.max_columns', None)
    df = pd.read_sql_query(f"""SELECT f.{feature}, ar.artist_genres FROM features_data f JOIN albums_data al ON al.track_id = f.id JOIN artist_data ar ON ar.id = al.artist_id""", database)
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

def top10_artists_feature_ranking(database, feature, very_low=True):
    pd.set_option('display.max_columns', None)
    artist_cols = [f'artist_{i}' for i in range(7)]
    df = pd.read_sql_query(f"""SELECT f.{feature}, {", ".join("al."+c for c in artist_cols)} FROM features_data f JOIN albums_data al ON al.track_id = f.id JOIN artist_data ar ON ar.id = al.artist_id""", database)
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