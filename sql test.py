import sqlite3
import pandas as pd

# importing own files
import part3_dingen_testen as p3dt

database = sqlite3.connect('spotify_database.db')
p3dt.album_features(database, 'Electric Ladyland (Redux)')