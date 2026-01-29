# Specification: Jarvis Loop

## Overview
This track implements the core 'Jarvis' loop: capturing user voice via Whisper, executing the transcribed command in the shell, and reading the output back to the user via Piper TTS.

## Requirements
- **Voice Input:** Use `faster-whisper` for low-latency, high-accuracy transcription.
- **Execution:** Securely execute transcribed commands in a subshell.
- **Voice Output:** Use `piper-tts` to read command results back to the user.
- **Interface:** Provide a visible terminal HUD for status and feedback.
