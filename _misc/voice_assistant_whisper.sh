#!/bin/bash

# Configuration
export YDOTOOL_SOCKET="/tmp/.ydotool_socket"
PATH=$PATH:/usr/bin:/usr/local/bin:$HOME/miniconda3/bin

# Paths
AUDIO_FILE="/tmp/whisper_recording.wav"
TRANSCRIBER="$HOME/scripts/transcribe_whisper.py"
PID_FILE="/tmp/voice_assistant_rec.pid"

function notify() {
    notify-send "Voice Assistant" "$1" -t 1500
}

if [ -f "$PID_FILE" ]; then
    # === STOP ===
    PID=$(cat "$PID_FILE")
    
    if ps -p "$PID" > /dev/null; then
        kill "$PID"
        rm -f "$PID_FILE"
        
        aplay -q "$HOME/.local/share/voice_assistant/mic_off.wav" 2>/dev/null &
        notify "Processing..."
        
        # Run Transcriber (Foreground)
        python3 "$TRANSCRIBER" "$AUDIO_FILE"
        
        notify "Done."
    else
        rm -f "$PID_FILE"
        notify "Error: Process lost."
    fi

else
    # === START ===
    # Record cleanly. using "sox" (rec) or "parec".
    # We use parecord because it's reliable on PipeWire.
    # We force the specific mic source we found earlier.
    MIC_SOURCE="alsa_input.pci-0000_07_00.6.HiFi__Mic1__source"
    
    # Remove old file
    rm -f "$AUDIO_FILE"
    
    aplay -q "$HOME/.local/share/voice_assistant/mic_on.wav" 2>/dev/null &
    notify "Listening..."
    
    # Start Recording
    parecord --device="$MIC_SOURCE" --file-format=wav "$AUDIO_FILE" &
    echo $! > "$PID_FILE"
fi
