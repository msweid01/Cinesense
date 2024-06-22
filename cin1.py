import threading
import multiprocessing
import time
from tools import load_data, get_video


# Initialize a semaphore for limiting concurrent threads
connection_semaphore = threading.Semaphore(5)

video_urls = load_data("video_urls.txt")

def serial_runner():
    t1 = time.perf_counter()
    for video_url in video_urls:
        get_video(video_url)
    t2 = time.perf_counter()
    print(f'Serial finished in {t2 - t1} seconds')

def process_runner():
    t1 = time.perf_counter()
    processes = []
    for video_url in video_urls:
        process = multiprocessing.Process(target=get_video, args=(video_url, "video_output", None, None, False))
        processes.append(process)
        process.start()

    # Wait for all processes to complete
    for process in processes:
        process.join()
    t2 = time.perf_counter()
    print(f'Parallel (processes) finished in {t2 - t1} seconds')


def thread_runner():
    t1 = time.perf_counter()
    threads = []
    for video_url in video_urls:
        thread = threading.Thread(target=get_video, args=(video_url, "video_output", connection_semaphore, None, False))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    t2 = time.perf_counter()
    print(f'Parallel (threads) finished in {t2 - t1} seconds')

if __name__ == "__main__":
    print("Running serially...")
    serial_runner()

    print("\nRunning with threads...")
    thread_runner()

    print("\nRunning with processes...")
    process_runner()
