import pandas as pd
import numpy as np

def tsma(arr, window_size):
    # Pad the array with zeros on both sides
    padded_arr = np.pad(arr, (window_size // 2, window_size // 2), mode='constant')
    
    # Calculate the moving average using convolution
    weights = np.ones(window_size) / window_size
    moving_avg = np.convolve(padded_arr, weights, mode='valid')
    
    return moving_avg



data = pd.DataFrame({'orig': np.zeros(50)})
data.loc[24, 'orig'] = 10
data['MA5'] = tsma(data['orig'], 5)
data['MA5-5'] = tsma(data['MA5'], 5)
data.plot()