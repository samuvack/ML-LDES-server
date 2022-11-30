import rdfpandas
import pandas as pd
from rdflib import Graph, URIRef, Literal, BNode
from rdflib.namespace import FOAF, RDF
import get_dataframe_sensor



def dataframe_to_rdf(dataframe, column_list, sensor_name):
    """extacts values out dataframe and converts them into rdf file"""
    g = Graph()
    i = 0
    g.bind("foaf", FOAF)
    df = pd.DataFrame({'@id': pd.Series(dtype='str'),
                       'rdfs:type': pd.Series(dtype='str'),
                       'togaf:businessCapabilityDecomposesBusinessCapability': pd.Series(dtype='str'),
                       'rdfs:label': pd.Series(dtype='str'),
                       'rdfs:comment': pd.Series(dtype='str')
                       })
    
    for i in range(len(column_list)):
        print(column_list[i])
        df_temp = dataframe[['time', column_list[i]]]
        df_temp['time'] = sensor_name + '/' + df_temp['time'].astype(str)
        df_temp['type'] = column_list[i]
        df_temp = df_temp.rename(columns={"time": "@id", "type": "rdfs:type", column_list[i]: 'rdfs:label'})
        df = pd.concat([df,df_temp], ignore_index=True, sort=False)
        df['togaf:businessCapabilityDecomposesBusinessCapability'] = 'test'
        new_row = ['test', 'sensor', '',sensor_name,'']
        print(df)
        df.loc[-1] = new_row
        df.index = df.index + 1  # shifting index
        df.sort_index(inplace=True) 
        print(df)
    g = rdfpandas.to_graph(df)
    ttl = g.serialize(format='json-ld')
    print(ttl)


df = get_dataframe_sensor.get_df_sensor('urn:ngsi-v2:cot-imec-be:Device:imec-iow-8o4PWPeZtfhQCX28MA9kTb')

dataframe_to_rdf(df, ['temperature'],
                 'urn:ngsi-v2:cot-imec-be:Device:imec-iow-8o4PWPeZtfhQCX28MA9kTb')

