import pandas as pd
import os

chunksize = 50000
filename = "./data/NPPES_Data_Dissemination_August_2021/npidata_pfile_20050523-20210808.csv"
processedDir = "./data/processedData/"

for f in os.listdir(processedDir):
    os.remove(os.path.join(processedDir, f))

cols = ['NPI',
 'Entity Type Code',
 'Replacement NPI',
 'Employer Identification Number (EIN)',
 'Provider Organization Name (Legal Business Name)',
 'Provider Last Name (Legal Name)',
 'Provider First Name',
 'Provider Middle Name',
 'Provider Name Prefix Text',
 'Provider Name Suffix Text',
 'Provider Credential Text',
 'Provider First Line Business Mailing Address',
 'Provider Second Line Business Mailing Address',
 'Provider Business Mailing Address City Name',
 'Provider Business Mailing Address State Name',
 'Provider Business Mailing Address Postal Code',
 'Provider Business Mailing Address Country Code (If outside U.S.)',
 'Provider Business Mailing Address Telephone Number',
 'Provider Business Mailing Address Fax Number',
 'Provider Enumeration Date',
 'Last Update Date',
 'NPI Deactivation Reason Code',
 'NPI Deactivation Date',
 'NPI Reactivation Date',
 'Provider Gender Code',
 'Authorized Official Last Name',
 'Authorized Official First Name',
 'Authorized Official Middle Name',
 'Authorized Official Title or Position',
 'Authorized Official Telephone Number',
 'Healthcare Provider Taxonomy Code_1',
 'Healthcare Provider Primary Taxonomy Switch_1',
 'Healthcare Provider Taxonomy Code_2',
 'Healthcare Provider Primary Taxonomy Switch_2',
 'Healthcare Provider Taxonomy Code_3',
 'Healthcare Provider Primary Taxonomy Switch_3',
 'Healthcare Provider Taxonomy Code_4',
 'Healthcare Provider Primary Taxonomy Switch_4',
 'Healthcare Provider Taxonomy Code_5',
 'Healthcare Provider Primary Taxonomy Switch_5',
 'Healthcare Provider Taxonomy Code_6',
 'Healthcare Provider Primary Taxonomy Switch_6',
 'Healthcare Provider Taxonomy Code_7',
 'Healthcare Provider Primary Taxonomy Switch_7',
 'Healthcare Provider Taxonomy Code_8',
 'Healthcare Provider Primary Taxonomy Switch_8',
 'Healthcare Provider Taxonomy Code_9',
 'Healthcare Provider Primary Taxonomy Switch_9',
 'Healthcare Provider Taxonomy Code_10',
 'Healthcare Provider Primary Taxonomy Switch_10',
 'Healthcare Provider Taxonomy Code_11',
 'Healthcare Provider Primary Taxonomy Switch_11',
 'Healthcare Provider Taxonomy Code_12',
 'Healthcare Provider Primary Taxonomy Switch_12',
 'Healthcare Provider Taxonomy Code_13',
 'Healthcare Provider Primary Taxonomy Switch_13',
 'Healthcare Provider Taxonomy Code_14',
 'Healthcare Provider Primary Taxonomy Switch_14',
 'Healthcare Provider Taxonomy Code_15',
 'Healthcare Provider Primary Taxonomy Switch_15',
 'Is Sole Proprietor',
 'Is Organization Subpart',
 'Parent Organization LBN',
 'Parent Organization TIN',
 'Authorized Official Name Prefix Text',
 'Authorized Official Name Suffix Text',
 'Authorized Official Credential Text',
 'Healthcare Provider Taxonomy Group_1',
 'Healthcare Provider Taxonomy Group_2',
 'Healthcare Provider Taxonomy Group_3',
 'Healthcare Provider Taxonomy Group_4',
 'Healthcare Provider Taxonomy Group_5',
 'Healthcare Provider Taxonomy Group_6',
 'Healthcare Provider Taxonomy Group_7',
 'Healthcare Provider Taxonomy Group_8',
 'Healthcare Provider Taxonomy Group_9',
 'Healthcare Provider Taxonomy Group_10',
 'Healthcare Provider Taxonomy Group_11',
 'Healthcare Provider Taxonomy Group_12',
 'Healthcare Provider Taxonomy Group_13',
 'Healthcare Provider Taxonomy Group_14',
 'Healthcare Provider Taxonomy Group_15',
 'Certification Date']


indAttributes = ['NPI',
 'Provider Last Name (Legal Name)',
 'Provider First Name',
 'Provider Middle Name',
 'Provider Name Prefix Text',
 'Provider Name Suffix Text',
 'Provider Credential Text']

orgAttributes = ['NPI',
 'Provider Organization Name (Legal Business Name)']

geogAttributes = ['NPI',
 'Provider First Line Business Mailing Address',
 'Provider Second Line Business Mailing Address',
 'Provider Business Mailing Address City Name',
 'Provider Business Mailing Address State Name',
 'Provider Business Mailing Address Postal Code',
 'Provider Business Mailing Address Country Code (If outside U.S.)']

taxonomyAttributes = ['NPI',
 'Healthcare Provider Taxonomy Code_1',
 'Healthcare Provider Primary Taxonomy Switch_1',
 'Healthcare Provider Taxonomy Code_2',
 'Healthcare Provider Primary Taxonomy Switch_2',
 'Healthcare Provider Taxonomy Code_3',
 'Healthcare Provider Primary Taxonomy Switch_3',
 'Healthcare Provider Taxonomy Code_4',
 'Healthcare Provider Primary Taxonomy Switch_4',
 'Healthcare Provider Taxonomy Code_5',
 'Healthcare Provider Primary Taxonomy Switch_5',
 'Healthcare Provider Taxonomy Code_6',
 'Healthcare Provider Primary Taxonomy Switch_6',
 'Healthcare Provider Taxonomy Code_7',
 'Healthcare Provider Primary Taxonomy Switch_7',
 'Healthcare Provider Taxonomy Code_8',
 'Healthcare Provider Primary Taxonomy Switch_8',
 'Healthcare Provider Taxonomy Code_9',
 'Healthcare Provider Primary Taxonomy Switch_9',
 'Healthcare Provider Taxonomy Code_10',
 'Healthcare Provider Primary Taxonomy Switch_10',
 'Healthcare Provider Taxonomy Code_11',
 'Healthcare Provider Primary Taxonomy Switch_11',
 'Healthcare Provider Taxonomy Code_12',
 'Healthcare Provider Primary Taxonomy Switch_12',
 'Healthcare Provider Taxonomy Code_13',
 'Healthcare Provider Primary Taxonomy Switch_13',
 'Healthcare Provider Taxonomy Code_14',
 'Healthcare Provider Primary Taxonomy Switch_14',
 'Healthcare Provider Taxonomy Code_15',
 'Healthcare Provider Primary Taxonomy Switch_15']

def getTaxonomyCodes(row):
    edges = []
    for i in range(1,15):
        if not(pd.isna(row["Healthcare Provider Taxonomy Code_"+str(i)])):
            edges.append({"NPI": row["NPI"], 
                          "TaxonomyCode": row["Healthcare Provider Taxonomy Code_"+str(i)],
                          "PrimaryCode": row["Healthcare Provider Primary Taxonomy Switch_"+str(i)]})
    return edges

for chunk in pd.read_csv(filename, chunksize=chunksize):
    edges = []
    df = chunk[cols]
    indvs = df[df["Entity Type Code"] == 1] # Individuals are designated by 1
    orgs = df[df["Entity Type Code"] == 2] # Organizations are designated by 2

    indvVertex = indvs[indAttributes]
    indvVertex.to_csv(processedDir+"individuals.csv", mode="a")
    orgVertex = orgs[orgAttributes]
    orgVertex.to_csv(processedDir+"organizations.csv", mode="a")

    geog = df[geogAttributes]
    geog.to_csv(processedDir+"geography.csv", mode="a")

    indvGeog = indvs[geogAttributes]
    indvGeog.to_csv(processedDir+"indvGeography.csv", mode="a")

    orgGeog = orgs[geogAttributes]
    orgGeog.to_csv(processedDir+"orgGeography.csv", mode="a")

    indvTaxonomy = pd.DataFrame([item for sublist in list(indvs.apply(getTaxonomyCodes, axis=1)) for item in sublist])
    indvTaxonomy.to_csv(processedDir+"indvTaxonomy.csv", mode="a")

    orgTaxonomy =pd.DataFrame([item for sublist in list(orgs.apply(getTaxonomyCodes, axis=1)) for item in sublist])
    orgTaxonomy.to_csv(processedDir+"orgTaxonomy.csv", mode="a")