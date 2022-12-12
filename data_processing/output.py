from rdflib import Graph, plugin
from rdflib.serializer import Serializer

testrdf = """
@prefix example: <http://example.org/> .
@prefix measurement: <http://def.isotc211.org/iso19156/2011/Measurement#> .
@prefix prov: <http://www.w3.org/ns/prov#> .

<http://example.org/id/forecasting/{sensorId}/{timestamp}>
    a example:ForecastingTimeseries ;
    example:isForecastingFor <urn:ngsi-v2:cot-imec-be:Device:imec-iow-kfoRZfEsBmK9Kuo4EpUBJm> ;
    example:forecastedProperty <http://example.org/id/temperatuur> ;
    example:unit "°C"^^<http://www.w3.org/2001/XMLSchema#celcius> ;
    example:forecastingCollection
        [
            a example:Forecasting;
            example:forecastedTimestamp "2021-05-14T11:46:08.000Z"^^<http://www.w3.org/2001/XMLSchema#datetime> ;
            example:value 25;
        ],
        [
            a example:Forecasting;
            example:forecastedTimestamp "2021-05-14T11:46:08.000Z"^^<http://www.w3.org/2001/XMLSchema#datetime> ;
            example:value 26;
        ];
    
    prov:generatedAtTime "2022-12-12T11:46:08.000Z"^^<http://www.w3.org/2001/XMLSchema#dateTime> .
"""

g = Graph().parse(data=testrdf, format='n3')
context = {"@vocab": "http://purl.org/dc/terms/", "@language": "en"}
print(g.serialize(format='json-ld', context=context, indent=4))


