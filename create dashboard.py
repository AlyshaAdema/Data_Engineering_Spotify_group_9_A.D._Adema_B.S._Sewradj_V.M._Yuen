import streamlit as st
import sqlite3

# Importing own files
import artist_data_analysis as arda
import artist_data_visualization as ardv
import album_data_analysis as alda
import full_database_analysis as flda
import full_database_visualization as fldv
import features_data_analysis as fda
import features_data_visualization as fdv
import album_data_visualization as aldv

st.set_page_config(
    page_title="Spotify Data Analysis",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)
# Cache General Page
@st.cache_data
def cached_unique_artists(_database, eras):
    return arda.unique_artists(database, eras)

@st.cache_data
def cached_unique_albums(_database, eras):
    return alda.unique_albums(database, eras)

@st.cache_data
def cached_unique_tracks(_database, eras):
    return alda.unique_tracks(database, eras)

@st.cache_data
def cached_number_of_genres(_database, eras):
    return arda.number_of_genres(database, eras)

@st.cache_data
def cached_line_chart_popularity(_database, eras):
    return fldv.line_chart_track_popularity(database, eras)

@st.cache_data
def cached_top10_followers(_database, eras):
    return ardv.top10_followers(database, eras)

@st.cache_data
def cached_top10_popularity(_database, eras):
    return ardv.top10_popularity(database, eras)

@st.cache_data
def cached_linear_regression(_database, eras):
    return ardv.linear_regression(database, eras)

@st.cache_data
def cached_pie_tracks(_database, eras):
    return fldv.donut_chart_tracks(database, eras)

@st.cache_data
def cached_pie_explicit(_database, eras):
    return fldv.donut_chart_explicit_vs_nonexplicit(database, eras)

# Cache Feature Page
@st.cache_data
def cached_mean_feature(_database, feature, eras):
    return fda.feature_stats(database, feature, eras, 'mean')

@st.cache_data
def cached_min_feature(_database, feature, eras):
    return fda.feature_stats(database, feature, eras, 'min')

@st.cache_data
def cached_max_feature(_database, feature, eras):
    return fda.feature_stats(database, feature, eras, 'max')

@st.cache_data
def cached_std_feature(_database, feature, eras):
    return fda.feature_stats(database, feature, eras, 'std')

@st.cache_data
def cached_line_chart_feature(_database, feature, eras):
    return fdv.line_chart_features_eras(database, feature, eras)

@st.cache_data
def cached_boxplot_feature(_database, feature, eras):
    return fdv.boxplot_feature(database, feature, eras)

@st.cache_data
def cached_correlation_list(_database, feature, compare_feature_list, eras):
    correlation_list = []
    for i in range(len(compare_feature_list)):
        correlation_list.append(
            fda.feature_correlation(database, feature, compare_feature_list[i], eras))
    return correlation_list

@st.cache_data
def cached_largest_index(correlation_list):
    largest_index = 0
    for i in range(1, len(correlation_list)):
        if correlation_list[i] > correlation_list[largest_index]:
            largest_index = i
    return largest_index

@st.cache_data
def cached_bar_feature_ranking_artist_high(_database, feature, eras):
    return fldv.bar_plot_top10_artist_feature_ranking(database, feature, eras, very_low=False)

@st.cache_data
def cached_bar_feature_ranking_artist_low(_database, feature, eras):
    return fldv.bar_plot_top10_artist_feature_ranking(database, feature, eras, very_low=True)

@st.cache_data
def cached_bar_feature_ranking_genre_high(_database, feature, eras):
    return fldv.bar_plot_top10_genres_feature_ranking(database, feature, eras, very_low=False)

@st.cache_data
def cached_bar_feature_ranking_genre_low(_database, feature, eras):
    return fldv.bar_plot_top10_genres_feature_ranking(database, feature, eras, very_low=True)

# Cache Genre Page
@st.cache_data
def cached_artists_per_genre(_database, genre):
    return arda.artists_per_genre(database, genre)

@st.cache_data
def cached_average_popularity_per_genre(_database, genre):
    return arda.average_popularity_per_genre(database, genre)

@st.cache_data
def cached_total_followers_per_genre(_database, genre):
    return arda.total_followers_per_genre(database, genre)

@st.cache_data
def cached_average_followers_per_genre(_database, genre):
    return arda.average_followers_per_genre(database, genre)

@st.cache_data
def cached_top10_followers_genre(_database, genre):
    return ardv.top10_followers_genre(database, genre)

@st.cache_data
def cached_top10_popularity_genre(_database, genre):
    return ardv.top10_popularity_genre(database, genre)

@st.cache_data
def cached_followers_distribution_genre(_database, genre):
    return ardv.followers_distribution_genres(database, genre)

@st.cache_data
def cached_popularity_distribution_genre(_database, genre):
    return ardv.popularity_distribution_genres(database, genre)

@st.cache_data
def cached_bar_genre_combination(_database, genre):
    return ardv.bar_plot_top_genre_combination(database, genre)

# Cache Artist Page
@st.cache_data
def cached_followers_artist(_database, artist):
    return arda.number_followers_artist(database, artist)

@st.cache_data
def cached_popularity_artist(_database, artist):
    return arda.popularity_artist(database, artist)

@st.cache_data
def cached_albums_artist(_database, artist):
    return flda.number_albums_artist(database, artist)

@st.cache_data
def cached_singles_artist(_database, artist):
    return flda.number_singles_artist(database, artist)

@st.cache_data
def cached_tracks_artist(_database, artist):
    return flda.number_tracks_artist(database, artist)

@st.cache_data
def cached_genres_artist(_database, artist):
    return arda.genres_artist(database, artist)

@st.cache_data
def cached_bar_top5_tracks_artist(_database, artist):
    return fldv.bar_plot_top_5_tracks_artist(database, artist)

@st.cache_data
def cached_bar_top5_albums_artist(_database, artist):
    return fldv.bar_plot_top_5_albums(database, artist)

@st.cache_data
def cached_artist_features_mean(_database, artist, feature):
    return flda.artist_features(database, artist, feature, 'mean')

@st.cache_data
def cached_artist_features_std(_database, artist, feature):
    return flda.artist_features(database, artist, feature, 'std')

@st.cache_data
def cached_artist_features_min(_database, artist, feature):
    return flda.artist_features(database, artist, feature, 'min')

@st.cache_data
def cached_artist_features_max(_database, artist, feature):
    return flda.artist_features(database, artist, feature, 'max')

@st.cache_data
def cached_boxplot_feature_artist(_database, artist, feature):
    return fldv.box_plot_feature_artist(database, artist, feature)

## ALYSHA KIJK DOE DE CACHE VAN ALBUMS HIER
# Cache Album Page


# Connect to database
database = sqlite3.connect('spotify_database.db')

# Pages and selections
pages = ['Overview', 'Album', 'Artist', 'Feature', 'Genre']
eras = ['1900s','1930s','1940s','1950s','1960s','1970s','1980s','1990s','2000s','2010s','2020s']
features = ['acousticness', 'danceability', 'duration_ms', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence']
genres = arda.all_genres(database)

# Initialize session state for navbar
if 'page' not in st.session_state:
    st.session_state.page = pages[0]

# ---------- NAVIGATION BAR ----------
cols = st.columns(len(pages))
for i, page_name in enumerate(pages):
    # active page style
    if st.session_state.page == page_name:
        style = """
            background-color: rgba(0,0,0,0.3);
            color: white;
            border-radius: 0.5rem;
            font-weight: bold;
            padding: 0.5rem 1rem;
            border: none;
            width: 100%;
        """
    else:
        style = """
            background-color: #1DB954;
            color: white;
            border-radius: 0.5rem;
            font-weight: bold;
            padding: 0.5rem 1rem;
            border: none;
            width: 100%;
        """
    if cols[i].button(page_name, key=page_name):
        st.session_state.page = page_name

# Current page
page = st.session_state.page

# ---------- OVERVIEW PAGE ----------
if page == 'Overview':
    st.title("General Analysis")
    selected_eras = st.sidebar.multiselect('Select Era(s) to Display:', eras, default=eras)
    total_artists = cached_unique_artists(database, selected_eras)
    total_albums = cached_unique_albums(database, selected_eras)
    total_tracks = cached_unique_tracks(database, selected_eras)
    total_genres = cached_number_of_genres(database, selected_eras)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Artists", f"{total_artists:,.0f}")
    with col2:
        st.metric("Total Albums", f"{total_albums:,.0f}")
    with col3:
        st.metric("Total Tracks", f"{total_tracks:,.0f}")
    with col4:
        st.metric("Total Genres", f"{total_genres:,.0f}")

    st.divider()

    fig = cached_line_chart_popularity(database, selected_eras)
    st.pyplot(fig)

    st.divider()

    left, right = st.columns(2)
    with left:
        chart_type = st.selectbox("Select metric to display for top artists:", ("Followers", "Popularity"))
        if chart_type == "Followers":
            fig = cached_top10_followers(database, selected_eras)
        else:
            fig = cached_top10_popularity(database, selected_eras)
        st.pyplot(fig)
    with right:
        fig = cached_linear_regression(database, selected_eras)
        st.pyplot(fig)

    st.divider()

    left, right = st.columns(2)
    with left:
        fig = cached_pie_tracks(database, selected_eras)
        st.pyplot(fig)
    with right:
        fig = cached_pie_explicit(database, selected_eras)
        st.pyplot(fig)

# ---------- FEATURE PAGE ----------
elif page == 'Feature':
    st.title("Feature Analysis")
    selected_feature = st.sidebar.selectbox('Select a main feature to display:', features)
    compare_feature_list = [feature for feature in features if feature != selected_feature]
    selected_eras = st.sidebar.multiselect('Select era(s) to display:', eras, default=eras)

    # Statistical metrics
    mean_feature = cached_mean_feature(database, selected_feature, selected_eras)
    min_feature = cached_min_feature(database, selected_feature, selected_eras)
    max_feature = cached_max_feature(database, selected_feature, selected_eras)
    std_feature = cached_std_feature(database, selected_feature, selected_eras)

    correlation_feature0 = fda.feature_correlation(database, selected_feature, compare_feature_list[0], selected_eras)
    correlation_feature1 = fda.feature_correlation(database, selected_feature, compare_feature_list[1], selected_eras)
    correlation_feature2 = fda.feature_correlation(database, selected_feature, compare_feature_list[2], selected_eras)
    correlation_feature3 = fda.feature_correlation(database, selected_feature, compare_feature_list[3], selected_eras)
    correlation_feature4 = fda.feature_correlation(database, selected_feature, compare_feature_list[4], selected_eras)
    correlation_feature5 = fda.feature_correlation(database, selected_feature, compare_feature_list[5], selected_eras)
    correlation_feature6 = fda.feature_correlation(database, selected_feature, compare_feature_list[6], selected_eras)
    correlation_feature7 = fda.feature_correlation(database, selected_feature, compare_feature_list[7], selected_eras)
    correlation_feature8 = fda.feature_correlation(database, selected_feature, compare_feature_list[8], selected_eras)

    st.markdown(f'Displayed Feature: {selected_feature.title()}')
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Mean", f"{mean_feature:,.2f}")
    with col2:
        st.metric("Minimum", f"{min_feature:,.2f}")
    with col3:
        st.metric("Maximum", f"{max_feature:,.2f}")
    with col4:
        st.metric("Standard Deviation", f"{std_feature:,.2f}")

    st.divider()

    left, right = st.columns(2)
    with left:
        fig = cached_line_chart_feature(database, selected_feature, selected_eras)
        st.pyplot(fig)
    with right:
        fig = cached_boxplot_feature(database, selected_feature, selected_eras)
        st.pyplot(fig)

    st.divider()

    correlation_list = cached_correlation_list(database, selected_feature, compare_feature_list, selected_eras)
    largest_index = cached_largest_index(correlation_list)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric(f"Correlation {compare_feature_list[0].title()} ", f"{correlation_list[0]:,.2f}")
        st.metric(f"Correlation {compare_feature_list[1].title()} ", f"{correlation_list[1]:,.2f}")
    with col2:
        st.metric(f"Correlation {compare_feature_list[2].title()} ", f"{correlation_list[2]:,.2f}")
        st.metric(f"Correlation {compare_feature_list[3].title()} ", f"{correlation_list[3]:,.2f}")
    with col3:
        st.metric(f"Correlation {compare_feature_list[4].title()} ", f"{correlation_list[4]:,.2f}")
        st.metric(f"Correlation {compare_feature_list[5].title()} ", f"{correlation_list[5]:,.2f}")
    with col4:
        st.metric(f"Correlation {compare_feature_list[6].title()} ", f"{correlation_list[6]:,.2f}")
        st.metric(f"Correlation {compare_feature_list[7].title()} ", f"{correlation_list[7]:,.2f}")
    with col5:
        st.metric(f"Correlation {compare_feature_list[8].title()} ", f"{correlation_list[8]:,.2f}")
        st.metric(f"Most correlated to {selected_feature.title()}", f"{compare_feature_list[largest_index]}")

    st.divider()

    chart_type = st.selectbox("Select metric to display:", ("Artists", "Genres"))
    chart_type_container = st.container()
    with chart_type_container:
        left, right = st.columns(2)
        with left:
            if chart_type == "Artists":
                fig = cached_bar_feature_ranking_artist_high(database, selected_feature, selected_eras)
            elif chart_type == "Genres":
                fig = cached_bar_feature_ranking_genre_high(database, selected_feature, selected_eras)
            st.pyplot(fig)
        with right:
            if chart_type == "Artists":
                fig = cached_bar_feature_ranking_artist_low(database, selected_feature, selected_eras)
            elif chart_type == "Genres":
                fig = cached_bar_feature_ranking_genre_low(database, selected_feature, selected_eras)
            st.pyplot(fig)

# ---------- GENRE PAGE ----------
elif page == 'Genre':
    st.title('Genre Analysis')
    selected_genre = st.sidebar.selectbox('Select a Genre to Display:', genres)
    total_artists = cached_artists_per_genre(database, selected_genre)
    average_popularity = cached_average_popularity_per_genre(database, selected_genre)
    total_followers = cached_total_followers_per_genre(database, selected_genre)
    average_followers = cached_average_followers_per_genre(database, selected_genre)

    st.markdown(f'Displayed Genre: {selected_genre.title()}')
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Artists", f"{total_artists:,.0f}")
    with col2:
        st.metric("Average Popularity", f"{average_popularity:,.0f}")
    with col3:
        st.metric("Total Followers", f"{total_followers:,.0f}")
    with col4:
        st.metric("Average Followers", f"{average_followers:,.0f}")

    st.divider()

    chart_type = st.selectbox("Select metric to display for top artists:", ("Followers", "Popularity"))
    left, right = st.columns(2)
    with left:
        if chart_type == "Followers":
            fig = cached_top10_followers_genre(database, selected_genre)
        elif chart_type == "Popularity":
            fig = cached_top10_popularity_genre(database, selected_genre)
        st.pyplot(fig)
    with right:
        if chart_type == "Followers":
            fig = cached_followers_distribution_genre(database, selected_genre)
        elif chart_type == "Popularity":
            fig = cached_popularity_distribution_genre(database, selected_genre)
        st.pyplot(fig)

    st.divider()
    fig = cached_bar_genre_combination(database, selected_genre)
    st.pyplot(fig)

# ---------- ARTIST PAGE ----------
elif page == 'Artist':
    st.title("Artist Analysis")
    artist = st.sidebar.text_input('Enter an artist name', 'Taylor Swift')
    number_followers = cached_followers_artist(database, artist)
    popularity = cached_popularity_artist(database, artist)

    number_of_albums = cached_albums_artist(database, artist)
    number_of_singles = cached_singles_artist(database, artist)
    number_of_tracks = cached_tracks_artist(database, artist)

    st.markdown(f'Displayed Artist: {artist}')
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Followers", f"{number_followers:,.0f}")
    with col2:
        st.metric("Popularity", f"{popularity:,.0f}")
    with col3:
        st.metric("Albums", f"{number_of_albums:,.0f}")
    with col4:
        st.metric("Singles", f"{number_of_singles:,.0f}")
    with col5:
        st.metric("Tracks", f"{number_of_tracks:,.0f}")

    genres = cached_genres_artist(database, artist)
    st.markdown(f'Artist Genres: {', '.join(genres).title()}')

    st.divider()

    left, right = st.columns(2)
    with left:
        fig = cached_bar_top5_tracks_artist(database, artist)
        st.pyplot(fig)
    with right:
        fig = cached_bar_top5_albums_artist(database, artist)
        st.pyplot(fig)

    st.divider()

    selected_feature = st.selectbox('Select a Feature to Display:', features)

    feature_mean = cached_artist_features_mean(database, artist, selected_feature)
    feature_max = cached_artist_features_max(database, artist, selected_feature)
    feature_min = cached_artist_features_min(database, artist, selected_feature)
    feature_std = cached_artist_features_std(database, artist, selected_feature)

    st.markdown(f'Artist Feature Analysis: {selected_feature.title()}')
    left, right = st.columns([1, 1])
    with left:
        row1_col1, row1_col2 = st.columns(2)
        with row1_col1:
            st.metric("Mean", f"{feature_mean:.2f}")
        with row1_col2:
            st.metric("Standard Deviation", f"{feature_std:.2f}")
        row2_col1, row2_col2 = st.columns(2)
        with row2_col1:
            st.metric("Minimum", f"{feature_min:.2f}")
        with row2_col2:
            st.metric("Maximum", f"{feature_max:.2f}")

    with right:
        fig = cached_boxplot_feature_artist(database, artist, selected_feature)
        st.pyplot(fig)

# ---------- ALBUM PAGE ----------
elif page == 'Album':
    st.title("Album Analysis")
    name = st.sidebar.text_input('Enter an album name', 'reputation')
    matching_artists = alda.artists_for_album(database, name)
    if not matching_artists:
        st.warning("No album found with that name.")
        st.stop()

    selected_artist = st.sidebar.selectbox('Select the artist:', matching_artists)
    album_duration = alda.album_duration(database, name, selected_artist)
    label = alda.label(database, name, selected_artist)
    total_tracks = alda.total_tracks(database, name, selected_artist)
    release_date = alda.release_date(database, name, selected_artist)
    tracks,fig = aldv.album_tracks(database, name, selected_artist)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Album", name)
    with col2:
        st.metric("Label", label)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric( "Artist", selected_artist)
    with col2:
        st.metric("Album Duration", album_duration)
    with col3:
        st.metric("Total Tracks", total_tracks)
    with col4:
        st.metric("Release Date", release_date.strftime("%d-%m-%Y"))

    st.divider()

    left, right = st.columns([1, 1])
    with left:
        st.pyplot(fig)
    with right:
        df_pop, fig_pop = aldv.album_track_popularity(database, name, selected_artist)
        st.pyplot(fig_pop)

    st.divider()

    selected_feature = st.selectbox("Choose a feature", features)
    df = alda.album_feature(database, name, selected_artist, selected_feature)
    fig = alda.plot_album_feature(df, name, selected_artist, selected_feature)
    st.pyplot(fig)

    st.divider()

    left, right = st.columns(2)
    with left:
        featured_df = alda.album_featured_artist_counts(database, name, selected_artist)
        if not featured_df.empty:
            fig_featured = alda.plot_featured_artist_counts(featured_df, name, selected_artist)
            st.pyplot(fig_featured)
        else:
            st.write("No featured artists on this album.")
    with right:
        fig_explicit = alda.album_explicit_pie(database, name, selected_artist)
        if fig_explicit is not None:
            st.pyplot(fig_explicit)
        else:
            st.write("No explicit track data found for this album and artist.")