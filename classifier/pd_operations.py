"""Small functions to clean up readability of the dataframe processing"""


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
        result = fxn_result/len(aggregated)
    except ZeroDivisionError:
        return -1
    return result
