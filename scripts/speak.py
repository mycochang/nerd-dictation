import subprocess
import sys

# Configuration
PIPER_MODEL = "/usr/share/piper-voices/en/en_US/ryan/high/en_US-ryan-high.onnx"

def speak_text(text):
    """Speak text using Piper."""
    if not text or not text.strip():
        return
    try:
        # echo "Text" | piper-tts --model ... --output-raw | aplay ...
        p1 = subprocess.Popen(["echo", text], stdout=subprocess.PIPE)
        p2 = subprocess.Popen([
            "piper-tts", 
            "--model", PIPER_MODEL, 
            "--output-raw"
        ], stdin=p1.stdout, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        if p1.stdout:
            p1.stdout.close()
        
        # Play audio (aplay is standard)
        subprocess.run(["aplay", "-q", "-r", "22050", "-f", "S16_LE", "-t", "raw"], stdin=p2.stdout)
    except Exception as e:
        print(f"TTS Error: {e}", file=sys.stderr)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 speak.py <text>")
        sys.exit(1)
    
    speak_text(sys.argv[1])

if __name__ == "__main__":
    main()
