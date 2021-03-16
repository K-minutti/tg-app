# import pyTigerGraphBeta as tg

# # TG_HOST = "https://sg-tg.i.tgcloud.io"
# # TG_USERNAME = "tigergraph"
# # TG_PASSWORD = "gsqlstart100"
# # TG_GRAPHNAME = "connectivity"
# # TG_SECRET = "skfpc7tke4n553umsrk7r0ddi2l2m4ep"

# # conn = tg.TigerGraphConnection(host=TG_HOST, username=TG_USERNAME, password=TG_PASSWORD, graphname=TG_GRAPHNAME)

# # token = conn.getToken(TG_SECRET)

# ls = conn.gsql("ls", options=[])

# queries = conn.gsql(""" 
#     use graph NetworkAnalysisTrial
#     show query *
# """, options=[])

# # print(queries)

# result = conn.runInstalledQuery("discoverSocialConnections", params={"A":115062, "B":198915 , "k":6})
# #resultTwo = https://sg-tg.i.tgcloud.io:9000/query/connectivity/discoverSocialConnections?A=<VERTEX_ID>&B=<VERTEX_ID>&k=<INT>
# print(result)

# # g = graphistry.tigergraph(protocol='https', )
# # g2 = g.gsql("...", {'edges': '@@eList'})
# # g2.plot()
# # print('# edges', len(g2._edges))

# def plot_url(nodes_df, edges_df):
#     # edge weight ( ==> score )
#     # edgeInfluence @ https://hub.graphistry.com/docs/api/1/rest/url/#urloptions
#     g = graphistry \
#         .edges(edges_df) \
#         .settings(url_params={'play': 7000, 'dissuadeHubs': True}) \
#         .bind(edge_weight='amount')      \
#         .bind(source='from_id', destination='to_id') \
#         .bind(edge_title='amount', edge_label='amount') \
#         .nodes(nodes_df) \
#         .bind(node='n') \
#         .addStyle(bg={'color': 'white'}) #\
#         # .encode_point_color("type", categorical_mapping={'User': 'orange',
#         #                                                  'Transaction': '#CCC'},
#         #                             default_mapping='black') \
#         # .encode_edge_color("type", categorical_mapping={'User_Transfer_Transaction': 'black',
#         #                                                 'User_Recieve_Transaction_Rev': '#add836'},
#         #                             default_mapping='black') \
#         # .encode_point_icon('type', categorical_mapping={'User': 'laptop',
#         #                                                 'Transaction': 'server'},
#         #                             default_mapping='question')

#     url = g.plot(render=False, as_files=True)
#     return url


# # Given filter settings, generate/cache/return dataframes & viz
# @st.cache(suppress_st_warning=True, allow_output_mutation=True)
# def run_filters(user_id, conn):  # noqa: C901
#     try:
#         res = conn.gsql(
#         '''
#         use graph {}
#         ls
#         '''.format(conn.graphname), options=[])
#     except SystemExit as e:
#         st.write('Failed listing graph queries')
#         st.write(e)
#         raise e
#     except Exception as e:
#         st.write(e)
#         raise e

#     ind = res.index('Queries:') + 1
#     installTran = True
#     for query in res[ind:]:
#         if 'totalTransaction' in query:
#             installTran = False
#     # leann query to select all
#     if installTran:
#         conn.gsql(
#         '''
#         use graph AntiFraud
#         CREATE QUERY totalTransaction(Vertex<User> Source) FOR GRAPH AntiFraud {
#             start = {Source};

#             transfer = SELECT tgt
#                 FROM start:s -(User_Transfer_Transaction:e) - :tgt;

#             receive = select tgt
#                 FROM start:s -(User_Recieve_Transaction:e) -:tgt;

#             PRINT transfer, receive;
#         }
#         Install query totalTransaction
#         ''', options=[])

#     raw_results = conn.runInstalledQuery("circleDetection", {"srcId": user_id}, sizeLimit=1000000000, timeout=120000)
#     results = raw_results[0]['@@circleEdgeTuples']

#     # FIXME: Automate
#     out = []
#     from_ids = []
#     to_ids = []
#     times = []
#     amounts = []
#     types = []
#     from_types = []
#     to_types = []
#     for o in results:
#         for s in o:
#             if {
#                 "from_id": s["e"]["from_id"], "to_id": s["e"]["to_id"], "amount": s["amount"], "time": s["ts"],
#                 "type": s["e"]["e_type"]
#             } not in out:
#                 out.append(
#                     {"from_id": s["e"]["from_id"], "to_id": s["e"]["to_id"], "amount": s["amount"], "time": s["ts"],
#                      "type": s["e"]["e_type"]})
#                 from_ids.append(s["e"]["from_id"])
#                 to_ids.append(s["e"]["to_id"])
#                 amounts.append(s["amount"])
#                 times.append(s["ts"])
#                 types.append(s["e"]["e_type"])
#                 from_types.append(s['e']['from_type'])
#                 to_types.append(s['e']['from_type'])

#     edges_df = pd.DataFrame({
#         'from_id': from_ids,
#         'to_id': to_ids,
#         'amount': amounts,
#         'time': times,
#         'type': types
#     })
#     node_idf = []
#     typef = []
#     for i in range(len(from_ids)):
#         if from_ids[i] not in node_idf:
#             node_idf.append(from_ids[i])
#             typef.append(from_types[i])
#         if to_ids[i] not in node_idf:
#             node_idf.append(to_ids[i])
#             typef.append(to_types[i])

#     nodes_df = pd.DataFrame({
#         'n': node_idf,
#         'type': typef,
#         'size': 0.1
#     })

#     try:
#         res = nodes_df.values.tolist()

#         # Calculate the metrics
#         metrics['node_cnt'] = nodes_df.size
#         metrics['edge_cnt'] = edges_df.size
#         metrics['prop_cnt'] = (nodes_df.size * nodes_df.columns.size) + \
#                               (edges_df.size * edges_df.columns.size)

#         if nodes_df.size > 0:
#             url = plot_url(nodes_df, edges_df)
#         else:
#             url = ""
#     except Exception as e:
#         raise e

#     try:
#         pass

#     except RuntimeError as e:
#         if str(e) == "There is no current event loop in thread 'ScriptRunner.scriptThread'.":
#             loop = asyncio.new_event_loop()
#             asyncio.set_event_loop(loop)

#         else:
#             raise e

#     except Exception as e:
#         logger.error('oops in TigerGraph', exc_info=True)
#         raise e

#     return {'nodes_df': nodes_df, 'edges_df': edges_df, 'url': url, 'res': res, 'conn': conn}

# def main_area(url, nodes, edges, user_id, conn):

#     logger.info('rendering main area, with url: %s', url)
#     GraphistrySt().render_url(url)

#     dates = []
#     amounts = []
#     transfer_type = []
#     results = None

#     try:
#         results = conn.runInstalledQuery("totalTransaction", params={"Source": user_id})[0]
#     except Exception as e:
#         print(e)

#     # Create bar chart of transactions
#     if results is not None:
#         for action in results:
#             for transfer in results[action]:
#                 dates.append(datetime.datetime.fromtimestamp(transfer['attributes']['ts']))
#                 amounts.append(transfer['attributes']['amount'])
#                 transfer_type.append(action)
#         cols = list(zip(dates, amounts, transfer_type))
#         cols = sorted(cols, key=lambda x: x[0].day)
#         cols = sorted(cols, key=lambda x: x[0].month)
#         cols = sorted(cols, key=lambda x: x[0].year)
#         df = pd.DataFrame(data=cols, columns=['Date', 'Amount', 'Type'])
#         df['Date'] = pd.to_datetime(df['Date'])
#         map_color = {"receive": "rgba(0,0,255,0.5)", "transfer": "rgba(255,0,0,0.5)"}
#         df['Color'] = df['Type'].map(map_color)

#         df = df.groupby([df['Date'].dt.to_period('M'), 'Type', 'Color']).sum()
#         df = df.reset_index(level=['Type', 'Color'])
#         df.index = df.index.values.astype('datetime64[M]')
#         bar = px.bar(df, x=df.index, y='Amount', labels={'x': 'Date'}, color='Type', color_discrete_map=map_color,
#                      text='Amount', title="Transaction Amounts by Month for User {}".format(user_id), height=350,
#                      barmode='group')
#         bar.update_xaxes(
#             dtick="M1",
#             tickformat="%b\n%Y")
#         try:
#             for trace in bar.data:
#                 trace.name = trace.name.split('=')[1].capitalize()
#         # FIXME exepct exn?
#         except:  # noqa: E722
#             for trace in bar.data:
#                 trace.name = trace.name.capitalize()

#         st.plotly_chart(bar, use_container_width=True)

# def run_all():
#     custom_css()
#     try:

#         # Render sidebar, get current settings and TG connection
#         sidebar_filters = sidebar_area()

#         # Stop if not connected to TG
#         if sidebar_filters is None:
#             return

#         # Compute filter pipeline, with auto-caching based on filter setting inputs
#         filter_pipeline_result = run_filters(**sidebar_filters)

#         # Render main viz area based on computed filter pipeline results and sidebar settings if data is returned
#         if filter_pipeline_result['nodes_df'].size > 0:
#             main_area(filter_pipeline_result['url'],
#                       filter_pipeline_result['nodes_df'],
#                       filter_pipeline_result['edges_df'],
#                       sidebar_filters['user_id'],
#                       filter_pipeline_result['conn'])
#         else:  # render a message
#             st.write("No data matching the specfiied criteria is found")

#     except Exception as exn:
#         st.write('Error loading dashboard')
#         st.write(exn)
