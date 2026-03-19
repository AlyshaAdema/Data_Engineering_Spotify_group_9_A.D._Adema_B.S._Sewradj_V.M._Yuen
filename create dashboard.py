import streamlit as st
import sqlite3

# importing own files
import artist_data_analysis as arda
import artist_data_visualization as ardv
import album_data_analysis as alda
import full_database_analysis as flda
import full_database_visualization as fldv
import features_data_analysis as fda
import features_data_visualization as fdv

st.set_page_config(
    page_title="Opening page",
    page_icon="start",
    layout="wide",
    initial_sidebar_state="expanded"
)

database = sqlite3.connect('spotify_database.db')
page = st.sidebar.radio('Navigation', ['Opening page', 'Features', 'Genres', 'Artist', 'Album'])
eras = ['1900s','1930s','1940s','1950s','1960s','1970s','1980s','1990s','2000s','2010s','2020s']
features = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms']
genres = arda.all_genres(database)

if page == 'Opening page':
    st.title("Opening page")
    selected_eras = st.sidebar.multiselect('Select Era(s) to Display:', eras, default=eras)
    total_artists = arda.unique_artists(database, selected_eras)
    total_albums = alda.unique_albums(database, selected_eras)
    total_tracks = alda.unique_tracks(database, selected_eras)
    total_genres = arda.number_of_genres(database, selected_eras)
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

    fig = fldv.line_chart_track_popularity(database, selected_eras)
    st.pyplot(fig)

    st.divider()

    left, right = st.columns(2)
    with left:
        chart_type = st.selectbox("Select metric to display for top artists:", ("Followers", "Popularity"))
        if chart_type == "Followers":
            fig = ardv.top10_followers(database, selected_eras)
        else:
            fig = ardv.top10_popularity(database, selected_eras)
        st.pyplot(fig)
    with right:
        fig = ardv.linear_regression(database, selected_eras)
        st.pyplot(fig)

    st.divider()

    left, right = st.columns(2)
    with left:
        fig = fldv.pie_chart_tracks(database, selected_eras)
        st.pyplot(fig)
    with right:
        fig = fldv.pie_chart_explicit_vs_nonexplicit(database, selected_eras)
        st.pyplot(fig)

elif page =='Features':
    st.title("Features")
    selected_feature = st.sidebar.selectbox('Select a main Feature to display:', features)
    compare_feature_list = [feature for feature in features if feature != selected_feature]
    selected_eras = st.sidebar.multiselect('Select Era(s) to Display:', eras, default=eras)
    mean_feature = fda.feature_stats(database, selected_feature, selected_eras, 'mean')
    min_feature = fda.feature_stats(database, selected_feature, selected_eras, 'min')
    max_feature = fda.feature_stats(database, selected_feature, selected_eras, 'max')
    std_feature = fda.feature_stats(database, selected_feature, selected_eras, 'std')
    correlation_feature0 = fda.feature_correlation(database, selected_feature, compare_feature_list[0], selected_eras)
    correlation_feature1 = fda.feature_correlation(database, selected_feature, compare_feature_list[1], selected_eras)
    correlation_feature2 = fda.feature_correlation(database, selected_feature, compare_feature_list[2], selected_eras)
    correlation_feature3 = fda.feature_correlation(database, selected_feature, compare_feature_list[3], selected_eras)
    correlation_feature4 = fda.feature_correlation(database, selected_feature, compare_feature_list[4], selected_eras)
    correlation_feature5 = fda.feature_correlation(database, selected_feature, compare_feature_list[5], selected_eras)
    correlation_feature6 = fda.feature_correlation(database, selected_feature, compare_feature_list[6], selected_eras)
    correlation_feature7 = fda.feature_correlation(database, selected_feature, compare_feature_list[7], selected_eras)
    correlation_feature8 = fda.feature_correlation(database, selected_feature, compare_feature_list[8], selected_eras)
    st.markdown(f'Displayed feature: {selected_feature}')

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
        fig = fdv.line_chart_features_eras(database, selected_feature, selected_eras)
        st.pyplot(fig)
    with right:
        fig = fdv.boxplot_feature(database, selected_feature, selected_eras)
        st.pyplot(fig)

    st.divider()

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric(f"Correlation {compare_feature_list[0]} ", f"{correlation_feature0:,.2f}")
        st.metric(f"Correlation {compare_feature_list[1]} ", f"{correlation_feature1:,.2f}")
    with col2:
        st.metric(f"Correlation {compare_feature_list[2]} ", f"{correlation_feature2:,.2f}")
        st.metric(f"Correlation {compare_feature_list[3]} ", f"{correlation_feature3:,.2f}")
    with col3:
        st.metric(f"Correlation {compare_feature_list[4]} ", f"{correlation_feature4:,.2f}")
        st.metric(f"Correlation {compare_feature_list[5]} ", f"{correlation_feature5:,.2f}")
    with col4:
        st.metric(f"Correlation {compare_feature_list[6]} ", f"{correlation_feature6:,.2f}")
        st.metric(f"Correlation {compare_feature_list[7]} ", f"{correlation_feature7:,.2f}")
    with col5:
        st.metric(f"Correlation {compare_feature_list[8]} ", f"{correlation_feature8:,.2f}")

elif page == 'Genres':
    st.title('Genres')
    selected_genre = st.sidebar.selectbox('Select a Genre to Display:', genres)
    total_artists = arda.artists_per_genre(database, selected_genre)
    average_popularity = arda.average_popularity_per_genre(database, selected_genre)
    total_followers = arda.total_followers_per_genre(database, selected_genre)
    average_followers = arda.average_followers_per_genre(database, selected_genre)
    st.markdown(f'Displayed Genre: {selected_genre}')
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
            fig = ardv.top10_followers_genre(database, selected_genre)
        elif chart_type == "Popularity":
            fig = ardv.top10_popularity_genre(database, selected_genre)
        st.pyplot(fig)
    with right:
        if chart_type == "Followers":
            fig = ardv.followers_distribution_genres(database, selected_genre)
        elif chart_type == "Popularity":
            fig = ardv.popularity_distribution_genres(database, selected_genre)
        st.pyplot(fig)

    st.divider()
    fig = ardv.bar_plot_top_genre_combination(database, selected_genre)
    st.pyplot(fig)

elif page == 'Artist':
    st.title("Artists")
    name = st.sidebar.text_input('Enter an artist name', 'Taylor Swift')
    feature = st.sidebar.selectbox('Select a Feature to Display:', features)
    number_followers = arda.number_followers_artist(database, name)
    popularity = arda.popularity_artist(database, name)
    number_of_albums = flda.number_albums_artist(database, name)
    number_of_singles = flda.number_singles_artist(database, name)
    number_of_tracks = flda.number_tracks_artist(database, name)
    feature_mean = flda.artist_features(database, name, feature, 'mean')
    feature_max = flda.artist_features(database, name, feature, 'max')
    feature_min = flda.artist_features(database, name, feature, 'min')
    feature_std = flda.artist_features(database, name, feature, 'std')
    st.markdown(f'Displayed Artist: {name}')
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
    genres = arda.genres_artist(database, name)
    st.markdown(f'Artist Genres: {', '.join(genres)}')

    st.divider()

    left, right = st.columns(2)
    with left:
        fig = fldv.bar_plot_top_5_tracks_artist(database, name)
        st.pyplot(fig)
    with right:
        fig = fldv.bar_plot_top_5_albums(database, name)
        st.pyplot(fig)

    st.divider()

    st.markdown(f'Artist Feature Analysis: {feature}')
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
        fig = fldv.box_plot_feature_artist(database, name, feature)
        st.pyplot(fig)

elif page == 'Album':
    st.title("Albums")
    name = st.sidebar.text_input('Enter an album name', 'reputation')