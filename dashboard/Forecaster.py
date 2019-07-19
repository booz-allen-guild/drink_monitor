# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 13:23:46 2019

@author: 598455
"""
# Import Libraries
import pandas as pd
import pymysql
from statsmodels.tsa.arima_model import ARIMA
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split


## Function to Aggregate a dataset at the seconds level
def aggregate(df): 
    df['timestamp'] = pd.to_datetime(df.time_taken, format='%d-%m-%Y %H:%M:%S')
    df.index = df.timestamp
    df = df.resample('S').mean().ffill()
    
    return df

time_df = aggregate(time_df)


## Creating a DF for each keg and breaking it into train & test
keg1_df = time_df.iloc[:,:3]
keg1_train, keg1_test = train_test_split(keg1_df.keg1_reading, test_size=0.25, random_state=42, shuffle=False)

keg2_df = time_df.iloc[:,[0,1,3]]
keg2_train, keg2_test = train_test_split(keg2_df.keg2_reading, test_size=0.25, random_state=42, shuffle=False)

keg3_df = time_df.iloc[:,[0,1,4]]
keg3_train, keg3_test = train_test_split(keg3_df.keg3_reading, test_size=0.25, random_state=42, shuffle=False)

keg4_df = time_df.iloc[:,[0,1,5]]
keg4_train, keg4_test = train_test_split(keg4_df.keg4_reading, test_size=0.25, random_state=42, shuffle=False)



## Function that Plots Arima Forcast 
## Inputs: Training Dataset, Test Dataset 
def arima_forecaster(train, test):
    # Build Model
    model = ARIMA(train, order=(3, 2, 1))  
    fitted = model.fit(disp=-1)  

    # Forecast
    fc, se, conf = fitted.forecast(len(test), alpha=0.05)  # 95% conf

    # Make as pandas series
    fc_series = pd.Series(fc, index=test.index)
    lower_series = pd.Series(conf[:, 0], index=test.index)
    upper_series = pd.Series(conf[:, 1], index=test.index)

    # Plot
    plt.figure(figsize=(12,5), dpi=100)
    plt.plot(train, label='training')
    plt.plot(test, label='actual')
    plt.plot(fc_series, label='forecast')
    plt.fill_between(lower_series.index, lower_series, upper_series, color='k', alpha=.15)
    plt.title('Forecast vs Actuals')
    plt.legend(loc='upper right', fontsize=8)
    plt.show()
