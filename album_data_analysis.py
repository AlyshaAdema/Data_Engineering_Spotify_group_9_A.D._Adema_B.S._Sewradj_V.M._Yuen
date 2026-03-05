import ast
import pandas as pd
import statsmodels.api as sm
import numpy as np
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
    correlation = df["year"].corr(df["album_popularity"])
    print("The correlation between release year and album popularity is: %f, as the release year increases, album popularity tends to decrease a little bit." % correlation)

def release_year_vs_duration(database):
    df = pd.read_sql_query("SELECT album_id, release_date, SUM(duration_sec) AS album_duration FROM albums_data GROUP BY album_id", database)
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df["year"] = df["release_date"].dt.year
    correlation = df["year"].corr(df["album_duration"])
    print("The correlation between release year and album duration is %f, as the release year increases (albums become newer), album duration tends to decrease slightly"  % correlation)

# def total_tracks_vs_duration(database):
#     df = pd.read_sql_query("SELECT album_id, MAX(total_tracks) AS total_tracks, SUM(duration_sec) AS album_duration_sec FROM albums_data GROUP BY album_id", database)
#     df["duration_hours"] = df["album_duration_sec"] / 3600
#     correlation = df["total_tracks"].corr(df["duration_hours"])
#     print("The correlation between the total tracks and album duration is %f, so albums with more tracks tend to be longer."  % correlation)
# deze is misschien beetje bs want het is logisch dat meer liedjes = langere album
