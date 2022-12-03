import re
from prophet.serialize import model_to_json, model_from_json
from prophet import Prophet
import pandas as pd
import matplotlib.pyplot as plt
import psycopg2
import seaborn as sns
import pandas.io.sql as sqlio
from sklearn.metrics import r2_score
import datetime
import pandas as pd


hostname = 'localhost'
port = '5432'
username = 'postgres'
password = 'password'
database = 'water_quality'

# Try to connect

try:
    conn = psycopg2.connect(host=hostname, user=username,
                            password=password, dbname=database, port=port)
    print('connected')
except:
    print("I am unable to connect to the database.")

cur = conn.cursor()


def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)


def stan_init(m):
    res = {}
    if m.mcmc_samples == 0:
        for pname in ['k', 'm', 'sigma_obs']:
            res[pname] = m.params[pname][0][0]
        for pname in ['delta', 'beta']:
            res[pname] = m.params[pname][0]
    else:
        for pname in ['k', 'm', 'sigma_obs']:
            res[pname] = m.params[pname]
        for pname in ['delta', 'beta']:
            res[pname] = m.params[pname]
    return res


def train_prophet_model(sensor_name):

    sql = """select replace(Replace(temperatuur_date, 'T', ' '), 'Z', '')::timestamp as ds,
            temperatuur_value, conductiviteit_value as y from public.water_quality
            where temperatuur_sensor = '""" + sensor_name + """'
            order by replace(Replace(temperatuur_date, 'T', ' '), 'Z', '')::timestamp"""

    dat = sqlio.read_sql_query(sql, conn)

    dat.insert(0, 'id', range(0, 0 + len(dat)))
    print(dat)
    if len(dat)<20:
        print('no data')
    else:
        dat.drop_duplicates(subset=['ds'])

        print('training model for sensor: ', sensor_name)
        sensor_name_new = get_valid_filename(sensor_name)
        print(sensor_name_new)

        m = Prophet()
        m.fit(dat)  # df is a pandas.DataFrame with 'y' and 'ds' columns

        with open('serialized_model_'+sensor_name_new+'.json', 'w') as fout:
            fout.write(model_to_json(m))  # Save model

        print('prophet model is trained for sensor: ', sensor_name)


def run_prophet_model(sensor_name):

    sql = """select replace(Replace(temperatuur_date, 'T', ' '), 'Z', '')::timestamp as ds,
            temperatuur_value, conductiviteit_value as y from public.water_quality
            where temperatuur_sensor = '""" + sensor_name + """'
            order by replace(Replace(temperatuur_date, 'T', ' '), 'Z', '')::timestamp"""

    dat = sqlio.read_sql_query(sql, conn)

    dat.insert(0, 'id', range(0, 0 + len(dat)))
    print(dat)

    last_value = dat['ds'].iat[-1]
    print('Last value :', last_value)

    sensor_name_new = get_valid_filename(sensor_name)

    with open('serialized_model_'+sensor_name_new+'.json', 'r') as fin:
        m = model_from_json(fin.read())  # Load model

    n_hours = 24

    # today's date in timestamp
    base = last_value

    # calculating timestamps for the next 10 days
    timestamp_list = [
        base + datetime.timedelta(hours=x) for x in range(n_hours)]

    future = pd.DataFrame(timestamp_list, columns=['ds'])

    #future = m.make_future_dataframe(periods=2)

    forecast = m.predict(future)
    forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

    values_forecasting = forecast[forecast['ds'] > last_value]
    print('filtered')
    print(values_forecasting)

train_prophet_model('urn:ngsi-v2:cot-imec-be:WaterQualityObserved:imec-iow-XFHusUMR9spmCDhwDZ7At8')
run_prophet_model(
    'urn:ngsi-v2:cot-imec-be:WaterQualityObserved:imec-iow-XFHusUMR9spmCDhwDZ7At8')

def train_all_models():
    sql = """select * from (select distinct(id) from devices) as q"""
    devices = sqlio.read_sql_query(sql, conn)
    print(devices)
    for row in devices.iterrows():
        print(row[1][0])
        train_prophet_model(str(row[1][0]))
    
#train_all_models()