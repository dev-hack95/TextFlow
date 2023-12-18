FROM python:3.10
WORKDIR /app
RUN apt update -y
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/
EXPOSE 8000
ENTRYPOINT python consumer.py