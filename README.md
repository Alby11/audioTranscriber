# 🎧 Audio Transcriber

Welcome to the **Audio Transcriber** project! This tool allows you to select MP3 files and transcribe their audio content using the OpenAI API. The transcriptions are saved as text files named after the source audio files.

## 📋 Features

- 🎵 **Select MP3 Files**: Easily select MP3 files using a graphical file dialog.
- ✂️ **Split Audio**: Automatically split large audio files into smaller chunks.
- 📝 **Transcribe Audio**: Transcribe audio content using the OpenAI API.
- 💾 **Save Transcriptions**: Save transcriptions to text files named after the source audio files.

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- Virtual environment (optional but recommended)

### Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/Alby11/audioTranscriber.git
   cd audioTranscriber
   ```

2. **Create and activate a virtual environment**:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the required libraries**:
   ```sh
   pip install openai pydub
   ```

### Usage

1. **Run the script**:
   ```sh
   python setup.py
   ```

2. **Select an MP3 file**:
   - A file dialog will pop up. Select the MP3 file you want to transcribe.

3. **Wait for the transcription**:
   - The script will split the audio file into chunks, transcribe each chunk, and save the transcription to a text file.

4. **Find your transcription**:
   - The transcription will be saved in the same directory as the source audio file, with `_transcription.txt` appended to the base name.

## 🛠️ Configuration

- **Chunk Length**: You can adjust the chunk length (in milliseconds) by modifying the `chunk_length_ms` parameter in the `split_audio` function.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## 📧 Contact

For any questions or suggestions, feel free to reach out to me on [GitHub](https://github.com/Alby11).

---

Happy transcribing! 🎉