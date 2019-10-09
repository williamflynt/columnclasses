import os
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from django.core.files import File

from classifier.assets import AssetHolder
from classifier.models import Source
from classifier.pd_operations import (
    mean_token_count,
    mean_token_length,
    avg_len,
    unq_char_count,
    unq_token_count,
    count_digits,
    count_letters,
    count_spaces,
    count_other_text,
    frac_fxn,
    frac_token,
    frac_regex,
)

assets = AssetHolder()


def load_csv(document: File) -> pd.DataFrame:
    """load a CSV from a Source.document field to a dataframe"""
    with document.open("r") as f:
        df = pd.read_csv(f, keep_default_na=False)
    return df


def label_or_reject(label_set: Tuple[str, str]) -> str:
    """return the joined label or 'reject' if the label is blank"""
    return "".join(label_set) or "reject"


def load_labels(source: Source) -> Dict[str, List[str]]:
    """make the list of labels, where Column index maps to the position in each list"""
    labels = [c.labels for c in source.column_set.all()]
    main, sub = zip(*labels)
    labels = {"main": main, "sub": sub, "label": [label_or_reject(x) for x in labels]}
    return labels


def analyze_dataframe(df: pd.DataFrame, labels: Dict[str, List[str]]) -> pd.DataFrame:
    """analyze all columns in a DataFrame and return a DataFrame of results"""
    # Make a container for the results of our analysis
    _df = pd.DataFrame()

    # write labels for magical mAcHiNe LeArNiNg
    _df["main"] = labels["main"]
    _df["sub"] = labels["sub"]
    _df["label"] = labels["label"]

    # mean token metrics aggregated across each column
    _df["mean_token_count"] = df.apply(mean_token_count).values
    _df["mean_token_length"] = df.apply(mean_token_length).values

    # fraction metrics aggregated across each column
    _df["frac_digit"] = df.apply(lambda rows: frac_fxn(count_digits, rows)).values
    _df["frac_alpha"] = df.apply(lambda rows: frac_fxn(count_letters, rows)).values
    _df["frac_space"] = df.apply(lambda rows: frac_fxn(count_spaces, rows)).values
    _df["frac_other"] = df.apply(lambda rows: frac_fxn(count_other_text, rows)).values

    # line length metrics
    _df["mean_line_length"] = df.apply(lambda rows: avg_len(np.mean, rows)).values
    _df["median_line_length"] = df.apply(lambda rows: avg_len(np.median, rows)).values
    _df["std_line_length"] = df.apply(lambda rows: avg_len(np.std, rows)).values

    # unique char / token metrics
    _df["unq_char_count"] = df.apply(unq_char_count).values
    _df["unq_token_count"] = df.apply(unq_token_count).values

    # list-matching metrics - fractional token counts for exact matches
    _df["frac_given"] = df.apply(lambda rows: frac_token(rows, assets.given)).values
    _df["frac_surnames"] = df.apply(
        lambda rows: frac_token(rows, assets.surnames)
    ).values
    _df["frac_states"] = df.apply(lambda rows: frac_token(rows, assets.states)).values
    _df["frac_canada"] = df.apply(lambda rows: frac_token(rows, assets.canada)).values
    _df["frac_cities"] = df.apply(lambda rows: frac_token(rows, assets.cities)).values
    _df["frac_counties"] = df.apply(
        lambda rows: frac_token(rows, assets.counties)
    ).values
    _df["frac_us_zip"] = df.apply(
        lambda rows: frac_token(rows, assets.zipcodes, left=5)
    ).values
    _df["frac_fips"] = df.apply(lambda rows: frac_token(rows, assets.fips)).values

    # Canadian zipcode pattern w/ pipe sep because of possible space in there
    _df["frac_can_zip_patt"] = df.apply(
        lambda rows: frac_regex(rows, r"^\w\d\w *\d\w\d$", sep="|")
    ).values

    # number of rows tagged on each column
    _df["row_count"] = df.apply(lambda rows: len(rows)).values

    return _df.transpose()


def json_fp(src_doc: File) -> str:
    """make a json filepath from a Source.document's path"""
    bn = os.path.basename(src_doc.name)
    return os.path.join("analysis", ".".join([bn.split(".")[0], "json"]))


def write_data(data: pd.DataFrame, filepath: str) -> None:
    """write some data to a file as json"""
    data.to_json(filepath)


def batch_analysis() -> None:
    """pull all applicable Source models and analyze the documents"""
    sources = Source.objects.filter(
        document__isnull=False, time_classified__isnull=False
    )
    for source in sources:
        df = load_csv(source.document)
        labels = load_labels(source)
        data = analyze_dataframe(df, labels)
        write_data(data, json_fp(source.document))
