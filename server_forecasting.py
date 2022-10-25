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
from rdflib.namespace import FOAF, RDF
from river import datasets
from river import metrics
from river import time_series
import datetime as dt
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

@lru_cache(maxsize=2048)
class One(object):
    def __init__(self):
        self.a = None

    def set_a(self,val):
        self.a = val

    def get_a(self):
        return self.a

One().set_a('There is no POST request received yet in the ml server')

file_names = []
y_list = []
time_history=[0]
temperature_history = []


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
                #print(output)
                return



        except IOError:
            self.send_error(404, "File not found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/input"):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                ctype, pdict = cgi.parse_header(self.headers.get('Content-Type'))


                content_len = int(self.headers.get('Content-length'))
                post_body = self.rfile.read(content_len)
                #pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                #pdict['CONTENT-LENGTH'] = content_len
                print('POST request input:')
                print(post_body)

                
                testrdf = """
                @prefix dcterms: <http://purl.org/dc/terms/> .
                <http://example.org/about>
                dcterms:temperature "10"@en ;
                dcterms:salinity "20"@en .
                """

                ##CONVERSION TO JSON-LD
                print('conversion to json-ld:')
                #print(data_processing.ttl2jsonld.convert_rdf_2_jsonld(post_body))
                input = data_processing.ttl2jsonld.convert_rdf_2_jsonld(post_body)
                
                g = Graph().parse(data=input, format='json-ld')
                salinity = data_processing.crawled.crawl_parameter('http://purl.org/dc/terms/salinity', g)
                print('crawled salinity is :' + salinity)

                #time = data_processing.crawled.crawl_parameter('http://purl.org/dc/terms/time', g)
                #print('crawled time is :' + time)

                temperature = data_processing.crawled.crawl_parameter('http://purl.org/dc/terms/temperature', g)
                print('crawled temperature is :' + temperature)
                temperature = float(temperature)
                temperature_history.append(float(temperature))

                model = time_series.HoltWinters(
                    alpha=0.1,
                    beta=0.1,
                    gamma=0.1,
                    seasonality=1,
                    multiplicative=True
                )

                """
                alpha: Smoothing parameter for the level.
                beta  (defaults to None): Smoothing parameter for the trend.
                gamma (defaults to None): Smoothing parameter for the seasonality.
                seasonality (defaults to 0): The number of periods in a season. For instance, this should be 4 for quarterly data, and 12 for yearly data.
                multiplicative (defaults to False): Whether or not to use a multiplicative formulation.
                """

                #Evalute TODO
                dataset = datasets.AirlinePassengers()
                metric = metrics.MAE()

                time_series.evaluate(
                    dataset,
                    model,
                    metric,
                    horizon=12
                )

                #Training Online Forecosting model
                horizon=12
                model = model.learn_one(temperature)
                print(model)
                
                #Online Forecasting
                forecast_output = model.forecast(horizon=horizon)
                print(forecast_output)
                t_list2=[]
                for i in range(len(forecast_output)):
                    t_list2.append(time_history[-1] + i )
                plt.figure()
                sns.set()

                #Plotting
                plt.scatter(time_history, temperature_history, c='r', alpha=0.6, s=4)
                plt.plot(time_history, temperature_history, linewidth=0.3)
                time_history.append(time_history[-1] + 1)
                print(forecast_output)
                plt.scatter(t_list2, forecast_output, c='b', alpha=0.6, s=4)
                plt.plot(t_list2, forecast_output, c='b', linewidth=0.3)
                plt.suptitle("Online Machine Learning (forecasting)", fontsize=18)
                plt.title("Iteration {y}".format(y=time_history[-1]), fontsize=10)
                plt.xlabel('Time')
                plt.ylabel('Value')
                plt.savefig("./output_ml/it_{y}.png".format(y=time_history[-1]))
                print("./output_ml/it_{y}.png".format(y=time_history[-1]))
                file_names.append("./output_ml/it_{y}.png".format(y=time_history[-1]))
                test = 'gelukt'
                One().set_a('gelukt')
                ##ADD PREDICTION TO GRAPH
                #self.wfile.write(test.encode())
                return
        except:
            #self.send_error(404, "{}".format(sys.exc_info()[1]))
            print(sys.exc_info())

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