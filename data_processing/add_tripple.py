from rdflib import Graph, URIRef, Literal, BNode
from rdflib.namespace import FOAF, RDF


def add_tripple_to_graph(graph_input, input_tripple) #, s_input, p_input, o_input
    g = graph_input
    g.bind("foaf", FOAF)
    bob = URIRef("http://example.org/people/Bob")
    linda = BNode()  # a GUID is generated
    name = Literal("Bob")
    age = Literal(24)
    g.add((bob, RDF.type, FOAF.Person))
    g.add((bob, FOAF.name, name))
    g.add((bob, FOAF.age, age))
    g.add((bob, FOAF.knows, linda))
    g.add((linda, RDF.type, FOAF.Person))
    g.add((linda, FOAF.name, Literal("Linda")))
    #print(g.serialize())
    return g

