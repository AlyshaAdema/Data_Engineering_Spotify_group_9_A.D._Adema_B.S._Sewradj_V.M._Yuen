import pandas as pd
import matplotlib.pyplot as plt

# importing own files
import full_database_analysis as fda

def line_chart_track_popularity(database, eras):
    if not eras:
        fig, ax = plt.subplots()
        ax.set_title("No eras selected")
        return fig
    eras_str = ','.join([f"'{era}'" for era in eras])
    df = pd.read_sql_query(f"SELECT t.track_popularity, al.era FROM tracks_data t JOIN albums_data al ON t.id = al.track_id WHERE al.era IN ({eras_str})", database)
    average = []
    for era in eras:
        average_popularity = df[df['era'] == era]['track_popularity'].mean()
        average.append(average_popularity)
    fig, ax = plt.subplots()
    ax.plot(eras, average)
    ax.set_xlabel('Era')
    ax.set_ylabel('Average Track Popularity')
    ax.set_title('Average Track Popularity by Era')
    plt.xticks(rotation=90)
    return fig

def pie_chart_tracks(database, eras):
    if not eras:
        fig, ax = plt.subplots()
        ax.set_title("No eras selected")
        return fig
    eras_str = ','.join([f"'{era}'" for era in eras])
    df = pd.read_sql_query(f"SELECT era FROM albums_data WHERE era IN ({eras_str})", database)
    tracks_released = []
    for era in eras:
        tracks_released.append(len(df[df['era'] == era]))
    fig, ax = plt.subplots()
    ax.pie(tracks_released, labels=eras, autopct='%1.1f%%')
    ax.set_title('Tracks released per era')
    return fig

def pie_chart_explicit_vs_nonexplicit(database, eras):
    if not eras:
        fig, ax = plt.subplots()
        ax.set_title("No eras selected")
        return fig
    eras_str = ','.join([f"'{era}'" for era in eras])
    df = pd.read_sql_query(f"SELECT t.explicit, t.track_popularity FROM tracks_data t JOIN albums_data al ON t.id = al.track_id WHERE era IN ({eras_str})", database)
    explicit_tracks = len(df[df['explicit'] == 'true'])
    non_explicit_tracks = len(df[df['explicit'] == 'false'])
    fig, ax = plt.subplots()
    ax.pie([explicit_tracks, non_explicit_tracks], labels=['Explicit', 'Non Explicit'], autopct='%1.1f%%')
    ax.set_title('Explicit tracks vs non explicit')
    return fig

def bar_plot_top_5_tracks_artist(database, artist):
    df = fda.most_popular_tracks(database, artist)
    if df is None or df.empty:
        fig, ax = plt.subplots()
        ax.set_title("No tracks found")
        return fig
    fig, ax = plt.subplots()
    ax.bar(df['track_name'], df['track_popularity'])
    ax.set_xticks(range(len(df)))
    ax.set_xticklabels([name[:15] + "…" if len(name) > 15 else name for name in df['track_name']], rotation=45, ha='right')
    ax.set_xlabel('Names top tracks')
    ax.set_ylabel('Popularity')
    ax.set_title('Popularity top tracks')
    plt.tight_layout()
    return fig

def bar_plot_top_5_albums(database, artist):
    df = fda.most_popular_albums(database, artist)
    if df is None or df.empty:
        fig, ax = plt.subplots()
        ax.set_title("No albums found")
        return fig
    fig, ax = plt.subplots()
    ax.bar(df['album_name'], df['album_popularity'])
    ax.set_xticks(range(len(df)))
    ax.set_xticklabels([name[:15] + "…" if len(name) > 15 else name for name in df['album_name']], rotation=45, ha='right')
    ax.set_xlabel('Names top albums')
    ax.set_ylabel('Popularity')
    ax.set_title('Popularity top albums')
    plt.tight_layout()
    return fig

def box_plot_feature_artist(database, artist, feature):
    df = pd.read_sql_query(f"SELECT al.track_id, al.album_id, f.{feature} FROM albums_data al JOIN features_data f ON al.track_id = f.id JOIN artist_data ar ON al.artist_id = ar.id WHERE ar.name = ?", database, params=[artist])
    if df is None or df.empty:
        fig, ax = plt.subplots()
        ax.set_title("Artist not found")
        return fig
    fig, ax = plt.subplots()
    ax.boxplot(df[feature], vert=False)
    ax.set_yticks([])
    ax.set_xlabel("Values")
    ax.set_title(f"Boxplot of {feature}")
    return fig

def bar_plot_top10_genres_feature_ranking(database, feature, eras, very_low=True):
    df = fda.top10_genres_feature_ranking(database, feature, eras, very_low)
    if df is None or df.empty:
        fig, ax = plt.subplots()
        ax.set_title("No eras selected")
        return fig
    fig, ax = plt.subplots()
    ax.bar(df['genres'], df['count'])
    ax.set_xticklabels(df['genres'], rotation=90)
    ax.set_xlabel('Genre')
    ax.set_ylabel('Count')
    if very_low:
        ax.set_title(f'Top genres with very low {feature} score')
    else:
        ax.set_title(f'Top genres with very high {feature} score')
    plt.tight_layout()
    return fig

def bar_plot_top10_artist_feature_ranking(database, feature, eras, very_low=True):
    df = fda.top10_artists_feature_ranking(database, feature, eras, very_low)
    if df is None or df.empty:
        fig, ax = plt.subplots()
        ax.set_title("No eras selected")
        return fig
    fig, ax = plt.subplots()
    ax.bar(df['name'], df['count'])
    ax.set_xticklabels(df['name'], rotation=90)
    ax.set_xlabel('Name')
    ax.set_ylabel('Count')
    if very_low:
        ax.set_title(f'Top artists with very low {feature} score')
    else:
        ax.set_title(f'Top artists with very high {feature} score')
    plt.tight_layout()
    return fig