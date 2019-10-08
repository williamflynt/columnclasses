"""Small functions to clean up readability of the dataframe processing"""
import itertools
from typing import Callable, List

import numpy as np
import pandas as pd


def tokenize(s: str, sep: str = None) -> List[str]:
    """split a string according to a separator (or Python default)"""
    if not isinstance(s, str):
        s = str(s)
    if sep is not None:
        return s.split(sep)
    return s.split()


def mean_token_count(rows: pd.Series, sep: str = None) -> float:
    """get the mean token count for each cell in a column"""
    result = np.mean([len(tokenize(s, sep)) for s in rows])
    return result


def mean_token_length(rows: pd.Series, sep: str = None) -> float:
    """get the mean token length for each cell in a column"""
    tokenized = [tokenize(s) for s in rows]
    tokens = list(itertools.chain.from_iterable(tokenized))
    if not tokens:
        return -1
    result = np.mean([len(t) for t in tokens])
    return result


def avg_len(avg_fxn: Callable, rows: pd.Series) -> float:
    """compute the average line length according to a passed averaging function"""
    return avg_fxn([len(str(s)) for s in rows])


def extract_chars(item) -> set:
    """get characters from a string, or list of strings, or list of list of strings"""
    if isinstance(item, str):
        return set(item)
    else:
        # recursion is fun!
        return extract_chars(
            "".join([str(i) for i in itertools.chain.from_iterable([item])])
        )


def unq_char_count(rows: pd.Series) -> int:
    """count the number of unique characters across an entire column"""
    return len(extract_chars(rows))


def unq_token_count(rows: pd.Series, sep=None) -> int:
    """count the number of unique tokens across an entire column"""
    aggregated = f"{sep or ' '}".join([str(r) for r in rows])
    tokens = tokenize(aggregated)
    return len(set(tokens))


def count_digits(s):
    """counts 0 thru 9 in strings"""
    return sum(c.isdigit() for c in s)


def count_letters(s):
    """counts A a thru Z z in strings"""
    return sum(c.isalpha() for c in s)


def count_spaces(s):
    """counts spaces"""
    return sum(c.isspace() for c in s)


def count_other_text(s):
    """counts non alphanum, non whitespace"""
    return len(s) - count_digits(s) - count_letters(s) - count_spaces(s)


def frac_fxn(fxn, rows) -> float:
    """
    calculates the numerator and denominator for functions requiring fractions

    1. Join the rows as one string (with no whitespace to avoid adding characters)
    2. Calculate the fraction function for the joined string
    3. Divide by the number of characters in the joined string
    4. Return that result

    Note: An empty column will produce a ZeroDivisionError - so let's just return -1
    """
    aggregated = "".join([str(r) for r in rows])
    fxn_result = fxn(aggregated)
    try:
        result = fxn_result / len(aggregated)
    except ZeroDivisionError:
        return -1
    return result


def frac_token(rows: pd.Series, asset: set, sep: str = None, left: int = None) -> float:
    """get the fraction of tokens that match a set of canonical tokens"""
    aggregated = f"{sep or ' '}".join([str(r) for r in rows])
    tokens = tokenize(aggregated)
    if not tokens:  # guard against empty column
        return -1
    match = 0
    for t in tokens:
        x = t[:left] if left else t
        if x.lower() in asset:
            match += 1
    return match / len(tokens)
