#!/usr/bin/env python3
import sys
import os
import signal
import subprocess
import threading
import time
import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
import evdev
from evdev import ecodes

# --- Mindful Configuration ---
# Focus on speed and minimizing cognitive load.
MODEL_SIZE = os.environ.get("JARVIS_MODEL", "Systran/faster-whisper-base.en")
DEVICE = "cpu"
COMPUTE_TYPE = "int8"
CPU_THREADS = int(os.environ.get("JARVIS_THREADS", 4))
SAMPLE_RATE = 16000

# To keep the system air-gapped and replicable, store models locally.
LOCAL_MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
os.makedirs(LOCAL_MODEL_DIR, exist_ok=True)

# The user requested a parallel track: Ctrl + Space.
# We map to Left Ctrl or Right Ctrl, plus Space.


def notify(message):
    """Gentle visual feedback. We don't want to break flow."""
    try:
        subprocess.run(
            ["notify-send", "-t", "800", "Jarvis Monolith", message], check=False
        )
    except FileNotFoundError:
        pass


def play_sound(sound_type):
    """Subtle audio cues for entering and exiting dictation states."""
    sound_file = (
        f"{os.environ.get('HOME')}/.local/share/voice_assistant/mic_{sound_type}.wav"
    )
    if os.path.exists(sound_file):
        subprocess.Popen(["aplay", "-q", sound_file], stderr=subprocess.DEVNULL)


def type_text(text):
    """Direct, Wayland-safe injection."""
    if not text:
        return
    try:
        # -d 2: 2ms delay between keys
        # -H 2: 2ms hold per key
        # This makes the typing ~10x faster than default, preventing window-switch errors
        subprocess.run(
            ["ydotool", "type", "-d", "2", "-H", "2", text + " "], check=True
        )
    except Exception as e:
        print(f"Error typing text: {e}")
        notify("❌ Error: ydotool failed. Is ydotoold running?")


class JarvisMonolith:
    """
    The elegant monolith.
    1. Preloads the CTranslate2 model into RAM.
    2. Binds directly to the hardware keyboard for zero-latency hotkeys.
    3. Records audio directly into a NumPy array in RAM (no disk I/O).
    4. Transcribes and injects instantly.
    """

    def __init__(self):
        print(f"Loading {MODEL_SIZE} into RAM from {LOCAL_MODEL_DIR}...")
        self.model = WhisperModel(
            MODEL_SIZE,
            device=DEVICE,
            compute_type=COMPUTE_TYPE,
            cpu_threads=CPU_THREADS,
            download_root=LOCAL_MODEL_DIR,
        )
        print("Model loaded into RAM. Ready.")

        self.keyboards = self.find_keyboards()
        if not self.keyboards:
            print(
                "WARNING: No keyboards detected via evdev. Are you in the 'input' group?"
            )
            sys.exit(1)

        print("Listening on:")
        for kb in self.keyboards:
            print(f" - {kb.name} ({kb.path})")

        self.ctrl_held = False
        self.is_recording = False
        self.audio_buffer = []
        self.stream = None
        self.lock = threading.Lock()
        self.keep_running = True

    def find_keyboards(self):
        """Find all devices that actually have keys (filtering out pure mice)."""
        keyboards = []
        for path in evdev.list_devices():
            try:
                dev = evdev.InputDevice(path)
                caps = dev.capabilities()
                if ecodes.EV_KEY in caps and ecodes.KEY_SPACE in caps[ecodes.EV_KEY]:
                    keyboards.append(dev)
            except Exception:
                pass
        return keyboards

    def audio_callback(self, indata, frames, time, status):
        """Streams audio directly into a RAM list."""
        if status:
            print(status, file=sys.stderr)
        with self.lock:
            if self.is_recording:
                self.audio_buffer.append(indata.copy())

    def start_recording(self):
        with self.lock:
            if self.is_recording:
                return
            self.is_recording = True
            self.audio_buffer = []

        play_sound("on")
        notify("🔴 Listening...")
        print("\n[Start Recording]")

        self.stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="int16",
            callback=self.audio_callback,
        )
        self.stream.start()

    def stop_recording_and_transcribe(self):
        """The core magic. Stop, convert RAM buffer to Float32, transcribe, and type."""
        with self.lock:
            if not self.is_recording:
                return
            self.is_recording = False

        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

        play_sound("off")
        notify("⏳ Processing...")
        print("[Stop Recording. Transcribing...]")

        with self.lock:
            if not self.audio_buffer:
                notify("❌ No audio.")
                return
            # Concatenate all RAM chunks into one 1D array
            audio_data_int16 = np.concatenate(self.audio_buffer, axis=0).flatten()

        if len(audio_data_int16) < SAMPLE_RATE * 0.3:  # Less than 0.3 seconds
            print("Audio too short, ignoring.")
            return

        # Whisper expects float32 array normalized between -1.0 and 1.0
        audio_data_float32 = audio_data_int16.astype(np.float32) / 32768.0

        try:
            start_time = time.time()
            # Pass the RAM array DIRECTLY to CTranslate2. Zero disk I/O.
            segments, _ = self.model.transcribe(audio_data_float32, beam_size=5)
            text = " ".join([s.text for s in segments]).strip()

            latency = (time.time() - start_time) * 1000
            print(f"Result ({latency:.0f}ms): {text}")

            if text:
                type_text(text)
                notify(f"✅ {text}")
            else:
                notify("⚠️ Could not hear anything.")
        except Exception as e:
            print(f"Transcription error: {e}")
            notify("❌ Failed.")

    def handle_event(self, event):
        """Process keyboard events."""
        if event.type == ecodes.EV_KEY:
            key_event = evdev.categorize(event)

            # Track Left Ctrl or Right Ctrl
            if key_event.keycode in ["KEY_LEFTCTRL", "KEY_RIGHTCTRL"] or (
                isinstance(key_event.keycode, list)
                and any("CTRL" in k for k in key_event.keycode)
            ):
                if key_event.keystate == key_event.key_down:
                    self.ctrl_held = True
                elif key_event.keystate == key_event.key_up:
                    self.ctrl_held = False
                    # Safety: If ctrl is released while recording, stop
                    if self.is_recording:
                        threading.Thread(
                            target=self.stop_recording_and_transcribe
                        ).start()

            # Track Space
            if key_event.keycode == "KEY_SPACE" or (
                isinstance(key_event.keycode, list) and "KEY_SPACE" in key_event.keycode
            ):
                if key_event.keystate == key_event.key_down:
                    if self.ctrl_held and not self.is_recording:
                        self.start_recording()
                elif key_event.keystate == key_event.key_up:
                    if self.is_recording:
                        threading.Thread(
                            target=self.stop_recording_and_transcribe
                        ).start()

    def listen_loop(self, device):
        """Blocking read loop for a single device. Run in a thread."""
        try:
            for event in device.read_loop():
                if not self.keep_running:
                    break
                self.handle_event(event)
        except Exception as e:
            print(f"Device {device.name} disconnected: {e}")

    def run(self):
        print("\nJarvis Monolith Active. Hold 'Ctrl + Space' on ANY keyboard to talk.")
        print(
            "(Your Meta+Z / Win+Z Nerd Dictation setup remains completely untouched in the background)."
        )

        # Spawn a thread for each keyboard to avoid complex asyncio loops
        threads = []
        for kb in self.keyboards:
            t = threading.Thread(target=self.listen_loop, args=(kb,), daemon=True)
            t.start()
            threads.append(t)

        # Keep main thread alive
        try:
            while self.keep_running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down gracefully...")
            self.keep_running = False


if __name__ == "__main__":
    try:
        app = JarvisMonolith()
        app.run()
    except Exception as e:
        print(f"Fatal Error: {e}", file=sys.stderr)
        sys.exit(1)
