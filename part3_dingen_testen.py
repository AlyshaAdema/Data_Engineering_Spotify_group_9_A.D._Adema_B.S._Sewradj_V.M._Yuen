import pandas as pd
import matplotlib.pyplot as plt

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

def top10_percent_tracks(database, feature):
    allowed_features = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms']
    if feature in allowed_features:
        df = pd.read_sql_query(f"""SELECT f.{feature}, ar.name FROM albums_data al JOIN features_data f ON al.track_id = f.id JOIN artist_data ar ON al.artist_id = ar.id""", database)
        ten_percent = int(len(df) * 0.1 + 0.5)
        top_df = df.nlargest(ten_percent, feature)[['name', feature]]
        sorted_top_df = top_df['name'].value_counts()
        print("The top 10 reoccuring artists for feature: %s" % feature)
        print(sorted_top_df.nlargest(10))
    # top 10% van tracks per feature. nieuwe df met naam artiest, welke artiest komt meest voor
# betere functie naam

def relationship_artist_album_popularity(database):
    df = pd.read_sql_query("SELECT al.album_popularity, ar.artist_popularity FROM albums_data al JOIN artist_data ar ON al.artist_id = ar.id", database)
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