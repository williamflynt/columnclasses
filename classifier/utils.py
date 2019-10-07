import os
from typing import Dict, List

import numpy as np
import pandas as pd
from django.core.files import File

from classifier.models import Source
from classifier.pd_operations import (
    count_digits,
    count_letters,
    count_spaces,
    count_other_text,
    frac_fxn,
)


def load_csv(document: File) -> pd.DataFrame:
    """load a CSV from a Source.document field to a dataframe"""
    with document.open("r") as f:
        df = pd.read_csv(f)
    return df


def load_labels(source: Source) -> Dict[str, List[str]]:
    """make the list of labels, where Column index maps to the position in each list"""
    labels = [c.labels for c in source.column_set.all()]
    main, sub = zip(*labels)
    labels = {"main": main, "sub": sub, "label": ["".join(item) for item in labels]}
    return labels


def analyze_dataframe(df: pd.DataFrame, labels: Dict[str, List[str]]) -> pd.DataFrame:
    """analyze all columns in a DataFrame and return a DataFrame of results"""

    _df = pd.DataFrame()

    # write labels for magical mAcHiNe LeArNiNg
    _df['main'] = labels["main"]
    _df['sub'] = labels["sub"]
    _df['label'] = labels["label"]

    # mean token metrics aggregated across each column
    _df['mean_token_count'] = df.apply(lambda rows: np.mean([len(str(s).split()) for s in rows]))
    _df['mean_token_length'] = df.apply(lambda rows: np.mean([len(i.split()) for s in rows for i in str(s)]))

    # fraction metrics aggregated across each column
    _df['frac_digit'] = df.apply(lambda rows: frac_fxn(count_digits, rows))
    _df['frac_alpha'] = df.apply(lambda rows: frac_fxn(count_letters, rows))
    _df['frac_space'] = df.apply(lambda rows: frac_fxn(count_spaces, rows))
    _df['frac_other_text'] = df.apply(lambda rows: frac_fxn(count_other_text, rows))

    # line length metrics
    _df['mean_line_length'] = df.apply(lambda rows: np.mean([len(str(s)) for s in rows]))
    _df['median_line_length'] = df.apply(lambda rows: np.median([len(str(s)) for s in rows]))
    _df['std_line_length'] = df.apply(lambda rows: np.std([len(str(s)) for s in rows]))

    # unique char / token metrics
    _df['unq_char_count'] = df.apply(lambda rows: len(set([i for s in rows for i in str(s)])))
    _df['unq_token_count'] = df.apply(lambda rows: len(set([str(s) for s in rows])))

    # number of rows tagged on each column
    _df['row_count'] = df.apply(lambda rows: len(rows))

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
