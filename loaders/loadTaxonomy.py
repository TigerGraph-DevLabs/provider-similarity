import pandas as pd

def load(conn, file1="./data/processedData/nucc_taxonomy_211.csv", **kwargs):
    df = pd.read_csv(file1)
    print(df.head())
    print(df.columns)
    
    #['Code', 'Grouping', 'Classification', 'Specialization', 'Definition', 'Notes', 'Display Name', 'Section']
    conn.upsertVertexDataframe(df, "Taxonomy", v_id="Code", attributes={"definition":"Definition", "notes": "Notes", "displayName": "Display Name"})