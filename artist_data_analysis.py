import pandas as pd
import matplotlib.pyplot as plt

def get_data(file_name):
    artist_data = pd.read_csv('artist_data.csv')


def visualization_top10_followers(data_frame):
    top10_followers = data_frame.nlargest(10, 'followers')
    plt.bar(top10_followers['artist'], top10_followers['followers'])
    plt.xticks(rotation=90)
    plt.xlabel('Names top 10 artists')
    plt.ylabel('Followers')
    plt.title('Amount of followers top 10 artists')
    plt.tight_layout()
    plt.show()

artist_data = pd.read_csv('artist_data.csv')
unique_artists = artist_data[artist_data['name']].nunique()
top10_popularity = artist_data.nlargest(10, 'artist_popularity')
visualization_top10_followers(artist_data)
