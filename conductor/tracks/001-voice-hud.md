# Track 001: Voice HUD (Jarvis)

## Goal
Reduce ADHD friction by enabling "Fire and Forget" voice commands via a popup CLI.

## Architecture
*   **Trigger:** `Meta+Z` (Global Shortcut) -> Runs `jarvis_launcher.sh`
*   **Input:** `parecord` (4s fixed window) -> `/tmp/jarvis_command.wav`
*   **Brain:** `faster-whisper` (CPU/Int8) -> Transcribes audio to text.
*   **Execution:** `subprocess` -> Runs command in shell.
*   **Feedback:** `piper-tts` -> Reads output back to user.

## Files
1.  `~/scripts/jarvis.py`: The Python brain.
2.  `~/scripts/jarvis_launcher.sh`: The bash trigger.

## Dependencies
*   `python-faster-whisper`
*   `piper-tts-bin` (AUR)
*   `piper-voices-en-us` (AUR)
*   `sox` / `libpulse`

## Status
*   [x] Prototype functionality working.
*   [x] Audio recording fixed (mic boost).
*   [x] TTS output working (Ryan voice).
*   [ ] Integration with LLM (Future: Replace `subprocess` with `Gemini` call).
