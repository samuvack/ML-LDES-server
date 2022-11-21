from rdflib import Graph, plugin
from rdflib.serializer import Serializer
from rdflib import URIRef
from rdflib.namespace import RDF


testrdf = """
_:Bc6bd21f176c98b8ebba307244ce8e109 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://def.isotc211.org/iso19156/2011/Measurement#OM_Measurement> .
_:Bc6bd21f176c98b8ebba307244ce8e109 <http://def.isotc211.org/iso19156/2011/Observation#OM_Observation.observedProperty> <https://data.vmm.be/concept/waterkwaliteitparameter/conductiviteit> .
_:Bc6bd21f176c98b8ebba307244ce8e109 <http://def.isotc211.org/iso19156/2011/Observation#OM_Observation.phenomenonTime> "2020-01-15T12:59:42.206Z"^^<http://www.w3.org/2001/XMLSchema#datetime> .
_:Bc6bd21f176c98b8ebba307244ce8e109 <http://def.isotc211.org/iso19156/2011/Observation#OM_Observation.result> _:B877b75f4c6281c28a434fa6233023d71 .
_:Bc6bd21f176c98b8ebba307244ce8e109 <http://www.w3.org/ns/sosa/madeBySensor> <urn:ngsi-v2:cot-imec-be:device:imec-wqsensor-2047475712> .
<urn:ngsi-ld:WaterQualityObserved:nbiot.2047475712/2020-01-15T12:59:42.206Z> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://www.w3.org/TR/vocab-ssn-ext/#sosa:ObservationCollection> .
<urn:ngsi-ld:WaterQualityObserved:nbiot.2047475712/2020-01-15T12:59:42.206Z> <http://def.isotc211.org/iso19156/2011/SamplingFeature#SF_SamplingFeatureCollection.member> _:Bc6bd21f176c98b8ebba307244ce8e109 .
<urn:ngsi-ld:WaterQualityObserved:nbiot.2047475712/2020-01-15T12:59:42.206Z> <http://def.isotc211.org/iso19156/2011/SamplingFeature#SF_SamplingFeatureCollection.member> _:B038df59a80f4a467e41ad783c84b3adf .
<urn:ngsi-ld:WaterQualityObserved:nbiot.2047475712/2020-01-15T12:59:42.206Z> <http://def.isotc211.org/iso19156/2011/SamplingFeature#SF_SamplingFeatureCollection.member> _:Ba31e3cc80aa0c2f03f2937547d2a27ab .
<urn:ngsi-ld:WaterQualityObserved:nbiot.2047475712/2020-01-15T12:59:42.206Z> <http://purl.org/dc/terms/isVersionOf> <urn:ngsi-ld:WaterQualityObserved:nbiot.2047475712> .
<urn:ngsi-ld:WaterQualityObserved:nbiot.2047475712/2020-01-15T12:59:42.206Z> <http://www.w3.org/ns/prov#generatedAtTime> "2020-01-15T12:59:42.206Z"^^<http://www.w3.org/2001/XMLSchema#dateTime> .
_:Ba31e3cc80aa0c2f03f2937547d2a27ab <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://def.isotc211.org/iso19156/2011/SpatialSamplingFeature#SF_SpatialSamplingFeature> .
_:Ba31e3cc80aa0c2f03f2937547d2a27ab <http://def.isotc211.org/iso19156/2011/SpatialSamplingFeature#SF_SpatialSamplingFeature.shape> "2.817023333E0"^^<http://www.w3.org/2001/XMLSchema#double> .
_:Ba31e3cc80aa0c2f03f2937547d2a27ab <http://def.isotc211.org/iso19156/2011/SpatialSamplingFeature#SF_SpatialSamplingFeature.shape> "5.09912403E1"^^<http://www.w3.org/2001/XMLSchema#double> .
_:Ba31e3cc80aa0c2f03f2937547d2a27ab <http://def.isotc211.org/iso19156/2011/SpatialSamplingFeature#SF_SpatialSamplingFeature.shape> _:Be1eeb70fc9df87c275dfd26269eda66f .
_:Bd577ef0f2bffeb73b8137b091613f002 <http://def.isotc211.org/iso19103/2005/UnitsOfMeasure#Measure.value> _:Beeae326921ead7ec5c93d26145ad09a9 .
_:B877b75f4c6281c28a434fa6233023d71 <http://def.isotc211.org/iso19103/2005/UnitsOfMeasure#Measure.value> _:B51924fbd62817cf364ce95702432a8fe .
_:Beeae326921ead7ec5c93d26145ad09a9 <https://schema.org/value> "7.75E0"^^<http://www.w3.org/2001/XMLSchema#double> .
_:B038df59a80f4a467e41ad783c84b3adf <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://def.isotc211.org/iso19156/2011/Measurement#OM_Measurement> .
_:B038df59a80f4a467e41ad783c84b3adf <http://def.isotc211.org/iso19156/2011/Observation#OM_Observation.observedProperty> <https://data.vmm.be/concept/waterkwaliteitparameter/temperatuur> .
_:B038df59a80f4a467e41ad783c84b3adf <http://def.isotc211.org/iso19156/2011/Observation#OM_Observation.phenomenonTime> "2020-01-15T12:59:42.206Z"^^<http://www.w3.org/2001/XMLSchema#datetime> .
_:B038df59a80f4a467e41ad783c84b3adf <http://def.isotc211.org/iso19156/2011/Observation#OM_Observation.result> _:Bd577ef0f2bffeb73b8137b091613f002 .
_:B038df59a80f4a467e41ad783c84b3adf <http://www.w3.org/ns/sosa/madeBySensor> <urn:ngsi-v2:cot-imec-be:device:imec-wqsensor-2047475712> .
<https://iow.smartdataspace.beta-vlaanderen.be/water-quality-observations> <https://w3id.org/tree#member> <urn:ngsi-ld:WaterQualityObserved:nbiot.2047475712/2020-01-15T12:59:42.206Z> .
_:B51924fbd62817cf364ce95702432a8fe <https://schema.org/value> "6.8237205524E2"^^<http://www.w3.org/2001/XMLSchema#double> .
"""

g = Graph().parse(data=testrdf, format='n3')

#print(g.serialize(format='json-ld', indent=4))

context = {"@vocab": "http://purl.org/dc/terms/", "@language": "en"}
#print(g.serialize(format='json-ld', context=context, indent=4))

temperature = []



def crawl_parameter(parameter_string, graph_input):
    for s, p, o in graph_input:
        if (str(p) == parameter_string):
           return str(o)


knows_query2 = """
PREFIX sosa: <https://www.w3.org/TR/vocab-ssn-ext/#sosa:>
PREFIX samplecollection: <http://def.isotc211.org/iso19156/2011/SamplingFeature#SF_SamplingFeatureCollection.>
PREFIX measure: <http://def.isotc211.org/iso19156/2011/Measurement#>
PREFIX unitsofmeasure: <http://def.isotc211.org/iso19103/2005/UnitsOfMeasure#Measure.>
PREFIX observation: <http://def.isotc211.org/iso19156/2011/Observation#OM_Observation.>
PREFIX waterkwaliteitparameter: <https://data.vmm.be/concept/waterkwaliteitparameter/>
PREFIX sensor: <https://data.vmm.be/concept/sensor/>
PREFIX schema: <https://schema.org/>
PREFIX prov: <http://www.w3.org/ns/prov#>
SELECT ?collection ?generated_at ?temperature ?conductivity ?batterylevel ?sensor_name
WHERE {
  ?collection a sosa:ObservationCollection .
  ?collection prov:generatedAtTime ?generated_at . 
  OPTIONAL {
    ?collection samplecollection:member ?member1 .
    ?member1 observation:observedProperty waterkwaliteitparameter:temperatuur .
    ?member1 observation:result/unitsofmeasure:value/schema:value ?temperature
  }
  OPTIONAL {
    ?collection samplecollection:member ?member2 .
    ?member2 observation:observedProperty waterkwaliteitparameter:conductiviteit .
    ?member2 observation:result/unitsofmeasure:value/schema:value ?conductivity
  }
  OPTIONAL {
    ?collection samplecollection:member ?member3 .
    ?member3 observation:observedProperty sensor:batterijniveau .
    ?member3 observation:result/unitsofmeasure:value/schema:value ?batterylevel
  }
  OPTIONAL {
    ?collection samplecollection:member ?member1 .
    ?member1 observation:observedProperty waterkwaliteitparameter:temperatuur .
    ?member1 ?s ?sensor_name


  }
}
    """


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
list = []

qres = g.query(knows_query)
for row in qres:
    print(row[0])
    print(row[1])
    print(row[2])
    if row[0].strip() == 'temperatuur':
        print('juij')
        temp = row[3].strip
        sensor_name_t = row[2].strip()
        time_temp = row[1].strip()
if row[2].strip() == 'urn:ngsi-v2:cot-imec-be:device:imec-wqsensor-2047475712':
      list.append(temp)