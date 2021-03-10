import app1
import app2
import streamlit as st

st.set_page_config(layout="wide",initial_sidebar_state="collapsed" )

PAGES = {
    "App1" : app1,
    "App2" : app2
}

#selection = st.sidebar.selectbox("NAVIGATION", list(PAGES.keys()))

col1, col2 = st.beta_columns([4, 1])
col1.title("Title of brand")
selection = col2.selectbox("", list(PAGES.keys()))
page = PAGES[selection]

#main container
page.app()
