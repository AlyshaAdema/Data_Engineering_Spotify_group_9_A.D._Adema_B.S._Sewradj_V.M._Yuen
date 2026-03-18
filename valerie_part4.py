import ast
import pandas as pd

def v(database): # look up certain artist
    pd.set_option('display.max_columns', None)
    df = pd.read_sql_query("SELECT * FROM albums_data WHERE artist_id == '002HSjuWsGMinkXTa7JcRp'", database)
    print(df.head(10))

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

def ranking_features(database, feature):
    pd.set_option('display.max_columns', None)
    df = pd.read_sql_query(f"""SELECT f.{feature}, ar.artist_genres FROM features_data f JOIN albums_data al ON al.track_id = f.id JOIN artist_data ar ON ar.id = al.artist_id""", database)
    df['feature_ranking'] = pd.cut(df[feature], 5, labels=['very low', 'low', 'medium', 'high', 'very high'])

    df['artist_genres'] = df['artist_genres'].apply(ast.literal_eval)
    df = df.explode(column=['artist_genres']).dropna(subset=['artist_genres'])

    low_df = df[df['feature_ranking'] == 'very low']
    print(f"The top 10 most frequently occurring genres among tracks that score very low for {feature} are: ")
    print(low_df['artist_genres'].value_counts().nlargest(10))

    high_df = df[df['feature_ranking'] == 'very high']
    print(f"The top 10 most frequently occurring genres among tracks that score very high for {feature} are: ")
    print(high_df['artist_genres'].value_counts().nlargest(10))

