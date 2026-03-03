import sqlite3
import pandas as pd

# importing own files
import part3_dingen_testen as p3dt
import artist_data_analysis as ada

database = sqlite3.connect('spotify_database.db')
# even lover uittesten van taylor swift. conclusie: NIET CONSISTENT !!!!!!!!!!!! TAYLOR WAT DOE JE?
# p3dt.album_features(database, '1NAmidJlEaVgA3MpcPFYGq', 'valence', visualization=True)

# danceability, various artists staat bovenaan, stands out want heel veel hoger dan de rest, maar dat is omdat het meerdere artiesten zijn bij 1 lied, dus is niet een unieke artiest
# p3dt.top10_percent_tracks(database, 'liveness')

