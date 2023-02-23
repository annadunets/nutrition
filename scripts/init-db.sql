--
-- PostgreSQL database dump

-- Dumped from database version 15.1 (Debian 15.1-1.pgdg110+1)
-- Dumped by pg_dump version 15.1 (Ubuntu 15.1-1.pgdg18.04+1)

\connect nutrition;

CREATE TABLE public.receipts (
    receipt_id SERIAL PRIMARY KEY,
    receipt_name VARCHAR(45) NOT NULL,
    date VARCHAR (20)
);

CREATE TABLE public.products (
    product_id SERIAL PRIMARY KEY,
    product_name character varying(45) NOT NULL,
    energy FLOAT,
    fat FLOAT,
    carbohydrate FLOAT,
    protein FLOAT
);

CREATE TABLE public.receipts_content (
    id SERIAL PRIMARY KEY,
    receipt_id INT REFERENCES receipts (receipt_id),
    product_id INT REFERENCES products (product_id),
    quantity FLOAT,
    unit_of_measurement VARCHAR
);

CREATE TABLE public.receipt_processing_logs (
    id SERIAL PRIMARY KEY,
    receipt_id INT REFERENCES receipts (receipt_id),
    message VARCHAR
);

--
-- PostgreSQL database dump complete
--
