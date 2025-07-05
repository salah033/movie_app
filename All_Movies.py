import streamlit as st
import sqlite3
import pandas as pd 
from utils import fetch_poster, detail_id_movie
from streamlit_extras.switch_page_button import switch_page # type: ignore

if 'movie_limit' not in st.session_state:
    st.session_state.movie_limit = 50

@st.cache_data(ttl=86400)
def get_movie(limit=50):
    conn = sqlite3.connect("movies.db")
    df = pd.read_sql(f"SELECT * FROM movies LIMIT {limit}", conn)
    conn.close()
    return df

def show_movies() :

    col1, col2, col3 = st.columns([1, 1, 1])
    page_title = " Movies " 
    with col2 : 
        st.title(f"{page_title}")
        st.title (" ")
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
                    st.image(poster_url, width=200)
                    st.markdown(f"**{i + j + 1} - {title}**")
                    
                    if  st.button(f"Show Details", key=movie_id) :                   
                        st.session_state.selected_movien = movie_id
                        detail_id_movie (movie_id)
                        st.switch_page("Details.py")
                        st.rerun()
                        
                        
    if st.button("🔁 Show More", key="show_more"):
        st.session_state.movie_limit += 50
        st.rerun()

show_movies()




