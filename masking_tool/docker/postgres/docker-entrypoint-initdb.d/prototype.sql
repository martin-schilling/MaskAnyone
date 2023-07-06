--
-- PostgreSQL database dump
--

-- Dumped from database version 15.3
-- Dumped by pg_dump version 15.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: prototype; Type: DATABASE; Schema: -; Owner: dev
--

CREATE DATABASE prototype WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';


ALTER DATABASE prototype OWNER TO dev;

\connect prototype

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: jobs; Type: TABLE; Schema: public; Owner: dev
--

CREATE TABLE public.jobs (
    id uuid NOT NULL,
    video_id uuid NOT NULL,
    result_video_id uuid NOT NULL,
    type character varying NOT NULL,
    status character varying NOT NULL,
    data jsonb NOT NULL,
    created_at timestamp without time zone NOT NULL,
    started_at timestamp without time zone,
    finished_at timestamp without time zone
);


ALTER TABLE public.jobs OWNER TO dev;

--
-- Name: result_videos; Type: TABLE; Schema: public; Owner: dev
--

CREATE TABLE public.result_videos (
    id uuid NOT NULL,
    video_id uuid NOT NULL,
    job_id uuid NOT NULL,
    video_info jsonb
);


ALTER TABLE public.result_videos OWNER TO dev;

--
-- Name: videos; Type: TABLE; Schema: public; Owner: dev
--

CREATE TABLE public.videos (
    id uuid NOT NULL,
    name character varying NOT NULL,
    status character varying NOT NULL,
    video_info jsonb
);


ALTER TABLE public.videos OWNER TO dev;

--
-- Name: jobs jobs_pkey; Type: CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.jobs
    ADD CONSTRAINT jobs_pkey PRIMARY KEY (id);


--
-- Name: result_videos result_videos_pkey; Type: CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.result_videos
    ADD CONSTRAINT result_videos_pkey PRIMARY KEY (id);


--
-- Name: jobs unique_result_video_id; Type: CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.jobs
    ADD CONSTRAINT unique_result_video_id UNIQUE (result_video_id);


--
-- Name: videos videos_pkey; Type: CONSTRAINT; Schema: public; Owner: dev
--

ALTER TABLE ONLY public.videos
    ADD CONSTRAINT videos_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--
