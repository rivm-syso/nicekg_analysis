import pandas as pd

def add_prefix(cell):
    if pd.notna(cell):
        return f"http://purl.obolibrary.org/obo/{cell}"
    return cell


