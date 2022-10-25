import requests
import datetime
import time
import numpy as np

i = 1

try:
    while True:
        rdf = """
        @prefix dcterms: <http://purl.org/dc/terms/> .

        <http://example.org/about>
        dcterms:temperature """


        
        test = np.sin((np.pi/30)*i)*10 + 10
        i += 1

        # using now() to get current time
        current_time = datetime.datetime.now()

        rdf += '"' + str(test) + '"'
        rdf += """@en ;
        dcterms:salinity "20"@en ;
        dcterms:time """
        rdf += '"' + str(current_time) + '"@en .'

        url = 'http://localhost:8000/input'



        headers = {'Content-Type': 'application/xml'}

        r = requests.post(url, data=rdf, headers=headers)

        print(r.text)

except KeyboardInterrupt:
    exit