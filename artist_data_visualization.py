import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def top10_followers(data_frame):
    top10_followers = data_frame.nlargest(10, 'followers')
    plt.bar(top10_followers['name'], top10_followers['followers'])
    plt.xticks(rotation=90)
    plt.xlabel('Names top 10 artists')
    plt.ylabel('Followers')
    plt.title('Amount of followers top 10 artists')
    plt.tight_layout()
    plt.show()

def top10_popularity(data_frame):
    top10_popularity = data_frame.nlargest(10, 'artist_popularity')
    plt.bar(top10_popularity['name'], top10_popularity['artist_popularity'])
    plt.xticks(rotation=90)
    plt.xlabel('Names top 10 artists')
    plt.ylabel('Popularity')
    plt.title('Popularity top 10 artists')
    plt.tight_layout()
    plt.show()

def linear_regression(data_frame):
    followers, popularity = np.polyfit(data_frame['followers'], data_frame['artist_popularity'], 1)
    plt.scatter(data_frame['followers'], data_frame['artist_popularity'], color='purple')
    plt.plot(data_frame['followers'], followers * data_frame['followers'] + popularity)
    plt.text(1, 90, 'y = ' + '{:.3f}'.format(popularity) + ' + {:.3f}'.format(followers) + 'x', size=12)
    plt.xlabel('Amount of followers')
    plt.ylabel('Artist popularity')
    plt.show()

def genres_histogram(data_frame):
    plt.hist(data_frame['number_of_genres'], bins=range(0, 10, 1))
    plt.xlabel('Number of Genres')
    plt.ylabel('Frequency')
    plt.title('Distribution genres')
    plt.show()
