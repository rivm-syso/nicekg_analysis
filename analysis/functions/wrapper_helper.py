import pandas as pd
from SPARQLWrapper import JSON, SPARQLWrapper


def open_query(path):
    """Opens an .rq file and can input it in the sparql wrapper."""
    with open(path, "r") as file:
        file = file.read()
    return file


def sparql_query_to_dataframe(query, endpoint="http://localhost:3030/publication_1_test/sparql"):
    """
    Execute a SPARQL query and return the results as a pandas DataFrame.

    Parameters:
    - query (str): The SPARQL query to execute.
    - endpoint (str): The SPARQL endpoint URL. Default is "http://localhost:3030/publication_1_test/sparql".

    Returns:
    - pd.DataFrame: The query results as a pandas DataFrame.
    """
    # Initialize the SPARQL wrapper
    sparql = SPARQLWrapper(endpoint)

    # Set the return format
    sparql.setReturnFormat(JSON)

    # Set the query
    sparql.setQuery(query)

    # Execute the query
    results = sparql.query().convert()

    # Extract the results bindings
    bindings = results["results"]["bindings"]

    # Convert to a list of dictionaries
    data = []
    for result in bindings:
        row = {var: result[var]["value"] for var in result}
        data.append(row)

    # Create a DataFrame
    df = pd.DataFrame(data)

    return df
