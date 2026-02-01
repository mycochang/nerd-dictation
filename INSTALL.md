# Jarvis Manual Installation Guide (CachyOS/Miniconda3)

**Status:** This guide reflects the current "Working State" as of Jan 2026.
**Environment:** CachyOS (Arch), Miniconda3, Wayland (KDE/Hyprland).

## Prerequisites

1.  **System Packages (Pacman/Paru):**
    ```bash
    sudo pacman -S python-evdev python-pydantic python-dasbus python-psutil python-gobject libpulse sox
    paru -S ydotoold piper-tts-bin piper-voices-en-us
    ```

2.  **Conda Environment:**
    *   Active environment: `base` (or your preferred env) at `$HOME/miniconda3`.
    *   Packages:
        ```bash
        pip install faster-whisper ctranslate2
        ```

3.  **Permissions:**
    *   User must be in the `input` group: `sudo usermod -aG input $USER`.

## Deployment

### 1. Scripts
Copy the handler script to your home directory:
```bash
cp scripts/jarvis_ptt_handler.sh ~/scripts/
chmod +x ~/scripts/jarvis_ptt_handler.sh
```

### 2. Systemd Services
Copy the unit files to your user config:
```bash
mkdir -p ~/.config/systemd/user
cp systemd/user/jarvis.service ~/.config/systemd/user/
cp systemd/user/jarvis-listener.service ~/.config/systemd/user/
cp systemd/user/jarvis.socket ~/.config/systemd/user/
```

### 3. Activation
Reload and start:
```bash
systemctl --user daemon-reload
systemctl --user enable --now ydotoold
systemctl --user enable --now jarvis.socket
systemctl --user enable --now jarvis-listener.service
```

## Architecture Note
This setup uses a **Hybrid Environment**:
*   **Listener Service:** Runs on **System Python** (`/usr/bin/python3`) to access `evdev`.
*   **Daemon Service:** Runs on **Conda Python** (`$HOME/miniconda3...`) to access `faster-whisper`.
*   **Handler Script:** Hardcodes paths to the Conda python to bridge the gap.
