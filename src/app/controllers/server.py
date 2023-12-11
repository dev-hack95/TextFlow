import os
import json
import pika
import gridfs
from pymongo import MongoClient
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from auth_svc import access
from auth import validate
from storage import utils

# config
load_dotenv()
MONGODB_URL = 'mongodb://192.168.29.186:27017'
mongo_client = MongoClient(MONGODB_URL)
db_instance = mongo_client.get_database("videos")

# Instnace of classes we are using
server = Flask(__name__)
fs = gridfs.GridFS(db_instance) # Video database (It is used to  upload large files in mongodb)

# Connecting RabbitMQ

# Setting up a rabbitMQ connction
connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.29.186', port=5672))
channel = connection.channel()

@server.post("/v1/server/login")
def login():
    token, err = access.login(request)

    if not err:
        return token
    else:
        return str(err)

@server.route("/v1/server/upload", methods=["POST", "GET"])
def upload():
    access, err = validate.token(request)

    try:
        access_dict = json.loads(access)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format in the 'access' token"}, 400

    if access_dict[0]["admin"]:
        if len(request.files) > 1 or len(request.files) < 1:
            return {"error": "Only Import one file"}, 400
        
        for _, file in request.files.items():
            err = utils.upload(file, fs, channel, access_dict[0])

            if err:
                return str(err)
            
        return "Uploded Succesfully!", 200
    else:
        return "Not Authorized!", 401



    
@server.get("/v1/server/download")
def download():
    pass


if __name__ == "__main__":
    server.run(debug=True, port=5001)