import pandas as pd

def load(conn, file1="./data/processedData/individuals.csv", **kwargs):
    for df in pd.read_csv(file1, names=['NPI',
                                    'Provider Last Name (Legal Name)',
                                    'Provider First Name',
                                    'Provider Middle Name',
                                    'Provider Name Prefix Text',
                                    'Provider Name Suffix Text',
                                    'Provider Credential Text',
                                    'NPI Deactivation Reason Code',
                                    'NPI Deactivation Date',
                                    'NPI Reactivation Date'], chunksize=10_000, quoting=1):

        df = df.fillna({'NPI': '', 
                        'Provider Last Name (Legal Name)': '', 
                        'Provider First Name': '', 
                        'Provider Middle Name': '', 
                        'Provider Name Prefix Text': '', 
                        'Provider Name Suffix Text': '', 
                        'Provider Credential Text': '', 
                        'NPI Deactivation Reason Code': '', 
                        'NPI Deactivation Date': '01/01/1970', 
                        'NPI Reactivation Date': '01/01/1970'})

        records = df.to_dict('records')

        vertices = [(x["NPI"], {
            "lastName": x["Provider Last Name (Legal Name)"],
            "firstName": x["Provider First Name"],
            "middleName": x["Provider Middle Name"],
            "prefix": x["Provider Name Prefix Text"],
            "suffix": x["Provider Name Suffix Text"],
            "deactivationCode": x["NPI Deactivation Reason Code"],
            #"deactivationDate": x["NPI Deactivation Date"],
            #"reactivationDate": x["NPI Reactivation Date"]
        }) for x in records]
        
        numUpserted = conn.upsertVertices("Individual", vertices)