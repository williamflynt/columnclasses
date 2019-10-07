"""Small functions to clean up readability of the dataframe processing"""
import numpy as np


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


def frac_fxn(fxn, rows):
    """calculates the numerator and denominator for functions requiring fractions"""
    s = 0  # prevents an error
    return np.sum([fxn(str(s)) for s in rows]) / np.sum([len(str(s)) for s in rows])
