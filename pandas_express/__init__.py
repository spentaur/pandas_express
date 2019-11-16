import pandas as pd
import pandas_flavor as pf
import re


@pf.register_dataframe_method
def split_date(df, intervals='some'):
    """
    all = ['year',
    'month',
    'day',
    'hour',
    'minute',
    'dayofyear',
    'weekofyear',
    'dayofweek',
    'quarter',
    'second',
    'microsecond',
    'nanosecond',
    'is_month_start',
    'is_month_end',
    'is_quarter_start',
    'is_quarter_end',
    'is_year_start',
    'is_year_end',
    'is_leap_year']

    some = ['year',
    'month',
    'day',
    'hour',
    'minute',
    'dayofyear',
    'weekofyear',
    'dayofweek',
    'quarter']
    """

    features = ['year',
                'month',
                'day',
                'hour',
                'minute',
                'dayofyear',
                'weekofyear',
                'dayofweek',
                'quarter',
                'second',
                'microsecond',
                'nanosecond',
                'is_month_start',
                'is_month_end',
                'is_quarter_start',
                'is_quarter_end',
                'is_year_start',
                'is_year_end',
                'is_leap_year']

    if intervals == 'all':
        intervals = features
    elif intervals == 'some':
        intervals = features[:10]

    assert isinstance(intervals, list)

    assert 'Date' in df

    df['Date'] = pd.to_datetime(df['Date'])

    for interval in intervals:
        df[interval] = getattr(df['Date'].dt, interval)

    return df


@pf.register_series_method
@pf.register_dataframe_method
def percent_missing(df):
    nulls = df.isna().sum()
    return (nulls[nulls > 0] / len(df) *
            100).sort_values(ascending=False)


@pf.register_dataframe_method
def drop_single_value_columns(df):
    nunique = df.nunique()
    return df.drop(nunique[nunique == 1].index.tolist(), axis=1)


@pf.register_dataframe_method
def drop_mostly_missing_columns(df, thresh=50):
    missing = df.percent_missing()
    return df.drop(
        missing[missing >= thresh].index.tolist(), axis=1)


@pf.register_dataframe_method
def get_cardinality(df, ascending=False):
    nunique = df.nunique().sort_values(ascending=ascending)
    return nunique


@pf.register_dataframe_method
def get_low_cardinality(df, thresh=10, ascending=False):
    nunique = get_cardinality(df, ascending)
    return nunique[nunique <= thresh]


@pf.register_dataframe_method
def get_high_cardinality(df, thresh=10, ascending=False):
    nunique = get_cardinality(df, ascending)
    return nunique[nunique <= thresh]


def rename_columns(df, method, columns=None, inplace=False):
    if columns:
        columns_dict = {column: getattr(column, method)() for column in
                        columns}
    else:
        columns_dict = {column: getattr(column, method)() for column in
                        df.columns}

    if inplace:
        df.rename(columns=columns_dict, inplace=inplace)
    else:
        return df.rename(columns=columns_dict)


@pf.register_dataframe_method
def set_column_name_capitalize(df, columns=None, inplace=False):
    return rename_columns(df, 'capitalize', columns, inplace)


@pf.register_dataframe_method
def set_column_name_lowercase(df, columns=None, inplace=False):
    return rename_columns(df, 'lower', columns, inplace)


@pf.register_dataframe_method
def set_column_name_uppercase(df, columns=None, inplace=False):
    return rename_columns(df, 'upper', columns, inplace)


@pf.register_dataframe_method
def remove_special_chars_from_column_name(df, columns=None, inplace=False):
    if columns:
        columns_dict = {column: re.sub('[^A-Za-z0-9]+', '_', column) for
                        column in columns}
    else:
        columns_dict = {column: re.sub('[^A-Za-z0-9]+', '_', column) for
                        column in
                        df.columns}

    if inplace:
        df.rename(columns=columns_dict, inplace=inplace)
    else:
        return df.rename(columns=columns_dict)


__version__ = "0.0.5"
