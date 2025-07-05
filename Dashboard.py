import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import time
import ast


st.title("📊 Movie Analytics Dashboard")

# Load data from DB
@st.cache_data(ttl=86400)
def load_movies() :

    with st.spinner("Fetching movies from database..."):
        time.sleep(3)
        conn = sqlite3.connect("movies.db")
        df = pd.read_sql(f"SELECT * FROM movies", conn)
        conn.close()
    return df

#def extract_genres(gstr) (NO NEED BECAUSE DATA ALREADY NO NEED TO CONVERT):
    try:
        genres = ast.literal_eval(gstr)
        return [g['name'] for g in genres if 'name' in g]
    except:
        return []
    

# Convert genre string to list
df = load_movies()
df = df.dropna()

###GENRES### 

list_genres = list(df['genres'])

ids = list(df['id'])
genres = [item.split() for item in list_genres]

genres = [[g.strip().strip(',') for g in sublist] for sublist in genres]

genre_df = pd.DataFrame({
    'ID': ids,
    'genres': genres,
})

all_genres = genre_df.explode(['genres'])

genre_counts = all_genres['genres'].value_counts()
genre_dict = genre_counts.head(10).to_dict()

for i in range (2) : 
    cols = st.columns(2)
    
with cols[0] : 
    st.title("TOP 10 GENRES : ")  
    for genre, count in genre_dict.items():
        st.markdown(f"**{genre}:** {count}")
with cols[0] : 
    for i in range (20) : 
        st.markdown(" ")

with cols[1] : 
    fig, ax = plt.subplots()
    genre_counts.head(10).plot(kind='bar', ax=ax)
    ax.set_title("Top 10 Genres")
    ax.set_ylabel("Number of Movies")
    st.pyplot(fig)
with cols[1] : 
    for i in range(10) : 
        st.markdown(" ")

###YEAR###
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
df['year'] = df['release_date'].dt.year
df['year'] = df['year'].astype('Int64')
yearly = df['year'].value_counts().sort_index()

with cols[0] :
    st.title("YEARS Line Chart: ") 

for i in range (27) :
    with cols[0] : 
        st.markdown("")

with cols[1] :
    st.subheader("📆 Movies Released per Year")
    st.bar_chart(yearly)

for i in range (5) :
    with cols[1] : 
        st.markdown("")

###LANGUAGE###
lang_counts = df['original_language'].value_counts().head(5)
lang_dict = lang_counts.to_dict()

val = [x for x in lang_dict.values()]
label = [x.upper() for x in lang_dict.keys()]

with cols[0] :
    st.title("🗣️ Top Languages")
    for lang, count in lang_dict.items():
        st.markdown(f"**{lang.upper()}:** {count}")

explode = [0.05] * len(val)  # Slightly separate all slices
fig, ax = plt.subplots()
wedges, texts, autotexts = ax.pie(val, autopct='%1.1f%%', startangle=90, explode=explode)
ax.axis('equal')
ax.legend(wedges, label, title="Languages", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

with cols [1] :
    st.pyplot(fig)        
