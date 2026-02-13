import pandas as pd
import matplotlib.pyplot as plt

def top10_followers(data_frame):
    top10_followers = data_frame.nlargest(10, 'followers')
    plt.bar(top10_followers['name'], top10_followers['followers'])
    plt.xticks(rotation=90)
    plt.xlabel('Names top 10 artists')
    plt.ylabel('Followers')
    plt.title('Amount of followers top 10 artists')
    plt.tight_layout()
    plt.show()

def top10_populartity(data_frame):
    top10_popularity = data_frame.nlargest(10, 'artist_popularity')
    plt.bar(top10_popularity['name'], top10_popularity['artist_popularity'])
    plt.xticks(rotation=90)
    plt.xlabel('Names top 10 artists')
    plt.ylabel('Popularity')
    plt.title('Popularity top 10 artists')
    plt.tight_layout()
    plt.show()

def genres_histogram(data_frame):
    return

