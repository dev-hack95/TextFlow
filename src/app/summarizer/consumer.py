import os
import sys
import logging
import pika
import gridfs
from pymongo import MongoClient
from converter import converter

logging.basicConfig(level=logging.INFO)

def main():
    try:
        client = MongoClient('mongodb://192.168.29.186:27017')
        db_videos = client.videos
        db_mp3 = client.mp3
        db_text = client.text

        fs_videos = gridfs.GridFS(db_videos)
        fs_mp3s = gridfs.GridFS(db_mp3)
        fs_text = gridfs.GridFS(db_text)

        connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.29.186', port=5672))
        channel = connection.channel()

        def callback(ch, method, properties, body):
                err = converter.start(body, fs_videos, fs_mp3s, ch)
                if err:
                    ch.basic_nack(delivery_tag=method.delivery_tag)
                else:
                    ch.basic_ack(delivery_tag=method.delivery_tag)

        print("To exit, press CTRL+C")

        channel.basic_consume(queue="video", on_message_callback=callback)

        channel.start_consuming()

    except KeyboardInterrupt:
        connection.close()
    except Exception as err:
        raise err

if __name__ == "__main__":
    main()
