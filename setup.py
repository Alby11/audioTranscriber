import os
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog, ttk
import openai  # Correct import
from pydub import AudioSegment
from tqdm import tqdm
import threading
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    print("Error: OPENAI_API_KEY environment variable not set.")
    exit(1)

# Token limit for the OpenAI API
TOKEN_LIMIT = 10000


# Function to select an audio file using a file dialog
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


# Function to split the audio file into smaller chunks
def split_audio(file_path, chunk_length_ms=60000):
    print("Starting audio splitting...")
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
        export_format = "mp4" if file_extension == "m4a" else file_extension
        chunk.export(chunk_file, format=export_format)
        chunk_files.append(chunk_file)
    print("Audio splitting completed.")
    return chunk_files


# Function to transcribe a single audio chunk using the OpenAI API
def transcribe(audio_file):
    try:
        with open(audio_file, "rb") as file:
            transcript = openai.Audio.transcribe(model="whisper-1", file=file)
        return transcript["text"]
    except Exception as e:
        print(f"Error transcribing {audio_file}: {e}")
        return ""


# Function to generate a corrected transcript using GPT
def generate_corrected_transcript(temperature, system_prompt, transcription_text):
    try:
        max_tokens = TOKEN_LIMIT
        chunks = [
            transcription_text[i : i + max_tokens]
            for i in range(0, len(transcription_text), max_tokens)
        ]
        corrected_text = ""
        for chunk in chunks:
            response = openai.ChatCompletion.create(
                model="91-preview",  # Updated model name
                temperature=temperature,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": chunk},
                ],
            )
            corrected_text += response.choices[0].message["content"]
        return corrected_text
    except Exception as e:
        print(f"Error during text correction: {e}")
        return transcription_text


# Custom dialog class to ask the user for a prompt
class PromptDialog(simpledialog.Dialog):
    def body(self, master):
        self.label = tk.Label(master, text="Please enter your prompt:")
        self.label.pack(pady=5)

        self.text = tk.Text(master, height=10, width=50)
        self.text.pack(pady=5)
        self.text.bind("<KeyRelease>", self.update_count)

        self.count_label = tk.Label(master, text="0 / 10000 characters")
        self.count_label.pack(pady=5)

        return self.text

    def update_count(self, event=None):
        current_length = len(self.text.get("1.0", "end-1c"))
        self.count_label.config(text=f"{current_length} / 10000 characters")
        if current_length >= TOKEN_LIMIT:
            self.text.delete("1.0 + %d chars" % TOKEN_LIMIT, "end")

    def apply(self):
        self.result = self.text.get("1.0", "end-1c")


# Function to ask the user if they want to input a prompt
def ask_for_prompt():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    answer = messagebox.askyesno(
        "Input Prompt", "Do you want to input a prompt to refine the transcript?"
    )
    if answer:
        dialog = PromptDialog(root)
        return dialog.result
    return None


# Function to show a spinner during the chunking process
def show_spinner(window, label_text):
    spinner_label = ttk.Label(window, text=label_text)
    spinner_label.pack(pady=10)
    spinner = ttk.Progressbar(window, mode="indeterminate")
    spinner.pack(pady=10)
    spinner.start()
    window.update()
    return spinner, spinner_label


# Main function to transcribe the audio file and generate the corrected transcript
def transcribe_file(file_path, user_prompt):
    print("Starting transcription process...")

    # Split the audio file
    chunk_files = split_audio(file_path)
    print("Chunking process completed.")
    print(f"Number of chunks created: {len(chunk_files)}")

    # Check if chunks were created
    if not chunk_files:
        print("No chunks were created.")
        return

    # Transcribe each chunk
    transcription_text = ""
    print("Starting chunk processing...")
    for i, chunk_file in enumerate(chunk_files):
        print(f"Processing chunk {i+1}/{len(chunk_files)}: {chunk_file}")
        result = transcribe(chunk_file)
        transcription_text += result + "\n"
        os.remove(chunk_file)  # Clean up
        print(f"Finished processing chunk {i+1}/{len(chunk_files)}")

    # Save the raw transcription
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    raw_transcription_file = f"{base_name}_raw_transcription.txt"
    with open(raw_transcription_file, "w") as f:
        f.write(transcription_text)
    print(f"Raw transcription saved to {raw_transcription_file}")

    # Generate corrected transcript if user provided a prompt
    if user_prompt:
        corrected_text = generate_corrected_transcript(
            0, user_prompt, transcription_text
        )
    else:
        corrected_text = transcription_text

    # Save the corrected transcription
    corrected_transcription_file = f"{base_name}_corrected_transcription.txt"
    with open(corrected_transcription_file, "w") as f:
        f.write(corrected_text)
    print(f"Corrected transcription saved to {corrected_transcription_file}")

    print("Transcription completed successfully!")


if __name__ == "__main__":
    file_path = select_file()
    if file_path:
        user_prompt = ask_for_prompt()
        transcribe_file(file_path, user_prompt)
    else:
        print("No file selected.")
