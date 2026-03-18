import sqlite3
import valerie_part4 as vp4

database = sqlite3.connect('spotify_database.db')

vp4.v(database)
vp4.w(database)
vp4.clean_artist_data(database)

# vp4.most_frequent_genre_combinations(database)

# vp4.ranking_features(database, "danceability")