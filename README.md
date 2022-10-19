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

Afterwards, it becomes possible to run the ML-LDES server by the following command:
```
python data_processing/server.py
```



## Documentation

The ML-LDES server listens on port 8000 and receives LDES N-tripples. Immediately afterwards, the relevant data is injected into the Machine Learning model. As a test, it was currently chosen to apply different regression models to the data.

## What's included




