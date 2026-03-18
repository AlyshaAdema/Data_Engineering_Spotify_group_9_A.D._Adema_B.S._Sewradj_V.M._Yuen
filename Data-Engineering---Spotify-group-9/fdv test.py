import sqlite3
import pandas as pd

# importing own files
import part3_dingen_testen as p3dt
import artist_data_analysis as ada
import features_data_visualization as fdv
from features_data_visualization import speechiness_vs_danceability

database = sqlite3.connect('spotify_database.db')

# fdv.x(database)

# uh, ik denk dat danceability varieert bij lage speechiness. opvallend is dat bij hoge speechiness zit danceability tussen 0.6 en 0.7. (en tussen speechiness van 0.5 en 0.9 zit weinig dancibility?)
# fdv.speechiness_vs_danceability(database)
# fdv.comparison_two_features(database, "speechiness", "danceability")

# tbh idrk of we hier iets aan hebben...?
# fdv.danceability_vs_energy_vs_tempo(database)
# fdv.acousticness_vs_instrumentalness_vs_speechiness(database)
# fdv.comparison_three_features(database, "acousticness", "instrumentalness", "speechiness")
