import pandas as pd

def load(conn, file1="./data/processedData/nucc_taxonomy_211.csv", **kwargs):
    df = pd.read_csv(file1)
    print(df.head())
    