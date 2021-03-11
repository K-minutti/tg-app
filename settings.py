import streamlit as st

NAME = "Your name"
IMAGE_LOGO = "./icon.png"

def app():
    st.header("Configure your settings here")
    
    st.write("")
    st.write("### Name")
    name = st.text_input("", '')
    st.write(name)
    NAME = name

    st.write("### Upload logo or image")
    image = st.file_uploader('', type=['png', 'jpg', 'jpeg'], accept_multiple_files=False)
    IMAGE_LOGO = image
    return NAME, IMAGE_LOGO