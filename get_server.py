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
import data_processing.output

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

class webserverHandler(BaseHTTPRequestHandler):
    """docstring for webserverHandler"""

    def do_GET(self):
        try:
            sql = """select * from trained_models ;"""
            devices = sqlio.read_sql_query(sql, conn)
            devices.insert(0, 'row', range(0, 0 + len(devices)))
            
            #create multiple endpoints on self.path per sensor_id in the form of /output/sensor_id
            for row in devices.iterrows():
                if self.path.endswith("/output/" + str(row[1][0])):
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/turtle')
                    self.end_headers()
                    
                    sql = """select * from public.forecast where sensor_id = '""" + str(row[1][1]) + """';"""
                    dat = sqlio.read_sql_query(sql, conn)
                    dat.insert(0, 'id', range(0, 0 + len(dat)))
                    print(dat)
                    
                    rdf = data_processing.output.createForecastingTimeseries(str(row[1][1]))
                    g = Graph().parse(data=rdf, format='n3')
                    
                    #iterate through dat dataframe and add the data to the rdf graph
                    for j in dat.iterrows():
                        data_processing.output.addForecastingMember(
                            g, j[1][1], j[1][2], row[1][1])  # adds new forecasting member to RDF
                    
                    context = {"@vocab": "http://purl.org/dc/terms/", "@language": "en"}

                    output = g.serialize(
                        format='n3', context=context, indent=4)
                    print(output)
                    #output = One().get_a()
                    #output = output + str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + '_nu_komt_het_' + str(row[1][0])

                    self.wfile.write(output.encode())
                    #print(output)
                    return

        except IOError:
            self.send_error(404, "File not found %s" % self.path)

def main():
    try:
        port = 8000
        server = HTTPServer(('', port), webserverHandler)
        print("Web server running on port %s" % port)
        server.serve_forever()

    except KeyboardInterrupt:
        print(" ^C entered stopping web server...")
        server.socket.close()


if __name__ == '__main__':
    main()
