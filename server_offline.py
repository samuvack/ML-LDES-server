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

import get_panda

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
                print(data_processing.ttl2jsonld.convert_rdf_2_jsonld(post_body))

                input = data_processing.ttl2jsonld.convert_rdf_2_jsonld(post_body)
                
                g = Graph().parse(data=input, format='json-ld')

                knows_query = """

                PREFIX sosa: <http://www.w3.org/ns/sosa/>
                PREFIX measure: <http://def.isotc211.org/iso19156/2011/Measurement#>
                PREFIX unitsofmeasure: <http://def.isotc211.org/iso19103/2005/UnitsOfMeasure#Measure.>
                PREFIX observation: <http://def.isotc211.org/iso19156/2011/Observation#OM_Observation.>
                PREFIX schema: <https://schema.org/>
                SELECT ?propertyname ?time ?sensor ?value
                WHERE {
                    ?reading a measure:OM_Measurement .
                    ?reading observation:observedProperty ?property .
                    ?reading observation:phenomenonTime ?time .
                    BIND (REPLACE(STR(?property), "^.*/([^/]*)$", "$1") as ?propertyname)
                    ?reading sosa:madeBySensor ?sensor .
                    ?reading observation:result/unitsofmeasure:value/schema:value ?value
                }
                """
               
                qres = g.query(knows_query)
                for row in qres:
                    sensor_name = row[2]
                    
                    output = get_panda.get_df_sensor("urn:ngsi-v2:cot-imec-be:Device:aqf-iow-JX3CPbvBck498C3uan9KNg")
                    print(output)

                

                from rdflib import URIRef, BNode, Literal

                bob = URIRef("http://example.org/people/Bob")
                linda = BNode()  # a GUID is generated

                name = Literal("Bob")  # passing a string
                age = Literal(24)  # passing a python int
                height = Literal(76.5)  # passing a python float

                from rdflib import Namespace

                n = Namespace("http://example.org/people/")

                n.bob  # == rdflib.term.URIRef("http://example.org/people/bob")
                n.eve  # == rdflib.term.URIRef("http://example.org/people/eve")


                from rdflib.namespace import CSVW, DC, DCAT, DCTERMS, DOAP, FOAF, ODRL2, ORG, OWL, \
                           PROF, PROV, RDF, RDFS, SDO, SH, SKOS, SOSA, SSN, TIME, \
                           VOID, XMLNS, XSD

                RDF.type
                # == rdflib.term.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")

                FOAF.knows
                # == rdflib.term.URIRef("http://xmlns.com/foaf/0.1/knows")

                PROF.isProfileOf
                # == rdflib.term.URIRef("http://www.w3.org/ns/dx/prof/isProfileOf")

                SOSA.Sensor
                # == rdflib.term.URIRef("http://www.w3.org/ns/sosa/Sensor")



                g = Graph()
                g.bind("foaf", FOAF)

                bob = URIRef("http://example.org/people/Bob")
                linda = BNode()  # a GUID is generated

                name = Literal("Bob")
                age = Literal(24)

                g.add((bob, RDF.type, FOAF.Person))
                g.add((bob, FOAF.name, name))
                g.add((bob, FOAF.age, age))
                g.add((bob, FOAF.knows, linda))
                g.add((linda, RDF.type, FOAF.Person))
                g.add((linda, FOAF.name, Literal("Linda")))

                test = g.serialize()
                print(test)



                One().set_a(test)

                ##ADD PREDICTION TO GRAPH
                self.wfile.write(test.encode())
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