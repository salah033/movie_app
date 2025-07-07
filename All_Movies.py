import streamlit as st
import sqlite3
import pandas as pd 
from utils import fetch_poster, add_favorite_movie,check_favorite_movie, add_visited_movie, get_last_visited

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
    movies_director = list(movie_df['director'])
    movies_cast = list(movie_df['cast'])    
    movies_release_date = list(movie_df['release_date'])
    movies_genres = list(movie_df['genres'])    
    movies_tagline = list(movie_df['tagline'])    
    movies_writers = list(movie_df['writers'])
    movies_overview = list(movie_df['overview'])    
  
    for i in range(0, len(movie_names), 5):
        cols = st.columns(5)
        for j in range(5):
            if i + j < len(movie_names):
                try : 
                    title = movie_names[i + j]
                    poster_url = fetch_poster(poster_paths[i + j])
                    movie_id = movies_id[i + j]
                    movie_director = movies_director[i + j]
                    movie_cast = movies_cast[i + j]
                    movie_release_date = movies_release_date[i + j]
                    movie_genres = movies_genres[i + j]
                    movie_tagline = movies_tagline[i + j]
                    movie_writers = movies_writers[i + j]
                    movie_overview = movies_overview[i + j]
                except TypeError as e:
                        print (f"Error processing movie data: {e}")

                with cols[j]:
                    with st.container():
                        st.markdown('<div class="movie-tile">', unsafe_allow_html=True)
                        st.image(poster_url, width=220)
                        st.markdown(f'<div class="movie-title">{i + j + 1} - {title}</div>', unsafe_allow_html=True)

                        details_btn = st.button("Show Details", key=f"detail_btn_{movie_id}_all", use_container_width=True)
                        fav_btn = st.button("♥️ Add to Favorites", key=f"fav_btn_{movie_id}_all", use_container_width=True)

                        movie_data = {
                                    'id': movie_id,
                                    'title': title,
                                    'poster_path': poster_url,
                                    'overview': movie_overview,
                                    'director': movie_director,
                                    'cast': movie_cast,
                                    'release_date': movie_release_date,
                                    'genres': movie_genres,
                                    'tagline': movie_tagline,
                                    'writers': movie_writers
                                }
                        
                        if details_btn:
                            #st.session_state.selected_movien = movie_data
                            add_visited_movie(movie_data)
                            get_last_visited(movie_data)
                            st.switch_page("Details.py")
                            st.rerun()

                        if fav_btn:
                            
                            if check_favorite_movie(movie_data) : 
                                add_favorite_movie(movie_data)
                                print ("ADDED TO FAVORITES")
                                st.success(f"{title} added to favorites!")
                            else:
                                st.warning(f"{title} is already in your favorites.")
                                print("MOVIE ALDREADY IN FAVORITES")
                        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔁 Show More", key="show_more"):
        st.session_state.movie_limit += 50
        st.rerun()

show_movies()




