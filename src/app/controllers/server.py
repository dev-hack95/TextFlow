import os
import json
import pika
import gridfs
from pymongo import MongoClient
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from bson.objectid import ObjectId
from auth_svc import access
from auth import validate
from storage import utils

# config
load_dotenv()
MONGODB_URL = 'mongodb://192.168.29.186:27017'
mongo_client = MongoClient(MONGODB_URL)
db_instance = mongo_client.get_database("videos")
db_text = mongo_client.text
fs_text = gridfs.GridFS(db_text)

# Instnace of classes we are using
server = Flask(__name__)
fs = gridfs.GridFS(db_instance) # Video database (It is used to  upload large files in mongodb)

# Connecting RabbitMQ

# Setting up a rabbitMQ connction
connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.29.186', port=5672))
channel = connection.channel()

@server.post("/v1/server/login")
def login() -> str:
    token, err = access.login(request)

    if not err:
        return str(token)
    else:
        return str(err)

@server.route("/v1/server/upload", methods=["POST", "GET"])
def upload():
    access, err= validate.token(request)

    try:
        access_dict = json.loads(access)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format in the 'access' token"}, 400

    if access_dict["admin"]:
        if len(request.files) > 1 or len(request.files) < 1:
            return {"error": "Only Import one file"}, 400
        
        for _, file in request.files.items():
            message = utils.upload(file, fs, channel, access_dict)

            # if err:
            #     return str(err)
            
        return jsonify(message, "Uploded Succesfully!", 200)
    else:
        return "Not Authorized!", 401


    
@server.route("/v1/server/download", methods=["GET"])
def download():
    access, err= validate.token(request)

    try:
        access_dict = json.loads(access)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format in the 'access' token"}, 400
    
    if access_dict["admin"]:
        fid_string = request.args.get("fid")

        if not fid_string:
            return {"error":"No File ID provided"}, 400
        
        try:
            out = fs_text.get(ObjectId(fid_string))
            print(out)
        except Exception as err:
            raise err
        
    return out



if __name__ == "__main__":
    server.run(debug=True, port=5001)
