# Jarvis System Architecture (v3.0 - PTT & CPU Daemon)

## Component Diagram (Mermaid)

```mermaid
graph TD
    User((User)) -->|Hold Meta+Z| Listener[Jarvis Listener Service]
    User -->|Release Meta+Z| Listener
    
    subgraph "Trigger Layer"
        Listener -->|Spawn| Handler[PTT Handler Script]
    end
    
    subgraph "Control Layer"
        Handler -->|Start| Recorder[parecord]
        Recorder -->|Audio File| WavFile[/tmp/jarvis_ptt.wav]
        Handler -->|Stop| Recorder
        Handler -->|Transcribe| Transcriber[Transcribe Client]
    end
    
    subgraph "Intelligence Layer (Daemon)"
        Transcriber -->|Socket Path| Socket((Unix Socket))
        Socket -->|Wake Up| Daemon[Jarvis Daemon Service]
        Daemon -->|Load Model| Model[Faster Whisper CPU]
        WavFile --> Daemon
        Daemon -->|Text| Transcriber
    end
    
    subgraph "Action Layer"
        Transcriber -->|Text| Typer[Type Input Script]
        Typer -->|Socket| Ydotool[ydotoold]
        Ydotool -->|Keystrokes| Window[Active Window]
    end
```

## High-Level Flow (ASCII)
```ascii
                                [ KEYBOARD (Hardware) ]
                                         |
                                         v
                                [ /dev/input/eventX ]
                                         |
                                         v
                          +-----------------------------+
                          |   jarvis-listener.service   |
                          | (Systemd User Service)      |
                          +-----------------------------+
                                         |
                                         |  <-- Uses: /usr/bin/python3 (System Python)
                                         |      Deps: python-evdev (via Pacman/Paru)
                                         |      User: <user> (input group)
                                         |
                                         v
                          +-----------------------------+
                          |    jarvis_ptt_handler.sh    | <---- (Lives in ~/scripts/)
                          +-----------------------------+
                                 /               \
                                / (Start)         \ (Stop)
                               /                   \
                              v                     v
[ parecord ] ----------------+                     [ python3 scripts/transcribe.py ]
(Records to /tmp/jarvis.wav)                       |  <-- Uses: $HOME/miniconda3/bin/python3
(System Binary)                                    |      Deps: faster-whisper (via Pip/Conda)
                                                   |      
                                                   | (Sends Path via Unix Socket)
                                                   v
                                     +-----------------------------+
                                     |       jarvis.service        |
                                     |      (Jarvis Daemon)        |
                                     +-----------------------------+
                                     |  <-- Uses: $HOME/miniconda3/bin/python3
                                     |      Deps: faster-whisper, ctranslate2 (Pip/Conda)
                                     |  * Runs in Background       |
                                     |  * Holds Model in RAM (CPU) |
                                     |  * Listens on jarvis.sock   |
                                     +-----------------------------+
                                                   |
                                                   | (Returns Text)
                                                   v
                                     +-----------------------------+
                                     |    scripts/type_input.py    |
                                     +-----------------------------+
                                                   |
                                                   | (Sends Keystrokes)
                                                   v
                                     +-----------------------------+
                                     |          ydotoold           |
                                     |      (System Daemon)        |
                                     +-----------------------------+
                                                   |
                                                   v
                                           [ ACTIVE WINDOW ]

## File Locations

| Component | Source (Repo) | Deploy Location (System) | Environment |
| :--- | :--- | :--- | :--- |
| **Listener** | `scripts/jarvis_listener.py` | (Run from Repo) | **System Python** |
| **Handler** | `scripts/jarvis_ptt_handler.sh` | `~/scripts/jarvis_ptt_handler.sh` | **Bash** |
| **Daemon** | `scripts/jarvis_daemon.py` | (Run from Repo) | **Conda Python** |
| **Transcriber** | `scripts/transcribe.py` | (Run from Repo) | **Conda Python** |
| **Typer** | `scripts/type_input.py` | (Run from Repo) | **Conda Python** |
| **Service (L)** | `systemd/user/jarvis-listener.service` | `~/.config/systemd/user/...` | **Systemd** |
| **Service (D)** | `systemd/user/jarvis.service` | `~/.config/systemd/user/...` | **Systemd** |

```