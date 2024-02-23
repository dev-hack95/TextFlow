import os
import json
import pika
from flask import jsonify
from bson.objectid import ObjectId
from summarizer import TransformerSummarizer
from moviepy.editor import VideoFileClip
import whisper

# Config
SESSION_FOLDER = "./session"
os.makedirs(SESSION_FOLDER, exist_ok=True)

def wav_to_text_summary(file_path):
    audio = file_path
    model = whisper.load_model("base")
    result = model.transcribe(audio)
    model = TransformerSummarizer(transformer_type="XLNet", transformer_model_key="xlnet-base-cased")
    summary = ''.join(model(result["text"], max_length=4000))
    return summary, result


def start(message, fs_videos, fs_text, fs_all_text, channel):
    message = json.loads(message)
    print(str(message))
    video_data = fs_videos.get(ObjectId(message["video_fid"]))
    video_filename = f"{SESSION_FOLDER}/{message['video_fid']}.mp4"
    with open(video_filename, 'wb') as video_file:
        video_file.write(video_data.read())

    video_clip = VideoFileClip(video_filename)
    audio_clip = video_clip.audio

    mp3_filename = f"{SESSION_FOLDER}/{message['video_fid']}.mp3"

    audio_clip.write_audiofile(mp3_filename)
    video_clip.close()
    audio_clip.close()

    # f = open(mp3_filename, 'rb')
    # data = f.read()

    # mp3fid = fs_mp3s.put(data)

    output, result = wav_to_text_summary(mp3_filename)
    print(output)
    output_bytes = output.encode('utf-8')
    all_text_bytes = result.encode('utf-8')

    fid = fs_text.put(output_bytes)
    all_text_fid = fs_all_text(all_text_bytes)
    #message["mp3_fid"] = str(mp3fid)
    message["all_text"] = str(all_text_fid)
    message["text_id"] = str(fid)
    print(message)

    try:
        channel.basic_publish(
            exchange="",
            routing_key="text",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
    except Exception as err:
        #fs_mp3s.delete(mp3fid)
        fs_text.delete(fid)
        return str(err)