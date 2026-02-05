# Jarvis Voice Assistant: User Guide & Best Practices

## Core Concept
Jarvis is your "Voice Keyboard". It listens to your voice, transcribes it securely on your device (CPU), and types the text into your active window.

**Trigger:** `Meta+Z` (Toggle On/Off)

---

## getting Best Accuracy from "Tiny" Mode

You are currently running the **tiny.en** model to save CPU cycles. It is fast but can be "dumb". Here is how to speak to it:

### 1. Speak Like a News Anchor
*   **Do:** Enunciate clearly. "Commit these changes."
*   **Don't:** Mumble or trail off. "Uhh commit ish."

### 2. The "Wake Up" Pause
*   **The Workflow:** Press `Meta+Z` -> *Wait for "Listening" notification* -> Speak -> Press `Meta+Z`.
*   If you speak *before* the notification, the first word might be cut off.

### 3. Punctuation is Manual
Whisper is okay at guessing sentences, but for coding/CLI work, be explicit if you need specific formatting:
*   "New line" -> (Types Enter) *[Note: Needs `nerd-dictation.py` config for this mapping]*
*   "Dash dash help" -> `--help`

### 4. Short Bursts
*   The system is optimized for commands (2-5 seconds).
*   If you speak for 30 seconds, the transcription latency will grow linearly. Keep it short.

---

## Troubleshooting

### "It typed nothing!"
*   **Cause:** You might have toggled it off too fast, or `ydotool` lost focus.
*   **Fix:** Wait 0.5s after you finish speaking before pressing `Meta+Z` again.

### "It typed garbage!"
*   **Cause:** Background noise or the "Tiny" model hallucinating.
*   **Fix:** Try to reduce background noise. If it persists, we can switch to `base.en` (5x slower but smarter).

### "It crashed my monitor!"
*   **Cause:** NVIDIA GPU waking up.
*   **Fix:** We moved Jarvis to **CPU Mode**. This should never happen again.

## System Details
*   **Model:** `faster-whisper-tiny.en`
*   **Hardware:** CPU (Int8 Quantization)
*   **Daemon:** Auto-starts on first use, stays active for 1 hour.
