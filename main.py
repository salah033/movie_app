import streamlit as st  
from utils import reload_csv_to_sqlite
from streamlit_extras.switch_page_button import switch_page

# Call only once
reload_csv_to_sqlite(
    csv_path="TMDB_all_movies.csv",
    db_path="movies.db"
)
# Set wide layout for the app
def wide_space_default():
    st.set_page_config(layout="wide")

# Import the navigation module
pg = st.navigation([st.Page("Search.py"), 
                    st.Page("All_Movies.py"), 
                    st.Page("Details.py"),
                    st.Page("Dashboard.py"),
                    st.Page("Favourite.py")
                    ])
wide_space_default()
pg.run()
