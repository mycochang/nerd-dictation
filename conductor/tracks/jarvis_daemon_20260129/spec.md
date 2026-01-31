# Specification: Jarvis Daemon & Resource Guard

## Overview
Transition the Jarvis Loop from a cold-start script to a persistent background daemon to eliminate transcription latency.

## Requirements
- **Persistence:** Model stays loaded in GPU VRAM (RTX 3070).
- **Communication:** Use Unix Domain Sockets (`/tmp/jarvis.sock`) with strict `0600` permissions.
- **Monitoring:** Integrated resource logging (VRAM/CPU) to verify system impact.
- **Management:** Systemd user service integration.
