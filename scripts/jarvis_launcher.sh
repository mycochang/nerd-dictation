#!/bin/bash

# Files
RUNTIME_DIR="${XDG_RUNTIME_DIR:-/tmp}"
AUDIO_FILE="$RUNTIME_DIR/jarvis_command.wav"
PID_FILE="$RUNTIME_DIR/jarvis.pid"
LOG_FILE="$RUNTIME_DIR/jarvis_debug.log"

echo "$(date): Triggered" >> "$LOG_FILE"

# Scripts
TRANSCRIBER="$SCRIPT_DIR/transcribe.py"
TYPER="$SCRIPT_DIR/type_input.py"
SPEAKER="$SCRIPT_DIR/speak.py"

function notify() {
    notify-send "Jarvis" "$1" -t 1000
}

# Toggle Logic
if [ -f "$PID_FILE" ]; then
    # === STOP ===
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null; then
        kill "$PID"
    fi
    rm -f "$PID_FILE"
    
    # Feedback
    aplay -q "$HOME/.local/share/voice_assistant/mic_off.wav" 2>/dev/null &
    notify "Processing..."
    
    # Transcribe
    TEXT=$(python3 "$TRANSCRIBER" "$AUDIO_FILE")
    
    # Type
    python3 "$TYPER" "$TEXT"
    
else
    # === START ===
    rm -f "$AUDIO_FILE"
    
    # Feedback
    aplay -q "$HOME/.local/share/voice_assistant/mic_on.wav" 2>/dev/null &
    notify "Listening..."
    
    # Mic Setup (Safety)
    MIC="@DEFAULT_SOURCE@"
    pactl set-source-mute "$MIC" 0 2>/dev/null
    pactl set-source-volume "$MIC" 100% 2>/dev/null

    # Record
    parecord --device="$MIC" --file-format=wav "$AUDIO_FILE" &
    echo $! > "$PID_FILE"
fi
