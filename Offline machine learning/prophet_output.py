from prophet import Prophet
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas.io.sql as sqlio
from sklearn.metrics import r2_score


def prophet_output(dat):
    """Runs forecasting model Prophet

    Args:
        dat (dataframe): ds, y columns in dataframe give info about time series

    Returns:
        dataframe: forecasting output in the form of a dataframe
    """
    dat.drop_duplicates(subset=['ds'])
    last_value = dat['ds'].iat[-1]
    m = Prophet()
    # df is a pandas.DataFrame with 'y' and 'ds' columns
    m.fit(dat)
    future = m.make_future_dataframe(periods=2)
    forecast = m.predict(future)
    values_forecasting = forecast[forecast['ds']
                                  > last_value]
    return values_forecasting



