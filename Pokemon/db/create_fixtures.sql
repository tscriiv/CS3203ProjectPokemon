--
SELECT 'CREATE DATABASE poke_dex'
    WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'poke_dex');

-- Create a table named 'users'
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS rosters (
    roster_id SERIAL PRIMARY KEY,
    user_id NUMERIC,
    pokemon_url VARCHAR(64)
);

INSERT INTO public.users
(user_id, username, "password")
VALUES(nextval('users_user_id_seq'::regclass), 'hulk', 'smash');

INSERT INTO public.users
(user_id, username, "password")
VALUES(nextval('users_user_id_seq'::regclass), 'spiderman', 'web');

INSERT INTO rosters (user_id, pokemon_url) VALUES (1, 'https://pokeapi.co/api/v2/pokemon/bulbasaur');
INSERT INTO rosters (user_id, pokemon_url) VALUES (1, 'https://pokeapi.co/api/v2/pokemon/66/');

INSERT INTO rosters (user_id, pokemon_url) VALUES (2, 'https://pokeapi.co/api/v2/pokemon/56/');
INSERT INTO rosters (user_id, pokemon_url) VALUES (2, 'https://pokeapi.co/api/v2/pokemon/80/');

