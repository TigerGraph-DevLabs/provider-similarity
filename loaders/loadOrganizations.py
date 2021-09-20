import pandas as pd

def load(conn, file1="./data/processedData/organizations.csv", **kwargs):
    for df in pd.read_csv(file1, names=['NPI',
                                        'Provider Organization Name (Legal Business Name)',
                                        'NPI Deactivation Reason Code',
                                        'NPI Deactivation Date',
                                        'NPI Reactivation Date'], chunksize=10_000, quoting=1):

        df = df.fillna({'NPI': '', 
                        'Provider Organization Name (Legal Business Name)': '', 
                        'NPI Deactivation Reason Code': '', 
                        'NPI Deactivation Date': '01/01/1970', 
                        'NPI Reactivation Date': '01/01/1970'})

        records = df.to_dict('records')

        vertices = [(x["NPI"], {
            "organizationName": x["Provider Organization Name (Legal Business Name)"],
            #"deactivationDate": x["NPI Deactivation Date"],
            #"reactivationDate": x["NPI Reactivation Date"]
        }) for x in records]
        
        numUpserted = conn.upsertVertices("Organization", vertices)