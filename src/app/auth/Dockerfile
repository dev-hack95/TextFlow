FROM python:3.10-slim-bullseye
WORKDIR /app
RUN apt update -y
RUN apt install -y --no-install-recommends --no-install-suggests build-essential gcc
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/
EXPOSE 8000
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
