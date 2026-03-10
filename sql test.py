import sqlite3
import pandas as pd
import datetime as dt
# importing own files
import part3_dingen_testen as p3dt
import artist_data_analysis as ada

database = sqlite3.connect('spotify_database.db')
# even lover uittesten van taylor swift. conclusie: NIET CONSISTENT !!!!!!!!!!!! TAYLOR WAT DOE JE?
# p3dt.album_features(database, '1NAmidJlEaVgA3MpcPFYGq', 'valence', visualization=True)

# danceability, various artists staat bovenaan, stands out want heel veel hoger dan de rest, maar dat is omdat het meerdere artiesten zijn bij 1 lied, dus is niet een unieke artiest
# p3dt.top10_percent_tracks(database, 'liveness')

# dus positieve correlation tussen album popularity en artist popularity (dus als artiest populair is is album wss ook populair, maar hoeft niet altijd zo te zijn want correlation is niet 1)
# p3dt.relationship_artist_album_popularity(database)

# de tijdperken ding is aangemaakt alleen geen analysis mee gedaan want dat vroeg de opdracht niet

# the gemiddelde popularity van explicit tracks ligt wel hoger dan die van niet explicit, maar is niet heel groot verschil (34 en 28) dus miss hoeft het niet eens iets te beteken
# p3dt.explicit_tracks_popularity(database)

# the top 10 artists with the most explicit tracks are: Snoop Dogg, Eminem, Lil Wayne, Various artists, Future, Nicki Minaj, Tyga, Busta Rhymes, Drake, Chris Brown. With Snoop Dogg and eminem taking a clear lead.
# p3dt.top10_artist_highest_proportion_explicit(database)

# collaborations moeten nog