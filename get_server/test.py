from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import sys
import rdflib
import sys
from rdflib import Graph, plugin
from functools import lru_cache
import datetime as dt
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import psycopg2
import numpy as np  # linear algebra
import pandas.io.sql as sqlio

HOSTNAME = 'localhost'
PORT = '5432'
USERNAME = 'postgres'
PASSWORD = 'password'
DATABASE = 'water_quality'

# Try to connect

try:
    conn = psycopg2.connect(host=HOSTNAME, user=USERNAME,
                            password=PASSWORD, dbname=DATABASE, port=PORT)
    print('connected')
except:
    print("I am unable to connect to the database.")

cur = conn.cursor()


@lru_cache(maxsize=2048)
class One(object):
    def __init__(self):
        self.a = None

    def set_a(self, val):
        self.a = val

    def get_a(self):
        return self.a


One().set_a('There is no POST request received yet in the ml server')

file_names = []
y_list = []
time_history = [0]
temperature_history = []

sql = """select * from trained_models ;"""
devices = sqlio.read_sql_query(sql, conn)
devices.insert(0, 'row', range(0, 0 + len(devices)))
for row in devices.iterrows():
    print(row[1][0])
    print(row[1][1])
    print(row[1][2])