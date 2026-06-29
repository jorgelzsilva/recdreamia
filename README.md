# RecDreamia

RecDreamia is a professional-grade audio recording application designed to capture dual-stream audio. It records both system audio (loopback) and microphone audio simultaneously, then merges them into a **single mono MP3 file** ready for transcription.

## 🚀 Key Features

- **Single Merged Output**: System and microphone audio are recorded in parallel and automatically mixed into one mono MP3 (`gravacao.mp3`), so transcription only needs to process a single file.
- **Real-Time MP3 Encoding**: Uses the `lameenc` library for efficient, high-quality encoding.
- **Multiprocessing Isolation**: Each recording stream runs in its own process, ensuring stability and preventing native crashes on Windows. The two streams are merged in a post-processing step after recording stops.
- **Resilient Architecure**: Implements "Crash Early" principles with robust configuration validation.
- **Configurable**: Easily adjust sample rates and filenames via environment variables or CLI flags.

> The microphone and system streams are written to temporary MP3 files during recording (`gravacao_microfone.mp3` / `gravacao_sistema.mp3`). Once recording stops they are mixed into the single output file and removed.

## 🏗️ Technical Architecture

RecDreamia is built with a focus on orthogonality and decoupling:

- **`rec.py`**: The main entry point. It orchestrates the starting and stopping of recording processes using `multiprocessing`.
- **`_record_worker`**: A standalone worker function that handles the low-level WASAPI/CoreAudio interactions, PCM conversion, and MP3 encoding.
- **`AppConfig`**: A Pydantic-based configuration model that validates inputs and environment variables (loaded via `python-dotenv`).
- **`SoundCard`**: Used for cross-platform audio device abstraction.

## 📦 Installation

RecDreamia requires Python 3.8 or higher.

### 1. Prerequisites

Before installing Python dependencies, ensure your system has the necessary audio drivers and libraries.

#### **Windows**
- No special system libraries required (uses WASAPI).
- Ensure your audio devices are active.

#### **macOS**
- No special system libraries required (uses CoreAudio).

#### **Linux (Ubuntu/Debian)**
- Install ALSA and PulseAudio development headers:
  ```bash
  sudo apt-get update
  sudo apt-get install libasound2-dev libportaudio2 pulse-audio
  ```

### 2. Setup Virtual Environment

It is highly recommended to use a virtual environment:

```bash
# Create the environment
python -m venv recdreamia

# Activate it
# Windows:
recdreamia\Scripts\activate
# macOS/Linux:
source recdreamia/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 🛠️ Usage

### Quick Start

To start recording both system audio and microphone:

```bash
python rec.py
```

To stop recording, press `Ctrl+C`.

### Flags

- `--system_only`: Records only the system audio, disabling the microphone.

```bash
python rec.py --system_only
```

### Configuration (.env)

You can customize the recording behavior by creating a `.env` file in the root directory:

```env
RECORDING_SAMPLE_RATE=44100
RECORDING_FILE_MIC=gravacao_microfone.mp3
RECORDING_FILE_SYS=gravacao_sistema.mp3
RECORDING_FILE_OUT=gravacao.mp3
```

- `RECORDING_FILE_MIC` / `RECORDING_FILE_SYS`: temporary per-stream files (removed after merging).
- `RECORDING_FILE_OUT`: the final single mono MP3 used for transcription.

## 📝 License

This project is for internal use. All rights reserved.
