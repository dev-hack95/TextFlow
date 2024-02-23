import os
import sys
import requests
import logging
import pika
import gridfs
from flask import jsonify
from pymongo import MongoClient
from converter import converter

logging.basicConfig(level=logging.INFO)

def main():
    client = MongoClient('mongodb://192.168.43.86:27017')
    db_videos = client.videos
    db_all_text = client.all_text
    db_text = client.text

    fs_videos = gridfs.GridFS(db_videos)
    fs_all_text = gridfs.GridFS(db_all_text)
    fs_text = gridfs.GridFS(db_text)

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.43.86', port=5672))
    channel = connection.channel()

    def callback(ch, method, properties, body):
            err = converter.start(body, fs_videos, fs_text, fs_all_text, ch)
            if err:
                ch.basic_nack(delivery_tag=method.delivery_tag)
            else:
                ch.basic_ack(delivery_tag=method.delivery_tag)

    print("To exit, press CTRL+C")

    channel.basic_consume(queue="video", on_message_callback=callback)
    #channel.basic_consume(queue="mp3", on_message_callback=callback1)

    channel.start_consuming()


if __name__ == "__main__":
    main()
