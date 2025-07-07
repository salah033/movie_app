import sqlite3
import pandas as pd 
import streamlit as st  
import os
import json
global last_movie

def fetch_poster(poster_path):

    try:
        full_path = "https://image.tmdb.org/t/p/w500" + poster_path
        return full_path
    except:
        return "images.png"
    
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

#create js file for data
def init_favorites_file(path):
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump({"favourite": [], "visited": []}, f, indent=4)

# Function to add favorites from JSON file   
def add_favorite_movie(movie, path="favorites.json"):

    if not os.path.exists(path) or os.stat(path).st_size == 0:
        with open(path, "w") as f:
            json.dump({"favourite": [], "visited": []}, f, indent=4)

    with open(path, "r") as f:
        data = json.load(f)

    fav_list = data.get("favourite", [])

    if not any(fav.get("id") == movie['id'] for fav in fav_list):
        fav_list.append(movie)
        data["favourite"] = fav_list

        with open(path, "w") as f:
            json.dump(data, f, indent=4)

#Function to check if favorites from JSON file
def check_favorite_movie(movie, path="favorites.json"):
    if not os.path.exists(path) or os.stat(path).st_size == 0:
        with open(path, "w") as f:
            json.dump({"favourite": [], "visited": []}, f, indent=4)
            return True

    with open(path, "r") as f:
        data = json.load(f)

    fav_list = data.get("favourite", [])
    if any(fav.get("id") == movie['id'] for fav in fav_list):
        return False
    else:
        return True
    
# Function to check if favorites from JSON file
def check_favorite_movie_2(path="favorites.json"):
    if not os.path.exists(path) or os.stat(path).st_size == 0:
        print ("FALSE_1")
        return False
    
    with open(path, "r") as f:
        data = json.load(f)

    fav_list = data.get("favourite", [])
    if not fav_list:
        print ("FALSE_2")
        return False
    else:
        return True
    
# Function to remove a movie from favorites
def remove_favorite_movie(movie_id, path="favorites.json"):
    # Load data
    with open(path, "r") as f:
        data = json.load(f)

    fav_list = data.get("favourite", [])

    # Filter out the movie with the matching ID
    new_fav_list = [movie for movie in fav_list if movie.get("id") != movie_id]

    # Save updated list
    data["favourite"] = new_fav_list

    with open(path, "w") as f:
        json.dump(data, f, indent=4)

# Function to add a movie to the visited list
def add_visited_movie(movie, path="favorites.json"):

    if not os.path.exists(path) or os.stat(path).st_size == 0:
        with open(path, "w") as f:
            json.dump({"favourite": [], "visited": []}, f, indent=4)
            
    with open(path, "r") as f:
        data = json.load(f)

    vis_list = data.get("visited", [])

    if not any(vis.get("id") == movie['id'] for vis in vis_list):
        vis_list.append(movie)
        data["visited"] = vis_list
        print ("ADDED TO VISITED")

        with open(path, "w") as f:
            json.dump(data, f, indent=4)
                
# Function to get the last favorite movie
def get_last_visited(movie, path="favorites.json"):
    global last_movie
    if not os.path.exists(path) or os.stat(path).st_size == 0:
        print ("FALSE_1")
        last_movie = False
    
    with open(path, "r") as f:
        data = json.load(f)

    mov_list = data.get("visited", [])

    if mov_list:
        if any(vis.get("id") == movie['id'] for vis in mov_list):
            last_movie = movie
        else : 
            last_movie = mov_list[-1]
    else:
        last_movie = False
    

