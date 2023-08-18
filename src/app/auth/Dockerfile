FROM python:3.10-slim-bullseye
RUN apt-get update \
   && apt-get install -y --no-install-recommends --no-install-suggests \
   build-essential default-libmysqlclient-dev libpq-dev postgresql postgresql-contrib
RUN  systemctl start postgresql.service
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/
EXPOSE 8000
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
