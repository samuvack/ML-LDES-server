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
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import io

# Connect to an existing database
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

engine = create_engine('postgresql+psycopg2://postgres:password@localhost:5432/water_quality')

#get valid filename without strange characters
def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)

#initialise model - used in future for incremental learning on offline trained model
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




#run this function to train the model
def train_prophet_model(sensor_name):
    sql = """select replace(Replace(temperatuur_date, 'T', ' '), 'Z', '')::timestamp as ds,
            temperatuur_value, conductiviteit_value as y from public.water_quality
            where id = '""" + sensor_name + """'
            order by replace(Replace(temperatuur_date, 'T', ' '), 'Z', '')::timestamp"""

    dat = sqlio.read_sql_query(sql, conn)

    dat.insert(0, 'id', range(0, 0 + len(dat)))
    dat.drop_duplicates(subset=['ds'])
    print(dat)
    latest_timestamp = dat['ds'].iloc[-1]
    latest_timestamp = get_valid_filename(latest_timestamp)
    print(dat)
    if len(dat) < 20:
        print('no data')
    else:
        print('training model for sensor: ', sensor_name)
        sensor_name_new = get_valid_filename(sensor_name)
        print(sensor_name_new)

        m = Prophet()
        m.fit(dat)  # df is a pandas.DataFrame with 'y' and 'ds' columns
        current_model_name = 'serialized_model_' + \
            str(sensor_name_new) + '_' + str(latest_timestamp) + '.json'
        with open('../saved_models/offline_models/' + current_model_name, 'w') as fout:
            fout.write(model_to_json(m))  # Save model

        print('prophet model is trained for sensor: ', sensor_name)
        sensor_df = pd.DataFrame({
                    'sensor_id': [],
                    'timestamp': [],
                    'model': []
                })
        print('this is the sensor df: '+ str(sensor_df))
        sensor_df.loc[len(sensor_df.index)] = [sensor_name,
                                               latest_timestamp, current_model_name]
        print(sensor_df)
        #sensor_df.head(0).to_sql('trained_models', engine, if_exists='replace',index=False) #drops old table and creates new empty table
        cur = conn.cursor()
        output = io.StringIO()
        sensor_df.to_csv(output, sep='\t', header=False, index=False)
        output.seek(0)
        contents = output.getvalue()
        # null values become ''
        cur.copy_from(output, 'trained_models', null="")
        conn.commit()

#run this function to run the trained model
def run_prophet_model(sensor_name):
    print('start with forecasting: '+  sensor_name)

    sql = """select replace(Replace(temperatuur_date, 'T', ' '), 'Z', '')::timestamp as ds,
            temperatuur_value, conductiviteit_value as y from public.water_quality
            where id = '""" + sensor_name + """'
            order by replace(Replace(temperatuur_date, 'T', ' '), 'Z', '')::timestamp"""

    dat = sqlio.read_sql_query(sql, conn)
    dat.insert(0, 'id', range(0, 0 + len(dat)))
    dat.drop_duplicates(subset=['ds'], keep='last')
    print(dat)
    latest_timestamp = dat['ds'].iloc[-1]

    sql = """select * from trained_models order by timestamp asc"""
    sensor_df = sqlio.read_sql_query(sql, conn)
    latest_model = sensor_df[sensor_df['sensor_id'] == sensor_name]['model'].iloc[-1]
    print('latest model')
    print(latest_model)
    with open('../saved_models/offline_models/' + latest_model, 'r') as fin:
        m = model_from_json(fin.read())  # Load model

    n_hours = 24

    # today's date in timestamp
    base = latest_timestamp

    # calculating timestamps for the next 10 days
    timestamp_list = [
        base + datetime.timedelta(hours=x) for x in range(n_hours)]

    future = pd.DataFrame(timestamp_list, columns=['ds'])

    #future = m.make_future_dataframe(periods=2)

    forecast = m.predict(future)
    forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
    
    values_forecasting = forecast[forecast['ds'] > latest_timestamp]
    print('filtered')
    print(values_forecasting[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])
    forecasting = values_forecasting[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    forecasting['sensor_id'] = sensor_name
    forecasting['model'] = latest_model
    
    #forecasting.head(0).to_sql('forecast', engine, if_exists='replace',index=False) #drops old table and creates new empty table
    cur = conn.cursor()
    output = io.StringIO()
    forecasting.to_csv(output, sep='\t', header=False, index=False)
    output.seek(0)
    contents = output.getvalue()
    cur.copy_from(output, 'forecast', null="") # null values become ''
    conn.commit()


#train_prophet_model('urn:ngsi-v2:cot-imec-be:WaterQualityObserved:imec-iow-Syje969TMMBaREmT5G7XkA')
#run_prophet_model('urn:ngsi-v2:cot-imec-be:WaterQualityObserved:imec-iow-Syje969TMMBaREmT5G7XkA')

#train models for all sensors and put the list overview in the database
def train_all_models():
    sql = """select * from (select distinct(id) from devices) as q"""
    devices = sqlio.read_sql_query(sql, conn)
    print(devices)
    for row in devices.iterrows():
        print(row[1][0])
        train_prophet_model(str(row[1][0]))

#run all the models for all sensors
def run_all_models():
    sql = """select * from (select distinct(id) from devices) as q"""
    devices = sqlio.read_sql_query(sql, conn)
    print(devices)
    for row in devices.iterrows():
        print(row[[1][0]])
        run_prophet_model(str(row[1][0]))

#train_all_models()
run_all_models()