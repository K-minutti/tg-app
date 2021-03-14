import pyTigerGraphBeta as tg

TG_HOST = "https://sg-tg.i.tgcloud.io"
TG_USERNAME = "tigergraph"
TG_PASSWORD = "gsqlstart100"
TG_GRAPHNAME = "connectivity"
TG_SECRET = "skfpc7tke4n553umsrk7r0ddi2l2m4ep"

conn = tg.TigerGraphConnection(host=TG_HOST, username=TG_USERNAME, password=TG_PASSWORD, graphname=TG_GRAPHNAME)

token = conn.getToken(TG_SECRET)

ls = conn.gsql("ls", options=[])

queries = conn.gsql(""" 
    use graph NetworkAnalysisTrial
    show query *
""", options=[])

# print(queries)

result = conn.runInstalledQuery("discoverSocialConnections", params={"A":115062, "B":198915 , "k":6})

#resultTwo = https://sg-tg.i.tgcloud.io:9000/query/connectivity/discoverSocialConnections?A=<VERTEX_ID>&B=<VERTEX_ID>&k=<INT>
print(result)