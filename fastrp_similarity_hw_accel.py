import pyTigerGraph as tg
import sys
import time

conn = tg.TigerGraphConnection(host="http://1.1.1.13", graphname="ProviderSimilarity")

precached = True

if not precached:
    retCode = conn.runInstalledQuery("tg_load_graph_cosinesim_ss_fpga_core", params={"vert_types":"Individual"}, timeout=1_024_000)
    print(retCode)

targetId = "1790766392"
#top10 = conn.runInstalledQuery("tg_cosinesim_ss_fpga_core", params={"source": "1457353518", "source.type": "Individual", "topK": 10})[0]["@@results"]

t1 = time.time()
top10 = conn.runInstalledQuery("tg_cosinesim_ss_fpga_core", params={"source": targetId, "source.type": "Individual", "topK": 10})[0]["@@results"]
t2 = time.time()
#print(top10)
print("Time Elapsed:", t2-t1)
print('Most Similar to Individual:', targetId)
for v in top10:
    #print(conn.runInstalledQuery("tg_vid_to_vertex", params={"v_id": int(v["Id"])}))
    #print(conn.runInstalledQuery("tg_vid_to_vertex", params={"v_id": v["Id"]}))
    print(v["Id"], v["score"])
    