import pandas as pd
from time import sleep

def processAndLoadDf(df, conn, loadType='indv'):
        cities = df["City"].unique()

        cityVerts = [(x, {}) for x in cities]
        cityUpserted = conn.upsertVertices("City", cityVerts)

        states = df["State"].unique()
        stateVerts = [(x, {}) for x in states]
        stateUpserted = conn.upsertVertices("State", stateVerts)

        zips = df["Zip"].unique()
        zipVerts = [(x, {}) for x in zips]
        zipUpserted = conn.upsertVertices("ZipCode", zipVerts)

        addresses = df[["FirstLineAddr", "SecondLineAddr"]].drop_duplicates()
        records = addresses.to_dict(orient="records")
        vertices = [(x["FirstLineAddr"], {"secondLine": x["SecondLineAddr"]}) for x in records]
        addressesUpserted = conn.upsertVertices("Address", vertices)

        addressZipEdges = df[["FirstLineAddr", "Zip"]].drop_duplicates()
        records = addressZipEdges.to_dict(orient="records")
        edges = [(x["FirstLineAddr"], x["Zip"], {}) for x in records]
        addressZipEdgesUpserted = conn.upsertEdges("Address", "ADDRESS_IN_ZIPCODE", "ZipCode", edges)

        addressStateEdges = df[["FirstLineAddr", "State"]].drop_duplicates()
        records = addressStateEdges.to_dict(orient="records")
        edges = [(x["FirstLineAddr"], x["State"], {}) for x in records]
        addressStateEdgesUpserted = conn.upsertEdges("Address", "ADDRESS_IN_STATE", "State", edges)

        addressCityEdges = df[["FirstLineAddr", "City"]].drop_duplicates()
        records = addressCityEdges.to_dict(orient="records")
        edges = [(x["FirstLineAddr"], x["City"], {}) for x in records]
        addressCityEdgesUpserted = conn.upsertEdges("Address", "ADDRESS_IN_CITY", "City", edges)

        zipInCityEdges = df[["Zip", "City"]].drop_duplicates()
        records = zipInCityEdges.to_dict(orient="records")
        edges = [(x["Zip"], x["City"], {}) for x in records]
        zipInCityEdgesUpserted = conn.upsertEdges("ZipCode", "ZIP_IN_CITY", "City", edges)

        cityInStateEdges = df[["City", "State"]].drop_duplicates()
        records = cityInStateEdges.to_dict(orient="records")
        edges = [(x["City"], x["State"], {}) for x in records]
        cityInStateEdgesUpserted = conn.upsertEdges("City", "CITY_IN_STATE", "State", edges)

        zipInStateEdges = df[["Zip", "State"]].drop_duplicates()
        records = zipInStateEdges.to_dict(orient="records")
        edges = [(x["Zip"], x["State"], {}) for x in records]
        zipInStateEdgesUpserted = conn.upsertEdges("ZipCode", "ZIP_IN_STATE", "State", edges)

        npiHasAddressEdges = df[["NPI", "FirstLineAddr"]].drop_duplicates()
        records = npiHasAddressEdges.to_dict(orient="records")
        edges = [(x["NPI"], x["FirstLineAddr"], {}) for x in records]
        if loadType == 'indv':
            npiHasAddressEdgesUpserted = conn.upsertEdges("Individual", "INDIVIDUAL_HAS_ADDRESS", "Address", edges)
        elif loadType == 'org':
            npiHasAddressEdgesUpserted = conn.upsertEdges("Organization", "ORGANIZATION_HAS_ADDRESS", "Address", edges)

        
def load(conn, file1="./data/processedData/indvGeography.csv", file2="./data/processedData/orgGeography.csv", **kwargs):
    for df in pd.read_csv(file1, names=['NPI',
                                    'FirstLineAddr',
                                    'SecondLineAddr',
                                    'City',
                                    'State',
                                    'Zip',
                                    'Country'], chunksize=1_000, quoting=1, dtype=str):
        df.fillna('', inplace=True)
        try:
            processAndLoadDf(df, conn, loadType='indv')
        except:
            sleep(5)
            processAndLoadDf(df, conn, loadType='indv')
    print("LOADED INDIVIDUALS")

    for df in pd.read_csv(file2, names=['NPI',
                                    'FirstLineAddr',
                                    'SecondLineAddr',
                                    'City',
                                    'State',
                                    'Zip',
                                    'Country'], chunksize=1_000, quoting=1, dtype=str):
        df.fillna('', inplace=True)
        try:
            processAndLoadDf(df, conn, loadType='org')
        except:
            sleep(5)
            processAndLoadDf(df, conn, loadType='org')
    print("LOADED ORGANIZATIONS")