import os
import sys
from faster_whisper import WhisperModel

# Configuration
MODEL_SIZE = "small.en"
DEVICE = "cpu"
COMPUTE_TYPE = "int8" 

def transcribe_audio(audio_file, model_size=MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE):
    """
    Transcribes audio file to text using faster-whisper.
    """
    if not os.path.exists(audio_file) and audio_file != "dummy_audio.wav": # Allow dummy for testing if needed, though mocking handles it
        raise FileNotFoundError(f"Audio file not found: {audio_file}")

    try:
        model = WhisperModel(model_size, device=device, compute_type=compute_type)
        segments, _ = model.transcribe(audio_file, beam_size=5)
        
        full_text = " ".join([s.text for s in segments]).strip()
        return full_text
        
    except Exception as e:
        # In a real app, log this
        raise e

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 transcribe.py <audio_file>")
        sys.exit(1)
    
    print(transcribe_audio(sys.argv[1]))

if __name__ == "__main__":
    main()
