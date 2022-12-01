import rdfpandas
import pandas as pd
from rdflib import Graph, URIRef, Literal, BNode
from rdflib.namespace import FOAF, RDF
import get_dataframe_sensor



def dataframe_to_rdf(dataframe, column_list, sensor_name):
    """extacts values out dataframe and converts them into rdf file"""
    i = 0
    df = pd.DataFrame({'@id': pd.Series(dtype='str'),
                       'rdfs:type': pd.Series(dtype='str'),
                       'togaf:businessCapabilityDecomposesBusinessCapability': pd.Series(dtype='str'),
                       'rdf:value': pd.Series(dtype='str'),
                       'rdfs:comment': pd.Series(dtype='str')
                       })
    
    for i in range(len(column_list)):
        print(column_list[i])
        df_temp = dataframe[['time', column_list[i]]][:5]
        df_temp['time'] = range(2, 2+len(df_temp))
        df_temp['time'] = 'im:' + df_temp['time'].astype(str)
        df_temp['rdfs:type']='togaf:BusinessCapability'
        
        df_temp['togaf:businessCapabilityDecomposesBusinessCapability'] = 'im:1'
        df_temp = df_temp.rename(columns={"time": "@id", "type": "rdfs:type", column_list[i]: 'rdf:value'})
        df = pd.concat([df,df_temp], ignore_index=True, sort=False)
        new_row = ['im:1', 'togaf:BusinessCapability', '', sensor_name, '']
        print(df)
        df['rdfs:comment'] = ''
        df.loc[-1] = new_row
        df.index = df.index + 1  # shifting index
        df.sort_index(inplace=True)
        
        # drop factor from axis 1 and make changes permanent by inplace=True
        df.reset_index(drop=True)
        df = df.set_index('@id')
        print(df.index.name)
        print(df)
    g = rdfpandas.to_graph(df)
    ttl = g.serialize(format='turtle')
    print(ttl)


df = get_dataframe_sensor.get_df_sensor('urn:ngsi-v2:cot-imec-be:Device:imec-iow-8o4PWPeZtfhQCX28MA9kTb')

dataframe_to_rdf(df, ['temperature'],
                 'urn:ngsi-v2:cot-imec-be:Device:imec-iow-8o4PWPeZtfhQCX28MA9kTb')

