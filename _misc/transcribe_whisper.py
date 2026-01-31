import sys
import os
import subprocess
from faster_whisper import WhisperModel

# Configuration
# "small.en" is accurate and reasonably fast on CPU.
# "tiny.en" is faster but dumber.
MODEL_SIZE = "small.en"
DEVICE = "cpu"
COMPUTE_TYPE = "int8" # Fastest for CPU

def type_text(text):
    if not text:
        return
    text = text.strip()
    
    # Send to ydotool
    try:
        env = os.environ.copy()
        if "YDOTOOL_SOCKET" not in env:
            env["YDOTOOL_SOCKET"] = "/tmp/.ydotool_socket"
        subprocess.run(["ydotool", "type", text + " "], env=env, check=True)
    except Exception as e:
        pass

def main():
    if len(sys.argv) < 2:
        sys.exit(1)

    audio_file = sys.argv[1]
    if not os.path.exists(audio_file):
        sys.exit(1)

    try:
        # Load model (this is cached after first run)
        model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)
        
        # Transcribe
        segments, _ = model.transcribe(audio_file, beam_size=5)
        
        # Combine segments
        full_text = " ".join([s.text for s in segments])
        
        # Type it
        type_text(full_text)
        
    except Exception as e:
        sys.exit(1)

if __name__ == "__main__":
    main()