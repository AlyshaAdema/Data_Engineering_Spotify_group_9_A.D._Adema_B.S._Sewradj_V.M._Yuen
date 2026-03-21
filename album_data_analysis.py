import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

database = sqlite3.connect('spotify_database.db')

def unique_albums(database, eras):
    eras_str = ','.join([f"'{era}'" for era in eras])
    df = pd.read_sql_query(f"SELECT album_id FROM albums_data WHERE era in ({eras_str})", database)
    return df['album_id'].nunique()

def unique_tracks(database, eras):
    eras_str = ','.join([f"'{era}'" for era in eras])
    df = pd.read_sql_query(f"SELECT track_id FROM albums_data WHERE era in ({eras_str})", database)
    return df['track_id'].nunique()

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
        ) AS artist_count
    FROM albums_data
    GROUP BY album_id
    """, database)

    solo = df[df["artist_count"] == 1]
    collabs = df[df["artist_count"] > 1]

    print("Total songs:", len(df))
    print("Solo songs:", len(solo))
    print("Collaboration songs:", len(collabs))

    average_artists = collabs["artist_count"].mean()
    print("Average artist count in collaboration songs:", average_artists)

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

def unique_album_names(database):
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

def artists_for_album(database, album_name):
    result = pd.read_sql_query(  "SELECT DISTINCT ar.name FROM albums_data al JOIN artist_data ar ON al.artist_id = ar.id WHERE LOWER(al.album_name) = LOWER(?) ORDER BY ar.name", database, params=(album_name,))
    return result["name"].tolist()

def album_duration(database, album_name, artist_name):
    df = pd.read_sql_query("SELECT SUM(duration_sec) AS album_duration_sec FROM albums_data al JOIN artist_data ar ON al.artist_id = ar.id WHERE LOWER(al.album_name) = LOWER(?) AND LOWER(ar.name) = LOWER(?)", database, params=(album_name, artist_name))
    if df.empty or df["album_duration_sec"].iloc[0] is None:
        return None
    total_sec = df["album_duration_sec"].iloc[0]
    minutes = int(total_sec // 60)
    seconds = int(total_sec % 60)
    return f"{minutes} min {seconds} sec"

def label(database, album_name, artist_name):
    df = pd.read_sql_query("SELECT label AS label FROM albums_data al JOIN artist_data ar ON al.artist_id = ar.id WHERE LOWER(al.album_name) = LOWER(?) AND LOWER(ar.name) = LOWER(?)", database, params=(album_name, artist_name))
    if df.empty:
        return None
    return df["label"].iloc[0]

def total_tracks(database, album_name, artist_name):
    df = pd.read_sql_query("SELECT total_tracks AS total FROM albums_data al JOIN artist_data ar ON al.artist_id = ar.id WHERE LOWER(al.album_name) = LOWER(?) AND LOWER(ar.name) = LOWER(?)", database, params=(album_name, artist_name))
    if df.empty:
        return None
    return df["total"].iloc[0]

def release_date(database, album_name, artist_name):
    df = pd.read_sql_query("SELECT release_date FROM albums_data al JOIN artist_data ar ON al.artist_id = ar.id WHERE LOWER(al.album_name) = LOWER(?) AND LOWER(ar.name) = LOWER(?)", database, params=(album_name, artist_name))
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    if df.empty:
        return None
    return df["release_date"].dt.date.iloc[0]

def album_feature(database, album_name, artist_name, feature):
    df = pd.read_sql_query(f"SELECT al.track_number, al.track_name, ft.{feature} FROM albums_data al JOIN features_data ft ON al.track_id = ft.id WHERE LOWER(al.album_name) = LOWER(?) AND LOWER(al.artist_0) = LOWER(?) ORDER BY al.track_number", database, params=(album_name, artist_name))
    if df.empty:
        return None
    df = df.drop_duplicates(subset=["track_number"])
    return df

def plot_album_feature(df, album_name, artist_name, feature):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df["track_number"], df[feature], marker='o')
    ax.set_title(f"{feature} across {album_name}")
    ax.set_xlabel("Track number")
    ax.set_ylabel(feature)
    ax.set_xticks(df["track_number"])
    ax.set_xticklabels(df["track_number"])
    plt.tight_layout()
    return fig

def album_featured_artist_counts(database, album_name, artist_name):
    df = pd.read_sql_query("SELECT artist_1, artist_2, artist_3, artist_4, artist_5, artist_6 FROM albums_data WHERE LOWER(album_name) = LOWER(?) AND LOWER(artist_0) = LOWER(?)", database, params=(album_name, artist_name))
    if df.empty:
        return pd.DataFrame(columns=["artist", "count"])
    feature_cols = ["artist_1", "artist_2", "artist_3", "artist_4", "artist_5", "artist_6"]
    all_artists = pd.concat([df[col] for col in feature_cols])
    all_artists = all_artists.dropna()
    all_artists = all_artists[all_artists.str.strip() != ""]
    if all_artists.empty:
        return pd.DataFrame(columns=["artist", "count"])
    result = all_artists.value_counts().reset_index()
    result.columns = ["artist", "count"]
    return result

def plot_featured_artist_counts(df, album_name, artist_name):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(df["artist"], df["count"])
    ax.set_title(f"Featured Artists on {album_name}")
    ax.set_xlabel("Number of Tracks")
    ax.set_ylabel("Artist")
    ax.set_xticks(np.arange(0, df["count"].max() + 1, 1))
    plt.tight_layout()
    return fig

def album_explicit_pie(database, album_name, artist_name):
    df = pd.read_sql_query("SELECT a.track_id, a.track_name, t.explicit FROM albums_data a JOIN tracks_data t ON a.track_id = t.id WHERE LOWER(a.album_name) = LOWER(?) AND LOWER(a.artist_0) = LOWER(?)",database, params=[album_name, artist_name])
    if df.empty:
        return None
    explicit_tracks = len(df[df["explicit"] == "true"])
    non_explicit_tracks = len(df[df["explicit"] == "false"])
    fig, ax = plt.subplots(figsize=(4, 2))
    ax.pie([explicit_tracks, non_explicit_tracks], autopct="%1.1f%%", pctdistance=0.7, startangle=90)
    centre_circle = plt.Circle((0, 0), 0.5, fc="w")
    fig.gca().add_artist(centre_circle)
    ax.set_title(f"Explicit vs Non-explicit on {album_name}")
    ax.legend(
        ["Explicit", "Non-explicit"],
        loc="upper left",
        bbox_to_anchor=(1.05, 1)
    )
    return fig