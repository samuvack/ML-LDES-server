## Test regression

Example of LDES member:

```
@prefix dcterms: <http://purl.org/dc/terms/> .
<http://example.org/about>
dcterms:temperature "10"@en ;
dcterms:salinity "20"@en .
```

send by POST request on `http://localhost:8000` with headers (key: 'Content-Type', value: 'application/n-triples')

this will be automatically converted to json-ld under the hood:
```
{
"@context": {
"@language": "en",
"@vocab": "http://purl.org/dc/terms/"
},
"@id": "http://example.org/about",
"salinity": "20",
"temperature": "10"
}
```
Hereafter, predefined relevant parameters (e.g., temperature, salinity) are extracted out the json-ld.

Based on a given salinity value, the temperature is predicted using the trained ML regression models (see figure).

<p align="center">
  <img src="https://github.com/samuvack/ML-LDES-server/blob/master/images/plots.png?raw=true"/>
</p>

