# Technology Stack

## Core Technologies
- **Language:** Python (>= 3.8)
- **Speech-to-Text (STT):** faster-whisper (Optimized for CPU with int8 quantization)
- **Daemon:** Python persistent process managed by `systemd` (User Service)
- **IPC:** Unix Domain Sockets for secure, local client-server communication
- **Audio Handling:** `parecord` (PulseAudio/PipeWire)
- **Input Simulation:** `ydotool` (Wayland-compatible keyboard event simulation)
- **Text-to-Speech (TTS):** `piper-tts` (high-quality, low-latency local TTS)

## Development Environment
- **OS:** Linux (Arch/CachyOS)
- **Architecture:** Local-first, privacy-preserving modular pipeline.
