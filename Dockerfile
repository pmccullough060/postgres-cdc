FROM postgres:latest
ENV POSTGRES_DB=postgres_db
ENV POSTGRES_USER=local
ENV POSTGRES_PASSWORD=local
COPY schema.sql /docker-entrypoint-initdb.d/