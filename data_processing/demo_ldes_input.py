import requests
import datetime
from river import datasets


dataset = datasets.AirlinePassengers()

i = 1
try:
    for t, (x, y) in enumerate(datasets.AirlinePassengers()):
        rdf = """
            @prefix dcterms: <http://purl.org/dc/terms/> .

            <http://example.org/about>
            dcterms:temperature """
        test = y
        print(y)
        # using now() to get current time
        current_time = datetime.datetime.now()
        rdf += '"' + str(test) + '"'
        rdf += """@en ;
            dcterms:salinity "20"@en ;
            dcterms:time """
        rdf += '"' + str(t) + '"@en .'
        url = 'http://localhost:8000/input'
        headers = {'Content-Type': 'application/xml'}
        r = requests.post(url, data=rdf, headers=headers)
        print(r.text)

except KeyboardInterrupt:
    exit