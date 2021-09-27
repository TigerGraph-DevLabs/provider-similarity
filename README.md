# Provider Similarity with Graph Embeddings
Demo Repository for Provider Similarity using Graph Embeddings using TigerGraph

## Python Environment Setup
To get started, create a Python virtual environment through virtualenv or conda. Then run ```pip install -r requirements.txt```

## Data
The data is from two different sources, one of which is individual providers and organizations using the NPI system, and the taxonomic codes describing their role. That dataset is found here: [https://download.cms.gov/nppes/NPI_Files.html](https://download.cms.gov/nppes/NPI_Files.html) [**Direct Download**](https://download.cms.gov/nppes/NPPES_Data_Dissemination_September_2021.zip)

The second data source describes the taxnomic system describing individuals' and organizations' roles. This data can be downloaded here: [https://www.nucc.org/index.php/code-sets-mainmenu-41/provider-taxonomy-mainmenu-40/csv-mainmenu-57](https://www.nucc.org/index.php/code-sets-mainmenu-41/provider-taxonomy-mainmenu-40/csv-mainmenu-57) [**Direct Download**](https://www.nucc.org/images/stories/CSV/nucc_taxonomy_211.csv)

### Processing the Data
The file ```processData.py``` processes the NPI files, and outputs cleaned CSVs inside of a processedData directory. To run this, unzip the NPI files into a folder inside a ```data/``` directory you create inside the main project directory. Then, run ```python processData.py```, which will read the files in and produce the cleaned file formats needed to load into the TigerGraph instance.

### Geographical Data
The NPI data also comes with geographical information. The processing script produces files that can be used to load this data if desired along with dataloaders defined for them. Currently this information is not used, but if desired, the schema can be altered by uncommenting out the lines that contain these vertex and edge definitions.

## TigerGraph Setup
The script ```main.py``` takes care of a lot of the schema creation, data loading, and query installation needed to run the similarity demo. Query installation is the least scripted of these, as TigerGraph User Defined Functions (UDFs) have to be installed ahead of time before installing the queries. 

### Configuration File
To save your TigerGraph configuration details, such as graph name, URL, username, password, and other things, there is a ```config-template.json``` file that is to be copied and and named ```config.json```. Fill the fields out according to your configuration.

### Schema Creation
To run the creation of the schema, simply run ```python main.py -cs``` in your Python virtual environment. This will read the ```config.json``` file and install the schema defined in ```gsql/schema/schema.gsql```.

### Data Loading
Data is loaded in four stages. Assuming that your NPI data resides in the ```./data/processedData``` directory, and your taxonomy data resides in ```./data/```, run:
```
python main.py --loadIndividuals
python main.py --loadOrganizations
python main.py --loadTaxonomy
python main.py --loadIndvOrgTax
```

### UDF Installation
To use the graph embedding and the embedding cosine similarity algorithms, there needs to be some TigerGraph UDFs installed beforehand. To do this, follow the directions [here](), and add the UDFs found in the ```gsql/udfs/``` directory.

### Query Installation

## Graph Embedding Algorithms


## Hardware Acceleration
