import home
import engagement
import ecosystem
import community
import plan
from PIL import Image
import streamlit as st

st.set_page_config(layout="wide",initial_sidebar_state="collapsed",page_icon="./column.png" )
#add page_icon=, page_title=

PAGES = {
    "Home" : home,
    "Engagement" : engagement, 
    "Ecosystem": ecosystem,
    "Community Search": community,
    "Planning" : plan,

}

#selection = st.sidebar.selectbox("NAVIGATION", list(PAGES.keys()))
title = "Home"
col1, col2 = st.beta_columns([4, 1])
selection = col2.selectbox("", list(PAGES.keys()))
title = selection
col1.title(title)
st.write("""***""")
sbCol1, sbCol2 = st.sidebar.beta_columns([1,2])
image = Image.open("./column.png")
sbCol1.image(image, use_column_width=False)
sbCol2.title("Iconic")

st.sidebar.subheader("CURRENT ARTISTS NAME")
# then name = settings.NAME
page = PAGES[selection]
#main container
page.app()
