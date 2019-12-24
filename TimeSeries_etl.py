import pandas as pd
import numpy as np

def detect_rise(df, signal_name, criteria):
     """
    This function detect rising signal point and return the index.
    
    Args:
        df : dataframe which include time series data
        signal_name: The name of signal which is detected 
        criteria : The value for judging rising
    
    Returns:
        rise_time: list of time of signal rising
    """
    df[signal_name] = df[signal_name].map(lambda x: 1 if x >= criteria else 0)
    df[signal_name + '_point'] = df[signal_name].diff()==1
    rise_time = list(df.loc[df[signal_name + '_point']].index.values)
    return rise_time