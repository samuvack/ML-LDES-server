from psycopg2.extensions import AsIs
import psycopg2
from multiprocessing import Pool
import datetime
import multiprocessing
# arrays and dataframes
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)



# visualization imports
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline

hostname = 'localhost:5432'
username = 'postgres'
password = 'password'
database = 'water_quality'

# Try to connect

try:
    conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
except:
    print("I am unable to connect to the database.")

cur = conn.cursor()

