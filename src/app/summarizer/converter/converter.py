import os
import json
import pika
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
    words = result["text"].split(" ")
    model = TransformerSummarizer(transformer_type="XLNet", transformer_model_key="xlnet-base-cased")
    summary = ''.join(model(result["text"], max_length=len(words)))
    return summary


def start(message, fs_videos, fs_mp3s, channel):
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


    f = open(mp3_filename, 'rb')
    data = f.read()
    fid = fs_mp3s.put(data)

    message["mp3_fid"] = str(fid)
    try:
        channel.basic_publish(
            exchange="",
            routing_key="mp3",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
    except Exception as err:
        print(err)
        fs_mp3s.delete(fid)
        return str(err)

