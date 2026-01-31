#!/bin/bash

# DEBUG LOGGING
LOG="/tmp/jarvis_debug.log"
exec 2>>"$LOG" # Redirect stderr to log

echo "--- $(date) ---" >> "$LOG"

# Configuration
export YDOTOOL_SOCKET="/tmp/.ydotool_socket"
export PYTHONPATH="$HOME/repos/nerd-dictation"
PATH=$PATH:/usr/bin:/usr/local/bin:/home/mchang/miniconda3/bin

# Files
AUDIO_FILE="/tmp/jarvis_command.wav"
PID_FILE="/tmp/jarvis.pid"

# Absolute Paths
TRANSCRIBER="$HOME/repos/nerd-dictation/scripts/transcribe.py"
TYPER="$HOME/repos/nerd-dictation/scripts/type_input.py"

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
    TEXT=$(/home/mchang/miniconda3/bin/python3 "$TRANSCRIBER" "$AUDIO_FILE")
    END_TIME=$(date +%s%N)
    DURATION=$(( ($END_TIME - $START_TIME) / 1000000 ))
    echo "Transcription Result ($DURATION ms): '$TEXT'" >> "$LOG"
    
    # Type
    if [ -n "$TEXT" ]; then
        echo "Action: Typing..." >> "$LOG"
        /home/mchang/miniconda3/bin/python3 "$TYPER" "$TEXT"
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
    
    MIC="alsa_input.pci-0000_07_00.6.HiFi__Mic1__source"
    pactl set-source-mute "$MIC" 0 2>/dev/null
    pactl set-source-volume "$MIC" 100% 2>/dev/null

    parecord --device="$MIC" --file-format=wav "$AUDIO_FILE" &
    echo $! > "$PID_FILE"
fi