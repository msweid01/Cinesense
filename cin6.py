import os
import concurrent.futures
from tools import save_to_file, translate_text

def translate_text_file(text_file_output_dir):
    text_file, output_dir = text_file_output_dir
    try:
        with open(text_file, 'r') as file:
            text = file.read()

        translated = translate_text(text)
        print(f"Translated text for {text_file}")

        file_name = os.path.splitext(os.path.basename(text_file))[0] + "_translated.txt"
        output_file_path = os.path.join(output_dir, file_name)
        save_to_file(translated, output_file_path)
    except Exception as e:
        print(f"Error translating text for {text_file}: {e}")

if __name__ == "__main__":
    text_output_dir = "text_output"
    output_translated_dir = "translated_texts"
    os.makedirs(output_translated_dir, exist_ok=True)

    text_files = [os.path.join(text_output_dir, filename) for filename in os.listdir(text_output_dir) if filename.endswith(".txt")]
    text_file_output_dirs = [(text_file, output_translated_dir) for text_file in text_files]

    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(translate_text_file, text_file_output_dirs)
