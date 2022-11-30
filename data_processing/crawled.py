from rdflib import Graph, plugin
from rdflib.serializer import Serializer
from rdflib import URIRef
from rdflib.namespace import RDF
import data_processing.ttl2jsonld

testrdf = """
@prefix dcterms: <http://purl.org/dc/terms/> .
<http://example.org/about>
dcterms:temperature "10"@en ;
dcterms:salinity "20"@en .
"""

g = Graph().parse(data=testrdf, format='n3')

#print(g.serialize(format='json-ld', indent=4))

context = {"@vocab": "http://purl.org/dc/terms/", "@language": "en"}
#print(g.serialize(format='json-ld', context=context, indent=4))



test_rdf = """_:B0ee11c309400bfc6f122b8db4a47ff87 <http://def.isotc211.org/iso19103/2005/UnitsOfMeasure#Measure.value> _:B641b132bc4971bdd1d54f9a4d637287e .
_:B7797edc0cc00c5c586c565dc60e2e402 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://def.isotc211.org/iso19156/2011/Measurement#OM_Measurement> .
_:B7797edc0cc00c5c586c565dc60e2e402 <http://def.isotc211.org/iso19156/2011/Observation#OM_Observation.observedProperty> <https://data.vmm.be/concept/waterkwaliteitparameter/temperatuur> .
_:B7797edc0cc00c5c586c565dc60e2e402 <http://def.isotc211.org/iso19156/2011/Observation#OM_Observation.phenomenonTime> "2022-11-22T23:46:05.000Z"^^<http://www.w3.org/2001/XMLSchema#datetime> .
_:B7797edc0cc00c5c586c565dc60e2e402 <http://def.isotc211.org/iso19156/2011/Observation#OM_Observation.result> _:B0378688d2265c3186dea7b77cc5f4235 .
_:B7797edc0cc00c5c586c565dc60e2e402 <http://www.w3.org/ns/sosa/madeBySensor> <urn:ngsi-v2:cot-imec-be:Device:imec-iow-aqvSqLxWp5haKcJhHwuin8> .
_:B32f3b154ac375bfd015e45bf31812003 <https://schema.org/value> "0"^^<http://www.w3.org/2001/XMLSchema#integer> .
<urn:ngsi-v2:cot-imec-be:WaterQualityObserved:imec-iow-SFiTxQxjouX5JZsyPKg9LE/2022-11-22T23:46:05.000Z> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://www.w3.org/TR/vocab-ssn-ext/#sosa:ObservationCollection> .
<urn:ngsi-v2:cot-imec-be:WaterQualityObserved:imec-iow-SFiTxQxjouX5JZsyPKg9LE/2022-11-22T23:46:05.000Z> <http://def.isotc211.org/iso19156/2011/SamplingFeature#SF_SamplingFeatureCollection.member> _:B2368f8a98d70b577200119882be2a7fd .
<urn:ngsi-v2:cot-imec-be:WaterQualityObserved:imec-iow-SFiTxQxjouX5JZsyPKg9LE/2022-11-22T23:46:05.000Z> <http://def.isotc211.org/iso19156/2011/SamplingFeature#SF_SamplingFeatureCollection.member> _:B55a2659775598c03f25fb52b0cd20aa0 .
<urn:ngsi-v2:cot-imec-be:WaterQualityObserved:imec-iow-SFiTxQxjouX5JZsyPKg9LE/2022-11-22T23:46:05.000Z> <http://def.isotc211.org/iso19156/2011/SamplingFeature#SF_SamplingFeatureCollection.member> _:B7797edc0cc00c5c586c565dc60e2e402 .
<urn:ngsi-v2:cot-imec-be:WaterQualityObserved:imec-iow-SFiTxQxjouX5JZsyPKg9LE/2022-11-22T23:46:05.000Z> <http://purl.org/dc/terms/isVersionOf> <urn:ngsi-v2:cot-imec-be:WaterQualityObserved:imec-iow-SFiTxQxjouX5JZsyPKg9LE> .
<urn:ngsi-v2:cot-imec-be:WaterQualityObserved:imec-iow-SFiTxQxjouX5JZsyPKg9LE/2022-11-22T23:46:05.000Z> <http://www.w3.org/ns/prov#generatedAtTime> "2022-11-22T23:46:05.000Z"^^<http://www.w3.org/2001/XMLSchema#dateTime> .
<urn:ngsi-v2:cot-imec-be:WaterQualityObserved:imec-iow-SFiTxQxjouX5JZsyPKg9LE/2022-11-22T23:46:05.000Z> <http://www.w3.org/ns/sosa/hasFeatureOfInterest> "spt-00080-41" .
_:Bec4ba164472cf483d17ddac99586f772 <https://schema.org/value> "-2.73333333E-1"^^<http://www.w3.org/2001/XMLSchema#double> .
_:B55a2659775598c03f25fb52b0cd20aa0 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://def.isotc211.org/iso19156/2011/Measurement#OM_Measurement> .
_:B55a2659775598c03f25fb52b0cd20aa0 <http://def.isotc211.org/iso19156/2011/Observation#OM_Observation.observedProperty> <https://data.vmm.be/concept/waterkwaliteitparameter/conductiviteit> .
_:B55a2659775598c03f25fb52b0cd20aa0 <http://def.isotc211.org/iso19156/2011/Observation#OM_Observation.phenomenonTime> "2022-11-22T23:46:05.000Z"^^<http://www.w3.org/2001/XMLSchema#datetime> .
_:B55a2659775598c03f25fb52b0cd20aa0 <http://def.isotc211.org/iso19156/2011/Observation#OM_Observation.result> _:B0ee11c309400bfc6f122b8db4a47ff87 .
_:B55a2659775598c03f25fb52b0cd20aa0 <http://www.w3.org/ns/sosa/madeBySensor> <urn:ngsi-v2:cot-imec-be:Device:imec-iow-aqvSqLxWp5haKcJhHwuin8> .
_:B0378688d2265c3186dea7b77cc5f4235 <http://def.isotc211.org/iso19103/2005/UnitsOfMeasure#Measure.value> _:B32f3b154ac375bfd015e45bf31812003 .
<https://iow.smartdataspace.beta-vlaanderen.be/water-quality-observations> <https://w3id.org/tree#member> <urn:ngsi-v2:cot-imec-be:WaterQualityObserved:imec-iow-SFiTxQxjouX5JZsyPKg9LE/2022-11-22T23:46:05.000Z> .
_:B2368f8a98d70b577200119882be2a7fd <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://def.isotc211.org/iso19156/2011/Measurement#OM_Measurement> .
_:B2368f8a98d70b577200119882be2a7fd <http://def.isotc211.org/iso19156/2011/Observation#OM_Observation.observedProperty> <https://data.vmm.be/concept/sensor/batterijniveau> .
_:B2368f8a98d70b577200119882be2a7fd <http://def.isotc211.org/iso19156/2011/Observation#OM_Observation.phenomenonTime> "2022-11-22T23:46:05.000Z"^^<http://www.w3.org/2001/XMLSchema#datetime> .
_:B2368f8a98d70b577200119882be2a7fd <http://def.isotc211.org/iso19156/2011/Observation#OM_Observation.result> _:Bd7ad48ca048a4443b36fefc6d1900e8d .
_:B2368f8a98d70b577200119882be2a7fd <http://www.w3.org/ns/sosa/madeBySensor> <urn:ngsi-v2:cot-imec-be:Device:imec-iow-aqvSqLxWp5haKcJhHwuin8> .
_:B641b132bc4971bdd1d54f9a4d637287e <https://schema.org/value> "2.65585344057E2"^^<http://www.w3.org/2001/XMLSchema#double> .
_:Bd7ad48ca048a4443b36fefc6d1900e8d <http://def.isotc211.org/iso19103/2005/UnitsOfMeasure#Measure.value> _:Bec4ba164472cf483d17ddac99586f772 .
"""

def crawl_parameter(parameter_string, graph_input):
    """_summary_

    Args:
        parameter_string (_type_): _description_
        graph_input (_type_): _description_

    Returns:
        _type_: _description_
    """
    for s, p, o in graph_input:
        if (str(p) == parameter_string):

           return str(o)

def carwl_graph(graph, list_input):
    """extract values out RDF

    Args:
        graph (RDF graph): RDF graph where to extact values out
        list_input (list): list all parameters that needs to be extracted

    Returns:
        dataframe: extracted list of values in order of 
    """
    jsonld = data_processing.ttl2jsonld.convert_rdf_2_jsonld(graph)
    g = Graph().parse(data=jsonld, format='json-ld')

    knows_query = """
    PREFIX sosa: <http://www.w3.org/ns/sosa/>
    PREFIX measure: <http://def.isotc211.org/iso19156/2011/Measurement#>
    PREFIX unitsofmeasure: <http://def.isotc211.org/iso19103/2005/UnitsOfMeasure#Measure.>
    PREFIX observation: <http://def.isotc211.org/iso19156/2011/Observation#OM_Observation.>
    PREFIX schema: <https://schema.org/>
    SELECT ?propertyname ?time ?sensor ?value
    WHERE {
        ?reading a measure:OM_Measurement .
        ?reading observation:observedProperty ?property .
        ?reading observation:phenomenonTime ?time .
        BIND (REPLACE(STR(?property), "^.*/([^/]*)$", "$1") as ?propertyname)
        ?reading sosa:madeBySensor ?sensor .
        ?reading observation:result/unitsofmeasure:value/schema:value ?value
    }
    """
    output=[]
    qres = g.query(knows_query)
    for row in qres:
        print(str(row[0]).strip())
        for i in range(len(list_input)):
            print(str(row[0]).strip())
            if (str(row[0]).strip() == list_input[i]):
                print('ok')
                value = row[3]
                print(str(value))
                output.insert(i, float(value))
    return output


def crawl_sensor_id(graph):
    """extract values out RDF

    Args:
        graph (RDF graph): RDF graph where to extact values out
        list_input (list): list all parameters that needs to be extracted

    Returns:
        dataframe: extracted list of values in order of 
    """
    jsonld = data_processing.ttl2jsonld.convert_rdf_2_jsonld(graph)
    g = Graph().parse(data=jsonld, format='json-ld')

    knows_query = """
    PREFIX sosa: <http://www.w3.org/ns/sosa/>
    PREFIX measure: <http://def.isotc211.org/iso19156/2011/Measurement#>
    PREFIX unitsofmeasure: <http://def.isotc211.org/iso19103/2005/UnitsOfMeasure#Measure.>
    PREFIX observation: <http://def.isotc211.org/iso19156/2011/Observation#OM_Observation.>
    PREFIX schema: <https://schema.org/>
    SELECT ?propertyname ?time ?sensor ?value
    WHERE {
        ?reading a measure:OM_Measurement .
        ?reading observation:observedProperty ?property .
        ?reading observation:phenomenonTime ?time .
        BIND (REPLACE(STR(?property), "^.*/([^/]*)$", "$1") as ?propertyname)
        ?reading sosa:madeBySensor ?sensor .
        ?reading observation:result/unitsofmeasure:value/schema:value ?value
    }
    """

    qres = g.query(knows_query)
    for row in qres:
        sensorid = row[2]
    return sensorid
        


