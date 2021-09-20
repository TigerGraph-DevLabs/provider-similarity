import pandas as pd
from time import sleep

def processAndLoadDf(df, conn, loadType='indv'):
        records = df.to_dict(orient="records")
        edges = [(x["NPI"], x["TaxonomyCode"], {"primaryTaxonomy": True if x["Primary"] == "Y" else False}) for x in records]

        if loadType == 'indv':
            npiHasTax = conn.upsertEdges("Individual", "INDIVIDUAL_IN_TAXONOMY", "Taxonomy", edges)
        elif loadType == 'org':
            npiHasTax = conn.upsertEdges("Organization", "ORGANIZATION_IN_TAXONOMY", "Taxonomy", edges)

        
def load(conn, file1="./data/processedData/indvTaxonomy.csv", file2="./data/processedData/orgTaxonomy.csv", **kwargs):
    for df in pd.read_csv(file1, names=['NPI',
                                    'TaxonomyCode',
                                    'Primary'], chunksize=10_000, quoting=1, dtype=str):
        df.fillna('', inplace=True)
        try:
            processAndLoadDf(df, conn, loadType='indv')
        except:
            sleep(5)
            processAndLoadDf(df, conn, loadType='indv')
    print("LOADED INDIVIDUALS")

    for df in pd.read_csv(file2, names=['NPI',
                                    'TaxonomyCode',
                                    'Primary'], chunksize=10_000, quoting=1, dtype=str):
        df.fillna('', inplace=True)
        try:
            processAndLoadDf(df, conn, loadType='org')
        except:
            sleep(5)
            processAndLoadDf(df, conn, loadType='org')
    print("LOADED ORGANIZATIONS")