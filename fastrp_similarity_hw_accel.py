import pyTigerGraph as tg
conn = tg.TigerGraphConnection(host="http://1.1.1.13", graphname="ProviderSimilarity")
retCode = conn.runInstalledQuery("load_graph_cosinesim_ss_fpga_core", params={"vert_types":"Individual"}, timeout=1_024_000)
print(retCode)

top10 = conn.runInstalledQuery("tg_cosinesim_ss_fpga_core", params={"source": "1457353518", "source.type": "Individual", "topK": 10})
print(top10)