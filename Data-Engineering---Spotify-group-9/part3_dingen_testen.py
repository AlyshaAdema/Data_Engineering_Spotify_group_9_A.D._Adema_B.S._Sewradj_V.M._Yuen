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

def top10_artists_per_feature(database, feature):
    allowed_features = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms']
    if feature in allowed_features:
        artist_cols = [f'artist_{i}' for i in range(12)]
        df = pd.read_sql_query(f"""SELECT f.{feature}, {", ".join("al."+c for c in artist_cols)} FROM albums_data al JOIN features_data f ON al.track_id = f.id """, database)

        ten_percent = int(len(df) * 0.1 + 0.5)
        ten_percent_df = df.nlargest(ten_percent, feature)[artist_cols]
        ten_percent_df["artists_list"] = ten_percent_df.apply(lambda row: [a for a in row.dropna() if a != ''], axis=1)
        sorted_ten_percent_df = ten_percent_df.explode('artists_list').dropna(subset=['artists_list'])['artists_list'].value_counts()

        print("The top 10 reoccurring artists for feature: %s" % feature)
        print(sorted_ten_percent_df.nlargest(10))

def relation_ship_artist_album_popularity(database):
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

# val: dit berekent nu artist met meeste tracks, maar dat is niet proportion?
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

## creativity:
# gemiddeld aantal artiesten per collab (tracks & albums)
def average_artists_per_collab(database):
    artist_cols = [f'artist_{i}' for i in range(12)]
    df = pd.read_sql_query(f"""SELECT track_name, {", ".join("al."+c for c in artist_cols)} FROM albums_data al JOIN tracks_data t ON al.track_id = t.id WHERE t.collaboration = 'true'""", database)

    df["artist_list"] = df[artist_cols].apply(lambda row: [a for a in row.dropna() if a != ''], axis=1)
    df["number_of_artists"] = df["artist_list"].apply(len)

    avg_artists_per_collab = int(df["number_of_artists"].mean() + 0.5)

    print("The average number of artists per collaboration is: %d" % avg_artists_per_collab)

# are explicit tracks longer in duration? (tracks & albums)
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