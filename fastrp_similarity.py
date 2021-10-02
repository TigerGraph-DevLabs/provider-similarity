import pyTigerGraph as tg
conn = tg.TigerGraphConnection(host="http://1.1.1.13", graphname="ProviderSimilarity")

preprocess = False
if preprocess:
    print("PREPROCESSING")
    conn.runInstalledQuery("tg_fastRP_preprocessing", params={"index_attr": "vert_index"}, timeout=4_096_000)
    print("Preprossing Complete")

import time
embed = False
if embed:
    params = {"num_nodes": 6_815_739,
            "num_edges": 16_201_798,
            "k": 3,
            "sampling_constant": 3,
            "reduced_dimension": 200,
            "normalization_strength": -0.1,
            "input_weights": "1,2,4", 
            "index_attr": "vert_index",
            "print_accum": False,
            "result_attr": "fastrp_embedding"}

    print("RUNNING FASTRP EMBEDDING")
    t1 = time.time()
    conn.runInstalledQuery("tg_fastRP", params=params, timeout=1_024_000)
    t2 = time.time()
    print("Time Elapsed: %.2f Seconds" % (t2-t1))

providers = []
times = []
for provider in providers:
    params = {"v1": provider,
            "v1.type": "Individual",
            "vert_types": "Individual", 
            "embeddingDim": 200,
            "k": 10}

    t1 = time.time()
    res = conn.runInstalledQuery("tg_embedding_cosine_similarity", params=params)[0]["kMostSimilar"]
    t2 = time.time()

    print("Time Elapsed:", t2-t1)
    print("Most Similar to Individual:", provider)
    for r in res:
        print(r["v_id"], r["attributes"]["@similarityScore"])
    print()
    times.append(t2-t1)

print("===== Average Time Elapsed =====")
print(sum(times)/len(times), "Seconds")