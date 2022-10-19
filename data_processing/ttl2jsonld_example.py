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

for s, p, o in g:
    print (s)
    print(p)
    print(o)
    if (p == 'http://purl.org/dc/terms/temperature'):
        temperature.append(o)
    if (p == 'http://purl.org/dc/terms/salinity'):
        salinity.append(o)

def convert_rdf_2_jsonld(rdf_input):
    g = Graph().parse(data=rdf_input, format='n3')
    print(g.serialize(format='json-ld', indent=4))
    context = {"@vocab": "http://purl.org/dc/terms/", "@language": "en"}
    print(g.serialize(format='json-ld', context=context, indent=4))

convert_rdf_2_jsonld(testrdf)

if __name__ == '__main__':
    # Script2.py executed as script
    # do something
    convert_rdf_2_jsonld()