# Implementation Plan: Jarvis Daemon & Resource Guard

## Phase 1: Resource Guard & Daemon
- [x] Task: Create `scripts/monitor_resources.sh` to log GPU/CPU footprint 050dfda
- [x] Task: Implement `scripts/jarvis_daemon.py` (Unix Socket Server + Model Persistence) 356b808
- [ ] Task: Update `scripts/transcribe.py` to act as a lightweight Socket Client
- [ ] Task: Conductor - User Manual Verification 'Resource Guard & Daemon' (Protocol in workflow.md)

## Phase 2: System Integration
- [ ] Task: Create Systemd User Service (`jarvis.service`) with Socket Activation
- [ ] Task: Update `voice_assistant.sh` to use the new daemon path
- [ ] Task: Perform 1-hour resource stress test and review logs
- [ ] Task: Conductor - User Manual Verification 'System Integration' (Protocol in workflow.md)
