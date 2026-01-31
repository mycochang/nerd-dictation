# Jarvis Daemon: Pre-Deployment Analysis

## 1. Resource Monitoring Strategy
Before we let a Python script eat your RAM/VRAM, we must verify its impact.

### Tools
*   **GPU (VRAM/Compute):** You have `nvtop` installed. This is the gold standard for NVIDIA cards. It shows exactly how much memory `python` is hogging.
*   **System (CPU/RAM):** You don't have `htop`, but we can use `top` or install `btop` (modern, pretty).
*   **Baseline:**
    *   `tiny.en`: ~75MB VRAM.
    *   `small.en`: ~500MB VRAM.
    *   `large-v3`: ~3GB VRAM.
    *   *Your 3070 has 8GB VRAM. `small.en` is negligible cost (6%).*

### Monitoring Plan
We will write a `monitor_resources.sh` script that logs the daemon's footprint over 1 hour of usage to prove it's safe.

## 2. Security Implications
Running a listening server (even locally) introduces risks.

### Risk: The "Hot Mic" / "Remote Execution" Fear
If we open a port (e.g., `localhost:8080`), any app on your machine (browser scripts, rogue extensions) *could* theoretically send audio to it or trigger it.

### Mitigation: Unix Domain Sockets
We will NOT use TCP ports. We will use a **Unix Domain Socket** (`/tmp/jarvis.sock`).
*   **Why:** File-system permissions apply.
*   **Lockdown:** `chmod 600 /tmp/jarvis.sock`. Only **your user** (mchang) can write to it. No other user, no remote attacker.
*   **No Execution:** The daemon ONLY accepts `.wav` file paths. It strictly does `File -> Text -> Type`. It never executes.

## 3. The Implementation Plan (Conductor Track)

**Track:** "Jarvis Daemon & Resource Guard"

1.  **Monitor:** Create `scripts/monitor.sh` to log PID resources.
2.  **Daemon:** Create `scripts/jarvis_daemon.py` (loads model, listens on socket).
3.  **Client:** Create `scripts/jarvis_client.py` (sends path to socket).
4.  **Systemd:** Create a user service to auto-start (optional, maybe manual start first).
5.  **Verify:** Run for 10 mins, check `nvtop`, verify no leaks.

**Shall I initiate this track?**
