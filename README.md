<p align="center">
  <img src="https://github.com/samuvack/ML-LDES-server/blob/master/images/logo.png?raw=true"/>
</p>

The ML-LDES server was built by the Flemish Smart Data Space project to predict, analyse and find relationships on Linked Data Event Streams (LDES) using Machine Learning quickly. The Machine Learning (ML) server for Linked Data Event Streams (LDES) is a configurable component that can ingest LDES members.  Hereafter, the ML-LDES server can unleash a machine-learning model on the LDES members.

## Quick start
First, you need the run the following command in your terminal. This will install the required python packages:
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
* runs Apache Nifi in `http://localhost:8443/nifi`


To showcase the different Machine Learning forecasts/estimations (regression, online ML, offline ML, offline/online ML) we use an Internet of Water (IoW) Linked Data Event Stream.

First, LDES Client must send the LDES members to the ML-LDES server via POST requests. We use Apache NIFI (included in the docker container) to pull the data stream into the ML-LDES server.

Go to: https://localhost:8443/nifi/

Pipeline for Online ML (LDES-client to invoke HTTP (Post request)):

<p align="center">
  <img src="https://github.com/samuvack/ML-LDES-server/blob/master/images/apache_nifi.png?raw=true"/>
</p>


Pipeline for Offline ML (LDES-Client to TimescaleDB):
![Nifi_timescale](https://user-images.githubusercontent.com/15192194/205595307-2d90ef65-73aa-4360-a2d8-94af87eb62b8.png)


## Operation of the server

Afterwards, it becomes possible to run the ML-LDES server by the following command:
```
python server.py
```


The ML-LDES server listens on port 8000 and receives LDES N-tripples. Immediately afterwards, the relevant data is injected into the Machine Learning model.

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

Depending on which ML model server is applied, a different forecasting/estimation is computed based on the fetched members.

To showcase the different possibilities, an Internet of Waters (IoW) LDES is applied, containing information about temperature and conductivity:

<p align="center">
  <img src="https://github.com/samuvack/ML-LDES-server/blob/master/images/plot_conductivity_temeprature.png?raw=true"/>
</p>

## Regression model

Hereafter, predefined relevant parameters (e.g., temperature, salinity) are extracted out the json-ld.

Based on a given conductivity value, the temperature is predicted using the trained ML regression models (see figure).

<p align="center">
  <img src="https://github.com/samuvack/ML-LDES-server/blob/master/images/plots.png?raw=true"/>
</p>

 As a test, it was currently chosen to apply different regression models to the data:
* linear regression,
* multiple linear regression,
* polynomial regression,
* decision tree regression,
* random forest regression.

When the ML model has calculated to predicted temperature based on the given salinity value, a JSON respons is send back with all the output data.


Of course a better way is by looking at the temporal scale (and even better spatio-temporal scale) instead of looking at all the historical measurments at ones (e.g. the case of regression models).

<p align="center">
  <img src="https://github.com/samuvack/ML-LDES-server/blob/master/images/timeseries3.png?raw=true"/>
</p>

Therefore some forecasting models are showcasted underneath:

  ## Online Machine Learning
  
  

<p align="center">
  <img src="https://github.com/samuvack/ML-LDES-server/blob/master/output_ml/online_forecasting_snarimax.gif?raw=true"/>
</p>

When running `python server_forecasting_snarimax.py` the ML server will listen on port 8000 for LDES Post requests, filtering out the relevant values, and sending it into the SNARIMAX forecasting model. Hereafter, the model will automatically forecast a serie of estimated values.

Via the python script `python ./data_processing/demo_ldes_input.py`) a demo LDES POST request will be send to http://localhost:8000/input

<p align="center">
  <img src="https://github.com/samuvack/ML-LDES-server/blob/master/output_ml/gif_forecasting_SNARIMAX.gif?raw=true"/>
</p>


<p align="center">
  <img src="https://github.com/samuvack/ML-LDES-server/blob/master/online_ml/online_iow_multiple_easy2.gif?raw=true"/>
</p>


## Offline Machine Learning

Prophet Forecasting Library
Prophet, or “Facebook Prophet,” is an open-source library for univariate (one variable) time series forecasting developed by Facebook.

Prophet implements what they refer to as an additive time series forecasting model, and the implementation supports trends, seasonality, and holidays.

Implements a procedure for forecasting time series data based on an additive model where non-linear trends are fit with yearly, weekly, and daily seasonality, plus holiday effects

— Package ‘prophet’, 2019.

It is designed to be easy and completely automatic, e.g. point it at a time series and get a forecast. As such, it is intended for internal company use, such as forecasting sales, capacity, etc.

For a great overview of Prophet and its capabilities, see the post:

Prophet: forecasting at scale, 2017.

<p align="center">
  <img src="https://github.com/samuvack/ML-LDES-server/blob/master/offline_ml/Prophet_plot1.png?raw=true?raw=true"/>
</p>

<p align="center">
  <img src="https://github.com/samuvack/ML-LDES-server/blob/master/offline_ml/Prophet_plot2.png?raw=true?raw=true"/>
</p>

<p align="center">
  <img src="https://github.com/samuvack/ML-LDES-server/blob/master/offline_ml/Prophet_plot3.png?raw=true?raw=true"/>
</p>

## Combination offline / online Machine learning

Holt-Winters forecasting is a way to model and predict the behaviour of a sequence of values over time (time series). Holt-Winters is one of the most popular forecasting techniques for time series. As a test, the Holt-Winters forecasting model from the Python package River has been tested.

For this ML model, first a batch dataset needs to be available before the ML model can run and forecast incrementally based on fetched members.


 ## Output as a collection
 
 
 When running the get_server.py script, the ML forecasting is generated in the form of a published collection on localhost:8000/output/{number}
for example ``localhost:8000/output/4``:
 
<pre><code> 
@prefix example: <http://example.org/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<http://example.org/id/forecasting/urn:ngsi-v2:cot-imec-be:WaterQualityObserved:imec-iow-4WYSEqBKuD2UKpNEQyW8AJ> a example:ForecastingTimeseries ;
    example:forecastedProperty <http://example.org/id/temperatuur> ;
    example:forecastingCollection [ a example:Forecasting ;
            example:forecastedTimestamp "2022-11-22T13:32:13"^^xsd:datetime ;
            example:value 9.500221e+02 ],
        [ a example:Forecasting ;
            example:forecastedTimestamp "2022-11-22T09:32:13"^^xsd:datetime ;
            example:value 9.39572e+02 ],
        [ a example:Forecasting ;
            example:forecastedTimestamp "2022-11-22T14:32:13"^^xsd:datetime ;
            example:value 9.480413e+02 ],
        [ a example:Forecasting ;
            example:forecastedTimestamp "2022-11-21T22:32:13"^^xsd:datetime ;
            example:value 9.628977e+02 ],
        [ a example:Forecasting ;
            example:forecastedTimestamp "2022-11-22T12:32:13"^^xsd:datetime ;
            example:value 9.497323e+02 ],
        [ a example:Forecasting ;
            example:forecastedTimestamp "2022-11-22T01:32:13"^^xsd:datetime ;
            example:value 9.551929e+02 ],
        [ a example:Forecasting ;
            example:forecastedTimestamp "2022-11-22T15:32:13"^^xsd:datetime ;
            example:value 9.446084e+02 ],
        [ a example:Forecasting ;
            example:forecastedTimestamp "2022-11-22T10:32:13"^^xsd:datetime ;
            example:value 9.434172e+02 ],
        [ a example:Forecasting ;
            example:forecastedTimestamp "2022-11-22T11:32:13"^^xsd:datetime ;
            example:value 9.472341e+02 ],
        [ a example:Forecasting ;
            example:forecastedTimestamp "2022-11-22T16:32:13"^^xsd:datetime ;
            example:value 9.409902e+02 ],
        [ a example:Forecasting ;
            example:forecastedTimestamp "2022-11-22T20:32:13"^^xsd:datetime ;
            example:value 9.342904e+02 ],
        [ a example:Forecasting ;
            example:forecastedTimestamp "2022-11-22T00:32:13"^^xsd:datetime ;
            example:value 9.57794e+02 ],
        [ a example:Forecasting ;
            example:forecastedTimestamp "2022-11-22T06:32:13"^^xsd:datetime ;
            example:value 9.373796e+02 ],
        [ a example:Forecasting ;
            example:forecastedTimestamp "2022-11-21T23:32:13"^^xsd:datetime ;
            example:value 9.603254e+02 ],
        [ a example:Forecasting ;
            example:forecastedTimestamp "2022-11-22T02:32:13"^^xsd:datetime ;
            example:value 9.521727e+02 ],
        [ a example:Forecasting ;
            example:forecastedTimestamp "2022-11-22T08:32:13"^^xsd:datetime ;
            example:value 9.36885e+02 ],
        [ a example:Forecasting ;
            example:forecastedTimestamp "2022-11-22T04:32:13"^^xsd:datetime ;
            example:value 9.443625e+02 ],
        [ a example:Forecasting ;
            example:forecastedTimestamp "2022-11-22T17:32:13"^^xsd:datetime ;
            example:value 9.382099e+02 ],
        [ a example:Forecasting ;
            example:forecastedTimestamp "2022-11-22T05:32:13"^^xsd:datetime ;
            example:value 9.40377e+02 ],
        [ a example:Forecasting ;
            example:forecastedTimestamp "2022-11-22T07:32:13"^^xsd:datetime ;
            example:value 9.36097e+02 ],
        [ a example:Forecasting ;
            example:forecastedTimestamp "2022-11-22T19:32:13"^^xsd:datetime ;
            example:value 9.354825e+02 ],
        [ a example:Forecasting ;
            example:forecastedTimestamp "2022-11-22T03:32:13"^^xsd:datetime ;
            example:value 9.485019e+02 ],
        [ a example:Forecasting ;
            example:forecastedTimestamp "2022-11-22T18:32:13"^^xsd:datetime ;
            example:value 9.365354e+02 ] ;
    example:isForecastingFor <urn:ngsi-v2:cot-imec-be:WaterQualityObserved:imec-iow-4WYSEqBKuD2UKpNEQyW8AJ> ;
    example:unit "Â°C"^^xsd:celcius ;
    prov:generatedAtTime "2022-12-12T11:46:08+00:00"^^xsd:dateTime .
</code></pre>
