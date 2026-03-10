import os
import sys
import argparse
import multiprocessing
import warnings
import numpy
from pydantic import BaseModel, Field, field_validator
from dotenv import load_dotenv


# --- Configuration (Design by Contract / Crash Early) ---
class AppConfig(BaseModel):
    sample_rate: int = Field(default=44100, gt=0, description="Sample rate for recording")
    file_mic: str = Field(default="gravacao_microfone.mp3")
    file_sys: str = Field(default="gravacao_sistema.mp3")
    system_only: bool = Field(default=False, description="Record only system audio")

    @field_validator('file_mic', 'file_sys')
    @classmethod
    def validate_extension(cls, v: str) -> str:
        if not v.endswith('.mp3'):
            raise ValueError("File name must end with .mp3")
        return v


def load_config(system_only: bool = False) -> AppConfig:
    """Loads configuration from environment variables and validates it."""
    load_dotenv()
    # Note: 44100 is more standard for MP3 than 48000
    return AppConfig(
        sample_rate=int(os.environ.get("RECORDING_SAMPLE_RATE", 44100)),
        file_mic=os.environ.get("RECORDING_FILE_MIC", "gravacao_microfone.mp3"),
        file_sys=os.environ.get("RECORDING_FILE_SYS", "gravacao_sistema.mp3"),
        system_only=system_only,
    )


# --- Core Business Logic (Orthogonal & Decoupled) ---
def _record_worker(device_id: str, filename: str, sample_rate: int, is_loopback: bool, stop_event):
    """Standalone worker: records in chunks, encodes to MP3 in real-time until stop_event.

    Each process gets its own COM initialization via lazy import,
    completely isolating WASAPI state and avoiding native-level crashes.
    """
    import warnings
    warnings.filterwarnings("ignore")
    # Silence specific soundcard warnings that can flood the console on Windows
    try:
        from soundcard.mediafoundation import SoundcardRuntimeWarning
        warnings.filterwarnings("ignore", category=SoundcardRuntimeWarning)
    except ImportError:
        pass

    import soundcard as sc
    import lameenc
    import os

    # Resolve device
    try:
        if is_loopback:
            device = sc.get_microphone(device_id, include_loopback=True)
        else:
            device = None
            for mic in sc.all_microphones():
                if mic.id == device_id:
                    device = mic
                    break
            if device is None:
                print(f"[Worker] Microfone nao encontrado: {device_id}")
                os._exit(1)
    except Exception as e:
        print(f"[Worker] Erro ao buscar dispositivo: {e}")
        os._exit(1)

    try:
        d_name = device.name
    except Exception:
        d_name = str(device_id)[:30]

    print(f"[{d_name}] Gravando em: {filename}")

    # Setup MP3 Encoder
    encoder = lameenc.Encoder()
    encoder.set_bit_rate(128)
    encoder.set_in_sample_rate(sample_rate)
    encoder.set_channels(device.channels)
    encoder.set_quality(2) # 2-high, 5-default, 7-fast

    # Small chunks for high responsiveness to stop event/interrupt
    chunk_frames = int(sample_rate * 0.1) 
    
    try:
        with open(filename, 'wb') as mp3_file:
            with device.recorder(samplerate=sample_rate) as recorder:
                while not stop_event.is_set():
                    data = recorder.record(numframes=chunk_frames)
                    
                    # Convert float32 [-1.0, 1.0] to int16 PCM
                    pcm_data = (data * 32767).astype(numpy.int16).tobytes()
                    
                    # Encode chunk
                    mp3_data = encoder.encode(pcm_data)
                    mp3_file.write(mp3_data)
                    
                # Finalize MP3
                mp3_file.write(encoder.flush())
        print(f"[{d_name}] Gravacao salva: {filename}")
    except (KeyboardInterrupt, SystemExit):
        # Quietly exit on Ctrl+C or termination
        pass
    except Exception as e:
        # Ignore errors during process termination
        if not stop_event.is_set():
            print(f"[{d_name}] Erro na gravacao: {e}")
    finally:
        # Crucial for Windows: force hard exit to release all native resources
        os._exit(0)


# --- Orchestration ---
class RecordingSession:
    """Manages the overall recording session, orchestrating multiple processes."""

    def __init__(self, config: AppConfig):
        self.config = config

    def start(self):
        import soundcard as sc

        try:
            speaker_device = sc.default_speaker()
            if not self.config.system_only:
                mic_device = sc.default_microphone()
        except Exception as e:
            print(f"Erro ao obter dispositivos de audio: {e}")
            return

        # Display device info
        try:
            speaker_name = speaker_device.name
        except Exception:
            speaker_name = speaker_device.id

        print("--- Dispositivos selecionados ---")
        if not self.config.system_only:
            try:
                mic_name = mic_device.name
            except Exception:
                mic_name = mic_device.id
            print(f"Microfone: {mic_name}")
        else:
            print("Microfone: DESATIVADO (--system_only)")
        print(f"Sistema (Loopback): {speaker_name}")
        print("-" * 31)
        print("Pressione Ctrl+C para parar a gravacao.\n")

        # Shared event to signal workers to stop
        stop_event = multiprocessing.Event()

        # Launch processes
        processes = []

        proc_sys = multiprocessing.Process(
            target=_record_worker,
            args=(speaker_device.id, self.config.file_sys, self.config.sample_rate, True, stop_event),
            daemon=True # Ensure children die if main process is killed
        )
        processes.append(("Sistema", proc_sys, self.config.file_sys))

        if not self.config.system_only:
            proc_mic = multiprocessing.Process(
                target=_record_worker,
                args=(mic_device.id, self.config.file_mic, self.config.sample_rate, False, stop_event),
                daemon=True
            )
            processes.append(("Microfone", proc_mic, self.config.file_mic))

        for _, proc, _ in processes:
            proc.start()

        # Wait for Ctrl+C
        try:
            while any(proc.is_alive() for _, proc, _ in processes):
                for _, proc, _ in processes:
                    proc.join(timeout=0.1)
        except KeyboardInterrupt:
            print("\n\nParando gravacao...")
            stop_event.set()
            # Immediate termination to stop blocking record calls
            for _, proc, _ in processes:
                if proc.is_alive():
                    proc.terminate()
            
            # Wait briefly for files to be closed
            import time
            time.sleep(0.5)

        # Report results
        print("\n--- Resultado ---")
        for label, proc, fname in processes:
            if stop_event.is_set() or proc.exitcode in (0, 1, -1, 15): 
                # Various exit codes occur when terminating processes on Windows
                print(f"  {label}: SALVO ({fname})")
            else:
                print(f"  {label}: FALHOU (exit code {proc.exitcode})")
        print("-" * 31)


# --- CLI ---
def parse_args():
    parser = argparse.ArgumentParser(description="RecDreamia - Gravador de audio do sistema e microfone (MP3)")
    parser.add_argument(
        "--system_only",
        action="store_true",
        help="Grava apenas o audio do sistema (sem microfone)",
    )
    return parser.parse_args()


# --- Entry Point ---
def main():
    warnings.filterwarnings("ignore")

    args = parse_args()

    try:
        config = load_config(system_only=args.system_only)
        session = RecordingSession(config)
        session.start()
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Erro de inicializacao ou configuracao fatal: {e}")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()

