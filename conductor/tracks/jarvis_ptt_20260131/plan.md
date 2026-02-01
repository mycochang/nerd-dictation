# Implementation Plan: Jarvis PTT Mode

## Phase 1: Event Detection
- [x] Task: Install and configure `input-remapper` (or equivalent) a4ea72c
- [x] Task: Create `scripts/jarvis_ptt_handler.sh` to accept 'start' and 'stop' arguments 5f05ac6
- [x] Task: Configure `input` group permissions for user 90d23b3
- [x] Task: Create `scripts/jarvis_listener.py` using `python-evdev` 31f0020
- [x] Task: Create Systemd service `jarvis-listener.service` 10ec6b3
- [x] Task: Conductor - User Manual Verification 'Event Detection' (Protocol in workflow.md) ed03475
