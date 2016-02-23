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
    # returns set with complete samples
    # and a set of samples with some of the features missing
    complete = df[pd.isnull(df).any(axis=1).apply(np.logical_not)]
    missing = df[pd.isnull(df).any(axis=1)]
    return complete, missing


def split_features_by_type(df):
    # boolean df showing where numerics are
    criteria = df.applymap(lambda x: isinstance(x, (int, float)))
    numeric_df = df[df.columns[criteria.all().values]]
    character_df = df[df.columns[~criteria.all().values]]
    return numeric_df, character_df


def is_characteristic_series(series):
    # checks if series is char or nan
    var = not series.apply(lambda x: np.isreal(x) and not pd.isnull(x)).any()
    return var


def is_numeric_series(series):
    # checks if series is numeric or nan
    return series.apply(lambda x: np.isreal(x)).all()


def series_type(series):
    if is_numeric_series(series):
        return 'Number'
    else:
        return 'Category'


def standardize_df(df):
    # will return new dataframe shifted to mean and divided by std
    # mean and std dfs will be passed as second and third result
    mean_df = df.mean(axis=0)
    std_df = df.std(axis=0)
    transformed = df.subtract(mean_df, axis=1)
    transformed = transformed.divide(std_df, axis=1)
    return transformed, mean_df, std_df


def back_transform(df, mean_df, std_df):
    original = df.multiply(std_df, axis=1)
    original = original.add(mean_df, axis=1)
    return original
