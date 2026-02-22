# Jarvis Monolith (The Elegant Path)

This is a single, zero-latency, standalone Python file that replicates the "Windows Experience" perfectly on Linux. 

**It does not replace your current `Win + Z` Nerd Dictation setup.** That still works perfectly in the background. This is a parallel track designed purely for extreme speed using `Ctrl + Space`.

## Why is it so fast?
Unlike the fragmented bash scripts that dump `.wav` files to your hard drive, the `scripts/jarvis_monolith.py`:
1. Uses `evdev` to bind directly to your physical keyboard hardware.
2. Streams audio directly into a NumPy array in your system RAM.
3. Passes that RAM array directly into the `faster-whisper` C++ inference engine.
4. Spits the text out through a virtual keyboard (`ydotool`).

Zero disk I/O. Zero inter-process communication. Instantaneous typing.

## How to Run It

1. Ensure your user is in the `input` group so the script can read your keyboard natively:
   ```bash
   sudo usermod -aG input $USER
   ```
   *(Log out and back in if this is your first time doing this).*

2. Make sure you have the required Python dependencies installed via `uv`:
   ```bash
   uv add sounddevice numpy scipy evdev
   ```

3. Start the `ydotoold` daemon (required for Wayland pasting):
   ```bash
   sudo systemctl enable --now ydotoold
   ```

4. Run the monolith:
   ```bash
   uv run scripts/jarvis_monolith.py
   ```

Now, just **Hold `Ctrl + Space`** to talk, and release it to type. It automatically monitors every keyboard plugged into your computer simultaneously.
