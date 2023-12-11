import os
import pika
import json


def upload(file, fs, channel, access):
    try:
        file_id = fs.put(file)
    except Exception as err:
        return 500, str(err)
    
    message = {
        "video_id": str(file_id),
        "audio_id": None,
        "username": access["user"],
    }

    try:
        channel.basic_publish(
            exchange='',
            routing_key="video",
            body=json.dumps(message),
            properties = pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except Exception as err:
        fs.delete(file_id)
        return str(err)
    
    return message