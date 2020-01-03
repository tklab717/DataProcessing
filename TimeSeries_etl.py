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

def get_d_signal(df, dt, sampling, signal_name):
    """
    This fucntion return dataset that includes signal features.
    The features are maximum width of singnal
    
    Args:
        df : dataframe which include time series index and signal which you want to get features
        dt: window size in which maximum width of signal is calculated
        sampling: sampling time
        signal_name: the name of the signal which is extracted signal features
    
    Returns:
        dict_set:extracted signal features(dmax, mintime_value, maxtime_value, mintime, maxtime)
    """   
    n = int(dt / sampling)
    df[signal_name + '_max'] =df[signal_name].rolling(n, center=True).max()
    df[signal_name + '_min'] = df[signal_name ].rolling(n, center= True).min()
    df[signal_name + '_delta'] = df[signal_name + '_max'] - df[signal_name + '_min']
    signal_dmax = np.nanmax(df[signal_name + '_delta'])
    df['F_' + signal_name + '_max_d'] =df[signal_name + '_delta'] .map(lambda x : 1 if x == signal_dmax else 0)
    pos_mm = df[df['F_' + signal_name + '_max_d'].diff().map(lambda x: abs(x)) == 1].index.values
    min_t = round(pos_mm[1] - dt/2 - sampling , 2)
    max_t = round(pos_mm[0] + dt/2- sampling , 2)
    min_value = df[df.index.values.round(3) == min_t][signal_name].values[0]
    max_value = df[df.index.values.round(3)  == max_t][signal_name].values[0]
    dict_set = {"dmax":signal_dmax, "mintime_value":min_value, "maxtime_value":max_value,"mintime":min_t, "maxtime":max_t}
    return dict_set

def plot_signal(df_W, features_sig, plot_sig, y1_name, y2_name, x_name):
    """
    This fucntion return figure that describe scatter plot that include 2 signals with max and min plot.
    
    Args:
        df_W : dataframe which include time series index and two signal 
        features_sig : dictionary that include features(dmax, mintime_value, maxtime_value, mintime, maxtime)
        plot_sig: list that are 1st and 2nd signal.
        y1_name: plot 1st axis name
        y2_name: plot 2nd axis name
        x_name:plot x axis name
    
    Returns:
        fig: scatter plot
    """   
      
    fig = df_W[[i for i in plot_sig]].plot(secondary_y=[y2_name], figsize=(7,4),legend="best",grid=True)
    fig.scatter([features_sig['mintime'], features_sig['maxtime']],[features_sig['mintime_value'], features_sig['maxtime_value']], color = 'red')
    # 左y軸のラベル
    fig.set_ylabel(y1_name, fontsize=15)

    # 右y軸のラベル
    fig.right_ax.set_ylabel(y2_name, fontsize=15)

    # x軸のラベル
    fig.set_xlabel(x_name, fontsize=15)
    
    # 左y軸の描画範囲 Auto range 
    fig.set_ylim(round(df_W[y1_name].min()/0.3,0), round(df_W[y1_name].max()/0.3,0))

    # 右y軸の描画範囲
    fig.right_ax.set_ylim(0,1)

    return fig