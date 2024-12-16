# 🎧 Audio Transcriber

Welcome to the **Audio Transcriber** project! This tool allows you to select audio files and transcribe their content using the OpenAI API. The transcriptions are saved as text files named after the source audio files.

## 📋 Features

- 🎵 **Select Audio Files**: Easily select audio files using a graphical file dialog.
- ✂️ **Split Audio**: Automatically split large audio files into smaller chunks.
- 📝 **Transcribe Audio**: Transcribe audio content using the OpenAI API.
- 💾 **Save Transcriptions**: Save transcriptions to text files named after the source audio files.
- ✨ **Refine Transcriptions**: Optionally refine transcriptions using a custom prompt with GPT-4.

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- Virtual environment (optional but recommended)
- OpenAI API key

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
   pip install openai pydub tqdm
   ```

4. **Set up the OpenAI API key**:
   - Obtain your OpenAI API key from [OpenAI](https://platform.openai.com/account/api-keys).
   - Set the `OPENAI_API_KEY` environment variable:
     ```sh
     export OPENAI_API_KEY='your-api-key-here'
     ```

### Usage

1. **Run the script**:
   ```sh
   python setup.py
   ```

2. **Select an audio file**:
   - A file dialog will pop up. Select the audio file you want to transcribe.

3. **Optionally input a prompt**:
   - You will be asked if you want to input a prompt to refine the transcript. If you choose yes, enter your prompt.

4. **Wait for the transcription**:
   - The script will split the audio file into chunks, transcribe each chunk, and save the transcription to a text file.

5. **Find your transcription**:
   - The transcription will be saved in the same directory as the source audio file, with `_raw_transcription.txt` and `_corrected_transcription.txt` appended to the base name.

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