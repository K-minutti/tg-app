import streamlit as st
import pyTigerGraphBeta as tg
import graphistry, os, pandas as pd
from css import all_css
from components import GraphistrySt 

TG_HOST = "https://sg-tg.i.tgcloud.io"
TG_USERNAME = "tigergraph"
TG_PASSWORD = "gsqlstart100"
TG_GRAPHNAME = "connectivity"
TG_SECRET = "skfpc7tke4n553umsrk7r0ddi2l2m4ep"

def custom_css():
    all_css()
    st.markdown(
        """<style>

        </style>""", unsafe_allow_html=True)

def sidebar():
    conn = tg.TigerGraphConnection(host=TG_HOST, username=TG_USERNAME, password=TG_PASSWORD, graphname=TG_GRAPHNAME)
    token = conn.getToken(TG_SECRET)
    st.sidebar.subheader("Select two People see their connection(s)")
    idList = [i for i in range(1,20000)]
    pid_a = st.sidebar.selectbox('Person A ID ', idList)
    pid_b = st.sidebar.selectbox('Person B ID ', idList)
    kList = [i for i in range(1,11)]
    k = st.sidebar.selectbox('K hops ', kList)
    return {'person_a': pid_a  , 'person_b': pid_b,'k_hops': k}

def plot_url(nodes_df, edges_df):
    g = graphistry \
        .edges(edges_df) \
        .settings(url_params={'play': 7000, 'dissuadeHubs': True}) \
        .bind(edge_weight='amount')      \
        .bind(source='from_id', destination='to_id') \
        .bind(edge_title='amount', edge_label='amount') \
        .nodes(nodes_df) \
        .bind(node='n') \
        .addStyle(bg={'color': 'white'}) \

    url = g.plot(render=False, as_files=True)
    return url

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def run_filters(person_a, person_b, k, conn):
    # try: 
    #     res = conn.gsql(
    #     '''
    #     use graph {}
    #     ls
    #     '''.format(conn.graphname), options=[])
    # except SystemExit as e:
    #     st.write('Failed listing graph queries')
    #     st.write(e)
    #     raise e 
    # except Exception as e:
    #     st.write(e)
    #     raise e
    raw_result = conn.runInstalledQuery("discoverSocialConnections", params={"A":person_a, "B":person_b , "k":k})
    #resultTwo = https://sg-tg.i.tgcloud.io:9000/query/connectivity/discoverSocialConnections?A=<VERTEX_ID>&B=<VERTEX_ID>&k=<INT>
    print(raw_result)
    results = raw_result[0]['@@edgeSet']

    # parse results getting the appropriate from , to ids and types as well as from and to types
    # for obj in results:
    #     for s in obj


    #turn in to a an edges_df and nodes_df
    # edges_df = pd.DataFrame({
    #     'from_id': from_ids,
    #     'to_id': to_ids,
    #     'amount': amounts,
    #     'time': times,
    #     'type': types
    # })
    # node_idf = []
    # typef = []
    # for i in range(len(from_ids)):
    #     if from_ids[i] not in node_idf:
    #         node_idf.append(from_ids[i])
    #         typef.append(from_types[i])
    #     if to_ids[i] not in node_idf:
    #         node_idf.append(to_ids[i])
    #         typef.append(to_types[i])

    # nodes_df = pd.DataFrame({
    #     'n': node_idf,
    #     'type': typef,
    #     'size': 0.1
    # })
    if nodes_df.size > 0:
        url = plot_url(nodes_df, edges_df)
    else:
        url = ""
    return {'nodes_df': nodes_df, 'edges_df': edges_df, 'url': url, 'res': res, 'conn': conn}

def main_area(url, nodes, edges, person_a, person_b, k_hops, conn):
    GraphistrySt().render_url(url)

def app():
    custom_css()
    st.title("This is APP2 and this will be our engagement section")
    try:
        sidebar_filters = sidebar_area()
        if sidebar_filters is None:
            return

        filter_pipeline_result = run_filters(**sidebar_filters)

        if filter_pipeline_result['nodes_df'].size > 0:
            main_area(filter_pipeline_result['url'], 
                      filter_pipeline_result['node_df'],
                      filter_pipeline_result['edges_df'],
                      sidebar_filters['person_a'],
                      sidebar_filters['person_b'],
                      sidebar_filters['k_hops'],
                      filter_pipeline_result['conn'])
        else:  # render a message
            st.write("No data matching the specfiied criteria is found")
    except Exception as e:
        st.write('Error loading dashboard')
        st.write(e)