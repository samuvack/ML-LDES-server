import pandas as pd
import rdfpandas
df = pd.read_csv('https://raw.githubusercontent.com/cadmiumkitty/capability-models/master/notebooks/information_security_capabilities.csv',
                 index_col='@id', keep_default_na=True)
print(df)
g = rdfpandas.to_graph(df)
ttl = g.serialize(format='json-ld')

print(ttl)

