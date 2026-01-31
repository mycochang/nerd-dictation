import sys
import os
import subprocess
from faster_whisper import WhisperModel

# Configuration
MODEL_SIZE = "small.en"
DEVICE = "cpu"
COMPUTE_TYPE = "int8"
PIPER_MODEL = "/usr/share/piper-voices/en/en_US/ryan/high/en_US-ryan-high.onnx"

def speak(text):
    """Speak text using Piper with controlled volume."""
    if not text or not text.strip():
        return
    try:
        # 1. Lower the volume for this process specifically (if possible)
        # Or just use amixer to set a comfortable level for the duration
        subprocess.run(["amixer", "set", "Master", "40%"], capture_output=True)
        
        p1 = subprocess.Popen(["echo", text], stdout=subprocess.PIPE)
        p2 = subprocess.Popen([
            "piper-tts", 
            "--model", PIPER_MODEL, 
            "--output-raw"
        ], stdin=p1.stdout, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        p1.stdout.close()
        
        subprocess.run(["aplay", "-q", "-r", "22050", "-f", "S16_LE", "-t", "raw"], stdin=p2.stdout)
        
        # 2. Return volume to a reasonable baseline
        subprocess.run(["amixer", "set", "Master", "60%"], capture_output=True)
    except Exception as e:
        print(f"TTS Error: {e}", file=sys.stderr)

def main():
    if len(sys.argv) < 2:
        sys.exit(1)

    audio_file = sys.argv[1]
    if not os.path.exists(audio_file):
        sys.exit(1)

    try:
        print("Thinking...", file=sys.stderr)
        model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)
        segments, _ = model.transcribe(audio_file, beam_size=5)
        command_text = " ".join([s.text for s in segments]).strip()
        
        if command_text.endswith("."):
            command_text = command_text[:-1]

        print(f"Command: {command_text}")
        speak(f"Running {command_text}")

        # Execute Command
        result = subprocess.run(
            command_text, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True
        )

        output = result.stdout
        if result.stderr:
            output += "\nError: " + result.stderr

        # Limit output for speaking
        spoken_output = output[:500] 
        if len(output) > 500:
            spoken_output += "... output truncated."

        print(output)
        speak(spoken_output)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        speak("I encountered an error.")

if __name__ == "__main__":
    main()