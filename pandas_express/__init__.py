import pandas as pd
import pandas_flavor as pf


@pf.register_dataframe_method
def split_date(df, intervals='some'):
    '''
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
    '''

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
    percent_missing = df.percent_missing()
    return df.drop(
        percent_missing[percent_missing >= thresh].index.tolist(), axis=1)


__version__ = "0.0.4"
