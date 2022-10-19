<p align="center">
  <img src="https://github.com/samuvack/ML-LDES-server/blob/master/images/logo.png?raw=true"/>
</p>

The Machine Learning (ML) server for Linked Data Event Streams (LDES) is a configurable component that can be used to ingest LDES, whereafter a machine learning model can be unleashed on it. The ML-LDES server was built in the context of the VSDS project in order to easily predict, analyse, find relationships, etc. with the use of ML.

## Quick start
First, you need the run the following command. This will install the required python packages:
```
pip install -r requirements.txt
```
Second, you need to start docker. You can do this by the following command (first open docker desktop in admin mode):
```
docker-compose up --build -d
```
* runs jupyter notebook on `http://localhost:7777/ipython/`
* runs postgis on `http://localhost:5432`
* runs pgadmin on `http://localhost:8001`

Afterwards, it becomes possible to run the ML-LDES server by the following command:
```
python server.py
```



## Documentation

The ML-LDES server listens on port 8000 and receives LDES N-tripples. Immediately afterwards, the relevant data is injected into the Machine Learning model. As a test, it was currently chosen to apply different regression models to the data:
* linear regression,
* multiple linear regression,
* polynomial regression,
* decision tree regression,
* random forest regression.

When the ML model has calculated to predicted temperature based on the given salinity value, a JSON respons is send back with all the output data.

## Test

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
Hereafter, json-ld is being crawled on the predefined relevant parameters (e.g., temperature, salinity).

Based on a given salinity value, the temperature is predicted using the trained ML regression models (see above).

<p align="center">
  <img src="https://github.com/samuvack/ML-LDES-server/blob/master/images/test copy.png?raw=true"/>
</p>
