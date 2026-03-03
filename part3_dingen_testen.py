import pandas as pd


def album_features(database, album):
    print(pd.read_sql_query("SELECT a.track_id, f.* FROM albums_data a JOIN features_data f ON a.track_id = f.id WHERE a.album_name = ?", database, params=[album]))