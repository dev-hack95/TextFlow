import os
import whisper
from summarizer import TransformerSummarizer
from moviepy.editor import VideoFileClip

#Config
model = whisper.load_model("base")


def video_to_wav(input_video_path, output_wav_path):
    video_clip = VideoFileClip(input_video_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(output_wav_path, codec='wav')
    video_clip.close()
    audio_clip.close()

def wav_to_text(file_path):
   audio = file_path
   result = model.transcribe(audio)
   words = result["text"].split(" ") 
   model = TransformerSummarizer(transformer_type="XLNet", transformer_model_key="xlnet-base-cased")
   summary = ''.join(model(result["text"], max_length= len(words)))
   return summary


def transcribe_video(input_video_path):
    output_wav_path = "./session/temp_audio.wav"
    video_to_wav(input_video_path, output_wav_path)
    transcriptions = wav_to_text(output_wav_path)
    return transcriptions

if __name__ == "__main__":
    video_path = "./Python OOP Tutorial 1_ Classes and Instances.mp4"
    output = transcribe_video(video_path)
    print(output)
