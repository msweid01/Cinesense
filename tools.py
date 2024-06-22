import os
import time
from pytube import YouTube
import speech_recognition as sr
from textblob import TextBlob
import spacy
from nrclex import NRCLex
from googletrans import Translator
from datetime import datetime
from moviepy.editor import VideoFileClip
import threading



def load_data(file_path):
    data_list = []
    with open(file_path, 'r') as file:
        for line in file:
            line_data = line.strip()
            data_list.append(line_data)
    return data_list


def log_download(url, success):
    log_lock = threading.Lock()
    timestamp = datetime.now().strftime('%H:%M, %d %B %Y')
    log_entry = f'"Timestamp": {timestamp}, "URL":"{url}", "Download":{success}\n'
    log_lock.acquire()
    try:
        with open("download_log.txt", "a") as log_file:
            log_file.write(log_entry)
    finally:
        log_lock.release()
def get_video(video_url, output_dir="video_output", semaphore=None, thread_id=None, logging=False):
    if semaphore:
        semaphore.acquire()
    try:
        os.makedirs(output_dir, exist_ok=True)
        yt = YouTube(video_url)
        stream = yt.streams.get_highest_resolution()
        if thread_id is not None:
            print(f"Thread {thread_id} is downloading video: {yt.title}")
        else:
            print(f"Downloading video: {yt.title}")
        stream.download(output_path=output_dir)
        if thread_id is not None:
            print(f"Thread {thread_id} has finished downloading video: {yt.title}")
        else:
            print(f"Download completed: {yt.title}")
        if logging:
            log_download(video_url, True)
    except Exception as e:
        print(f"Error downloading video from {video_url}: {e}")
        if logging:
            log_download(video_url, False)
    finally:
        if semaphore:
            semaphore.release()


def measure_time(func, *args):
    start_time = time.time()
    func(*args)
    end_time = time.time()
    return end_time - start_time

def save_to_file(data, file_path):
    try:
        with open(file_path, 'w') as file:
            file.write(data)
        print(f"Data has been written to {file_path}")
    except Exception as e:
        print(f"Error writing data to {file_path}: {e}")


def recognize_audio(audio_file_path):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file_path) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio)
        return text
    except Exception as e:
        print(f"Error recognizing audio '{audio_file_path}': {e}")
        return None

def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment
    return sentiment.polarity, sentiment.subjectivity

def translate_text(text, src_lang='en', dest_lang='es'):
    translator = Translator()
    translated = translator.translate(text, src=src_lang, dest=dest_lang).text
    return translated

def extract_emotions(text):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    full_text = ' '.join([sent.text for sent in doc.sents])
    emotion = NRCLex(full_text)
    return emotion.affect_frequencies


def extract_audio(video_file_output_dir):
    video_file, output_dir = video_file_output_dir
    try:
        video = VideoFileClip(video_file)
        audio_file = os.path.join(output_dir, os.path.splitext(os.path.basename(video_file))[0] + ".wav")
        audio = video.audio
        audio.write_audiofile(audio_file, codec='pcm_s16le')
        print(f"Audio extracted and saved: {audio_file}")
    except Exception as e:
        print(f"Error extracting audio from {video_file}: {e}")