from rdflib import Graph, plugin
from rdflib.serializer import Serializer
from rdflib import URIRef
from rdflib.namespace import RDF


testrdf = """
@prefix dcterms: <http://purl.org/dc/terms/> .
<http://example.org/about>
dcterms:temperature "10"@en ;
dcterms:salinity "20"@en .
"""

g = Graph().parse(data=testrdf, format='n3')

print(g.serialize(format='json-ld', indent=4))

context = {"@vocab": "http://purl.org/dc/terms/", "@language": "en"}
print(g.serialize(format='json-ld', context=context, indent=4))

temperature = []



def crawl_parameter(parameter_string, graph_input):
    for s, p, o in graph_input:
        print (s)
        print(p)
        print(o)
        if (p == 'http://purl.org/dc/terms/temperature'):
           print('gelukt')

crawl_parameter('http://purl.org/dc/terms/temperature', g)