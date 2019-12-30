import pandas as pd
import numpy as np

def detect_rise(df, signal_name, criteria):
    """
    This function detect rising signal point and return the index time.
    
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

def detect_down(df, signal_name, criteria):
    """
    This function detect down signal point and return the index time.
    
    Args:
        df : dataframe which include time series data
        signal_name: The name of signal which is detected 
        criteria : The value for judging down
    
    Returns:
        rise_time: list of time of signal rising
    """
    df[signal_name] = df[signal_name].map(lambda x: 0 if x >= criteria else 1)
    df[signal_name + '_point'] = df[signal_name].diff()==1
    down_time = list(df.loc[df[signal_name + '_point']].index.values)
    return down_time

def ave_move(df, dt, sampling, signal_name):
    """
    This function add moving average of selecting signal to dataframe.
    
    Args:
        df : dataframe which include time series data that\
        includes signal gives moving average process
        dt : moving average period
        sampling : sampling time of signal that is index
        signal_name: The name of signal which is processed by moving average 
    
    Returns:
        df: dataframe include moving average signal
    """
    n = int(dt / sampling)
    #df['F_CH_rise'] = df.F_CH.diff()==1
    df[signal_name + '_mean'] = df[signal_name].rolling(n, center = True).mean()
    return df

def window_data(df, w_t, F_CH_point):
    """
    This function return extracting dataframe.
    
    Args:
        df : dataframe which include time series data
        w_t: window for extracting data 
        F_CH_point : The mid point of extracting data
    
    Returns:
        df_W : dataframe which is extracted
    """   
    
    t_point = df[df[F_CH_point]].index.values[0]
    df_W = df[df.index.map(lambda x: True if (x < t_point + w_t) & (x > t_point - w_t) else False )].copy()
    df_W.index = np.arange(0, len(df_W))/100
    return df_W
