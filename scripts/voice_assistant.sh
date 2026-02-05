#!/bin/bash

# Configuration
export YDOTOOL_SOCKET="/tmp/.ydotool_socket"



# Files
RUNTIME_DIR="${XDG_RUNTIME_DIR:-/tmp}"
LOG="$RUNTIME_DIR/jarvis_debug.log"
exec 2>>"$LOG" # Redirect stderr to log

echo "--- $(date) ---" >> "$LOG"

AUDIO_FILE="$RUNTIME_DIR/jarvis_command.wav"
PID_FILE="$RUNTIME_DIR/jarvis.pid"

# Absolute Paths
TRANSCRIBER="$SCRIPT_DIR/transcribe.py"
TYPER="$SCRIPT_DIR/type_input.py"

function notify() {
    notify-send "Jarvis" "$1" -t 1000
}

if [ -f "$PID_FILE" ]; then
    # === STOP ===
    echo "State: Stopping..." >> "$LOG"
    PID=$(cat "$PID_FILE")
    
    # Graceful Kill
    sleep 0.2 # Wait for buffer flush
    kill "$PID" 2>/dev/null
    rm -f "$PID_FILE"
    
    aplay -q "$HOME/.local/share/voice_assistant/mic_off.wav" 2>/dev/null &
    notify "Processing..."
    
    # Transcribe
    echo "Action: Transcribing..." >> "$LOG"
    START_TIME=$(date +%s%N)
    TEXT=$(python3 "$TRANSCRIBER" "$AUDIO_FILE")
    END_TIME=$(date +%s%N)
    DURATION=$(( ($END_TIME - $START_TIME) / 1000000 ))
    echo "Transcription Result ($DURATION ms): '$TEXT'" >> "$LOG"
    
    # Type
    if [ -n "$TEXT" ]; then
        echo "Action: Typing..." >> "$LOG"
        python3 "$TYPER" "$TEXT"
        notify "Done."
    else
        echo "Warning: Empty transcription." >> "$LOG"
        notify "Heard nothing."
    fi
    
else
    # === START ===
    echo "State: Starting..." >> "$LOG"
    rm -f "$AUDIO_FILE"
    aplay -q "$HOME/.local/share/voice_assistant/mic_on.wav" 2>/dev/null &
    notify "Listening..."
    
    MIC="@DEFAULT_SOURCE@"
    pactl set-source-mute "$MIC" 0 2>/dev/null
    pactl set-source-volume "$MIC" 100% 2>/dev/null

    parecord --device="$MIC" --file-format=wav "$AUDIO_FILE" &
    echo $! > "$PID_FILE"
fi