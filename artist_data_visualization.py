import ast
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
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
    ax.set_xlabel('Names artists')
    ax.set_ylabel('Followers')
    ax.set_title('Amount of Followers Top 10 Artists')
    plt.tight_layout()
    return fig

def top10_popularity(database, eras):
    if not eras:
        fig, ax = plt.subplots()
        ax.set_title("No eras selected")
        return fig
    eras_str = ','.join([f"'{era}'" for era in eras])
    df = pd.read_sql_query(f"SELECT ar.name, MAX(ar.artist_popularity) as artist_popularity FROM artist_data ar JOIN albums_data al ON ar.id = al.artist_id WHERE era IN ({eras_str}) GROUP BY ar.name", database)
    top10_popularity = df.nlargest(10, 'artist_popularity')
    fig, ax = plt.subplots()
    ax.bar(top10_popularity['name'], top10_popularity['artist_popularity'])
    ax.set_xticklabels(top10_popularity['name'], rotation=90)
    ax.set_xlabel('Names artists')
    ax.set_ylabel('Artist Popularity')
    ax.set_title('Popularity Top 10 Artists')
    plt.tight_layout()
    return fig

def top10_followers_genre(database, genre):
    df = arda.top10_followers_artists_genre(database, genre)
    fig, ax = plt.subplots()
    ax.bar(df['name'], df['followers'])
    ax.set_xticklabels(df['name'], rotation=90)
    ax.set_xlabel('Names top artists')
    ax.set_ylabel('Followers')
    ax.set_title(f'Amount of Followers Top Artists {genre}')
    plt.tight_layout()
    return fig

def top10_popularity_genre(database, genre):
    df = arda.top10_popularity_artists_genre(database, genre)
    fig, ax = plt.subplots()
    ax.bar(df['name'], df['artist_popularity'])
    ax.set_xticklabels(df['name'], rotation=90)
    ax.set_xlabel('Names top artists')
    ax.set_ylabel('Popularity')
    ax.set_title(f'Popularity Top Artists {genre}')
    plt.tight_layout()
    return fig

def followers_distribution_genres(database, genre):
    df = pd.read_sql_query("SELECT followers, artist_genres FROM artist_data", database)
    df['artist_genres'] = df['artist_genres'].apply(ast.literal_eval)
    df = df[df['artist_genres'].apply(lambda x: genre in x)]
    fig, ax = plt.subplots()
    sns.histplot(data=np.log1p(df['followers']), kde=True, ax=ax)
    ax.set_title(f"Followers Distribution for {genre}")
    ax.set_xlabel("Log(Followers + 1)")
    ax.set_ylabel("Number of Artists")
    plt.tight_layout()
    return fig

def popularity_distribution_genres(database, genre):
    df = pd.read_sql_query("SELECT artist_popularity, artist_genres FROM artist_data", database)
    df['artist_genres'] = df['artist_genres'].apply(ast.literal_eval)
    df = df[df['artist_genres'].apply(lambda x: genre in x)]
    fig, ax = plt.subplots()
    sns.histplot(data=df['artist_popularity'], kde=True, ax=ax)
    ax.set_title(f"Popularity Distribution for {genre}")
    ax.set_xlabel("Popularity")
    ax.set_ylabel("Number of Artists")
    plt.tight_layout()
    return fig

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
    ax.set_title('Scatterplot Followers vs Popularity')
    return fig

def genres_histogram(database):
    df = pd.read_sql_query("SELECT artist_genres FROM artist_data", database)
    df['artist_genres'] = df['artist_genres'].apply(ast.literal_eval)
    df['number_of_genres'] = df['artist_genres'].apply(len)
    plt.hist(df['number_of_genres'], bins=range(0, 10, 1))
    plt.xlabel('Number of Genres')
    plt.ylabel('Frequency')
    plt.title('Distribution Genres')
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
    ax.set_title('Amount of Followers Top 10 Genres')
    plt.tight_layout()
    return fig

def bar_plot_top_genre_combination(database, genre):
    df = arda.most_frequent_combination_genre(database, genre)
    fig, ax = plt.subplots()
    ax.bar(df['genre'], df['count'])
    ax.set_xticklabels(df['genre'], rotation=90)
    ax.set_xlabel('Genre')
    ax.set_ylabel('Appears together')
    ax.set_title(f'Genres Most Often Paired with {genre}')
    plt.tight_layout()
    return fig

