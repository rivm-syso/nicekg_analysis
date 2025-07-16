# NICE-FoodKG analysis
This repository provides all code necessary for the analyses and visualizations discussed in (F. Bindt, M. Ocke et al. 2025).

## Overview
The primary aim of this repository is to provide insights in how data is retrieved and figures are created using the NICE-FoodKG. The workflow leverages ontologies and semantic web technologies to enable rich querying and visualization of food-related data. For code how the data was processed, please go to [nicekg_processing repository](https://github.com/rivm-syso/nicekg_processing). 

## Contents

```
analysis/
├── figures                     # contains recreated figures created using the information retrieved with the SPARQL queries
├── functions                   # contains helper functions used in the repositories
├── queries                     # contains the underlying SPARQL queries for the use-cases
├── class_overlap.ipynb         # notebook used to create the VENN diagram in the publication
├── size_nice_food.ipynb        # notebook used to assess the size of NICE-Food
├── use_case_nice_food.ipynb    # notebook connected to a localhost:3030 which can be used for SPARQL querying and vizualisations 

```

## Software and Setup
All analyses and queries are performed in Jupyter notebooks, connected with a local Jena Apache Fuseki triplestore. SPARQL queries are executed from the notebook using the SPARQLWrapper package.

Steps to start querying:

Clone This Repository & Set Up Environment
```bash
mkdir nicefood_project
cd nicefood_project
git clone https://github.com/rivm-syso/nicekg_processing
git clone https://github.com/rivm-syso/nicekg_analysis
cd nicekg_analysis
conda env create -f environment.yml
conda activate nicekg_analysis
```
Obtain RDF subgraphs

- NICE-Subgraphs and relevant ontologies can be obtained from the nice [nicekg_processing repository](https://github.com/rivm-syso/nicekg_processing) in the \data\graph folder, or ZENODO for the most up to date version [NICE-Food RDF files](https://doi.org/10.5281/zenodo.15837271). When downloading from Zenodo, SPARQL queries might break due to updates in the underlying data model.

Install Jena Apache Fuseki
- Follow the official documentation for installation. [Fuseki documentation](https://jena.apache.org/documentation/fuseki2/)
- Start the fuseki-server 
- Through the Fuseki interface (usually at localhost:3030 in your browser), create a new dataset (recommended name: nice_food) 
- upload the downloaded .ttl files.
- the interface can be closed now

Saving files locally 
- If you want to save the files in another directory other than this repository. Create a local_path.py file with the following content

```
path_figure_4a = "your local path here"
path_figure_4b = "your local path here"
path_figure_4c = "your local path here"
```

## Project status
NICE-Food is part of the BigFood project funded by the Netherlands Institute of Public Health and the Environment strategic programme. In this project we aim to accelerate protein transition research through food data FAIRificaiton and artificial intelligence.  

## Licence
EUPL-1.2

## Acknowledgements
The authors thank the BIGFOOD project team for their valuable input at various stages of the project.

## Use of generative AI
In development of this work the author used OpenAI-4o in order to create and enhance the code. After using this tool/service, author(s) reviewed and edited the content as needed.  







