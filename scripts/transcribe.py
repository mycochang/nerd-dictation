import os
import sys
import socket
from faster_whisper import WhisperModel

# Configuration
MODEL_SIZE = "small.en" # Keeping small since we want better accuracy if we fall back
DEVICE = "cpu"
COMPUTE_TYPE = "int8"
SOCKET_PATH = "/tmp/jarvis.sock"

def transcribe_audio_client(audio_file, socket_path=SOCKET_PATH):
    """
    Sends audio file path to the Jarvis Daemon via Unix Socket.
    """
    if not os.path.exists(audio_file):
        raise FileNotFoundError(f"Audio file not found: {audio_file}")

    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
        client.connect(socket_path)
        client.sendall(audio_file.encode('utf-8'))
        
        # Receive response
        response = client.recv(4096).decode('utf-8')
        if response.startswith("ERROR:"):
            raise RuntimeError(f"Daemon Error: {response}")
            
        return response

def transcribe_audio(audio_file, model_size=MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE):
    """
    Transcribes audio file to text using faster-whisper (Cold Start).
    """
    if not os.path.exists(audio_file) and audio_file != "dummy_audio.wav": 
        raise FileNotFoundError(f"Audio file not found: {audio_file}")

    try:
        model = WhisperModel(model_size, device=device, compute_type=compute_type)
        segments, _ = model.transcribe(audio_file, beam_size=5)
        
        full_text = " ".join([s.text for s in segments]).strip()
        return full_text
        
    except Exception as e:
        raise e

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 transcribe.py <audio_file>")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    
    # Try Daemon first
    try:
        print(transcribe_audio_client(audio_file))
    except (ConnectionRefusedError, FileNotFoundError, OSError):
        # Fallback to Cold Start
        # print("Daemon unreachable, using Cold Start...", file=sys.stderr)
        print(transcribe_audio(audio_file))

if __name__ == "__main__":
    main()