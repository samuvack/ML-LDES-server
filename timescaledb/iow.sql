
drop table if exists public.water_quality;

CREATE TABLE IF NOT EXISTS public.water_quality
(
    id character varying NOT NULL,
    "batterijniveau_value" double precision, 
    "batterijniveau_date" text,
    "batterijniveau_sensor" character varying,
    "temperatuur_value" double precision,
    "temperatuur_date" text,
    "temperatuur_sensor" character varying,
    "conductiviteit_value"  double precision,
    "conductiviteit_date" text,
    "conductiviteit_sensor"  character varying,
    "hydro_druk_value" double precision,
    "hydro_druk_date" text,
    "hydro_druk_sensor" character varying
);


ALTER TABLE IF EXISTS public.water_quality OWNER to postgres;


SELECT create_hypertable('public.water_quality', 'generatedattime');

CREATE TABLE IF NOT EXISTS public.devices
(
    id character varying NOT NULL
);


CREATE TABLE IF NOT EXISTS public.gtfs
(
     "member_id" text,
    "arrival_id" text,
    "arrival_wkt" text,
    "arrival_halte" text,
    "arrival_time" text,
    "departure_id" text,
    "departure_wkt" text,
    "departure_halte" text,
    "departure_time"text
);

create table IF NOT EXISTS public.forecasting_models 
(
sensor_id text,
timestamp timestamp,
model text
)

create table IF NOT EXISTS public.forecasting
(
sensor_id text,
timestamp timestamp,
forecasting double precision,
model text
)

create table IF NOT EXISTS public.forecast(
id serial,
"sensor_id" text,
"ds" timestamp,
"yhat" double precision,
"yhat_lower" double precision,
"yhat_upper" double precision,
"latest_trained" timestamp,
"model_name" text
)

create view IF NOT EXISTS public.devices as
select *
from(
select distinct(id), min(temperatuur_date)
from water_quality
group by id) q
where q.min>'2022-11-08T16:28:53.000Z';

create table IF NOT EXISTS public.trained_models(
sensor_id text,
timestamp timestamp,
model text
)

