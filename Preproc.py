import pandas as pd
import numpy as np
import matplotlib as plt


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_categorical(s):
    try:
        float(s)
        return False or pd.isnull(s)
    except ValueError:
        return True


def get_total_numeric_features(dataframe):
    total = 0
    for key in dataframe.keys():
        check = True
        not_empty = False
        for value in dataframe[key]:
            not_empty = not_empty or (not pd.isnull(value))
            check = is_number(value)
            if not check:
                break
        total += int(check) * int(not_empty)
    return total


def get_total_categorical_features(dataframe):
    total = 0
    for key in dataframe.keys():
        check = True
        not_empty = False
        for value in dataframe[key]:
            not_empty = not_empty or (not pd.isnull(value))
            check = is_categorical(value)
            if not check:
                break
        total += int(check) * int(not_empty)
    return total
