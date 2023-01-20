--
-- PostgreSQL database dump

-- Dumped from database version 15.1 (Debian 15.1-1.pgdg110+1)
-- Dumped by pg_dump version 15.1 (Ubuntu 15.1-1.pgdg18.04+1)

\connect nutrition;

CREATE TABLE public.files (
    id SERIAL PRIMARY KEY,
    filename character varying(45) NOT NULL,
    date character varying(20)
);

--
-- PostgreSQL database dump complete
--
