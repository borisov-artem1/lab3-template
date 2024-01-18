--
-- PostgreSQL database cluster dump
--

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Roles
--

CREATE ROLE postgres;
ALTER ROLE postgres WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN REPLICATION BYPASSRLS PASSWORD 'SCRAM-SHA-256$4096:8uGrnbrmCBLLabRHWjNRzQ==$mQAOWifv+9lZaHAv7OZbs7cPGZAZIUCngB06LLLFx+M=:Xe13LTWZUGIoCfahdRWFxV6XAHNEWwaocMgfeN0wbEc=';
CREATE ROLE program;
ALTER ROLE program WITH NOSUPERUSER INHERIT NOCREATEROLE NOCREATEDB LOGIN NOREPLICATION NOBYPASSRLS PASSWORD 'SCRAM-SHA-256$4096:Eg6+qfSNo735RMq7PfNY3g==$GZUFGymXnwOeNpWkGzYL2NgHFm1LpeluCyuS8cAh7WU=:TRTrC46x7dXDC+gyOn4CNeorFuaTA6m69rV1mZ1XxZA=';

--
-- User Configurations
--








--
-- Databases
--

--
-- Database "template1" dump
--

\connect template1

--
-- PostgreSQL database dump
--

-- Dumped from database version 16.1
-- Dumped by pg_dump version 16.1

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
-- PostgreSQL database dump complete
--

--
-- Database "libraries" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 16.1
-- Dumped by pg_dump version 16.1

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
-- Name: libraries; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE libraries WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';


ALTER DATABASE libraries OWNER TO postgres;

\connect libraries

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
-- Name: book; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.book (
    id integer NOT NULL,
    book_uid uuid NOT NULL,
    name character varying(255) NOT NULL,
    author character varying(255) NOT NULL,
    genre character varying(255) NOT NULL,
    condition character varying(20),
    CONSTRAINT book_condition_check CHECK (((condition)::text = ANY ((ARRAY['EXCELLENT'::character varying, 'GOOD'::character varying, 'BAD'::character varying])::text[])))
);


ALTER TABLE public.book OWNER TO postgres;

--
-- Name: book_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.book_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.book_id_seq OWNER TO postgres;

--
-- Name: book_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.book_id_seq OWNED BY public.book.id;


--
-- Name: library; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.library (
    id integer NOT NULL,
    library_uid uuid NOT NULL,
    name character varying(80) NOT NULL,
    city character varying(255) NOT NULL,
    address character varying(255) NOT NULL
);


ALTER TABLE public.library OWNER TO postgres;

--
-- Name: library_book; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.library_book (
    id integer NOT NULL,
    book_id integer,
    library_id integer,
    available_count integer NOT NULL
);


ALTER TABLE public.library_book OWNER TO postgres;

--
-- Name: library_book_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.library_book_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.library_book_id_seq OWNER TO postgres;

--
-- Name: library_book_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.library_book_id_seq OWNED BY public.library_book.id;


--
-- Name: library_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.library_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.library_id_seq OWNER TO postgres;

--
-- Name: library_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.library_id_seq OWNED BY public.library.id;


--
-- Name: book id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book ALTER COLUMN id SET DEFAULT nextval('public.book_id_seq'::regclass);


--
-- Name: library id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.library ALTER COLUMN id SET DEFAULT nextval('public.library_id_seq'::regclass);


--
-- Name: library_book id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.library_book ALTER COLUMN id SET DEFAULT nextval('public.library_book_id_seq'::regclass);


--
-- Data for Name: book; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.book (id, book_uid, name, author, genre, condition) FROM stdin;
1	f7cdc58f-2caf-4b15-9727-f89dcc629b27	Краткий курс C++ в 7 томах	Бьерн Страуструп	Научная фантастика	EXCELLENT
\.


--
-- Data for Name: library; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.library (id, library_uid, name, city, address) FROM stdin;
1	83575e12-7ce0-48ee-9931-51919ff3c9ee	Библиотека имени 7 Непьющих	Москва	2-я Бауманская ул., д.5, стр.1
\.


--
-- Data for Name: library_book; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.library_book (id, book_id, library_id, available_count) FROM stdin;
1	1	1	1
\.


--
-- Name: book_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.book_id_seq', 1, true);


--
-- Name: library_book_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.library_book_id_seq', 1, true);


--
-- Name: library_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.library_id_seq', 1, true);


--
-- Name: book book_book_uid_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book
    ADD CONSTRAINT book_book_uid_key UNIQUE (book_uid);


--
-- Name: book book_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book
    ADD CONSTRAINT book_pkey PRIMARY KEY (id);


--
-- Name: library_book library_book_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.library_book
    ADD CONSTRAINT library_book_pkey PRIMARY KEY (id);


--
-- Name: library library_library_uid_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.library
    ADD CONSTRAINT library_library_uid_key UNIQUE (library_uid);


--
-- Name: library library_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.library
    ADD CONSTRAINT library_name_key UNIQUE (name);


--
-- Name: library library_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.library
    ADD CONSTRAINT library_pkey PRIMARY KEY (id);


--
-- Name: ix_book_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_book_id ON public.book USING btree (id);


--
-- Name: ix_library_book_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_library_book_id ON public.library_book USING btree (id);


--
-- Name: ix_library_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_library_id ON public.library USING btree (id);


--
-- Name: library_book library_book_book_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.library_book
    ADD CONSTRAINT library_book_book_id_fkey FOREIGN KEY (book_id) REFERENCES public.book(id);


--
-- Name: library_book library_book_library_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.library_book
    ADD CONSTRAINT library_book_library_id_fkey FOREIGN KEY (library_id) REFERENCES public.library(id);


--
-- Name: DATABASE libraries; Type: ACL; Schema: -; Owner: postgres
--

GRANT ALL ON DATABASE libraries TO program;


--
-- PostgreSQL database dump complete
--

--
-- Database "postgres" dump
--

\connect postgres

--
-- PostgreSQL database dump
--

-- Dumped from database version 16.1
-- Dumped by pg_dump version 16.1

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
-- Name: book; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.book (
    id integer NOT NULL,
    book_uid uuid NOT NULL,
    name character varying(255) NOT NULL,
    author character varying(255) NOT NULL,
    genre character varying(255) NOT NULL,
    condition character varying(20),
    CONSTRAINT book_condition_check CHECK (((condition)::text = ANY (ARRAY[('EXCELLENT'::character varying)::text, ('GOOD'::character varying)::text, ('BAD'::character varying)::text])))
);


ALTER TABLE public.book OWNER TO postgres;

--
-- Name: book_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.book_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.book_id_seq OWNER TO postgres;

--
-- Name: book_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.book_id_seq OWNED BY public.book.id;


--
-- Name: library; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.library (
    id integer NOT NULL,
    library_uid uuid NOT NULL,
    name character varying(80) NOT NULL,
    city character varying(255) NOT NULL,
    address character varying(255) NOT NULL
);


ALTER TABLE public.library OWNER TO postgres;

--
-- Name: library_book; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.library_book (
    id integer NOT NULL,
    book_id integer,
    library_id integer,
    available_count integer NOT NULL
);


ALTER TABLE public.library_book OWNER TO postgres;

--
-- Name: library_book_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.library_book_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.library_book_id_seq OWNER TO postgres;

--
-- Name: library_book_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.library_book_id_seq OWNED BY public.library_book.id;


--
-- Name: library_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.library_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.library_id_seq OWNER TO postgres;

--
-- Name: library_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.library_id_seq OWNED BY public.library.id;


--
-- Name: rating; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rating (
    id integer NOT NULL,
    username character varying(80) NOT NULL,
    stars integer,
    CONSTRAINT rating_stars_check CHECK (((stars >= 0) AND (stars <= 100)))
);


ALTER TABLE public.rating OWNER TO postgres;

--
-- Name: rating_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rating_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.rating_id_seq OWNER TO postgres;

--
-- Name: rating_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rating_id_seq OWNED BY public.rating.id;


--
-- Name: reservation; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reservation (
    id integer NOT NULL,
    reservation_uid uuid NOT NULL,
    username character varying(80) NOT NULL,
    book_uid uuid NOT NULL,
    library_uid uuid NOT NULL,
    status character varying(20),
    start_date timestamp with time zone NOT NULL,
    till_date timestamp with time zone NOT NULL,
    CONSTRAINT reservation_status_check CHECK (((status)::text = ANY (ARRAY[('RENTED'::character varying)::text, ('RETURNED'::character varying)::text, ('EXPIRED'::character varying)::text])))
);


ALTER TABLE public.reservation OWNER TO postgres;

--
-- Name: reservation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.reservation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reservation_id_seq OWNER TO postgres;

--
-- Name: reservation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.reservation_id_seq OWNED BY public.reservation.id;


--
-- Name: book id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book ALTER COLUMN id SET DEFAULT nextval('public.book_id_seq'::regclass);


--
-- Name: library id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.library ALTER COLUMN id SET DEFAULT nextval('public.library_id_seq'::regclass);


--
-- Name: library_book id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.library_book ALTER COLUMN id SET DEFAULT nextval('public.library_book_id_seq'::regclass);


--
-- Name: rating id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rating ALTER COLUMN id SET DEFAULT nextval('public.rating_id_seq'::regclass);


--
-- Name: reservation id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reservation ALTER COLUMN id SET DEFAULT nextval('public.reservation_id_seq'::regclass);


--
-- Data for Name: book; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.book (id, book_uid, name, author, genre, condition) FROM stdin;
1	f7cdc58f-2caf-4b15-9727-f89dcc629b27	Краткий курс C++ в 7 томах	Бьерн Страуструп	Научная фантастика	EXCELLENT
\.


--
-- Data for Name: library; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.library (id, library_uid, name, city, address) FROM stdin;
1	83575e12-7ce0-48ee-9931-51919ff3c9ee	Библиотека имени 7 Непьющих	Москва	2-я Бауманская ул., д.5, стр.1
\.


--
-- Data for Name: library_book; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.library_book (id, book_id, library_id, available_count) FROM stdin;
1	1	1	1
\.


--
-- Data for Name: rating; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rating (id, username, stars) FROM stdin;
\.


--
-- Data for Name: reservation; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reservation (id, reservation_uid, username, book_uid, library_uid, status, start_date, till_date) FROM stdin;
\.


--
-- Name: book_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.book_id_seq', 1, true);


--
-- Name: library_book_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.library_book_id_seq', 1, true);


--
-- Name: library_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.library_id_seq', 1, true);


--
-- Name: rating_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rating_id_seq', 1, false);


--
-- Name: reservation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.reservation_id_seq', 1, false);


--
-- Name: book book_book_uid_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book
    ADD CONSTRAINT book_book_uid_key UNIQUE (book_uid);


--
-- Name: book book_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book
    ADD CONSTRAINT book_pkey PRIMARY KEY (id);


--
-- Name: library_book library_book_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.library_book
    ADD CONSTRAINT library_book_pkey PRIMARY KEY (id);


--
-- Name: library library_library_uid_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.library
    ADD CONSTRAINT library_library_uid_key UNIQUE (library_uid);


--
-- Name: library library_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.library
    ADD CONSTRAINT library_name_key UNIQUE (name);


--
-- Name: library library_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.library
    ADD CONSTRAINT library_pkey PRIMARY KEY (id);


--
-- Name: rating rating_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rating
    ADD CONSTRAINT rating_pkey PRIMARY KEY (id);


--
-- Name: reservation reservation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reservation
    ADD CONSTRAINT reservation_pkey PRIMARY KEY (id);


--
-- Name: reservation reservation_reservation_uid_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reservation
    ADD CONSTRAINT reservation_reservation_uid_key UNIQUE (reservation_uid);


--
-- Name: ix_book_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_book_id ON public.book USING btree (id);


--
-- Name: ix_library_book_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_library_book_id ON public.library_book USING btree (id);


--
-- Name: ix_library_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_library_id ON public.library USING btree (id);


--
-- Name: ix_rating_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_rating_id ON public.rating USING btree (id);


--
-- Name: ix_reservation_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_reservation_id ON public.reservation USING btree (id);


--
-- Name: library_book library_book_book_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.library_book
    ADD CONSTRAINT library_book_book_id_fkey FOREIGN KEY (book_id) REFERENCES public.book(id);


--
-- Name: library_book library_book_library_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.library_book
    ADD CONSTRAINT library_book_library_id_fkey FOREIGN KEY (library_id) REFERENCES public.library(id);


--
-- PostgreSQL database dump complete
--

--
-- Database "ratings" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 16.1
-- Dumped by pg_dump version 16.1

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
-- Name: ratings; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE ratings WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';


ALTER DATABASE ratings OWNER TO postgres;

\connect ratings

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
-- Name: rating; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rating (
    id integer NOT NULL,
    username character varying(80) NOT NULL,
    stars integer,
    CONSTRAINT rating_stars_check CHECK (((stars >= 0) AND (stars <= 100)))
);


ALTER TABLE public.rating OWNER TO postgres;

--
-- Name: rating_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rating_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.rating_id_seq OWNER TO postgres;

--
-- Name: rating_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rating_id_seq OWNED BY public.rating.id;


--
-- Name: rating id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rating ALTER COLUMN id SET DEFAULT nextval('public.rating_id_seq'::regclass);


--
-- Data for Name: rating; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rating (id, username, stars) FROM stdin;
\.


--
-- Name: rating_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rating_id_seq', 1, false);


--
-- Name: rating rating_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rating
    ADD CONSTRAINT rating_pkey PRIMARY KEY (id);


--
-- Name: ix_rating_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_rating_id ON public.rating USING btree (id);


--
-- Name: DATABASE ratings; Type: ACL; Schema: -; Owner: postgres
--

GRANT ALL ON DATABASE ratings TO program;


--
-- PostgreSQL database dump complete
--

--
-- Database "reservations" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 16.1
-- Dumped by pg_dump version 16.1

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
-- Name: reservations; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE reservations WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';


ALTER DATABASE reservations OWNER TO postgres;

\connect reservations

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
-- Name: reservation; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reservation (
    id integer NOT NULL,
    reservation_uid uuid NOT NULL,
    username character varying(80) NOT NULL,
    book_uid uuid NOT NULL,
    library_uid uuid NOT NULL,
    status character varying(20),
    start_date timestamp with time zone NOT NULL,
    till_date timestamp with time zone NOT NULL,
    CONSTRAINT reservation_status_check CHECK (((status)::text = ANY ((ARRAY['RENTED'::character varying, 'RETURNED'::character varying, 'EXPIRED'::character varying])::text[])))
);


ALTER TABLE public.reservation OWNER TO postgres;

--
-- Name: reservation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.reservation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reservation_id_seq OWNER TO postgres;

--
-- Name: reservation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.reservation_id_seq OWNED BY public.reservation.id;


--
-- Name: reservation id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reservation ALTER COLUMN id SET DEFAULT nextval('public.reservation_id_seq'::regclass);


--
-- Data for Name: reservation; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reservation (id, reservation_uid, username, book_uid, library_uid, status, start_date, till_date) FROM stdin;
\.


--
-- Name: reservation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.reservation_id_seq', 1, false);


--
-- Name: reservation reservation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reservation
    ADD CONSTRAINT reservation_pkey PRIMARY KEY (id);


--
-- Name: reservation reservation_reservation_uid_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reservation
    ADD CONSTRAINT reservation_reservation_uid_key UNIQUE (reservation_uid);


--
-- Name: ix_reservation_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_reservation_id ON public.reservation USING btree (id);


--
-- Name: DATABASE reservations; Type: ACL; Schema: -; Owner: postgres
--

GRANT ALL ON DATABASE reservations TO program;


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database cluster dump complete
--

