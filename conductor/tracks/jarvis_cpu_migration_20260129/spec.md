# Specification: Jarvis CPU Migration

## Overview
Move the Jarvis transcription workload from the NVIDIA GPU to the CPU. This prevents VRAM contention with Agisoft Metashape and resolves Wayland compositor crashes caused by GPU power state transitions on HP Omen laptops where the HDMI port is hardwired to the dGPU.

## Requirements
- **Compute:** Force `device='cpu'` and `compute_type='int8'`.
- **Model:** Switch to `tiny.en` or `base.en` to maintain low latency on CPU.
- **Verification:** Confirm VRAM usage is 0MB and transcription latency is <1.5s.
