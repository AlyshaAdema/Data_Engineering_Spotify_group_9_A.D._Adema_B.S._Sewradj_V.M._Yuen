import ast
import pandas as pd

def v(database): # look up certain artist
    pd.set_option('display.max_columns', None)
    df = pd.read_sql_query("SELECT track_name FROM albums_data WHERE artist_id == '0TYydMAKPBYjZB0jgGCN7h' AND album_type == 'album'", database)
    print(df)

def w(database): # show all artist with same name
    pd.set_option('display.max_columns', None)
    df = pd.read_sql_query("SELECT * FROM artist_data", database)
    print(df[df['name'] == 'Turbo'])

def clean_artist_data(database):
    df = pd.read_sql_query("SELECT id, name FROM artist_data", database)

    print(df['name'].duplicated() == True)
    print(df[df['name'].duplicated() == True].value_counts())

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



