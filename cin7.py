import os
import concurrent.futures
from tools import save_to_file, extract_emotions

def extract_emotions_file(text_file_output_dir):
    text_file, output_dir = text_file_output_dir
    try:
        with open(text_file, 'r') as file:
            text = file.read()

        emotions = extract_emotions(text)
        print(f"Detected emotions for {text_file}")

        file_name = os.path.splitext(os.path.basename(text_file))[0] + "_emotions.txt"
        output_file_path = os.path.join(output_dir, file_name)
        emotions_data = '\n'.join([f"{emotion}: {frequency}" for emotion, frequency in emotions.items()])
        save_to_file(emotions_data, output_file_path)
    except Exception as e:
        print(f"Error extracting emotions from {text_file}: {e}")

if __name__ == "__main__":
    text_output_dir = "text_output"
    output_emotions_dir = "emotions_output"
    os.makedirs(output_emotions_dir, exist_ok=True)

    text_files = [os.path.join(text_output_dir, filename) for filename in os.listdir(text_output_dir) if filename.endswith(".txt")]
    text_file_output_dirs = [(text_file, output_emotions_dir) for text_file in text_files]

    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(extract_emotions_file, text_file_output_dirs)
