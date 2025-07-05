import streamlit as st  
import pandas as pd
import sqlite3
from utils import reload_csv_to_sqlite

# Call only once
reload_csv_to_sqlite(
    csv_path="TMDB_all_movies.csv",
    db_path="movies.db"
)


pg = st.navigation([st.Page("Search.py"), 
                    st.Page("All_Movies.py"), 
                    st.Page("Details.py"),
                    st.Page("Dashboard.py")
                    ])
pg.run()