import streamlit as st
from utils import fetch_poster
import requests
import time

TMDB_API_KEY = st.secrets["api"]["TMDB_API_KEY"]

if 'selected_movien' in st.session_state:
    from utils import sel_movi_dt
    

    st.title(sel_movi_dt['title'][0])
    
    for i in range(3) : 
        cols = st.columns(3)
    
    with cols [0] : 
        
        st.image(fetch_poster(sel_movi_dt['poster_path'][0]), width=350)
        
        
    with cols [2] : 

        original_title = '<p style="font-family:Helvetica; color:Yellow; font-size: 60px;">Details</p>'
        st.markdown(original_title, unsafe_allow_html=True)
        
        st.markdown(f"📅 **Release Date:** {sel_movi_dt['release_date'][0]}")
        st.markdown(f"🎭 **Genres:** {sel_movi_dt['genres'][0]}")

        original_title = '<p style="font-family:Helvetica; color:Yellow; font-size: 60px;">Overview</p>'
        st.markdown(original_title, unsafe_allow_html=True)
        st.markdown(f"📝 **Overview:**\n\n{sel_movi_dt['overview'][0]}")
    with cols [1] : 

        original_title = '<p style="font-family:Helvetica; color:Yellow; font-size: 60px;">Staff</p>'
        st.markdown(original_title, unsafe_allow_html=True)

        st.markdown(f"🎬 **Director:** {sel_movi_dt['director'][0]}")
        st.markdown(f"🧑‍🎤 **Cast:** {sel_movi_dt['cast'][0]}")

    url = f"https://api.themoviedb.org/3/movie/{sel_movi_dt['id'][0]}/videos?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        
        data = response.json()
        if not (data['results']) : 
            original_title = '<p style="font-family:Helvetica; color:Yellow; font-size: 60px;">Trailers</p>'
            st.markdown(f"{original_title}", unsafe_allow_html=True)
            st.info("No trailer found.")
        else : 
            original_title = '<p style="font-family:Helvetica; color:Yellow; font-size: 60px;">Trailers</p>'
            st.markdown(f"{original_title}", unsafe_allow_html=True)
        
        for video in data['results']:
            if video['type'] == 'Trailer' and video['site'] == 'YouTube':
                trailer_url = f"https://www.youtube.com/watch?v={video['key']}"
                st.video(trailer_url)
                
                
                
            #elif not data['results']: 
                #print ("OKBB")
                #original_title = '<p style="font-family:Helvetica; color:Yellow; font-size: 60px;">Trailer</p>'
                #st.markdown(original_title, unsafe_allow_html=True)
                #st.info("No trailer found.")
    else : 
        st.warning("Connection Error")

else:
    st.warning("No movie selected.")