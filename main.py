import streamlit as st  
import pandas as pd
import sqlite3
from utils import reload_csv_to_sqlite

pg = st.navigation([st.Page("Search.py"), 
                    st.Page("All_Movies.py"), 
                    st.Page("Details.py"),
                    st.Page("Dashboard.py")
                    ])
pg.run()
