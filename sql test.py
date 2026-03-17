import sqlite3
import pandas as pd
import datetime as dt
# importing own files
import full_database_analysis as p3dt
import album_data_analysis as ada

database = sqlite3.connect('spotify_database.db')
database.execute("UPDATE tracks_data SET collaboration = 'false'")
database.execute("UPDATE tracks_data SET collaboration = 'true' WHERE id IN (SELECT track_id FROM albums_data WHERE artist_1 != '');")


# even lover uittesten van taylor swift. conclusie: NIET CONSISTENT !!!!!!!!!!!! TAYLOR WAT DOE JE?
#p3dt.album_features(database, '1NAmidJlEaVgA3MpcPFYGq', 'valence', visualization=True)

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
# hier doe ik mijn dingen voor deel 4 dus niet raar opkijken pls

# outlier detection (moet nog gedaan worden maar kan denk ik het best bij de analysis van de verschillende datasets gezet worden dus bij artists data en bij features data/ tracks data moet nog even kijken want die is samen)

# heb alle invalid records waar ik op kon komen gecheckt

#cursor.execute("ALTER TABLE albums_data DROP COLUMN artists;")
#database.commit()


# album features score GEDAAAAAAAAAAAAAAAAAAAAAN
#p3dt.album_features_summary(database, 'Reputation')

# check artist_data for duplicates

# group the features by the era and create barplots with the era on the x-axis that the average on the y-axis for all features you find interesting

# iets met popularity en streams maar we hebben helemaal geen streams?!?!??!?!?!?

# genres die het vaakst samen voorkomen

# for features label tracks as very low, low, medium, high and very high and identify genres that occur frequently among other tracks that score very low or very high

database.close()