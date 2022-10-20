from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import sys
import rdflib
import sys
import data_processing.ttl2jsonld
import data_processing.crawled
import ml_tests.regression_input
#import ml_tests.add_tripple

from functools import lru_cache



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
            if self.path.endswith("/output_rdf"):
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

            """

            ##CONVERSION TO JSON-LD
            print('conversion to json-ld:')
            print(data_processing.ttl2jsonld.convert_rdf_2_jsonld(post_body))

            graph = data_processing.ttl2jsonld.convert_rdf_2_jsonld(post_body)
            g = Graph().parse(data=testrdf, format='n3')
            print(g)
            salinity = data_processing.crawled.crawl_parameter('http://purl.org/dc/terms/salinity', g)
            print('crawled salinity is :' + salinity)


            print('--Nu gaan we Linear model runnen--')
            print('Schatting temperatuur volgens linear regression:')
            print(ml_tests.regression_input.run_linear_model(salinity))
            temp_ml_lin = str(ml_tests.regression_input.run_linear_model(salinity))

            One().set_a(temp_ml_lin)
            
            """

            output = ""
            output += '<html><body>&#161Hola <a href="/hello">Back to Hello</a>'
            output += '<form method="POST" enctype="multipart/form-data" action="/hello"><h2> What would you like me to say?</h2><input name="message" type="text" /><input type="submit" value="Submit" /></form>'
            output += '</body></html>'

            ##ADD PREDICTION TO GRAPH
            test = postbody
            self.wfile.write(str(output).encode())
        except:
            self.send_error(404, "{}".format(sys.exc_info()[0]))
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