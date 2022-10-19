from rdflib import Graph, plugin
from rdflib.serializer import Serializer
from rdflib import URIRef
from rdflib.namespace import RDF


def convert_rdf_2_jsonld(rdf_input):
    g = Graph().parse(data=rdf_input, format='n3')
    #print(g.serialize(format='json-ld', indent=4))
    context = {"@vocab": "http://purl.org/dc/terms/", "@language": "en"}
    print(g.serialize(format='json-ld', context=context, indent=4))



if __name__ == '__main__':
    # Script2.py executed as script
    # do something
    convert_rdf_2_jsonld(rdf_input)