import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

database = sqlite3.connect('spotify_database.db')

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
    df["year_bin"] = pd.cut(
        df["year"],
        bins=np.arange(df["year"].min(), df["year"].max() + 20, 20)
    )
    year_counts = df["year_bin"].value_counts().sort_index()

    fig, ax = plt.subplots(1, 2, figsize=(12,5))

    ax[0].scatter(df["year"], df["album_popularity"])
    ax[0].set_xlabel("Release Year")
    ax[0].set_ylabel("Album Popularity")
    ax[0].set_title("Release Year vs Album Popularity")

    ax[1].bar(year_counts.index.astype(str), year_counts.values)
    ax[1].set_xlabel("Release Year (20-year bins)")
    ax[1].set_ylabel("Number of Albums")
    ax[1].set_title("Albums per Time Period")

    ax[0].tick_params(axis="x", rotation=40)
    ax[1].tick_params(axis="x", rotation=40)

    plt.tight_layout()
    plt.show()

def release_year_vs_duration(database):
    df = pd.read_sql_query("SELECT album_id, release_date, SUM(duration_sec) AS album_duration FROM albums_data GROUP BY album_id", database)
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df["year"] = df["release_date"].dt.year
    df["duration_hours"] = df["album_duration"] / 3600
    duration_bins = pd.cut(
        df["duration_hours"],
        bins=np.arange(0, df["duration_hours"].max() + 0.5, 0.5)
    )
    duration_counts = duration_bins.value_counts().sort_index()

    fig, ax = plt.subplots(1, 2, figsize=(12,5))

    ax[0].scatter(df["year"], df["duration_hours"])
    ax[0].set_xlabel("Release Year")
    ax[0].set_ylabel("Album Duration (hours)")
    ax[0].set_title("Release Year vs Album Duration")

    ax[1].bar(duration_counts.index.astype(str), duration_counts.values)
    ax[1].set_xlabel("Album Duration (hours)")
    ax[1].set_ylabel("Number of Albums")
    ax[1].set_title("Album Duration Distribution")
    ax[1].tick_params(axis="x", rotation=40)

    plt.tight_layout()
    plt.show()

# def total_tracks_vs_album_duration(database):
#     df = pd.read_sql_query("SELECT album_id, MAX(total_tracks) AS total_tracks, SUM(duration_sec) AS album_duration_sec FROM albums_data GROUP BY album_id", database)
#     df["duration_hours"] = df["album_duration_sec"] / 3600
#
#     fig, ax = plt.subplots(1, 2, figsize=(12,5))
#
#     ax[0].scatter(df["total_tracks"], df["duration_hours"])
#     ax[0].set_xlabel("Total tracks")
#     ax[0].set_ylabel("Album duration (hours)")
#     ax[0].set_title("Total Tracks vs Album Duration")
#
#     mean_by_tracks = df.groupby("total_tracks")["duration_hours"].mean().sort_index()
#     ax[1].bar(mean_by_tracks.index.astype(int), mean_by_tracks.values)
#     ax[1].set_xlabel("Total tracks")
#     ax[1].set_ylabel("Avg album duration (hours)")
#     ax[1].set_title("Average Duration by Total Tracks")
#
#     plt.tight_layout()
#     plt.show()
# deze is misschien beetje bs want het is logisch dat meer liedjes = langere album

