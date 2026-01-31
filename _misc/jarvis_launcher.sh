#!/bin/bash

# Configuration
PATH=$PATH:/usr/bin:/usr/local/bin:/home/mchang/miniconda3/bin

# Files
AUDIO_FILE="/tmp/jarvis_command.wav"
JARVIS_SCRIPT="$HOME/scripts/jarvis.py"

# Feedback (Start Recording)
aplay -q "$HOME/.local/share/voice_assistant/mic_on.wav" 2>/dev/null &
notify-send "Jarvis" "Listening..." -t 1000

# Cleanup
rm -f "$AUDIO_FILE"

# Mic Setup
MIC="alsa_input.pci-0000_07_00.6.HiFi__Mic1__source"
pactl set-source-mute "$MIC" 0 2>/dev/null
pactl set-source-volume "$MIC" 100% 2>/dev/null

# Record (4 seconds fixed window for now)
timeout 4s parecord --device="$MIC" --file-format=wav "$AUDIO_FILE"

# Feedback (Stop Recording)
aplay -q "$HOME/.local/share/voice_assistant/mic_off.wav" 2>/dev/null &

# Open Terminal and Run Jarvis
# This ensures you SEE the output and HEAR it.
# We use gnome-terminal as a default; adjust if using kitty/alacritty.
gnome-terminal --title="Jarvis" -- bash -c "python3 $JARVIS_SCRIPT $AUDIO_FILE; echo; read -p 'Press Enter to close...' "
