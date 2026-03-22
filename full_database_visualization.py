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
        ax.set_title("No Eras Selected", color='white')
        return fig

    eras_str = ','.join([f"'{era}'" for era in eras])

    df = pd.read_sql_query(f"""
        SELECT t.track_popularity, al.era 
        FROM tracks_data t 
        JOIN albums_data al ON t.id = al.track_id 
        WHERE al.era IN ({eras_str})""", database)

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

def donut_chart_tracks(database, eras):
    if not eras:
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('#121212')
        ax.set_facecolor('#121212')
        ax.set_title("No Eras Selected", color='white')
        return fig

    eras_str = ','.join([f"'{era}'" for era in eras])

    df = pd.read_sql_query(f"""
        SELECT era 
        FROM albums_data 
        WHERE era IN ({eras_str})""", database
    )

    tracks_released = []
    for era in eras:
        tracks_released.append(len(df[df['era'] == era]))

    fig, ax = plt.subplots(figsize=(8,5))
    fig.patch.set_facecolor('#121212')
    ax.set_facecolor('#121212')

    ax.pie(tracks_released, autopct='%1.1f%%', pctdistance=0.7, startangle=90, colors=['#1DB954', '#0E7C3A', '#064F2A', '#C8F7D1', '#9BF0B6', '#66E28A', '#4AE68A', '#1ED760'])
    centre_circle = plt.Circle((0, 0), 0.5, color='#121212')
    ax.add_artist(centre_circle)

    ax.set_title('Tracks Released per Era', color='w', fontsize=16, weight='bold')
    ax.legend(eras, loc="upper right", bbox_to_anchor=(1, 0.5))

    fig.subplots_adjust(right=0.75)
    return fig

def donut_chart_explicit_vs_nonexplicit(database, eras):
    if not eras:
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('#121212')
        ax.set_facecolor('#121212')
        ax.set_title("No Eras Selected", color='white')
        return fig

    eras_str = ','.join([f"'{era}'" for era in eras])

    df = pd.read_sql_query(f"""
        SELECT t.explicit, t.track_popularity 
        FROM tracks_data t 
        JOIN albums_data al ON t.id = al.track_id 
        WHERE era IN ({eras_str})""", database
    )

    explicit_tracks = len(df[df['explicit'] == 'true'])
    non_explicit_tracks = len(df[df['explicit'] == 'false'])

    fig, ax = plt.subplots(figsize=(8,5))
    fig.patch.set_facecolor('#121212')
    ax.set_facecolor('#121212')

    ax.pie([explicit_tracks, non_explicit_tracks], autopct='%1.1f%%', pctdistance=0.7, startangle=90, colors=['#1DB954', '#0E7C3A'])
    centre_circle = plt.Circle((0, 0), 0.5, color='#121212')
    ax.add_artist(centre_circle)

    ax.set_title('Explicit vs Non-explicit Tracks', color="w", fontsize=16, weight='bold')
    ax.legend(['Explicit', 'Non-explicit'], loc="upper right", bbox_to_anchor=(1, 0.5))

    fig.subplots_adjust(right=0.75)
    return fig

def bar_plot_top_5_tracks_artist(database, artist):
    df = fda.most_popular_tracks(database, artist)

    if df is None or df.empty:
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('#121212')
        ax.set_facecolor('#121212')
        ax.set_title("No Tracks Found", color='white')
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

    ax.set_xlabel('Top Tracks')
    ax.set_ylabel('Popularity')

    ax.set_title('Popularity Top Tracks', fontsize=16, weight='bold')

    plt.tight_layout()
    return fig

def bar_plot_top_5_albums(database, artist):
    df = fda.most_popular_albums(database, artist)

    if df is None or df.empty:
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('#121212')
        ax.set_facecolor('#121212')
        ax.set_title("No Albums Found", color='white')
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

    ax.set_xlabel('Top Albums')
    ax.set_ylabel('Popularity')

    ax.set_title('Popularity Top Albums', fontsize=16, weight='bold')

    plt.tight_layout()
    return fig

def box_plot_feature_artist(database, artist, feature):
    df = pd.read_sql_query(f"SELECT al.track_id, al.album_id, f.{feature} FROM albums_data al JOIN features_data f ON al.track_id = f.id JOIN artist_data ar ON al.artist_id = ar.id WHERE ar.name = ?", database, params=[artist])

    if df is None or df.empty:
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('#121212')
        ax.set_facecolor('#121212')
        ax.set_title("Artist Not Found", color='white')
        return fig

    fig, ax = plt.subplots()
    fig.patch.set_facecolor('#121212')
    ax.set_facecolor('#121212')

    ax.boxplot(df[feature], vert=False, patch_artist=True, boxprops=dict(facecolor='#1DB954', color='white'), medianprops=dict(color='white'), whiskerprops=dict(color='white'), capprops=dict(color='white'))
    ax.set_yticks([])
    ax.set_xlabel("Values", color='white')
    ax.tick_params(colors='white')

    ax.set_title(f"{artist} - {feature.title()} Distribution", fontsize=16, weight='bold', color='white')

    plt.tight_layout()
    return fig

def bar_plot_top10_artist_feature_ranking(database, feature, eras, very_low=True):
    df = fda.top10_artists_feature_ranking(database, feature, eras, very_low)

    if df is None or df.empty:
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('#121212')
        ax.set_facecolor('#121212')
        ax.set_title("No Eras Selected", color='white')
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
    ax.set_xticklabels([artist[:15] + "…" if len(artist) > 15 else artist for artist in df['artist']], rotation=45,
                       ha='right')
    ax.set_xlabel('Artist')
    ax.set_ylabel('Count')

    if very_low:
        ax.set_title(f'Top Artists with Very Low {feature.title()}', fontsize=16, weight='bold')
    else:
        ax.set_title(f'Top Artists with Very High {feature.title()}', fontsize=16, weight='bold')

    ax.grid(axis='x', linestyle='', alpha=0.3, color='white')

    plt.tight_layout()
    return fig

def bar_plot_top10_genres_feature_ranking(database, feature, eras, very_low=True):
    df = fda.top10_genres_feature_ranking(database, feature, eras, very_low)

    if df is None or df.empty:
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('#121212')
        ax.set_facecolor('#121212')
        ax.set_title("No Eras Selected", color='white')
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
        ax.set_title(f'Top Genres with Very Low {feature.title()}', fontsize=16, weight='bold')
    else:
        ax.set_title(f'Top Genres with Very High {feature.title()}', fontsize=16, weight='bold')

    ax.grid(axis='x', linestyle='', alpha=0.3, color='white')

    plt.tight_layout()
    return fig
