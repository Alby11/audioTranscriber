import os
import tkinter as tk
from tkinter import filedialog
from openai import OpenAI
from pydub import AudioSegment
from tqdm import tqdm


def select_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        filetypes=[
            ("MP3 files", "*.mp3"),
            ("MP4 files", "*.mp4"),
            ("MPEG files", "*.mpeg"),
            ("MPGA files", "*.mpga"),
            ("M4A files", "*.m4a"),
            ("WAV files", "*.wav"),
            ("WEBM files", "*.webm"),
        ],
        title="Select an audio file",
    )
    return file_path


def split_audio(file_path, chunk_length_ms=60000):
    audio = AudioSegment.from_file(file_path)
    file_extension = os.path.splitext(file_path)[1][
        1:
    ]  # Get file extension without dot
    chunks = [
        audio[i : i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)
    ]
    chunk_files = []
    for i, chunk in enumerate(chunks):
        chunk_file = f"chunk_{i}.{file_extension}"
        chunk.export(
            chunk_file, format="mp4" if file_extension == "m4a" else file_extension
        )
        chunk_files.append(chunk_file)
    return chunk_files


def transcribe_file(file_path):
    client = OpenAI()
    chunk_files = split_audio(file_path)
    transcription_text = ""
    print("Processing...")
    for chunk_file in tqdm(chunk_files, desc="Transcribing", unit="chunk"):
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

    print("Transcription completed successfully!")


def main_function():
    file_path = select_file()
    if file_path:
        transcribe_file(file_path)
    else:
        print("No file selected.")
