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


Of course a better way is by looking at the temporal scale (and even better spatio-temporal scale) instead of looking at all the historical measurments at ones (e.g. the case of regression models).
<p align="center">
  <img src="https://github.com/samuvack/ML-LDES-server/blob/master/images/timeseries3.png?raw=true"/>
</p>

  ## Online Machine Learning
  
  As a test, Holt Winters forecasting model from the Python package River has been tested. Holt-Winters forecasting is a way to model and predict the behavior of a sequence of values over time (time series). Holt-Winters is one of the most popular forecasting techniques for time series.
  

<p align="center">
  <img src="https://github.com/samuvack/ML-LDES-server/blob/master/output_ml/online_forecasting_snarimax.gif?raw=true"/>
</p>

When running `python server_forecasting_snarimax.py` the ML server will listen on port 8000 for LDES Post requests, filtering out the relevant values, and sending it into the SNARIMAX forecasting model. Hereafter, the model will automatically forecast a serie of estimated values.

Via the python script `python ./data_processing/demo_ldes_input.py`) a demo LDES POST request will be send to http://localhost:8000/input

<p align="center">
  <img src="https://github.com/samuvack/ML-LDES-server/blob/master/output_ml/gif_forecasting_SNARIMAX.gif?raw=true"/>
</p>

## Case study IoW (Internet of Water)

<p align="center">
  <img src="https://github.com/samuvack/ML-LDES-server/blob/master/images/plot_conductivity_temeprature.png?raw=true"/>
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
