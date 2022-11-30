from prophet import Prophet
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas.io.sql as sqlio
from sklearn.metrics import r2_score


def prophet_output(dat, time_parameter, value_parameter):
    """Runs forecasting model Prophet

    Args:
        dat (dataframe): ds, y columns in dataframe give info about time series

    Returns:
        dataframe: forecasting output in the form of a dataframe
    """
    dat.rename(columns={str(time_parameter): 'ds'}, inplace=True)
    dat.rename(columns={str(value_parameter): 'y'}, inplace=True)
    
    dat = dat.drop_duplicates(subset=['ds'])
    print('cleaned dataframe')
    print(dat)
    
    if len(dat)<20:
        return
    else:    
        last_value = dat['ds'].iat[-1]
        print(last_value)
        m = Prophet()
        # df is a pandas.DataFrame with 'y' and 'ds' columns
        m.fit(dat)
        print(m)
        future = m.make_future_dataframe(periods=2)
        print(future)
        forecast = m.predict(future)
        print('forecast')
        print(forecast)
        print(forecast['ds'])
        values_forecasting = forecast[forecast['ds'] > last_value]
    return values_forecasting
