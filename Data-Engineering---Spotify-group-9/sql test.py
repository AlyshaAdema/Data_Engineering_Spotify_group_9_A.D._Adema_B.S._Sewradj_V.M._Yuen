import sqlite3
import pandas as pd

# importing own files
import part3_dingen_testen as p3dt
import artist_data_analysis as ada

database = sqlite3.connect('spotify_database.db')
database.execute("UPDATE tracks_data SET collaboration = 'false'")
database.execute("UPDATE tracks_data SET collaboration = 'true' WHERE id IN (SELECT track_id FROM albums_data WHERE artist_1 != '');")


# even lover uittesten van taylor swift. conclusie: NIET CONSISTENT !!!!!!!!!!!! TAYLOR WAT DOE JE?
# p3dt.album_features(database, '1NAmidJlEaVgA3MpcPFYGq', 'valence', visualization=True)

# val: ik heb ervoor gezorgd dat 'Various Artists' niet meer wordt vertoond, want toen ik die artist_id ging opzoeken in excel, stond er elke keer gewoon een
# p3dt.top10_artists_per_feature(database, 'danceability')

# dus positieve correlation tussen album popularity en artist popularity (dus als artiest populair is is album wss ook populair, maar hoeft niet altijd zo te zijn want correlation is niet 1)
# p3dt.relation_ship_artist_album_popularity(database)

# the gemiddelde popularity van explicit tracks ligt wel hoger dan die van niet explicit, maar is niet heel groot verschil (34 en 28) dus miss hoeft het niet eens iets te beteken
# p3dt.explicit_tracks_popularity(database)

# the top 10 artists with the most explicit tracks are: Snoop Dogg, Eminem, Lil Wayne, Various artists, Future, Nicki Minaj, Tyga, Busta Rhymes, Drake, Chris Brown. With Snoop Dogg and eminem taking a clear lead.
# p3dt.top10_artist_highest_proportion_explicit(database)

# collaborations dingetje moet nog
# p3dt.popularity_collaboration(database)

# p3dt.average_artists_per_collab(database)

# creativiteit deel wat kunnen we allemaal checken?

# p3dt.duration_explicit(database)

p3dt.longest_or_shortest_explicit_or_non_explicit_tracks(database, longest=False, explicit=True)
