import os
import pika
import json
from fastapi import status

def upload(file, fs, channel, access):
    try:
        file_id = fs.put(file)
    except Exception as err:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    
    message = {
        "video_id": str(file_id),
        "audio_id": None,
        "username": access["username"],
    }

    try:
        channel.basic_publish(
            exchange='',
            routing_key="video",
            body=json.dumps(message),
            properties = pika.BasicProperties(
                delivery_mode=pika.spec.PRESISTENT_DELIVERY_MODE
            ),
        )
    except Exception as err:
        fs.delete(file_id)
        return err