import streamlit as st
from utils import fetch_poster, check_favorite_movie_2, remove_favorite_movie, add_visited_movie, get_last_visited
import json
import time

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

    if not check_favorite_movie_2():
        st.error("No favorite movies found. Please add some movies to your favorites first.")
    else : 
        path = "favorites.json"
        with open(path, "r") as f:
            data = json.load(f)
        
        fav_list = data.get("favourite", [])

        movies_id = []
        movie_name = []
        movie_poster = []
        movies_overview = []
        movies_director = []
        movies_cast = []
        movies_release_date = []
        movies_genres = []
        movies_tagline = []
        movies_writers = []

        for index in fav_list :
            #x = detail_id_movie(index)
            #new_df =pd.concat([x, new_df], ignore_index=True)

            movies_id.append(index['id'])
            movie_name.append(index['title'])
            movie_poster.append(index['poster_path'])
            movies_overview.append(index['overview'])
            movies_director.append(index['director'])
            movies_cast.append(index['cast'])
            movies_release_date.append(index['release_date'])
            movies_genres.append(index['genres'])
            movies_tagline.append(index['tagline'])
            movies_writers.append(index['writers'])
        
        #fav_movies = [[x, y, z] for x, y, z in zip(movies_id, movie_name, movie_poster)]
        
         #Display the favorite movies
        if len(movies_id) < 5:
            movies_id += [False] * (5 - len(movies_id))

        for i in range(0, len(movies_id), 5):
            cols = st.columns(5)
            for j in range(5):
                if (i + j < len(movies_id)) and (movies_id[i + j] is not False):
                    try : 
                        movie_id = movies_id[i + j]
                        movie_title = movie_name[i + j]
                        movie_poster_url = fetch_poster(movie_poster[i + j])
                        movie_overview = movies_overview[i + j]
                        movie_director = movies_director[i + j]
                        movie_cast = movies_cast[i + j]
                        movie_release_date = movies_release_date[i + j]
                        movie_genres = movies_genres[i + j]
                        movie_tagline = movies_tagline[i + j]
                        movie_writers = movies_writers[i + j]
                    except TypeError as e:
                        print (f"Error processing movie data: {e}")

                    with cols[j]:
                        
                        with st.container():
                            st.markdown('<div class="movie-tile">', unsafe_allow_html=True)
                            st.image(movie_poster_url, width=220)
                            st.markdown(f'<div class="movie-title">{i + j + 1} - {movie_title}</div>', unsafe_allow_html=True)

                            details_btn = st.button("Show Details", key=f"detail_btn_{movie_id}", use_container_width=True)
                            del_fav_btn = st.button("💔 Remove From Favorites", key=f"del_fav_btn{movie_id}", use_container_width=True)

                            movie_data = {
                                    'id': movie_id,
                                    'title': movie_title,
                                    'poster_path': movie_poster_url,
                                    'overview': movie_overview,
                                    'director': movie_director,
                                    'cast': movie_cast,
                                    'release_date': movie_release_date,
                                    'genres': movie_genres,
                                    'tagline': movie_tagline,
                                    'writers': movie_writers
                                }
                            
                            if details_btn:
                                add_visited_movie(movie_data)
                                get_last_visited(movie_data)
                                st.switch_page("Details.py")
                                st.rerun()
                                
                            if del_fav_btn:
                                remove_favorite_movie(movie_id)
                                st.success(f"{movie_title} removed from favorites!")
                                time.sleep(2)
                                st.rerun()
                                

                            st.markdown('</div>', unsafe_allow_html=True)

# Call the function to display favorite movies
show_favourie()
