# Import Libraries 
import pandas as pd 
import sqlite3
import streamlit as st
from utils import fetch_poster, check_favorite_movie, add_favorite_movie, add_visited_movie, get_last_visited

#Load File 
#conn = sqlite3.connect("/home/salah/Documents/Python lessons/movie/my_prg/movies.db")
#df = pd.read_sql("SELECT * FROM movies", conn)
#conn.close()
@st.cache_data(ttl=86400)
def get_movie_by_title(title):
    conn = sqlite3.connect("movies.db")
    df = pd.read_sql("SELECT * FROM movies WHERE LOWER(title) = ?", conn, params=(title.lower(),))
    conn.close()
    return df

#Display found movies
def display_movies():

    if "search_results" not in st.session_state:
        st.session_state.search_results = None
    if "movie_input" not in st.session_state:
        st.session_state.movie_input = ""

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
        .search-box {
            display: flex;
            justify-content: center;
            margin-bottom: 2em;
        }
        .stTextInput>div>div>input {
            font-size: 1.2rem;
            padding: 0.5em;
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
        .rec-title {
            color: #0099ff;
            font-size: 2rem;
            font-weight: bold;
            margin-top: 2em;
        }
        </style>
        <div class="main-title">🎬 Movies Application 🎬</div>
        """,
        unsafe_allow_html=True
    )

    # Centered search box
    st.markdown('<div class="search-box">', unsafe_allow_html=True)
    movie_input = st.text_input("Type a Movie Name Here..", value=st.session_state.movie_input, key="movie_input_box")
    st.markdown('</div>', unsafe_allow_html=True)

    search_col, _ = st.columns([1, 5])
    with search_col:
        search_clicked = st.button("🔍 Search", key="searchbutton", use_container_width=True)

    if search_clicked:
        st.session_state.movie_input = movie_input.strip().lower()
        movie_df = get_movie_by_title(st.session_state.movie_input)

        if movie_df.empty:
            st.session_state.search_results = "not_found"
        else:
            st.session_state.search_results = movie_df

    if isinstance(st.session_state.search_results, str) and st.session_state.search_results == "not_found":
        st.error(f"❌ Movie '{st.session_state.movie_input}' not found.")
    elif isinstance(st.session_state.search_results, pd.DataFrame):
        movie_df = st.session_state.search_results

        st.markdown('<div class="rec-title">🔎 Search Results</div>', unsafe_allow_html=True)
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

        #movies_data = [[x, y, z] for x, y, z in zip(movie_name, movie_poster, movies_id)]

        # Fill empty slots for layout
        if len(movie_names) < 5:
            movie_names += [False] * (5 - len(movie_names))

        for i in range(0, len(movie_names), 5):
            cols = st.columns(5)
            for j in range(5):
                if (i + j < len(movie_names)) and (movie_names[i + j] is not False):
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

                            details_btn = st.button("Show Details", key=f"detail_btn_{movie_id}", use_container_width=True)
                            fav_btn = st.button("♥️ Add to Favorites", key=f"fav_btn_{movie_id}", use_container_width=True)

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

                                #st.session_state.selected_movien = movie_id
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

        # Recommended section
        st.markdown('<div class="rec-title">📽️ Similar Movies</div>', unsafe_allow_html=True)
        recommended_movies(movie_df)

#Funtction Recommended_movies: 
def recommended_movies(movies_df) : 
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    conn = sqlite3.connect("movies.db")
    df = pd.read_sql("SELECT * FROM movies WHERE vote_average > 7", conn)
    conn.close()

    movies = df.sort_values(by='vote_average', ascending=False)
    movies = movies.head(5000)
    movies = pd.concat([movies_df, movies], ignore_index=True)
    movies['overview'] = movies['overview'].fillna('NoData')
    movies['tagline'] = movies['tagline'].fillna('NoData')
    movies['genres'] = movies['genres'].fillna('NoData')
    movies['cast'] = movies['cast'].fillna('NoData')
    movies['director'] = movies['director'].fillna('NoData')
    movies['writers'] = movies['writers'].fillna('NoData')
    movies['release_date'] = movies['release_date'].fillna('NoData')

    movies['tags'] = movies['overview'] + " " + movies['tagline'] + " " + movies['genres'] + " " + movies['cast'] + " " + movies['director'] + " " + movies['writers']

    id_list = list(movies_df['id'])
    
    new_df = movies[['id', 'title', 'tags', 'poster_path']]

    seen = set()
    rows_to_keep = []

    for index, row in new_df.iterrows():
        current_id = row['id']
        if current_id in id_list:
            if current_id not in seen:
                seen.add(current_id)
                rows_to_keep.append(index)
        else:
            rows_to_keep.append(index)
    
    new_df = new_df.loc[rows_to_keep].reset_index(drop=True)
    
    cv = CountVectorizer(max_features=1000, stop_words='english')
    vectors = cv.fit_transform(new_df['tags']).toarray()
    similarity = cosine_similarity(vectors)

    simular_movies = []

    for i in range (len(movies_df)) : 

        distances = list(enumerate(similarity[i]))
        y = sorted(distances, key=lambda x: x[1], reverse=True)[1:6]
        simular_movies.append(y)
    
    sorted_l = []
    
    for i in simular_movies : 
        for j in i :
            sorted_l.append(j)

    sorted_l = sorted(sorted_l, key=lambda x: x[1], reverse=True)
    
    seen = set() 
    clean_list = [] 

    for item in sorted_l:
        if item[0] not in seen:
            clean_list.append(item)
            seen.add(item[0])
    
    for i in range(0, len(clean_list), 5):
        cols = st.columns(5)
        for j in range(5):
            if i + j < len(clean_list):
                try : 
                    title = new_df.iloc[clean_list[i+j][0]].title
                    poster_url = fetch_poster(new_df.iloc[clean_list[i+j][0]].poster_path)
                    movie_index_id = int(new_df.iloc[clean_list[i+j][0]].id)
                    movie_overview = (movies.iloc[clean_list[i+j][0]].overview)
                    movie_director = movies.iloc[clean_list[i+j][0]].director
                    movie_cast = movies.iloc[clean_list[i+j][0]].cast
                    movie_release_date = movies.iloc[clean_list[i+j][0]].release_date
                    movie_genres = movies.iloc[clean_list[i+j][0]].genres
                    movie_tagline = movies.iloc[clean_list[i+j][0]].tagline
                    movie_writers = movies.iloc[clean_list[i+j][0]].writers
                except TypeError as e:
                        print (f"Error processing movie data: {e}")

                with cols[j]:
                    with st.container():
                        st.markdown('<div class="movie-tile">', unsafe_allow_html=True)
                        st.image(poster_url, width=220)
                        st.markdown(f'<div class="movie-title">{title}</div>', unsafe_allow_html=True)

                        details_btn = st.button("Show Details", key=f"detail_btn_{movie_index_id}_rec", use_container_width=True)
                        fav_btn = st.button("♥️ Add to Favorites", key=f"fav_btn_{movie_index_id}_rec", use_container_width=True)

                        movie_data = {
                                    'id': movie_index_id,
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

#Main_Program : 

display_movies()



    
