from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import sys
import rdflib
import sys
import data_processing.ttl2jsonld
import data_processing.crawled
import ml_tests.regression_input
import ml_tests.add_tripple


class webserverHandler(BaseHTTPRequestHandler):
    """docstring for webserverHandler"""

    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()

                output = ""
                output += '<html><body>Hello!'
                output += '<form method="POST" enctype="multipart/form-data" action="/hello"><h2> What would you like me to say?</h2><input name="message" type="text" /><input type="submit" value="Submit" /></form>'
                output += '</body></html>'
                self.wfile.write(output.encode())
                print(output)
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()

                output = ""
                output += '<html><body>&#161Hola <a href="/hello">Back to Hello</a>'
                output += '<form method="POST" enctype="multipart/form-data" action="/hello"><h2> What would you like me to say?</h2><input name="message" type="text" /><input type="submit" value="Submit" /></form>'
                output += '</body></html>'
                self.wfile.write(output.encode())
                print(output)
                return

        except IOError:
            self.send_error(404, "File not found %s" % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(self.headers.get('Content-Type'))


            content_len = int(self.headers.get('Content-length'))
            post_body = self.rfile.read(content_len)
            #pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            #pdict['CONTENT-LENGTH'] = content_len
            print('POST request input:')
            print(post_body)

            print('--Nu gaan we Linear model runnen--')
            print('Schatting temperatuur volgens linear regression:')
            print(ml_tests.regression_input.run_linear_model(33))
            temp_ml_lin = str(ml_tests.regression_input.run_linear_model(33))

            ##CONVERSION TO JSON-LD
            print('conversion to json-ld:')
            print(data_processing.ttl2jsonld.convert_rdf_2_jsonld(post_body))

            graph = data_processing.ttl2jsonld.convert_rdf_2_jsonld(post_body)
            temperature = data_processing.crawled.crawl_parameter('http://purl.org/dc/terms/temperature', graph)
            print('crawled temperature is :' + temperature)

            ##ADD PREDICTION TO GRAPH
            

            self.wfile.write(test.encode())
            print('respons :')
            print(output)
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