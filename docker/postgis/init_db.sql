CREATE TABLE IF NOT EXISTS public.iow
(
     id character varying COLLATE pg_catalog."default" NOT NULL,
     sal double precision,
     temp double precision,
     pred_lin double precision,
     r2_lin double precision,
     rmse_lin double precision,
     CONSTRAINT iow_pkey PRIMARY KEY (id)
)


TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.iow
    OWNER to ldes;