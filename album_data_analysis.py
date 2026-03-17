import pandas as pd
import sqlite3

database = sqlite3.connect('spotify_database.db')

def album_duration_vs_popularity(database):
    df = pd.read_sql_query("SELECT album_id, SUM(duration_sec) AS album_duration_sec, MAX(album_popularity) AS album_popularity FROM albums_data GROUP BY album_id", database)
    correlation = df["album_duration_sec"].corr(df["album_popularity"])
    print('The correlation between album duration and popularity is: %f, as the album duration increases, album popularity tends to increase.' % correlation)

def release_year_vs_popularity(database):
    df = pd.read_sql_query("SELECT release_date, album_popularity FROM albums_data", database)
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df["year"] = df["release_date"].dt.year
    result = df.groupby("year")["album_popularity"].mean()
    print(result.reset_index(name="Average Album Popularity"))

def release_year_vs_duration(database):
    df = pd.read_sql_query("SELECT album_id, release_date, SUM(duration_sec) AS album_duration FROM albums_data GROUP BY album_id", database)
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df["year"] = df["release_date"].dt.year
    df = df.dropna(subset=["year"])
    df["album_duration_min"] = df["album_duration"] / 60
    average_duration = df.groupby("year")["album_duration_min"].mean().sort_index()
    print("Average album duration per year (minutes):")
    print(average_duration.reset_index(name="Average Duration (min)"))

def total_tracks_vs_popularity(database):
    df = pd.read_sql_query("SELECT album_id, MAX(total_tracks) AS total_tracks, MAX(album_popularity) AS album_popularity FROM albums_data GROUP BY album_id", database)
    average_popularity = df.groupby("total_tracks")["album_popularity"].mean().sort_index()
    print("Average album popularity per year (minutes):")
    print(average_popularity.reset_index(name="Average Popularity (min)"))

def album_type_vs_popularity(database):
    df = pd.read_sql_query("SELECT album_id, album_type, MAX(album_popularity) AS album_popularity FROM albums_data GROUP BY album_id", database)
    average_popularity = df.groupby("album_type")["album_popularity"].mean()
    print("Average album popularity by album type:")
    print(average_popularity)

def album_collabs(database):
    df = pd.read_sql_query("""
    SELECT 
        album_id,
        (   CASE WHEN artist_0 IS NOT NULL AND TRIM(artist_0) != '' THEN 1 ELSE 0 END +
            CASE WHEN artist_1 IS NOT NULL AND TRIM(artist_1) != '' THEN 1 ELSE 0 END +
            CASE WHEN artist_2 IS NOT NULL AND TRIM(artist_2) != '' THEN 1 ELSE 0 END +
            CASE WHEN artist_3 IS NOT NULL AND TRIM(artist_3) != '' THEN 1 ELSE 0 END +
            CASE WHEN artist_4 IS NOT NULL AND TRIM(artist_4) != '' THEN 1 ELSE 0 END +
            CASE WHEN artist_5 IS NOT NULL AND TRIM(artist_5) != '' THEN 1 ELSE 0 END +
            CASE WHEN artist_6 IS NOT NULL AND TRIM(artist_6) != '' THEN 1 ELSE 0 END +
            CASE WHEN artist_7 IS NOT NULL AND TRIM(artist_7) != '' THEN 1 ELSE 0 END +
            CASE WHEN artist_8 IS NOT NULL AND TRIM(artist_8) != '' THEN 1 ELSE 0 END +
            CASE WHEN artist_9 IS NOT NULL AND TRIM(artist_9) != '' THEN 1 ELSE 0 END +
            CASE WHEN artist_10 IS NOT NULL AND TRIM(artist_10) != '' THEN 1 ELSE 0 END +
            CASE WHEN artist_11 IS NOT NULL AND TRIM(artist_11) != '' THEN 1 ELSE 0 END
        ) AS artist_count
    FROM albums_data
    GROUP BY album_id
    """, database)

    solo = df[df["artist_count"] == 1]
    collabs = df[df["artist_count"] > 1]

    print("Total albums:", len(df))
    print("Solo albums:", len(solo))
    print("Collaboration albums:", len(collabs))

    average_artists = collabs["artist_count"].mean()
    print("Average artist count in collaboration albums:", average_artists)

def top_10_labels(database):
    df = pd.read_sql_query("SELECT album_id, label, album_popularity FROM albums_data", database)
    result = (df.groupby("label").agg(label_count=("label", "size"),avg_popularity=("album_popularity", "mean")).sort_values("label_count", ascending=False).head(10))
    print("Top 10 labels and average popularity:")
    print(result)

def top_10_labels_singles_vs_albums(database):
    df = pd.read_sql_query("SELECT album_id, MAX(label) AS label MAX(total_tracks) AS total_track FROM albums_data GROUP BY album_id", database)
    df = df[df["label"].notna() & (df["label"].str.strip() != "")]

    singles = df[df["total_tracks"] == 1]
    albums = df[df["total_tracks"] > 1]

    top_singles = singles["label"].value_counts().head(10)
    top_albums = albums["label"].value_counts().head(10)

    print("Top 10 labels for singles:")
    print(top_singles)

    print("\nTop 10 labels for albums:")
    print(top_albums)

def unique_albums(database):
    df = pd.read_sql_query("SELECT COUNT(DISTINCT album_name) AS unique_albums FROM albums_data", database)
    print("Number of unique album names:", df["unique_albums"][0])

def top_albums_per_era(database):
    df = pd.read_sql_query("SELECT DISTINCT era, album_name, album_popularity FROM albums_data WHERE album_popularity IS NOT NULL", database)
    top5 = df.groupby("era").head(5).reset_index(drop=True)
    for era, group in top5.groupby("era"):
        print(f"\nTop 5 albums of the {era}:")
        print(group[["album_name", "album_popularity"]])

#part 4
def music_trends_over_time(database):
    df = pd.read_sql_query("SELECT a.release_date, f.danceability, f.energy, f.valence, f.tempo FROM albums_data a JOIN features_data f ON a.track_id = f.id", database)
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    df['year'] = df['release_date'].dt.year

    trend = df.groupby('year')[['danceability', 'energy', 'valence', 'tempo']].mean()
    print(trend)

def outliers(database):
    df = pd.read_sql("SELECT * FROM features_data", database)
    features = [
        'danceability', 'energy', 'loudness', 'speechiness',
        'acousticness', 'instrumentalness', 'liveness',
        'valence', 'tempo', 'duration_ms'
    ]
    outlier_counts = {}
    for col in features:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        outliers = df[(df[col] < lower) | (df[col] > upper)]
        outlier_counts[col] = len(outliers)
    print(outlier_counts)

