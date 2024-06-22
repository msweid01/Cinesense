import os
import concurrent.futures
from tools import save_to_file, analyze_sentiment

def analyze_sentiment_file(text_file_output_dir):
    text_file, output_dir = text_file_output_dir
    try:
        with open(text_file, 'r') as file:
            text = file.read()

        polarity, subjectivity = analyze_sentiment(text)
        print(f"Analyzed sentiment for {text_file}")
        print(f"Polarity: {polarity}, Subjectivity: {subjectivity}")

        file_name = os.path.splitext(os.path.basename(text_file))[0] + "_sentiment.txt"
        output_file_path = os.path.join(output_dir, file_name)
        sentiment_data = f"Polarity: {polarity}\nSubjectivity: {subjectivity}\n"
        save_to_file(sentiment_data, output_file_path)
    except Exception as e:
        print(f"Error analyzing sentiment for {text_file}: {e}")

if __name__ == "__main__":
    text_audio_dir = "text_output"
    output_sentiment_dir = "sentiment_analysis"
    os.makedirs(output_sentiment_dir, exist_ok=True)

    text_files = [os.path.join(text_audio_dir, filename) for filename in os.listdir(text_audio_dir) if filename.endswith(".txt")]
    text_file_output_dirs = [(text_file, output_sentiment_dir) for text_file in text_files]

    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(analyze_sentiment_file, text_file_output_dirs)
