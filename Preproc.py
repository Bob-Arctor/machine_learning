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
    
    
def split_complete_data(df):
    #returns set with complete samples 
    #and a set of samples with some of the features missing    
    return df[pd.isnull(df).any(axis=1).apply(np.logical_not)], df[pd.isnull(df).any(axis=1)]
