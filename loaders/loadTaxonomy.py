import pandas as pd

def load(conn, file1="./data/nucc_taxonomy_211.csv", **kwargs):
    df = pd.read_csv(file1)

    def get_super(row):
        try:
            higherDf = df[df["Specialization"].isna()]
            superCode = higherDf[higherDf["Classification"] == row["Classification"]]["Code"].unique()
            return superCode[0]
        except:
            return None

    df["Super"] = df[~df["Specialization"].isna()].apply(get_super, axis=1)
    
    edges = df[["Code", "Super"]].drop_duplicates().dropna()
    records = edges.to_dict(orient="records")
    edges = [(x["Super"], x["Code"], {}) for x in records]
    numEdges = conn.upsertEdges("Taxonomy", "HAS_SUB_GROUP", "Taxonomy", edges)

    df.fillna("", inplace=True)
    #['Code', 'Grouping', 'Classification', 'Specialization', 'Definition', 'Notes', 'Display Name', 'Section']
    conn.upsertVertexDataFrame(df, "Taxonomy", v_id="Code", attributes={"definition":"Definition", "notes": "Notes", "displayName": "Display Name"})

    grouping = df[["Grouping", "Classification"]].drop_duplicates().merge(df)

    conn.upsertEdgeDataFrame(grouping, "Taxonomy", "HAS_SUB_GROUP", "Taxonomy", "Grouping", "Code", {})