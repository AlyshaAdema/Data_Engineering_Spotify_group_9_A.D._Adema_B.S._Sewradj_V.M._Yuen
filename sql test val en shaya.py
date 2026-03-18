import sqlite3
import pandas as pd
import full_database_analysis as p3dt

database = sqlite3.connect("spotify_database.db")

# # Speed things up
# database.execute("CREATE INDEX IF NOT EXISTS idx_albums_track_id ON albums_data(track_id);")
# database.execute("CREATE INDEX IF NOT EXISTS idx_tracks_id ON tracks_data(id);")
# database.commit()
#
# # Faster update
# database.execute("""
# UPDATE tracks_data
# SET collaboration =
#   CASE WHEN EXISTS (
#     SELECT 1
#     FROM albums_data
#     WHERE albums_data.track_id = tracks_data.id
#       AND albums_data.artist_1 <> ''
#   )
#   THEN 'true' ELSE 'false' END
# """)
# database.commit()
#
# # Don’t print the whole DB
# df = pd.read_sql_query("""
# SELECT t.id, t.collaboration, al.artist_1
# FROM tracks_data t
# JOIN albums_data al ON t.id = al.track_id
# LIMIT 20
# """, database)
# print(df)

p3dt.explicit_tracks_popularity(database)

database.close()