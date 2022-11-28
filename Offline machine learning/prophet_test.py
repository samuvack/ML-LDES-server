import gradio as gr
import pypistats
from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd
from prophet import Prophet
pd.options.plotting.backend = "plotly"

def get_forecast(lib, time):

    data = pypistats.overall(lib, total=True, format="pandas")
    data = data.groupby("category").get_group("with_mirrors").sort_values("date")
    start_date = date.today() - relativedelta(months=int(time.split(" ")[0]))
    df = data[(data['date'] > str(start_date))] 

    df1 = df[['date','downloads']]
    df1.columns = ['ds','y']

    m = Prophet()
    m.fit(df1)
    future = m.make_future_dataframe(periods=90)
    forecast = m.predict(future)
    fig1 = m.plot(forecast)
    return fig1 

get_forecast("pandas", "3 months")

