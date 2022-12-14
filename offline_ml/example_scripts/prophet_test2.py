import time
from prophet.serialize import model_to_json, model_from_json
from prophet import Prophet
import pandas as pd
import matplotlib.pyplot as plt
import psycopg2
import seaborn as sns
import pandas.io.sql as sqlio
from sklearn.metrics import r2_score

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


sql = """select replace(Replace(temperatuur_date, 'T', ' '), 'Z', '')::timestamp as ds,
        temperatuur_value, conductiviteit_value as y from public.water_quality
        where temperatuur_sensor = 'urn:ngsi-v2:cot-imec-be:Device:aqf-iow-JX3CPbvBck498C3uan9KNg'
        order by replace(Replace(temperatuur_date, 'T', ' '), 'Z', '')::timestamp"""

dat = sqlio.read_sql_query(sql, conn)

dat.insert(0, 'id', range(0, 0 + len(dat)))
print(dat)

last_value = dat['ds'].iat[-1]
print('Last value :', last_value)


dat.drop_duplicates(subset=['ds'])


# import the builtin time module

# Grab Currrent Time Before Running the Code
start = time.time()
print(start)



m = Prophet()
m.fit(dat)  # df is a pandas.DataFrame with 'y' and 'ds' columns


end = time.time()
total_time = end - start
print("\n" + str(total_time))

with open('serialized_model.json', 'w') as fout:
    fout.write(model_to_json(m))  # Save model



with open('serialized_model.json', 'r') as fin:
    m = model_from_json(fin.read())  # Load model



future = m.make_future_dataframe(periods=2)
forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

values_forecasting = forecast[forecast['ds'] > last_value]
print('filtered')
print(values_forecasting)

total_time = time.time() - end
print("\n" + str(total_time))


# Python




