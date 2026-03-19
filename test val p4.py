import sqlite3
import valerie_part4 as vp4
import pandas as pd

database = sqlite3.connect('spotify_database.db')
# df = pd.read_sql_query("SELECT * FROM artist_data", database)
# df['name'] = df['name'].str.title()
# df.to_sql('artist_data', database, if_exists='replace', index=False)

# vp4.w(database, 'Turbo')
# print("\nArtist 1:")
# vp4.v(database, '0TYydMAKPBYjZB0jgGCN7h')
# print("\nArtist 2:")
# vp4.v(database, '002HSjuWsGMinkXTa7JcRp')
# # print("\nArtist 3:")
# # vp4.v(database, '7n2Ycct7Beij7Dj7meI4X0')
#
# # print("")
#
# # print('\nDuplicate artists:')
# # # vp4.clean_artist_data(database)
# #
# # # vp4.duplicates(database)
# # vp4.duplicate_artists(database)
#
# # vp4.all_genres(database)
#
# # vp4.check_exact_duplicates(database)
# vp4.check_duplicates(database)

# vp4.most_frequent_genre_combinations(database)

vp4.top10_genres_feature_ranking(database, "danceability", very_low=True)
vp4.top10_genres_feature_ranking(database, "danceability", very_low=False)