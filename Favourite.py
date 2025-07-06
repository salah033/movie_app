import streamlit as st
from utils import detail_id_movie, fetch_poster
import pandas as pd

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
    .details-section {
        background: transparent;
        border-radius: 18px;
        box-shadow: none;
        padding: 0 0.5em 0.5em 0.5em;
        margin-bottom: 1em;
        text-align: center;
    }
    .details-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #333;
        margin: 0.5em 0 0.2em 0;
    }
    .details-label {
        color: #0099ff;
        font-weight: bold;
    }
    </style>
    <div class="main-title">🎬 Favourite Movies</div>
    """,
    unsafe_allow_html=True
)

def show_favourie ():

    if 'favorites' not in st.session_state:
        st.error("No favorite movies found. Please add some movies to your favorites first.")
    else : 
        new_df = pd.DataFrame()
        
        for index in st.session_state.favorites:

            x = detail_id_movie(index)
            new_df =pd.concat([x, new_df], ignore_index=True)

        movies_id = list(new_df['id'])
        movie_name = list(new_df['title'])
        movie_poster = list(new_df['poster_path'])
        
        fav_movies = [[x, y, z] for x, y, z in zip(movies_id, movie_name, movie_poster)]

         #Display the favorite movies
        if len(fav_movies) < 5:
            fav_movies += [False] * (5 - len(fav_movies))

        for i in range(0, len(fav_movies), 5):
            cols = st.columns(5)
            for j in range(5):
                if (i + j < len(fav_movies)) and (fav_movies[i + j] is not False):
                    fav_movie_id = fav_movies[i + j][0]
                    fav_movie_title = fav_movies[i + j][1]
                    fav_movie_poster_url = fetch_poster(fav_movies[i + j][2])

                    with cols[j]:
                        
                        with st.container():
                            st.markdown('<div class="movie-tile">', unsafe_allow_html=True)
                            st.image(fav_movie_poster_url, width=220)
                            st.markdown(f'<div class="movie-title">{i + j + 1} - {fav_movie_title}</div>', unsafe_allow_html=True)

                            details_btn = st.button("Show Details", key=f"detail_btn_{fav_movie_id}", use_container_width=True)
                            del_fav_btn = st.button("💔 Remove From Favorites", key=f"del_fav_btn{fav_movie_id}", use_container_width=True)

                            if details_btn:
                                st.session_state.selected_movien = fav_movie_id
                                detail_id_movie(fav_movie_id)
                                st.switch_page("Details.py")

                            
                            
                            if not st.session_state.favorites:
                                print("No favorite movies found. Please add some movies to your favorites first.")
                                
                            if del_fav_btn:
                                st.session_state.favorites.remove(fav_movie_id)
                                st.success(f"{fav_movie_title} removed from favorites!")
                                #st.rerun()

                            st.markdown('</div>', unsafe_allow_html=True)

# Call the function to display favorite movies
show_favourie()
