FROM postgres:latest
ENV POSTGRES_PASSWORD=pokeDexv1.0
ENV POSTGRES_USER=pokeDex_admin
ENV POSTGRES_DB=poke_dex
COPY create_fixtures.sql /docker-entrypoint-initdb.d/create_fixtures.sql