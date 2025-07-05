import streamlit as st
from utils import fetch_poster
import requests
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
    <div class="main-title">🎬 Movie Details</div>
    """,
    unsafe_allow_html=True
)

TMDB_API_KEY = st.secrets["api"]["TMDB_API_KEY"]

if 'selected_movien' in st.session_state:
    from utils import sel_movi_dt

    st.markdown(f'<div class="details-title">{sel_movi_dt["title"][0]}</div>', unsafe_allow_html=True)
    cols = st.columns(3)

    with cols[0]:
        st.image(fetch_poster(sel_movi_dt['poster_path'][0]), width=300)

    with cols[1]:
        st.markdown('<div class="details-title details-label">Staff</div>', unsafe_allow_html=True)
        st.markdown(f"🎬 <span class='details-label'>Director:</span> {sel_movi_dt['director'][0]}", unsafe_allow_html=True)
        st.markdown(f"🧑‍� <span class='details-label'>Cast:</span> {sel_movi_dt['cast'][0]}", unsafe_allow_html=True)

    with cols[2]:
        st.markdown('<div class="details-title details-label">Details</div>', unsafe_allow_html=True)
        st.markdown(f"� <span class='details-label'>Release Date:</span> {sel_movi_dt['release_date'][0]}", unsafe_allow_html=True)
        st.markdown(f"🎭 <span class='details-label'>Genres:</span> {sel_movi_dt['genres'][0]}", unsafe_allow_html=True)
        st.markdown('<div class="details-title details-label">Overview</div>', unsafe_allow_html=True)
        st.markdown(f"📝 <span class='details-label'>Overview:</span> {sel_movi_dt['overview'][0]}", unsafe_allow_html=True)

    url = f"https://api.themoviedb.org/3/movie/{sel_movi_dt['id'][0]}/videos?api_key={TMDB_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        st.markdown('<div class="details-title details-label">Trailers</div>', unsafe_allow_html=True)
        if not (data['results']):
            st.info("No trailer found.")
        else:
            for video in data['results']:
                if video['type'] == 'Trailer' and video['site'] == 'YouTube':
                    trailer_url = f"https://www.youtube.com/watch?v={video['key']}"
                    st.video(trailer_url)
    else:
        st.warning("Connection Error")

else:
    st.warning("No movie selected.")