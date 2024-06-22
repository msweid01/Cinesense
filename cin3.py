import os
import concurrent.futures
import threading
from tools import measure_time, extract_audio


def extract_audio_serial(video_file_output_dirs):
    for video_file_output_dir in video_file_output_dirs:
        extract_audio(video_file_output_dir)

def extract_audio_threading(video_file_output_dirs):
    threads = []
    for video_file_output_dir in video_file_output_dirs:
        thread = threading.Thread(target=extract_audio, args=(video_file_output_dir,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def extract_audio_threadpool(video_file_output_dirs):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(extract_audio, video_file_output_dirs)

def extract_audio_multiprocessing(video_file_output_dirs):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(extract_audio, video_file_output_dirs)

if __name__ == "__main__":
    output_audio_dir = "audio_output"
    os.makedirs(output_audio_dir, exist_ok=True)

    video_dir = "video_output"
    video_files = [os.path.join(video_dir, filename) for filename in os.listdir(video_dir) if filename.endswith(".mp4")]
    video_file_output_dirs = [(video_file, output_audio_dir) for video_file in video_files]

    serial_time = measure_time(extract_audio_serial, video_file_output_dirs)
    print(f"Serial processing time: {serial_time:.2f} seconds")

    threading_time = measure_time(extract_audio_threading, video_file_output_dirs)
    print(f"Threading (manual threading) processing time: {threading_time:.2f} seconds")

    threadpool_time = measure_time(extract_audio_threadpool, video_file_output_dirs)
    print(f"ThreadPoolExecutor processing time: {threadpool_time:.2f} seconds")

    multiprocessing_time = measure_time(extract_audio_multiprocessing, video_file_output_dirs)
    print(f"Multiprocessing time: {multiprocessing_time:.2f} seconds")
