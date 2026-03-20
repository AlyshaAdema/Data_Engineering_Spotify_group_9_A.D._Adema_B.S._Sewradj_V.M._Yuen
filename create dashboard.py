import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sqlite3
import artist_data_analysis as arda
import artist_data_visualization as ardv
import album_data_analysis as alda
import album_data_visualization as aldv
import full_database_analysis as fda
import full_database_visualization as fdv

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
genres = ['pop', 'hiphop', 'rap', 'rock']

if page == 'Opening page':
    st.title("Opening page")
    selected_eras = st.sidebar.multiselect('Select Era(s) to Display:', eras, default=eras)
    total_artists = arda.unique_artists(database, selected_eras)
    total_albums = alda.unique_albums(database, selected_eras)
    total_tracks = alda.unique_tracks(database, selected_eras)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Artists", f"{total_artists:,.0f}")
    with col2:
        st.metric("Total Albums", f"{total_albums:,.0f}")
    with col3:
        st.metric("Total Tracks", f"{total_tracks:,.0f}")

    st.divider()

    fig = fdv.line_chart_track_popularity(database, selected_eras)
    st.pyplot(fig)

    st.divider()

    left, right = st.columns(2)
    with left:
        fig = ardv.top10_followers(database, selected_eras)
        st.pyplot(fig)
    with right:
        fig = ardv.linear_regression(database, selected_eras)
        st.pyplot(fig)

    st.divider()

    left, right = st.columns(2)
    with left:
        fig = fdv.pie_chart_tracks(database, selected_eras)
        st.pyplot(fig)
    with right:
        fig = fdv.pie_chart_explicit_vs_nonexplicit(database, selected_eras)
        st.pyplot(fig)

elif page =='Features':
    st.title("Features")
    selected_feature = st.sidebar.selectbox('Select a Feature to Display:', features)

elif page == 'Genres':
    st.title('Genres')
    selected_genre = st.sidebar.selectbox('Select a Genre to Display:', genres)

elif page == 'Artist':
    st.title("Artists")
    name = st.sidebar.text_input('Enter an artist name', 'Taylor Swift')
    feature = st.sidebar.selectbox('Select a Feature to Display:', features)
    number_followers = arda.number_followers_artist(database, name)
    popularity = arda.popularity_artist(database, name)
    number_of_albums = fda.number_albums_artist(database, name)
    number_of_singles = fda.number_singles_artist(database, name)
    number_of_tracks = fda.number_tracks_artist(database, name)
    feature_mean = fda.artist_features(database, name, feature, 'mean')
    feature_median = fda.artist_features(database, name, feature, 'median')
    feature_max = fda.artist_features(database, name, feature, 'max')
    feature_min = fda.artist_features(database, name, feature, 'min')
    feature_std = fda.artist_features(database, name, feature, 'std')
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
        fig = fdv.bar_plot_top_5_tracks_artist(database, name)
        st.pyplot(fig)
    with right:
        fig = fdv.bar_plot_top_5_albums(database, name)
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
        fig = fdv.box_plot_feature_artist(database, name, feature)
        st.pyplot(fig)

elif page == 'Album':
    st.title("Albums")
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
        featured_df = alda.album_featured_artist_counts(database, name, selected_artist)
        if not featured_df.empty:
            fig_featured = alda.plot_featured_artist_counts(featured_df, name, selected_artist)
            st.pyplot(fig_featured)
        else:
            st.write("No featured artists on this album.")

    st.divider()

    selected_feature = st.selectbox("Choose a feature", features)
    df = alda.album_feature(database, name, selected_artist, selected_feature)
    fig = alda.plot_album_feature(df, name, selected_artist, selected_feature)
    st.pyplot(fig)

    st.divider()

    left, right = st.columns(2)
    with left:
        fig_explicit = alda.album_explicit_pie(database, name, selected_artist)
        if fig_explicit is not None:
            st.pyplot(fig_explicit)
        else:
            st.write("No explicit track data found for this album and artist.")
    with right:
        df_pop, fig_pop = aldv.album_track_popularity(database, name, selected_artist)
        st.pyplot(fig_pop)