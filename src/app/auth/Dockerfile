FROM python:3.10-slim-bullseye
RUN apt-get update \
   && apt-get install -y --no-install-recommends --no-install-suggests \
   build-essential default-libmysqlclient-dev libpq-dev postgresql postgresql-contrib

ENV POSTGRES_USER=postgres
ENV POSTGRES_DB=auth_service
ENV POSTGRES_PASSWORD=postgres

RUN service postgresql start
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/
EXPOSE 8000
EXPOSE 5432
CMD service postgresql start && \
    su - postgres -c "createdb $POSTGRES_DB -E UTF8" && \
    su - postgres -c "psql -U $POSTGRES_USER -d $POSTGRES_DB -c \"ALTER SCHEMA public OWNER TO $POSTGRES_USER;\"" && \
    su - postgres -c "psql -U $POSTGRES_USER -d $POSTGRES_DB -c \"ALTER USER $POSTGRES_USER CREATEDB;\"" && \
    su - postgres -c "createdb auth_service -E UTF8" && \
    uvicorn server:app --host 0.0.0.0 --port 8000
