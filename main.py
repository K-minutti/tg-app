import home
import engagement
import ecosystem
import community
import plan
import settings
from PIL import Image
import streamlit as st

st.set_page_config(layout="wide",initial_sidebar_state="collapsed" )

PAGES = {
    "Home" : home,
    "Engagement" : engagement, 
    "Ecosystem": ecosystem,
    "Community Search": community,
    "Planning" : plan,
    "Settings" : settings

}

#selection = st.sidebar.selectbox("NAVIGATION", list(PAGES.keys()))
title = "Home"
col1, col2 = st.beta_columns([4, 1])
selection = col2.selectbox("", list(PAGES.keys()))
title = selection
col1.title(title)
st.write("""***""")
image = Image.open(settings.IMAGE_LOGO)
st.sidebar.image(image, use_column_width=True)
name = settings.NAME
st.sidebar.subheader(name)
# then name = settings.NAME
page = PAGES[selection]

#main container
page.app()
