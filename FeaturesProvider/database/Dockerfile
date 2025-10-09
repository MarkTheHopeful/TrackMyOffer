FROM postgres:14-alpine

# Set environment variables
ENV POSTGRES_USER=features_user
ENV POSTGRES_PASSWORD=features_password
ENV POSTGRES_DB=features_db
ENV PGDATA=/var/lib/postgresql/data/pgdata

COPY initial_database.sql /docker-entrypoint-initdb.d/init.sql

EXPOSE 5432

HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
  CMD pg_isready -U features_user -d features_db

VOLUME ["/var/lib/postgresql/data"]
