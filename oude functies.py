def top10_percent_tracks(database, feature):
    allowed_features = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms']
    if feature in allowed_features:
        df = pd.read_sql_query(f"""SELECT f.{feature}, ar.name FROM albums_data al JOIN features_data f ON al.track_id = f.id JOIN artist_data ar ON al.artist_id = ar.id""", database)
        ten_percent = int(len(df) * 0.1 + 0.5)
        top_df = df.nlargest(ten_percent, feature)[['name', feature]]
        sorted_top_df = top_df['name'].value_counts()
        print("The top 10 reoccurring artists for feature: %s" % feature)
        print(sorted_top_df.nlargest(10))
    #
    # top 10% van tracks per feature. nieuwe df met naam artiest, welke artiest komt meest voor
# betere functie naam

# danceability, various artists staat bovenaan, stands out want heel veel hoger dan de rest, maar dat is omdat het meerdere artiesten zijn bij 1 lied, dus is niet een unieke artiest
p3dt.top10_percent_tracks(database, 'danceability')


# minst voorkomende genres
def top10_genres_by_least_followers(database):
    return df_followers_all_genres(database).nsmallest(10, 'followers')

