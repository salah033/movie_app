import streamlit as st
import sqlite3
import pandas as pd 
from utils import fetch_poster, detail_id_movie
from streamlit_extras.switch_page_button import switch_page 

if 'movie_limit' not in st.session_state:
    st.session_state.movie_limit = 50

@st.cache_data(ttl=86400)
def get_movie(limit=50):
    conn = sqlite3.connect("movies.db")
    df = pd.read_sql(f"SELECT * FROM movies LIMIT {limit}", conn)
    conn.close()
    return df

def show_movies() :


    st.markdown(
        """
        <style>
        .main-title {
            font-size: 3rem;
            font-weight: bold;
            color: #FF4B4B;
            text-align: center;
            margin-bottom: 0.5em;
        }
        .movie-tile {
            background: transparent;
            border-radius: 18px;
            box-shadow: none;
            padding: 0 0.5em 0.5em 0.5em;
            margin-bottom: 1em;
            text-align: center;
        }
        .movie-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: #333;
            margin: 0.5em 0 0.2em 0;
        }
        .fav-btn, .details-btn {
            width: 100%;
            margin-top: 0.5em;
        }
        </style>
        <div class="main-title">🎬 Movie Gallery</div>
        """,
        unsafe_allow_html=True
    )

    movie_df = get_movie(limit=st.session_state.movie_limit)
    movie_names = list(movie_df['title'])
    poster_paths = list(movie_df['poster_path'])
    movies_id = list(movie_df['id'])

    for i in range(0, len(movie_names), 5):
        cols = st.columns(5)
        for j in range(5):
            if i + j < len(movie_names):
                title = movie_names[i + j]
                poster_url = fetch_poster(poster_paths[i + j])
                movie_id = movies_id[i + j]

                with cols[j]:
                    with st.container():
                        st.markdown('<div class="movie-tile">', unsafe_allow_html=True)
                        st.image(poster_url, width=220)
                        st.markdown(f'<div class="movie-title">{i + j + 1} - {title}</div>', unsafe_allow_html=True)

                        details_btn = st.button("Show Details", key=f"detail_btn_{movie_id}_all", use_container_width=True)
                        fav_btn = st.button("♥️ Add to Favorites", key=f"fav_btn_{movie_id}_all", use_container_width=True)

                        if details_btn:
                            st.session_state.selected_movien = movie_id
                            detail_id_movie(movie_id)
                            st.switch_page("Details.py")
                            st.rerun()

                        if fav_btn:
                            if 'favorites' not in st.session_state:
                                st.session_state.favorites = []
                            if movie_id not in st.session_state.favorites:
                                st.session_state.favorites.append(movie_id)
                                st.success(f"{title} added to favorites!")
                            else:
                                st.warning(f"{title} is already in your favorites.")
                        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔁 Show More", key="show_more"):
        st.session_state.movie_limit += 50
        st.rerun()

show_movies()




