import streamlit as st
import graphistry
import pandas as pd
from css import all_css
from components import GraphistrySt #URLParam
graphistry.register(api=3, protocol="https", server="hub.graphistry.com", username="kevin", password="KM!3000billion")
    
    ## or via fresh short-lived token below that expires in 1:00:00 after initial generation 
    ## graphistry.register(api=3, protocol="https", server="hub.graphistry.com", token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImtldmluIiwiaWF0IjoxNjE1NzU4MzM5LCJleHAiOjE2MTU3NjE5MzksImp0aSI6ImUzNDIzZWZiLTFhZjEtNDljMC05OTQ1LTRhMWVjYzE0ZTEyYiIsInVzZXJfaWQiOjM4ODQsIm9yaWdfaWF0IjoxNjE1NzU4MzM5fQ.bcUynRysVUwVrWQcTaD1Dv-U7GqlImNFXLMeLUhql_A") 

def sidebar_area():
    # regular param (not in url)
    e = st.sidebar.number_input('Number of edges', min_value=10, max_value=100000, value=100, step=20)
    # deep-linkable param (in url)
    # n_init = urlParams.get_field('N', 100)
    n_init = 100
    n = st.sidebar.number_input('Number of nodes', min_value=10, max_value=100000, value=n_init, step=20)
    # urlParams.set_field('N', n)

    return {'num_nodes': n, 'num_edges': e}

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def run_filters(num_nodes, num_edges):
    nodes_df = pd.DataFrame({ 'n': [x for x in range(0, num_nodes)] })
    edges_df = pd.DataFrame({
        's': [x % num_nodes for x in range(0, num_edges)],
        'd': [(x + 1) % num_nodes for x in range(0, num_edges)],
    })
    graph_url = \
        graphistry.nodes(nodes_df).edges(edges_df) \
            .bind(source='s', destination='d', node='n')\
            .plot(render=False)
    return { 'nodes_df': nodes_df, 'edges_df': edges_df, 'graph_url': graph_url }


def main_area(num_nodes, num_edges, nodes_df, edges_df, graph_url):
    #logger.debug('rendering main area, with url: %s', graph_url)
    GraphistrySt().render_url(graph_url)


def app():
    all_css()
    #st.set_page_config(page_title="Home", page_icon=":shark:",layout="wide")
    st.title("This is APP1 and will be our default page as HOME")
    st.write("Hello this will be our simple analytics dashboard")
    try:

        # Render sidebar and get current settings
        sidebar_filters = sidebar_area()
        # Compute filter pipeline (with auto-caching based on filter setting inputs)
        # Selective mark these as URL params as well
        filter_pipeline_result = run_filters(**sidebar_filters)

        # Render main viz area based on computed filter pipeline results and sidebar settings
        main_area(**sidebar_filters, **filter_pipeline_result)

    except Exception as exn:
        st.write('Error loading dashboard')
        st.write(exn)

    # links = pd.read_csv("./lesm.csv")
    # g = graphistry.bind(source="source", destination="target")
    # g.edges(links).plot()