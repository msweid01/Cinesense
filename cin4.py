import os
import concurrent.futures
from tools import save_to_file, recognize_audio

def recognize_audio_file(audio_file_output_dir):
    audio_file, output_dir = audio_file_output_dir
    try:
        recognized_text = recognize_audio(audio_file)
        file_name = os.path.splitext(os.path.basename(audio_file))[0] + "_recognized.txt"
        output_file_path = os.path.join(output_dir, file_name)
        save_to_file(recognized_text, output_file_path)
    except Exception as e:
        print(f"Error recognizing audio for {audio_file}: {e}")

if __name__ == "__main__":
    audio_dir = "audio_output"
    output_text_dir = "text_output"

    os.makedirs(output_text_dir, exist_ok=True)
    audio_files = [os.path.join(audio_dir, filename) for filename in os.listdir(audio_dir) if filename.endswith(".wav")]
    audio_file_output_text_dirs = [(audio_file, output_text_dir) for audio_file in audio_files]

    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(recognize_audio_file, audio_file_output_text_dirs)
