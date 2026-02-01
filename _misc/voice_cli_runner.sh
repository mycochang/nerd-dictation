#!/bin/bash

# Configuration
export YDOTOOL_SOCKET="/tmp/.ydotool_socket"
PATH=$PATH:/usr/bin:/usr/local/bin:$HOME/miniconda3/bin

# Files
AUDIO_FILE="/tmp/cli_command.wav"
TRANSCRIBER="$HOME/scripts/transcribe_cli_command.py"

# Feedback
aplay -q "$HOME/.local/share/voice_assistant/mic_on.wav" 2>/dev/null &
notify-send "CLI Command" "Listening..." -t 1000

# Record 5 seconds OR until silence (using sox silence detection if available, simpler to just timeout for now)
# We'll use a fixed 4-second window for commands to keep it snappy.
MIC="alsa_input.pci-0000_07_00.6.HiFi__Mic1__source"
rm -f "$AUDIO_FILE"

# Boost Mic
pactl set-source-mute "$MIC" 0 2>/dev/null
pactl set-source-volume "$MIC" 100% 2>/dev/null

# Record for 4 seconds
timeout 4s parecord --device="$MIC" --file-format=wav "$AUDIO_FILE"

# Feedback
aplay -q "$HOME/.local/share/voice_assistant/mic_off.wav" 2>/dev/null &
notify-send "CLI Command" "Executing..." -t 1000

# Transcribe & Execute
python3 "$TRANSCRIBER" "$AUDIO_FILE"
