# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pyTigerGraph as tg
conn = tg.TigerGraphConnection(host="http://1.1.1.13", graphname="ProviderSimilarity")

preprocess = False
if preprocess:
    print("PREPROCESSING")
    conn.runInstalledQuery("tg_fastRP_preprocessing", params={"index_attr": "vert_index"}, timeout=4_096_000)


# %%
import time

params = {"num_nodes": 6_769_471,
          "num_edges": 16_080_752 ,
          "k": 3,
          "sampling_constant": 3,
          "reduced_dimension": 64,
          "normalization_strength": -0.1,
          "input_weights": "1,2,4", 
          "index_attr": "vert_index",
          "print_accum": False,
          "result_attr": "fastrp_embedding"}

print("RUNNING FASTRP EMBEDDING")
t1 = time.time()
conn.runInstalledQuery("tg_fastrp", params=params, timeout=1_024_000)
t2 = time.time()


# %%
print("Time Elapsed: %.2f Seconds" % (t2-t1))


# %%
params = {"v1": "207WX0120X",
          "v1.type": "Taxonomy",
          "vert_types": "Taxonomy", 
          "embeddingDim": 64,
          "k": 5}

res = conn.runInstalledQuery("tg_embedding_cosine_similarity", params=params)[0]["kMostSimilar"]


# %%
for r in res:
    print(r["v_id"], r["attributes"]["@similarityScore"])


# %%
params = {"v1": "1457353518",
          "v1.type": "Individual",
          "vert_types": "Individual", 
          "embeddingDim": 64,
          "k": 5}

res = conn.runInstalledQuery("tg_embedding_cosine_similarity", params=params, timeout=64_000)[0]["kMostSimilar"]


# %%
for r in res:
    print(r["v_id"], r["attributes"]["@similarityScore"])


# %%
params = {"v1": "1912997503",
          "v1.type": "Individual",
          "vert_types": "Individual", 
          "embeddingDim": 64,
          "k": 5}

res = conn.runInstalledQuery("tg_embedding_cosine_similarity", params=params, timeout=64_000)[0]["kMostSimilar"]
for r in res:
    print(r["v_id"], r["attributes"]["@similarityScore"])


# %%
params = {"v1": "1457353518", 
          "v1.type": "Individual", 
          "v2": "1912997503", 
          "v2.type": "Individual",
          "embedding_dim": 64}

conn.runInstalledQuery("tg_embedding_pairwise_cosine_similarity", params=params)[0]["similarity"]


# %%
# Two individuals only described by 207RA0000X taxonomy

params = {"v1": "1316025943", 
          "v1.type": "Individual", 
          "v2": "1306802426", 
          "v2.type": "Individual",
          "embedding_dim": 64}

conn.runInstalledQuery("tg_embedding_pairwise_cosine_similarity", params=params)[0]["similarity"]


# %%
# Two individuals - both described by 207RA0000X taxonomy, but 1790766392 also has 2 other codes

params = {"v1": "1316025943", 
          "v1.type": "Individual", 
          "v2": "1790766392", 
          "v2.type": "Individual",
          "embedding_dim": 64}

conn.runInstalledQuery("tg_embedding_pairwise_cosine_similarity", params=params)[0]["similarity"]


# %%
params = {"v1": "1790766392",
          "v1.type": "Individual",
          "vert_types": "Individual", 
          "embeddingDim": 64,
          "k": 5}

res = conn.runInstalledQuery("tg_embedding_cosine_similarity", params=params, timeout=64_000)[0]["kMostSimilar"]
for r in res:
    print(r["v_id"], r["attributes"]["@similarityScore"])


# %%



