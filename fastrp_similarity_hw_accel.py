import pyTigerGraph as tg
import sys
import time

conn = tg.TigerGraphConnection(host="http://1.1.1.13", graphname="ProviderSimilarity")

precached = False

if not precached:
    print("===== Caching Embeddings =====")
    setNumDevices = conn.runInstalledQuery("cosinesim_set_num_devices", params={"num_devicese":7})
    retCode = conn.runInstalledQuery("tg_load_graph_cosinesim_ss_fpga_core", params={"vert_types":"Individual"}, timeout=1_024_000)
    print(retCode)
    print("===== Embeddings Cached ======\n")
#top10 = conn.runInstalledQuery("tg_cosinesim_ss_fpga_core", params={"source": "1457353518", "source.type": "Individual", "topK": 10})[0]["@@results"]
providers = ["1790766392", "1669475711", "1154324184", "1275536443", "1225031859",
             "1114920642", "1366444697", "1417959669", "1386318749", "1659576965"]
times = []
for provider in providers:
    t1 = time.time()
    top10 = conn.runInstalledQuery("tg_cosinesim_ss_fpga_core", params={"source": provider, "source.type": "Individual", "topK": 10})[0]["@@results"]
    t2 = time.time()
    #print(top10)
    print("Time Elapsed:", t2-t1)
    print('Most Similar to Individual:', provider)
    for v in top10:
        print(v["Id"], v["score"])
    print()
    times.append(t2-t1)

print("===== Average Time Elapsed =====")
print(sum(times)/len(times), "Seconds")
    
