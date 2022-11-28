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
import numpy as np
from sklearn.metrics import r2_score


def mae(y_true, predictions):
    y_true, predictions = np.array(y_true), np.array(predictions)
    return np.mean(np.abs(y_true - predictions))

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

                time_it = data_processing.crawled.crawl_parameter('http://purl.org/dc/terms/time', g)
                print('crawled time is :' + time_it)

                temperature = data_processing.crawled.crawl_parameter('http://purl.org/dc/terms/temperature', g)
                print('crawled temperature is :' + temperature)
                temperature = float(temperature)
                temperature_history.append(float(temperature))

                print (len(time_history))
                if len(time_history)==1:
                    global model
                    period = 12
                    model = time_series.SNARIMAX(
                    p=period,
                    d=1,
                    q=period,
                    m=period,
                    sd=1
                    )
                    
                    """
                    p (int): Order of the autoregressive part. This is the number of past target values that will be included as features.
                    d (int):Differencing order.
                    q (int):Order of the moving average part. This is the number of past error terms that will be included as features.
                    m (int) – defaults to 1:Season length used for extracting seasonal features. If you believe your data has a seasonal pattern, then set this accordingly. For instance, if the data seems to exhibit a yearly seasonality, and that your data is spaced by month, then you should set this to 12. Note that for this parameter to have any impact you should also set at least one of the p, d, and q parameters.
                    sp (int) – defaults to 0: Seasonal order of the autoregressive part. This is the number of past target values that will be included as features.
                    sd (int) – defaults to 0: Seasonal differencing order.
                    sq (int) – defaults to 0: Seasonal order of the moving average part. This is the number of past error terms that will be included as features.
                    """  

                #Training Online Forecosting model
                horizon=12
                model = model.learn_one(temperature)
                
                #Online Forecasting
                forecast_output = model.forecast(horizon=horizon)
                print(forecast_output)
                t_list2=[]
                for i in range(len(forecast_output)+1):
                    t_list2.append(time_history[-1] + i )
                forecast_output.insert(0, temperature_history[-1])

                plt.figure()
                sns.set()

                #Plotting
                print(forecast_output)
                evaluation.append(forecast_output)
                if (int(time_it) > 13):
                    current_values =  []
                for i in range(14, 1, -1):
                        current_values.append(temperature_history[-i])
                    print(str(r2_score(current_values, evaluation[int(time_it)-13])))
                    print(mae(current_values, evaluation[int(time_it)-13]))




                plt.scatter(t_list2, forecast_output, c='b', alpha=0.6, s=4)
                plt.plot(t_list2, forecast_output, c='orange', linewidth=0.3, label='Forecasted data')
                plt.scatter(time_history, temperature_history, c='r', alpha=0.6, s=6)
                plt.plot(time_history, temperature_history, linewidth=0.3, label='Historical data')
                time_history.append(time_history[-1] + 1)
                plt.suptitle("Online Machine Learning (forecasting)", fontsize=12)
                plt.title("Iteration {y}".format(y=time_history[-1]), fontsize=8)
                plt.legend(loc='upper right')
                plt.savefig("./output_ml/it_{y}.png".format(y=time_history[-1]))
                print("./output_ml/it_{y}.png".format(y=time_history[-1]))
                file_names.append("./output_ml/it_{y}.png".format(y=time_history[-1]))

                test = 'gelukt'
                One().set_a('gelukt')


                ##ADD PREDICTION TO GRAPH
                #self.wfile.write(test.encode())

                if (time_it == 140):
                    import imageio
                    images = []
                    for filename in file_names:
                        images.append(imageio.imread(filename))
                    imageio.mimsave('./output_ml/movie.gif', images)

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