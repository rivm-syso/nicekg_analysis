import urllib.request, urllib.error, urllib.parse
import json
from dotenv import load_dotenv
import os
from pprint import pprint
import pandas as pd
from tqdm import tqdm
import urllib.parse

load_dotenv()

REST_URL = "http://data.bioontology.org"
API_KEY = os.getenv("BIO_KEY")

def get_json(url):
    opener = urllib.request.build_opener()
    opener.addheaders = [('Authorization', 'apikey token=' + API_KEY)]
    return json.loads(opener.open(url).read())

def print_annotations(text_to_annotate, annotations, get_class=True):
    print(text_to_annotate)
    for result in annotations:
        class_details = result["annotatedClass"]
        if get_class:
            try:
                class_details = get_json(result["annotatedClass"]["links"]["self"])
            except urllib.error.HTTPError:
                print(f"Error retrieving {result['annotatedClass']['@id']}")
                continue
        print("Class details")
        print("\tid: " + class_details["@id"])
        print("\tprefLabel: " + class_details["prefLabel"])
        print("\tontology: " + class_details["links"]["ontology"])

        print("Annotation details")
        for annotation in result["annotations"]:
            print("\tfrom: " + str(annotation["from"]))
            print("\tto: " + str(annotation["to"]))
            print("\tmatch type: " + annotation["matchType"])

        if result["hierarchy"]:
            print("\n\tHierarchy annotations")
            for annotation in result["hierarchy"]:
                try:
                    class_details = get_json(annotation["annotatedClass"]["links"]["self"])
                except urllib.error.HTTPError:
                    print(f"Error retrieving {annotation['annotatedClass']['@id']}")
                    continue
                pref_label = class_details["prefLabel"] or "no label"
                print("\t\tClass details")
                print("\t\t\tid: " + class_details["@id"])
                print("\t\t\tprefLabel: " + class_details["prefLabel"])
                print("\t\t\tontology: " + class_details["links"]["ontology"])
                print("\t\t\tdistance from originally annotated class: " + str(annotation["distance"]))

        print("\n\n")


def get_annotation(result, get_class = True):
    # print(result)
    api_result = {}
    if result is not None:
        try:
            class_details = get_json(result)
            # print(class_details)
            # print("ja")
        except Exception as e: 
            print(e)
            class_details = {}

    return class_details


def annotate_text(df, ontology, text_column, rest_url = REST_URL):
    """
    Annotate text from a DataFrame using a specified ontology and REST API.

    Parameters:
    df (pd.DataFrame): DataFrame containing the text to annotate.
    ontology (str): The ontology to use for annotation.
    rest_url (str): The base URL of the REST API.
    text_column (str): The name of the column containing the text to annotate.

    Returns:
    list: A list of results with the original text and annotations.
    """
    results = []
    for _, row in tqdm(df.iterrows(), total=len(df)):
        row_result = []
        text_to_annotate = row[text_column]
        row_result.append(text_to_annotate)
        encoded_text = urllib.parse.quote(text_to_annotate)
        annotations = get_json(f"{rest_url}/annotator?text={encoded_text}&ontologies={ontology}")
        try:
            row_result.append(annotations)
        except Exception as e:
            print("Nothing found")
        results.append(row_result)
    return results


def process_annotations(results, original_df, text_column):
    """
    Process the annotation results and integrate them back into the original DataFrame.

    Parameters:
    results (list): List of results with the original text and annotations.
    original_df (pd.DataFrame): The original DataFrame.
    text_column (str): The name of the column containing the text to annotate.

    Returns:
    pd.DataFrame: The original DataFrame with the annotations integrated.
    """
    # Create a DataFrame from the results
    df_results = pd.DataFrame(results, columns=[text_column, "api_results"])
    
    # Explode the 'api_results' column
    exploded = df_results.explode('api_results').reset_index(drop=True)
    
    # Normalize the exploded 'api_results' column
    normalized = pd.json_normalize(exploded['api_results'])
    
    # Join the normalized results back to the exploded DataFrame
    api_results = exploded.join(normalized)
    
    # Apply the get_annotation function to the 'annotatedClass.links.self' column
    api_annotations = api_results['annotatedClass.links.self'].apply(lambda x: get_annotation(x))
    
    # Normalize the annotations
    normalized_annotations = pd.json_normalize(api_annotations)
    
    # Join the normalized annotations back to the api_results DataFrame
    annotation_results = api_results.join(normalized_annotations)
    
    # Merge the annotation results back to the original DataFrame
    final_df = original_df.merge(annotation_results, left_on=text_column, right_on=text_column, how='left')
    
    return final_df