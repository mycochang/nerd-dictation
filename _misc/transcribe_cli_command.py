import sys
import os
import subprocess
from faster_whisper import WhisperModel

# Configuration
MODEL_SIZE = "small.en"
DEVICE = "cpu"
COMPUTE_TYPE = "int8" 

def type_command(text):
    if not text:
        return
    text = text.strip()
    
    # 1. Type the text
    # 2. Press Enter (to execute)
    try:
        env = os.environ.copy()
        if "YDOTOOL_SOCKET" not in env:
            env["YDOTOOL_SOCKET"] = "/tmp/.ydotool_socket"
            
        # Type the command
        subprocess.run(["ydotool", "type", text], env=env, check=True)
        # Hit Enter (Key 28 is usually Enter)
        subprocess.run(["ydotool", "key", "28:1", "28:0"], env=env, check=True)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

def main():
    if len(sys.argv) < 2:
        sys.exit(1)

    audio_file = sys.argv[1]
    if not os.path.exists(audio_file):
        sys.exit(1)

    try:
        model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)
        segments, _ = model.transcribe(audio_file, beam_size=5)
        full_text = " ".join([s.text for s in segments])
        
        # Clean up text (remove trailing punctuation like periods often added by Whisper)
        if full_text.endswith("."):
            full_text = full_text[:-1]
            
        type_command(full_text)
        
    except Exception as e:
        sys.exit(1)

if __name__ == "__main__":
    main()
