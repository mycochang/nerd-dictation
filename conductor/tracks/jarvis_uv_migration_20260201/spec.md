# Specification: UV Migration

## Overview
Replace the fragile hybrid environment (System Python for Listener + Conda for Daemon) with a single, reproducible `uv` project. This ensures all dependencies (including `evdev` and `faster-whisper`) are managed in one lockfile and virtual environment.

## Requirements
- **Tooling:** Use `uv` for dependency management.
- **Isolation:** Project must run independent of the user's global Conda environment.
- **System Deps:** Ensure `evdev` works within the venv (requires user permissions, not system python).
