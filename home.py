import streamlit as st
import graphistry
import pandas
graphistry.register(api=3, protocol="https", server="hub.graphistry.com", username="kevin", password="KM!3000billion")
    
    ## or via fresh short-lived token below that expires in 1:00:00 after initial generation 
    ## graphistry.register(api=3, protocol="https", server="hub.graphistry.com", token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImtldmluIiwiaWF0IjoxNjE1NzU4MzM5LCJleHAiOjE2MTU3NjE5MzksImp0aSI6ImUzNDIzZWZiLTFhZjEtNDljMC05OTQ1LTRhMWVjYzE0ZTEyYiIsInVzZXJfaWQiOjM4ODQsIm9yaWdfaWF0IjoxNjE1NzU4MzM5fQ.bcUynRysVUwVrWQcTaD1Dv-U7GqlImNFXLMeLUhql_A") 
  

def app():
    #st.set_page_config(page_title="Home", page_icon=":shark:",layout="wide")
    st.title("This is APP1 and will be our default page as HOME")
    st.write("Hello this will be our simple analytics dashboard")
    links = pandas.read_csv("./lesm.csv")
    g = graphistry.bind(source="source", destination="target")
    g.edges(links).plot()