# Implementation Plan: UV Migration

## Phase 1: Research & Prototype
- [ ] Task: Install `uv` and initialize project
- [ ] Task: Create `pyproject.toml` with separate dependency groups (daemon vs listener)
- [ ] Task: Test `evdev` access from within a user-owned venv

## Phase 2: Migration
- [ ] Task: Update Systemd services to point to `.venv/bin/python`
- [ ] Task: Update scripts to remove hardcoded Conda paths
- [ ] Task: Verify end-to-end functionality
