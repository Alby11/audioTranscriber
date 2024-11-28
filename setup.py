import tkinter as tk
from tkinter import filedialog
from openai import OpenAI
from pydub import AudioSegment
import os


def select_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        filetypes=[("MP3 files", "*.mp3")], title="Select an MP3 file"
    )
    return file_path


def split_audio(file_path, chunk_length_ms=60000):
    audio = AudioSegment.from_mp3(file_path)
    chunks = [
        audio[i : i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)
    ]
    chunk_files = []
    for i, chunk in enumerate(chunks):
        chunk_file = f"chunk_{i}.mp3"
        chunk.export(chunk_file, format="mp3")
        chunk_files.append(chunk_file)
    return chunk_files


def transcribe_file(file_path):
    client = OpenAI()
    chunk_files = split_audio(file_path)
    transcription_text = ""
    for chunk_file in chunk_files:
        with open(chunk_file, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1", file=audio_file, response_format="text"
            )
        transcription_text += transcription + "\n"
        os.remove(chunk_file)  # Clean up the chunk file

    # Save the transcription to a file named after the source audio file
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    transcription_file = f"{base_name}_transcription.txt"
    with open(transcription_file, "w") as f:
        f.write(transcription_text)


if __name__ == "__main__":
    file_path = select_file()
    if file_path:
        transcribe_file(file_path)
    else:
        print("No file selected.")
