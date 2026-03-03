import pandas as pd
import matplotlib.pyplot as plt

def album_features(database, album_id, feature, visualization=False):
    allowed_features = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms']
    if feature in allowed_features:
        df = pd.read_sql_query(f"""SELECT a.track_id, a.track_name, a.track_number, f.{feature} FROM albums_data a JOIN features_data f ON a.track_id = f.id WHERE a.album_id = ?""", database, params=[album_id])
        df = df.sort_values(by=['track_number'])
        print('Statistics for feature: %s' % feature)
        print('Mean: %f' % df[feature].mean())
        print('Standard deviation: %f' % df[feature].std())
        print('Minimum: %f' % df[feature].min())
        print('Maximum: %f' % df[feature].max())
        if visualization:
            plt.plot(df['track_number'], df[feature])
            plt.xticks(range(1, len(df) + 1, 1))
            plt.xlabel('Track number')
            plt.ylabel('%s values' % feature)
            plt.title('Results of %s' % feature)
            plt.show()

def top10_percent_tracks(database, feature):
    pd.set_option("display.max_columns", None)
    allowed_features = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms']
    if feature in allowed_features:
        df = pd.read_sql_query(f"""SELECT al.track_id, al.artist_id, f.{feature}, ar.name FROM albums_data al JOIN features_data f ON al.track_id = f.id JOIN artist_data ar ON al.artist_id = ar.id""", database)
        ten_percent = int(len(df) * 0.1 + 0.5)
        top_df = df.nlargest(ten_percent, feature)[['name', feature]]
        sorted_top_df = top_df['name'].value_counts()
        print("The top 10 reoccuring artists for feature: %s" % feature)
        print(sorted_top_df.nlargest(10))




    # top 10% van tracks per feature. nieuwe df met naam artiest, welke artiest komt meest voor
# betere functie naam