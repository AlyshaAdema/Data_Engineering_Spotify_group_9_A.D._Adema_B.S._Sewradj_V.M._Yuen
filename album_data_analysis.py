import pandas as pd

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

# def total_tracks_vs_duration(database):
#     df = pd.read_sql_query("SELECT album_id, MAX(total_tracks) AS total_tracks, SUM(duration_sec) AS album_duration_sec FROM albums_data GROUP BY album_id", database)
#     df["duration_hours"] = df["album_duration_sec"] / 3600
#     correlation = df["total_tracks"].corr(df["duration_hours"])
#     print("The correlation between the total tracks and album duration is %f, so albums with more tracks tend to be longer."  % correlation)
# deze is misschien beetje bs want het is logisch dat meer liedjes = langere album

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

def unique_album_names(database):
    df = pd.read_sql_query("""
                           SELECT COUNT(DISTINCT album_name) AS unique_albums
                           FROM albums_data
                           """, database)

    print("Number of unique album names:", df["unique_albums"][0])