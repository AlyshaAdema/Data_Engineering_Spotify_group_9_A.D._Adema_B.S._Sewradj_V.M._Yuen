import ast
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import artist_data_analysis as arda

def top10_followers(database, eras):
    if not eras:
        fig, ax = plt.subplots()
        ax.set_title("No eras selected")
        return fig
    eras_str = ','.join([f"'{era}'" for era in eras])
    df = pd.read_sql_query(f"SELECT ar.name, MAX(ar.followers) as followers FROM artist_data ar JOIN albums_data al ON ar.id = al.artist_id WHERE era IN ({eras_str}) GROUP BY ar.name", database)
    top10_followers = df.nlargest(10, 'followers')
    fig, ax = plt.subplots()
    ax.bar(top10_followers['name'], top10_followers['followers'])
    ax.set_xticklabels(top10_followers['name'], rotation=90)
    ax.set_xlabel('Names top 10 artists')
    ax.set_ylabel('Followers')
    ax.set_title('Amount of followers top 10 artists')
    plt.tight_layout()
    return fig

def top10_popularity(database):
    df = pd.read_sql_query("SELECT name, artist_popularity FROM artist_data", database)
    top10_popularity = df.nlargest(10, 'artist_popularity')
    plt.bar(top10_popularity['name'], top10_popularity['artist_popularity'])
    plt.xticks(rotation=90)
    plt.xlabel('Names top 10 artists')
    plt.ylabel('Popularity')
    plt.title('Popularity top 10 artists')
    plt.tight_layout()
    plt.show()

def linear_regression(database, eras):
    if not eras:
        fig, ax = plt.subplots()
        ax.set_title("No eras selected")
        return fig
    eras_str = ','.join([f"'{era}'" for era in eras])
    df = pd.read_sql_query(f"SELECT MAX(ar.followers) as followers, MAX(ar.artist_popularity) as artist_popularity FROM artist_data ar JOIN albums_data al ON ar.id = al.artist_id WHERE era IN ({eras_str}) GROUP BY ar.name", database)
    slope, intercept = np.polyfit(np.log1p(df['followers']), df['artist_popularity'], 1)
    fig, ax = plt.subplots()
    ax.scatter(df['followers'], df['artist_popularity'])
    sorted_followers = np.sort(df['followers'])
    ax.plot(sorted_followers, intercept + slope * np.log1p(sorted_followers), color='red')
    ax.set_xlabel('Amount of followers')
    ax.set_ylabel('Artist popularity')
    ax.set_title('Scatter plot followers vs popularity')
    return fig

def genres_histogram(database):
    df = pd.read_sql_query("SELECT artist_genres FROM artist_data", database)
    df['artist_genres'] = df['artist_genres'].apply(ast.literal_eval)
    df['number_of_genres'] = df['artist_genres'].apply(len)
    plt.hist(df['number_of_genres'], bins=range(0, 10, 1))
    plt.xlabel('Number of Genres')
    plt.ylabel('Frequency')
    plt.title('Distribution genres')
    plt.show()

def top10_genres(database, eras):
    if not eras:
        fig, ax = plt.subplots()
        ax.set_title("No eras selected")
        return fig
    top10_genres = arda.top10_genres_by_most_followers(database, eras)
    fig, ax = plt.subplots()
    ax.bar(top10_genres['genre'], top10_genres['followers'])
    ax.set_xticklabels(top10_genres['genre'], rotation=90)
    ax.set_xlabel('Genres')
    ax.set_ylabel('Followers')
    ax.set_title('Amount of followers top 10 genres')
    plt.tight_layout()
    return fig