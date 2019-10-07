import json
import os
import pandas as pd
import numpy as np
from django.core.files import File

from classifier.models import Source


def load_csv(document: File) -> pd.DataFrame:
    """load a CSV from a Source.document field to a dataframe"""
    with document.open("r") as f:
        df = pd.read_csv(f)
    return df


def analyze_column(index: int, df: pd.DataFrame) -> dict:
    """get metrics about a column in a DataFrame, as identified by index"""
    # Not needed.
    return {}


"""
    Small functions to clean up readability of the dataframe processing
"""
def count_digits(s):   # counts 0 thru 9 in strings
    return sum(c.isdigit() for c in s)

def count_letters(s): # counts A a thru Z z in strings
    return sum(c.isalpha() for c in s)

def count_spaces(s):  # counts spaces
    return sum(c.isspace() for c in s)

def count_other_text(s):  # counts non alphanum, non whitespace
    return len(s) - count_digits(s) - count_letters(s) - count_spaces(s)

def frac_fxn(fxn, rows):  # calculates the numerator and denominator for functions requiring fractions
    s=0 # prevents a error
    return np.sum([fxn(str(s)) for s in rows])/np.sum([len(str(s)) for s in rows])


def analyze_dataframe(df: pd.DataFrame) -> dict:
    """analyze all columns in a DataFrame"""
    
    # mean token metrics aggregated across each column
    _df['mean_token_count'] = df.apply(lambda rows: np.mean([len(str(s).split()) for s in rows]))
    _df['mean_token_length'] = df.apply(lambda rows: np.mean( [len(i.split()) for s in rows for i in str(s) ]   ))

    # fraction metrics aggregated across each column
    _df['frac_digit'] = df.apply(lambda rows: frac_fxn(count_digits,rows))
    _df['frac_alpha'] = df.apply(lambda rows: frac_fxn(count_letters,rows))
    _df['frac_space'] = df.apply(lambda rows: frac_fxn(count_spaces,rows))
    _df['frac_other_text'] = df.apply(lambda rows: frac_fxn(count_other_text,rows))
    
    # line length metrics
    _df['mean_line_length'] = df.apply(lambda rows: np.mean([len(str(s)) for s in rows]))
    _df['median_line_length'] = df.apply(lambda rows: np.median([len(str(s)) for s in rows]))
    _df['std_line_length'] = df.apply(lambda rows: np.std([len(str(s)) for s in rows]))

    # unique char / token metrics
    _df['unq_char_count'] = df.apply(lambda rows: len(set([i for s in rows for i in str(s)])))
    _df['unq_token_count'] = df.apply(lambda rows: len(set([str(s) for s in rows])))

    # number of rows tagged on each column
    _df['row_count'] = df.apply(lambda rows: len(rows))
    
    # use pandas to_json to convert the df directly into a json format
    # that can then be read directly back into a dataframe format later.
    # a .transpose() method is used before converting in order to give the
    # following format:
    """
    {"columnname1":{"mean_token_count":1.035,"mean_token_length":2.100, ...}, "columnname2": {...}, ... }
    """
    json_dataframe = _df.transpose().to_json()
    
    return json_dataframe


def json_fp(src_doc: File) -> str:
    """make a json filepath from a Source.document's path"""
    bn = os.path.basename(src_doc.name)
    return os.path.join("analysis", ".".join([bn.split(".")[0], "json"]))


def write_data(data: dict, filepath: str) -> None:
    """write some data to a file as json"""
    with open(filepath, "w") as f:
        json.dump(data, f)


def batch_analysis() -> None:
    """pull all applicable Source models and analyze the documents"""
    sources = Source.objects.filter(
        document__isnull=False, time_classified__isnull=False
    )
    for source in sources:
        df = load_csv(source.document)
        data = analyze_dataframe(df)
        write_data(data, json_fp(source.document))
