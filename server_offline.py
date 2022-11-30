from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import sys
import rdflib
import sys
import data_processing.ttl2jsonld
import data_processing.crawled
from rdflib import Graph, plugin
from functools import lru_cache
from rdflib import Graph, URIRef, Literal, BNode
from rdflib import Graph, Namespace
from rdflib.namespace import FOAF, RDF
from river import datasets
from river import metrics
from river import time_series
import datetime as dt
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import r2_score
from rdflib import Graph, URIRef, Literal, BNode
from rdflib.namespace import FOAF, RDF
import offline_ml.prophet_output
import data_processing.get_dataframe_sensor as get_dataframe_sensor


def mae(y_true, predictions):
    """calculates Mean Absolute Error

    Args:
        y_true (list): true y values
        predictions (list): predicted values

    Returns:
        float: Mean absolute error of forecasting model
    """
    y_true, predictions = np.array(y_true), np.array(predictions)
    return np.mean(np.abs(y_true - predictions))


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
evaluation = []


class webserverHandler(BaseHTTPRequestHandler):
    """docstring for webserverHandler"""

    def do_GET(self):
        try:
            if self.path.endswith("/output"):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()

                """
                output = ""
                output += '<html><body>Hello!'
                output += '<form method="POST" enctype="multipart/form-data" action="/hello"><h2> What would you like me to say?</h2><input name="message" type="text" /><input type="submit" value="Submit" /></form>'
                output += '</body></html>'
                """

                output = One().get_a()

                self.wfile.write(output.encode())
                # print(output)
                return

        except IOError:
            self.send_error(404, f"File not found {self.path}")

    def do_POST(self):
        try:
            if self.path.endswith("/input"):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                ctype, pdict = cgi.parse_header(
                    self.headers.get('Content-Type'))

                content_len = int(self.headers.get('Content-length'))
                post_body = self.rfile.read(content_len)
                print('POST request input:')
                print(post_body)


                #Get sensor_id
                sensor_name = data_processing.crawled.crawl_sensor_id(post_body)
                print(sensor_name)
                
                #get dataframe out timescaleDb
                dataframe_sensor = get_dataframe_sensor.get_df_sensor(str(sensor_name))
                print(dataframe_sensor)
                
                #runs a Prophet model on timeseries defined by time and conductivity
                test = offline_ml.prophet_output.prophet_output(dataframe_sensor, 'time', 'conductivity') 
                print(test)
                One().set_a(test)
                
                
                
                # ADD PREDICTION TO GRAPH
                self.wfile.write(test.encode())
                return
        except:
            #self.send_error(404, "{}".format(sys.exc_info()[1]))
            print(sys.exc_info())


def main():
    try:
        port = 8000
        server = HTTPServer(('', port), webserverHandler)
        print(f"Web server running on port {port}")
        server.serve_forever()

    except KeyboardInterrupt:
        print(" ^C entered stopping web server...")
        server.socket.close()


if __name__ == '__main__':
    main()
