# Implementation Plan: Jarvis Daemon & Resource Guard

## Phase 1: Resource Guard & Daemon
- [x] Task: Create `scripts/monitor_resources.sh` to log GPU/CPU footprint 050dfda
- [x] Task: Implement `scripts/jarvis_daemon.py` (Unix Socket Server + Model Persistence) ce73721
- [x] Task: Update `scripts/transcribe.py` to act as a lightweight Socket Client 9707863
- [x] Task: Conductor - User Manual Verification 'Resource Guard & Daemon' (Protocol in workflow.md) e8b4cc9

## Phase 2: System Integration
- [x] Task: Create Systemd User Service (`jarvis.service`) with Socket Activation 9ca5bf7
- [x] Task: Update `voice_assistant.sh` to use the new daemon path 9ca5bf7
- [x] Task: Perform 1-hour resource stress test and review logs 9ca5bf7
- [ ] Task: Conductor - User Manual Verification 'System Integration' (Protocol in workflow.md)
