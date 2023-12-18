import os
import sys
import requests
import logging
import pika

logging.basicConfig(level=logging.INFO)

def main():

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.43.86', port=5672))
    channel = connection.channel()

    def callback(ch, method, properties, body):
            message = body.decode('utf-8')
            return message

    print("To exit, press CTRL+C")

    channel.basic_consume(queue="text", on_message_callback=callback)
    #channel.basic_consume(queue="mp3", on_message_callback=callback1)

    channel.start_consuming()

