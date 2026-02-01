#!/bin/bash

# Configuration
export YDOTOOL_SOCKET="${YDOTOOL_SOCKET:-$XDG_RUNTIME_DIR/.ydotool_socket}"
export PYTHONPATH="$HOME/repos/nerd-dictation"
PATH=$PATH:/usr/bin:/usr/local/bin:$HOME/miniconda3/bin

# Files (Override via ENV for testing)
RUNTIME_DIR="${XDG_RUNTIME_DIR:-/tmp}"
AUDIO_FILE="${AUDIO_FILE:-$RUNTIME_DIR/jarvis_ptt.wav}"
PID_FILE="${PID_FILE:-$RUNTIME_DIR/jarvis_ptt.pid}"

# Scripts
PYTHON_INTERPRETER="${PYTHON_INTERPRETER:-$HOME/miniconda3/bin/python3}"
TRANSCRIBER="$HOME/repos/nerd-dictation/scripts/transcribe.py"
TYPER="$HOME/repos/nerd-dictation/scripts/type_input.py"

function notify() {
    notify-send "Jarvis PTT" "$1" -t 500
}

COMMAND="$1"

if [ "$COMMAND" == "start" ]; then
    # Prevent double-start
    if [ -f "$PID_FILE" ]; then
        exit 0
    fi

    # Cleanup
    rm -f "$AUDIO_FILE"
    
    # Feedback
    aplay -q "$HOME/.local/share/voice_assistant/mic_on.wav" 2>/dev/null &
    notify "Listening..."
    
    # Mic Setup
    MIC="alsa_input.pci-0000_07_00.6.HiFi__Mic1__source"
    pactl set-source-mute "$MIC" 0 2>/dev/null
    pactl set-source-volume "$MIC" 100% 2>/dev/null

    # Record
    # We use 'parecord'
    parecord --device="$MIC" --file-format=wav "$AUDIO_FILE" &
    echo $! > "$PID_FILE"

elif [ "$COMMAND" == "stop" ]; then
    if [ ! -f "$PID_FILE" ]; then
        exit 0
    fi

    PID=$(cat "$PID_FILE")
    
    # Kill recording
    # Give it a split second to flush if it was very short?
    # For PTT, users usually release AFTER speaking, so maybe not needed as much as toggle.
    kill "$PID" 2>/dev/null
    rm -f "$PID_FILE"
    
    aplay -q "$HOME/.local/share/voice_assistant/mic_off.wav" 2>/dev/null &
    notify "Processing..."
    
    # Transcribe
    # If python is mocked in test, this will just exit 0
    TEXT=$("$PYTHON_INTERPRETER" "$TRANSCRIBER" "$AUDIO_FILE")
    
    # Type
    if [ -n "$TEXT" ]; then
        "$PYTHON_INTERPRETER" "$TYPER" "$TEXT"
    fi
else
    echo "Usage: $0 {start|stop}"
    exit 1
fi
