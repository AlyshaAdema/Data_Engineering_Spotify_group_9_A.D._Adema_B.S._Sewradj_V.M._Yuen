import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

def album_duration_vs_popularity(database):
    df = pd.read_sql_query("SELECT album_id, SUM(duration_sec) AS album_duration_sec, MAX(album_popularity) AS album_popularity FROM albums_data GROUP BY album_id",database)
    df["duration_hours"] = df["album_duration_sec"] / 3600
    df["duration_bin"] = pd.cut(
        df["duration_hours"],
        bins=np.arange(0, df["duration_hours"].max() + 0.5, 0.5))
    bin_counts = df["duration_bin"].value_counts().sort_index()

    fig, ax = plt.subplots(1, 2, figsize=(12,5))

    ax[0].scatter(df["duration_hours"], df["album_popularity"])
    ax[0].set_xlabel("Album duration (hours)")
    ax[0].set_ylabel("Album popularity")
    ax[0].set_title("Album Duration vs Popularity")

    ax[1].bar(bin_counts.index.astype(str), bin_counts.values)
    ax[1].set_xlabel("Album duration (hours)")
    ax[1].set_ylabel("Number of albums")
    ax[1].set_title("Album Duration Distribution")
    ax[1].tick_params(axis="x", rotation=40)
    plt.tight_layout()
    plt.show()

def release_year_vs_popularity(database):
    df = pd.read_sql_query("SELECT release_date, album_popularity FROM albums_data", database)
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df["year"] = df["release_date"].dt.year

    result = df.groupby("year")["album_popularity"].mean()
    print(result)

    result.plot()
    plt.xlabel("Release Year")
    plt.ylabel("Average Album Popularity")
    plt.title("Average Album Popularity by Release Year")
    plt.show()

def release_year_vs_duration(database):
    df = pd.read_sql_query("SELECT album_id, release_date, SUM(duration_sec) AS album_duration FROM albums_data GROUP BY album_id", database)
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df["year"] = df["release_date"].dt.year
    df = df.dropna(subset=["year"])
    df["album_duration_min"] = df["album_duration"] / 60

    average_duration = df.groupby("year")["album_duration_min"].mean().sort_index()
    average_duration.plot()
    plt.xlabel("Release Year")
    plt.ylabel("Average Album Duration (minutes)")
    plt.title("Average Album Duration by Release Year")
    plt.show()

def total_tracks_vs_popularity(database):
    df = pd.read_sql_query("SELECT album_id, MAX(total_tracks) AS total_tracks, MAX(album_popularity) AS album_popularity FROM albums_data GROUP BY album_id", database)
    plt.scatter(df["total_tracks"],df["album_popularity"], alpha=0.5)
    plt.xlabel("Total Tracks in Album")
    plt.ylabel("Album Popularity")
    plt.title("Total Tracks vs Album Popularity")
    plt.show()

    average_popularity = df.groupby("total_tracks")["album_popularity"].mean().sort_index()
    average_popularity.plot()
    plt.xlabel("Total Tracks in Album")
    plt.ylabel("Album Popularity")
    plt.title("Total Tracks vs Album Popularity")
    plt.show()

def album_type_vs_popularity(database):
    df = pd.read_sql_query("SELECT album_id, album_type, MAX(album_popularity) AS album_popularity FROM albums_data GROUP BY album_id", database)
    average_popularity = df.groupby("album_type")["album_popularity"].mean()
    average_popularity.plot(kind="bar")
    plt.xlabel("Album Type")
    plt.ylabel("Average Album Popularity")
    plt.title("Average Album Popularity by Album Type")
    plt.show()

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
    labels = ["Solo albums", "Collaboration albums"]
    values = [len(solo), len(collabs)]

    plt.bar(labels, values)
    plt.ylabel("Number of Albums")
    plt.title("Solo vs Collaboration Albums")
    plt.show()

def top_10_labels_singles_vs_albums(database):
    df = pd.read_sql_query("""
        SELECT 
            album_id,
            MAX(label) AS label,
            MAX(total_tracks) AS total_tracks
        FROM albums_data
        GROUP BY album_id
    """, database)

    df = df[df["label"].notna() & (df["label"].str.strip() != "")]

    singles = df[df["total_tracks"] == 1]
    albums = df[df["total_tracks"] > 1]

    top_singles = singles["label"].value_counts().head(10)
    top_albums = albums["label"].value_counts().head(10)

    print("Top 10 labels for singles:")
    print(top_singles)

    print("\nTop 10 labels for albums:")
    print(top_albums)

    fig, ax = plt.subplots(1, 2, figsize=(14, 5))

    top_singles.plot(kind="bar", ax=ax[0])
    ax[0].set_title("Top 10 Labels for Singles")
    ax[0].set_xlabel("Label")
    ax[0].set_ylabel("Count")
    ax[0].tick_params(axis="x", rotation=45)

    top_albums.plot(kind="bar", ax=ax[1])
    ax[1].set_title("Top 10 Labels for Albums")
    ax[1].set_xlabel("Label")
    ax[1].set_ylabel("Count")
    ax[1].tick_params(axis="x", rotation=45)

    plt.tight_layout()
    plt.show()

def songs_per_era(database):
    df = pd.read_sql_query("SELECT era, COUNT(*) as song_count FROM albums_data GROUP BY era ORDER BY era", database)
    df = df.set_index("era")

    df.plot(kind="bar")
    plt.xlabel("Era")
    plt.ylabel("Number of Songs")
    plt.title("Songs per Era")
    plt.show()

def top_albums_per_era(database):
    df = pd.read_sql_query("SELECT DISTINCT era, album_name, album_popularity FROM albums_data WHERE album_popularity IS NOT NULL", database)
    df_avg = df.groupby("era")["album_popularity"].mean()
    df_avg.plot(kind="bar", title="Average Album Popularity per Era")
    plt.xlabel("Era")
    plt.ylabel("Average Popularity")
    plt.show()

def music_trends_over_time(database):
    df = pd.read_sql_query("SELECT a.release_date, f.danceability, f.energy, f.valence, f.tempo FROM albums_data a JOIN features_data f ON a.track_id = f.id", database)
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    df['year'] = df['release_date'].dt.year
    trend = df.groupby('year')[['danceability', 'energy', 'valence', 'tempo']].mean()
    trend[['danceability', 'energy', 'valence']].plot(figsize=(10, 6))
    plt.title("Danceability, Energy, and Valence Over Time")
    plt.xlabel("Year")
    plt.ylabel("Average Value")
    trend[['tempo']].plot(figsize=(10, 6))
    plt.title("Tempo over Time")
    plt.xlabel("Year")
    plt.ylabel("Average Tempo")
    plt.show()

def album_tracks(database, album_name, artist_name):
    df = pd.read_sql_query("SELECT al.track_number, al.track_name, al.duration_sec FROM albums_data al JOIN artist_data ar ON al.artist_id = ar.id WHERE LOWER(al.album_name) = LOWER(?) AND LOWER(ar.name) = LOWER(?) GROUP BY al.track_number, al.track_name ORDER BY al.track_number", database,params=(album_name, artist_name))
    df = df.drop_duplicates(subset=["track_number", "track_name"])
    return df

def plot_album_tracks(df, album_name):
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('#121212')
    ax.set_facecolor('#121212')
    ax.tick_params(colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.title.set_color('white')
    start_color = np.array(mcolors.to_rgb('#1DB954'))
    end_color = np.array(mcolors.to_rgb('#1DE97C'))
    n = len(df)
    if n == 1:
        colors = [mcolors.to_hex(start_color)]
    else:
        colors = [
            mcolors.to_hex(start_color + (end_color - start_color) * (i / (n - 1)))
            for i in range(n)
        ]
    x = np.arange(len(df))
    ax.bar(x, df["duration_sec"] / 60, color=colors)
    ax.set_title(f"Tracks on {album_name}", fontsize=16, weight='bold')
    ax.set_xlabel("Track")
    ax.set_ylabel("Duration (min)")
    short_names = [
        name[:15] + "…" if len(name) > 15 else name
        for name in df["track_name"]
    ]
    ax.set_xticks(x)
    ax.set_xticklabels(short_names, rotation=45, ha="right")
    plt.tight_layout()
    return fig

def album_track_popularity(database, album_name, artist_name):
    df = pd.read_sql_query("SELECT al.track_number, al.track_name, t.track_popularity FROM albums_data al JOIN artist_data ar ON al.artist_id = ar.id JOIN tracks_data t ON al.track_id = t.id WHERE LOWER(al.album_name) = LOWER(?) AND LOWER(ar.name) = LOWER(?) GROUP BY al.track_number, al.track_name ORDER BY al.track_number", database, params=(album_name, artist_name))
    df = df.drop_duplicates(subset=["track_number", "track_name"])
    return df

def plot_album_track_popularity(df, album_name):
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('#121212')
    ax.set_facecolor('#121212')
    ax.tick_params(colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.title.set_color('white')
    start_color = np.array(mcolors.to_rgb('#1DB954'))
    end_color = np.array(mcolors.to_rgb('#1DE97C'))
    n = len(df)
    if n == 1:
        colors = [mcolors.to_hex(start_color)]
    else:
        colors = [
            mcolors.to_hex(start_color + (end_color - start_color) * (i / (n - 1)))
            for i in range(n)
        ]
    x = np.arange(len(df))
    ax.bar(x, df["track_popularity"], color=colors)
    ax.set_title(f"Track Popularity on {album_name}", fontsize=16, weight='bold')
    ax.set_xlabel("Track")
    ax.set_ylabel("Popularity")
    short_names = [
        name[:15] + "…" if len(name) > 15 else name
        for name in df["track_name"]
    ]
    ax.set_xticks(x)
    ax.set_xticklabels(short_names, rotation=45, ha="right")
    plt.tight_layout()
    return fig

