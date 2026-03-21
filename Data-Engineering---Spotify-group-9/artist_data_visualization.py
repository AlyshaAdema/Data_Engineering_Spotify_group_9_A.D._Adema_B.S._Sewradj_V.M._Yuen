import ast
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def top10_followers(database):
    df = pd.read_sql_query("SELECT name, followers FROM artist_data", database)
    top10_followers = df.nlargest(10, 'followers')
    plt.bar(top10_followers['name'], top10_followers['followers'])
    plt.xticks(rotation=90)
    plt.xlabel('Names top 10 artists')
    plt.ylabel('Followers')
    plt.title('Amount of followers top 10 artists')
    plt.tight_layout()
    plt.show()

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

def linear_regression(database):
    df = pd.read_sql_query("SELECT followers, artist_popularity FROM artist_data", database)
    slope, intercept = np.polyfit(np.log1p(df['followers']), df['artist_popularity'], 1)
    plt.scatter(df['followers'], df['artist_popularity'], color='purple')
    sorted_followers = np.sort(df['followers'])
    plt.plot(sorted_followers, intercept + slope * np.log1p(sorted_followers))
    plt.xlabel('Amount of followers')
    plt.ylabel('Artist popularity')
    plt.show()

def genres_histogram(database):
    df = pd.read_sql_query("SELECT artist_genres FROM artist_data", database)
    df['artist_genres'] = df['artist_genres'].apply(ast.literal_eval)
    df['number_of_genres'] = df['artist_genres'].apply(len)
    plt.hist(df['number_of_genres'], bins=range(0, 10, 1))
    plt.xlabel('Number of Genres')
    plt.ylabel('Frequency')
    plt.title('Distribution genres')
    plt.show()
