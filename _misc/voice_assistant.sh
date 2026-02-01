#!/bin/bash

# Configuration
export YDOTOOL_SOCKET="/tmp/.ydotool_socket"
PATH=$PATH:/usr/bin:/usr/local/bin:$HOME/miniconda3/bin

# Files
AUDIO_FILE="/tmp/voice_assistant.wav"
PID_FILE="/tmp/voice_assistant.pid"
TRANSCRIBER="$HOME/scripts/transcribe_whisper.py"

function notify() {
    notify-send "Voice Assistant" "$1" -t 1000
}

# Check if we are RECORDING (PID file exists)
if [ -f "$PID_FILE" ]; then
    # === STOP RECORDING & TRANSCRIBE ===
    PID=$(cat "$PID_FILE")
    
    # Kill the recorder
    if ps -p "$PID" > /dev/null; then
        kill "$PID"
    fi
    rm -f "$PID_FILE"
    
    # Feedback
    aplay -q "$HOME/.local/share/voice_assistant/mic_off.wav" 2>/dev/null &
    notify "Thinking..."
    
    # Transcribe (This blocks until done)
    python3 "$TRANSCRIBER" "$AUDIO_FILE"
    
else
    # === START RECORDING ===
    # Cleanup old audio
    rm -f "$AUDIO_FILE"
    
    # Feedback
    aplay -q "$HOME/.local/share/voice_assistant/mic_on.wav" 2>/dev/null &
    notify "Listening..."
    
    # Record (using parecord which is reliable on your system)
    # Target the specific MIC we found
    MIC="alsa_input.pci-0000_07_00.6.HiFi__Mic1__source"
    
    # Boost Mic Volume (Safety)
    pactl set-source-mute "$MIC" 0 2>/dev/null
    pactl set-source-volume "$MIC" 100% 2>/dev/null

    # Start Recording in Background
    parecord --device="$MIC" --file-format=wav "$AUDIO_FILE" &
    
    # Save PID
    echo $! > "$PID_FILE"
fi