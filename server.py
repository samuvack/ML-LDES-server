from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import sys
import rdflib
import sys
import data_processing.ttl2jsonld
import data_processing.crawled
import ml_tests.regression_input
#import data_processing.add_tripple
from rdflib import Graph, plugin
from functools import lru_cache
from rdflib import Graph, URIRef, Literal, BNode
from rdflib.namespace import FOAF, RDF


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

                # LINEAR REGRESSION
                print('--running regression models--')
                print('estimated temperature based on linear regression:')
                print(ml_tests.regression_input.run_linear_model(float(salinity)))
                temp_lin = str(ml_tests.regression_input.run_linear_model(float(salinity)))
                temp_lin = Literal(temp_lin)

                # MULTIPLE LINEAR REGRESSION
                print('estimated temperature based on polynomial regression:')
                print(ml_tests.regression_input.run_multiple_lin_regression(float(salinity)))
                temp_mul_lin = str(ml_tests.regression_input.run_multiple_lin_regression(float(salinity)))
                temp_mul_lin = Literal(temp_mul_lin)

                # DECISION TREE REGRESSION
                print('estimated temperature based on decision tree regression:')
                print(ml_tests.regression_input.run_decisiontreeregressor(float(salinity)))
                temp_dec_tree = str(ml_tests.regression_input.run_decisiontreeregressor(float(salinity)))
                temp_dec_tree = Literal(temp_dec_tree)

                #ADDING TON JSON-LD
                g.add((Literal('temp_lin'), RDF.value, temp_lin))
                g.add((Literal('temp_mul_lin'), RDF.value, temp_mul_lin))
                g.add((Literal('temp_dec_tree'), RDF.value, temp_dec_tree))
                print(g.serialize())
                test = str(g.serialize())

                One().set_a(test)

                ##ADD PREDICTION TO GRAPH
                self.wfile.write(test.encode())
                return
        except:
            self.send_error(404, "{}".format(sys.exc_info()[1]))
            #print(sys.exc_info())

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