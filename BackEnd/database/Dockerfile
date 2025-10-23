FROM postgres:14-alpine

ENV POSTGRES_USER=utility_user
ENV POSTGRES_PASSWORD=utility_password
ENV POSTGRES_DB=utility_db
ENV PGDATA=/var/lib/postgresql/data/pgdata

COPY initial_database.sql /docker-entrypoint-initdb.d/init.sql

EXPOSE 5432

HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
  CMD pg_isready -U utility_user -d utility_db

VOLUME ["/var/lib/postgresql/data"]