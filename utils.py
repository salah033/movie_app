import sqlite3
import pandas as pd 
import streamlit as st  
import os

global sel_movi_dt

def fetch_poster(poster_path):

    try:
        full_path = "https://image.tmdb.org/t/p/w500" + poster_path
        return full_path
    except:
        return "images.png"
    
def detail_id_movie (mov_id) : 
    global sel_movi_dt

    conn = sqlite3.connect("movies.db")
    df = pd.read_sql("SELECT * FROM movies WHERE id = ?", conn, params=(mov_id,))
    conn.close()

    selected_movie = df
    sel_movi_dt = selected_movie[['id', 'title', 'release_date', 'genres', 'director', 'cast', 'overview', 'poster_path']]
  
    return sel_movi_dt

@st.cache_data
def reload_csv_to_sqlite(csv_path, db_path, table_name="movies"):
    if not os.path.exists(db_path):
        df = pd.read_csv(csv_path)
        conn = sqlite3.connect(db_path)
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        conn.close()
        print("✅ Database created from CSV.")
    else:
        print("ℹ️ Database already exists — skipped reloading.")
            