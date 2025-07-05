# Import Libraries 
import pandas as pd 
import sqlite3
import streamlit as st
from utils import fetch_poster, detail_id_movie
from streamlit_extras.switch_page_button import switch_page

@st.cache_data(ttl=86400)
def get_movie_by_title(title):
    conn = sqlite3.connect("movies.db")
    df = pd.read_sql("SELECT * FROM movies WHERE LOWER(title) = ?", conn, params=(title.lower(),))
    conn.close()
    return df

def display_movies():

    if "search_results" not in st.session_state:
        st.session_state.search_results = None
    if "movie_input" not in st.session_state:
        st.session_state.movie_input = ""

    st.title("🎬 Movies Application 🎬")

    movie_input = st.text_input("Type a Movie Name Here..", value=st.session_state.movie_input)

    if st.button("Search", key="searchbutton"):
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

        st.header("🔎 Search Results")
        movie_name = list(movie_df['title'])
        movie_poster = list(movie_df['poster_path'])
        movies_id = list(movie_df['id'])
        movies_data = [[x, y, z] for x, y, z in zip(movie_name, movie_poster, movies_id)]

        if len(movies_data) < 5:
            movies_data += [False] * (5 - len(movies_data))

        for i in range(0, len(movies_data), 5):
            cols = st.columns(5)
            for j in range(5):
                if (i + j < len(movies_data)) and (movies_data[i + j] is not False):
                    title = movies_data[i + j][0]
                    poster_url = fetch_poster(movies_data[i + j][1])
                    movie_id = movies_data[i + j][2]

                    with cols[j]:
                        st.image(poster_url, width=200)
                        st.markdown(f"**{i + j + 1} - {title}**")

                        if st.button("Show Details", key=f"detail_btn_{movie_id}"):
                            st.session_state.selected_movien = movie_id
                            detail_id_movie (movie_id)
                            st.switch_page("Details.py")  # or "pages/Details.py" if needed

        st.title("📽️ Recommended Movies")
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
    
    for i in range(0, len(clean_list), 5) : 
        cols = st.columns(5)
        for j in range (5) : 
            if i + j < len(clean_list) : 
                title = new_df.iloc[clean_list[i+j][0]].title 
                poster_url = fetch_poster(new_df.iloc[clean_list[i+j][0]].poster_path)
                movie_index_id = int(new_df.iloc[clean_list[i+j][0]].id)
                

                with cols[j] : 
                    st.image(poster_url, width=200)
                    st.markdown(f"**{title}**")

                    if  st.button(f"Show Details", key=f"detail_btn_{movie_index_id}") :      
                        st.session_state.selected_movien = movie_index_id
                        detail_id_movie (movie_index_id)
                        st.switch_page("Details.py")
                        st.rerun()

#Main_Program : 
display_movies()



    
