# Jarvis Installation Guide

This guide covers installation of the Jarvis voice assistant on Linux with Wayland.

## Prerequisites

### System Packages (Arch/CachyOS)
```bash
sudo pacman -S python-evdev ydotool sox libpulse
paru -S piper-tts-bin piper-voices-en-us  # Optional: for TTS
```

### Python Dependencies
Using UV (recommended):
```bash
uv sync
```

Or pip:
```bash
pip install faster-whisper evdev
```

### Permissions
Add user to input group for evdev access:
```bash
sudo usermod -aG input $USER
# Log out and back in
```

## Deployment

### 1. Systemd Services (Optional)
```bash
mkdir -p ~/.config/systemd/user
cp systemd/user/*.service systemd/user/*.socket ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now ydotoold
systemctl --user enable --now jarvis.socket
systemctl --user enable --now jarvis-listener.service
```

### 2. Manual Usage
Start the daemon:
```bash
python scripts/jarvis_daemon.py
```

In another terminal, start the PTT listener:
```bash
python scripts/jarvis_listener.py
```

Hold `Meta+Z` to talk, release to transcribe and paste.

## Configuration

Set these environment variables to customize behavior:

| Variable | Description | Default |
|----------|-------------|---------|
| `JARVIS_MIC` | PulseAudio source name | `@DEFAULT_SOURCE@` |
| `JARVIS_SOUNDS_DIR` | Directory with mic_on.wav/mic_off.wav | (none) |
| `PYTHON_INTERPRETER` | Python to use for scripts | `python3` |

## Troubleshooting

### "Permission denied" on /dev/input
Ensure you're in the `input` group and have logged out/in.

### ydotool not working
Make sure ydotoold is running:
```bash
systemctl --user status ydotoold
```

### Daemon won't start
Check if socket path is accessible:
```bash
ls -la ${XDG_RUNTIME_DIR}/jarvis.sock
```
