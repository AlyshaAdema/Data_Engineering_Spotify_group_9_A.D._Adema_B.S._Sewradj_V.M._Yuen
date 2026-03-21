import pandas as pd

def feature_stats(database, feature, eras, stat):
    eras_str = ','.join([f"'{era}'" for era in eras])
    df = pd.read_sql_query(f"SELECT f.{feature} FROM features_data f JOIN albums_data al ON al.track_id = f.id WHERE al.era IN ({eras_str})", database)
    if stat == 'mean':
        return df[feature].mean()
    elif stat == 'max':
        return df[feature].max()
    elif stat == 'min':
        return df[feature].min()
    elif stat == 'std':
        return df[feature].std()

def feature_correlation(database, feature1, feature2, eras):
    eras_str = ','.join([f"'{era}'" for era in eras])
    df = pd.read_sql_query(f"SELECT f.{feature1}, f.{feature2} FROM features_data f JOIN albums_data al ON al.track_id = f.id WHERE al.era IN ({eras_str})", database)
    return df[feature1].corr(df[feature2])