from rdflib import Graph, plugin
from rdflib.serializer import Serializer
from rdflib import URIRef, BNode, Literal, RDF

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


#create function that insert <http://example.org/id/forecasting/sensorId/timestamp> in testrdf
def createForecastingTimeseries(sensorId, timestamp):
    testrdf = """
    @prefix example: <http://example.org/> .
    @prefix measurement: <http://def.isotc211.org/iso19156/2011/Measurement#> .
    @prefix prov: <http://www.w3.org/ns/prov#> .

    <http://example.org/id/forecasting/""" + sensorId + """/"""+timestamp+""">
        a example:ForecastingTimeseries ;
        example:isForecastingFor <"""+ sensorId + """> ;
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
    return g


g = createForecastingTimeseries("urn:ngsi-v2:cot-imec-be:Device:imec-iow-kfoRZfEsBmK9Kuo4EpUBJm", "timestamp2")


context = {"@vocab": "http://purl.org/dc/terms/", "@language": "en"}


#creates function that adds a new example:Forecasting member to example:forecastingCollection in Graph g
def addForecastingMember(g, timestamp, value):
    newForecasting = BNode()
    g.add((newForecasting, RDF.type, URIRef("http://example.org/Forecasting")))
    g.add((newForecasting, URIRef("http://example.org/forecastedTimestamp"), Literal(timestamp, datatype=XSD.datetime)))
    g.add((newForecasting, URIRef("http://example.org/value"), Literal(value)))
    g.add((URIRef("http://example.org/id/forecasting/sensorId/timestamp"), URIRef("http://example.org/forecastingCollection"), newForecasting))


#function that change value of example:forecastedProperty in Graph g
#for example add conductivity property instead of temperature
def changeForecastedProperty(g, newProperty):
    g.set((URIRef("http://example.org/id/forecasting/sensorId/timestamp"), URIRef("http://example.org/forecastedProperty"), URIRef(newProperty))) 

#function that change value of example:unit in Graph g
def changeUnit(g, newUnit):
    g.set((URIRef("http://example.org/id/forecasting/sensorId/timestamp"), URIRef("http://example.org/unit"), Literal(newUnit, datatype=XSD.string)))

#function that change value of example:isForecastingFor in Graph g
def changeIsForecastingFor(g, newIsForecastingFor):
    g.set((URIRef("http://example.org/id/forecasting/sensorId/timestamp"), URIRef("http://example.org/isForecastingFor"), URIRef(newIsForecastingFor)))
    

addForecastingMember(g, "2021-05-14T11:46:08.000Z", 28) #adds new forecasting member to RDF
changeForecastedProperty(g, 'http://example.org/id/conductiviteit')


# Code that prints the Graph g in N3 format
print(g.serialize(format='n3', context=context, indent=4))
