import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np


# importing own files
import full_database_analysis as fda

def line_chart_track_popularity(database, eras):
    if not eras:
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('#121212')
        ax.set_facecolor('#121212')
        ax.set_title("No eras selected", color='white')
        return fig
    eras_str = ','.join([f"'{era}'" for era in eras])
    df = pd.read_sql_query(f"SELECT t.track_popularity, al.era FROM tracks_data t JOIN albums_data al ON t.id = al.track_id WHERE al.era IN ({eras_str})", database)
    average = []
    for era in eras:
        average_popularity = df[df['era'] == era]['track_popularity'].mean()
        average.append(average_popularity)
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('#121212')
    ax.set_facecolor('#121212')

    ax.tick_params(colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.title.set_color('white')
    ax.plot(eras, average, color='#1DB954', marker='o')
    ax.set_xlabel('Era')
    ax.set_ylabel('Average Track Popularity')
    ax.set_title('Average Track Popularity by Era', fontsize=16, weight='bold')
    ax.grid(axis='y', linestyle='--', alpha=0.3, color='white')
    plt.xticks(rotation=45, ha='right')
    return fig

def pie_chart_tracks(database, eras):
    if not eras:
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('#121212')
        ax.set_facecolor('#121212')
        ax.set_title("No eras selected", color='white')
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
        fig.patch.set_facecolor('#121212')
        ax.set_facecolor('#121212')
        ax.set_title("No eras selected", color='white')
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
        fig.patch.set_facecolor('#121212')
        ax.set_facecolor('#121212')
        ax.set_title("No tracks found", color='white')
        return fig
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('#121212')
    ax.set_facecolor('#121212')
    ax.tick_params(colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.title.set_color('white')
    start_color = np.array(mcolors.to_rgb('#1DB954'))
    end_color = np.array(mcolors.to_rgb('#1DE97C'))
    n = len(df)
    if n == 1:
        colors = [mcolors.to_hex(start_color)]
    else:
        colors = [mcolors.to_hex(start_color + (end_color - start_color) * (i / (n - 1))) for i in range(n)]
    ax.bar(df['track_name'], df['track_popularity'], color=colors)
    ax.set_xticks(range(len(df)))
    ax.set_xticklabels([name[:15] + "…" if len(name) > 15 else name for name in df['track_name']], rotation=45, ha='right')
    ax.set_xlabel('Tracks')
    ax.set_ylabel('Popularity')
    ax.set_title(f'Top Tracks of {artist} by Popularity', fontsize=16, weight='bold')
    plt.tight_layout()
    return fig

def bar_plot_top_5_albums(database, artist):
    df = fda.most_popular_albums(database, artist)
    if df is None or df.empty:
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('#121212')
        ax.set_facecolor('#121212')
        ax.set_title("No albums found", color='white')
        return fig
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('#121212')
    ax.set_facecolor('#121212')
    ax.tick_params(colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.title.set_color('white')
    start_color = np.array(mcolors.to_rgb('#1DB954'))
    end_color = np.array(mcolors.to_rgb('#1DE97C'))
    n = len(df)
    if n == 1:
        colors = [mcolors.to_hex(start_color)]
    else:
        colors = [mcolors.to_hex(start_color + (end_color - start_color) * (i / (n - 1))) for i in range(n)]
    ax.bar(df['album_name'], df['album_popularity'], color=colors)
    ax.set_xticks(range(len(df)))
    ax.set_xticklabels([name[:15] + "…" if len(name) > 15 else name for name in df['album_name']], rotation=45, ha='right')
    ax.set_xlabel('Albums')
    ax.set_ylabel('Popularity')
    ax.set_title(f'Top Albums of {artist} by Popularity', fontsize=16, weight='bold')
    plt.tight_layout()
    return fig

def box_plot_feature_artist(database, artist, feature):
    df = pd.read_sql_query(f"SELECT al.track_id, al.album_id, f.{feature} FROM albums_data al JOIN features_data f ON al.track_id = f.id JOIN artist_data ar ON al.artist_id = ar.id WHERE ar.name = ?", database, params=[artist])
    if df is None or df.empty:
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('#121212')
        ax.set_facecolor('#121212')
        ax.set_title("Artist not found", color='white')
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
        fig.patch.set_facecolor('#121212')
        ax.set_facecolor('#121212')
        ax.set_title("No eras selected", color='white')
        return fig
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('#121212')
    ax.set_facecolor('#121212')
    ax.tick_params(colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.title.set_color('white')
    start_color = np.array(mcolors.to_rgb('#1DB954'))
    end_color = np.array(mcolors.to_rgb('#1DE97C'))
    n = len(df)
    if n == 1:
        colors = [mcolors.to_hex(start_color)]
    else:
        colors = [mcolors.to_hex(start_color + (end_color - start_color) * (i / (n - 1))) for i in range(n)]
    ax.bar(df['genres'], df['count'], color=colors)
    ax.set_xticklabels([genres[:15] + "…" if len(genres) > 15 else genres for genres in df['genres']], rotation=45, ha='right')
    ax.set_xlabel('Genre')
    ax.set_ylabel('Count')
    if very_low:
        ax.set_title(f'Top Genres with very low {feature}', fontsize=16, weight='bold')
    else:
        ax.set_title(f'Top Genres with very high {feature}', fontsize=16, weight='bold')
    ax.grid(axis='x', linestyle='', alpha=0.3, color='white')
    plt.tight_layout()
    return fig

def bar_plot_top10_artist_feature_ranking(database, feature, eras, very_low=True):
    df = fda.top10_artists_feature_ranking(database, feature, eras, very_low)
    if df is None or df.empty:
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('#121212')
        ax.set_facecolor('#121212')
        ax.set_title("No eras selected", color='white')
        return fig
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('#121212')
    ax.set_facecolor('#121212')
    ax.tick_params(colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.title.set_color('white')
    start_color = np.array(mcolors.to_rgb('#1DB954'))
    end_color = np.array(mcolors.to_rgb('#1DE97C'))
    n = len(df)
    if n == 1:
        colors = [mcolors.to_hex(start_color)]
    else:
        colors = [mcolors.to_hex(start_color + (end_color - start_color) * (i / (n - 1))) for i in range(n)]
    ax.bar(df['artist'], df['count'], color=colors)
    ax.set_xticklabels([artist[:15] + "…" if len(artist) > 15 else artist for artist in df['artist']], rotation=45, ha='right')
    ax.set_xlabel('Artist')
    ax.set_ylabel('Count')
    if very_low:
        ax.set_title(f'Top Artists with very low {feature}', fontsize=16, weight='bold')
    else:
        ax.set_title(f'Top Artists with very high {feature}', fontsize=16, weight='bold')
    ax.grid(axis='x', linestyle='', alpha=0.3, color='white')
    plt.tight_layout()
    return fig