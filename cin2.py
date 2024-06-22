import threading
import time
from tools import load_data, get_video


def thread_runner():
    video_urls = load_data("video_urls.txt")
    t1 = time.perf_counter()
    threads = []
    for i, video_url in enumerate(video_urls):
        thread = threading.Thread(target=get_video, args=(video_url, "video_output", None, i, True))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    t2 = time.perf_counter()
    print(f'Parallel (threads) finished in {t2 - t1} seconds')

if __name__ == "__main__":
    print("\nRunning with threads...")
    thread_runner()
