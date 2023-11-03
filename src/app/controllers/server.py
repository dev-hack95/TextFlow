import os
import json
import pika
import gridfs
from pymongo import MongoClient
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status, Depends, Request
from auth_svc import access
from auth import validate
from storage import utils

# config
load_dotenv()
MONGODB_URL = os.getenv('MONGO_CONNECTION_STRING')
mongo_client = MongoClient(MONGODB_URL)
db_instance = mongo_client.get_database("videos")

# Instnace of classes we are using
server = FastAPI()
fs = gridfs.GridFS(db_instance) # Video database (It is used to  upload large files in mongodb)

# Connecting RabbitMQ

# Setting up a rabbitMQ connction
connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()

@server.post("/v1/server/login")
def login():
    token, err = access.login(Request)

    if not err:
        return token
    else:
        return err

@server.post("/v1/server/upload")
def upload():
    access, err = validate.token(Request)
    access = json.loads(access)

    if access['admin']:
        if len(Request.files) > 1 or len(Request.files) < 1:
            return {"error": "Only Import one file"}, status.HTTP_400_BAD_REQUEST
        
        for _, file in Request.files.items():
            err = utils.upload(file, fs, channel, access)

            if err:
                return err
            
        return "Uploded Succesfully!", status.HTTP_200_OK
    else:
        return "Not Authorised!", status.HTTP_401_UNAUTHORIZED
    
@server.get("/v1/server/download")
def download():
    pass
