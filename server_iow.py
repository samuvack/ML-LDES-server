from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import sys
import rdflib
import sys
import data_processing.ttl2jsonld
import data_processing.crawled
#import ml_tests.regression_input
#import data_processing.add_tripple
from rdflib import Graph, plugin
from functools import lru_cache
from rdflib import Graph, URIRef, Literal, BNode
from rdflib.namespace import FOAF, RDF

list = []

@lru_cache(maxsize=2048)
class One(object):
    def __init__(self):
        self.a = None

    def set_a(self,val):
        self.a = val

    def get_a(self):
        return self.a

One().set_a('There is no POST request received yet in the ml server')

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
                #print(post_body)

                ##CONVERSION TO JSON-LD
                print('conversion to json-ld:')
                print(data_processing.ttl2jsonld.convert_rdf_2_jsonld(post_body))
                input = data_processing.ttl2jsonld.convert_rdf_2_jsonld(post_body)
                
                
                g = Graph().parse(data=input, format='json-ld')
                #time = data_processing.crawled.crawl_parameter('http://www.w3.org/ns/prov#generatedAtTime', g)
                #print('crawled time is :' + time)


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
                    print(row[0])
                    print(row[1])
                    print(row[2])
                    if row[0].strip() == 'temperatuur':
                        print('juij')
                        temp = row[3].strip
                        sensor_name_t = row[2].strip()
                        time_temp = row[1].strip()
                if row[2].strip() == 'urn:ngsi-v2:cot-imec-be:device:imec-wqsensor-2047475712':
                    list.append(temp)


                if len(list) % 2 ==0:
                    import pickle
                    with open('list_1.ob', 'wb') as fp:
                        pickle.dump(list, fp)

                

                One().set_a(test)

                ##ADD PREDICTION TO GRAPH
                self.wfile.write(test.encode())
                return
        except:
            #self.send_error(404, "{}".format(sys.exc_info()[1]))
            #print(sys.exc_info())
            print('hallo')

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