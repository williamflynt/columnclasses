import json
import os
import pandas as pd
from django.core.files import File

from classifier.models import Source


def load_csv(document: File) -> pd.DataFrame:
    """load a CSV from a Source.document field to a dataframe"""
    with document.open("r") as f:
        df = pd.read_csv(f)
    return df


def analyze_column(index: int, df: pd.DataFrame) -> dict:
    """get metrics about a column in a DataFrame, as identified by index"""
    # TODO
    return {}


def analyze_dataframe(df: pd.DataFrame) -> dict:
    """analyze all columns in a DataFrame"""
    # TODO
    # for col in df: ...
    analyze_column(0, df)
    return {}


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
