# Specification: Jarvis PTT Mode

## Overview
Transition from Toggle mode to Push-to-Talk (PTT). The system should record audio while a key is held and trigger transcription immediately upon release.

## Requirements
- **Trigger:** Global KeyDown (Start) and KeyUp (Stop).
- **Tooling:** Use custom \`python-evdev\` script to listen for key events directly (low-level input) because \`input-remapper\` does not support executing shell commands.
- **Compatibility:** Must work on Wayland/KDE.
