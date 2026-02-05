import evdev
from evdev import InputDevice, categorize, ecodes
import sys
import os
import subprocess
import signal

# Configuration
TARGET_DEVICE_NAME = "AT Translated Set 2 keyboard" # Adjust as needed
HANDLER_SCRIPT = os.path.expanduser("~/scripts/jarvis_ptt_handler.sh")

class KeyboardListener:
    def __init__(self, device_name=TARGET_DEVICE_NAME):
        self.device = self.find_device(device_name)
        if not self.device:
            raise FileNotFoundError(f"Device '{device_name}' not found")
        
        print(f"Listening on: {self.device.name}")
        self.meta_held = False
        self.active = False

    def find_device(self, name):
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for device in devices:
            if device.name == name:
                return device
        return None

    def run_handler(self, action):
        try:
            subprocess.Popen([HANDLER_SCRIPT, action])
        except Exception as e:
            print(f"Error running handler: {e}", file=sys.stderr)

    def listen(self):
        # Exclusive access - DISABLED for safety
        # self.device.grab()
        print("Device listening (Passive). Press Meta+Z to talk.")
        
        try:
            for event in self.device.read_loop():
                if event.type == ecodes.EV_KEY:
                    key_event = evdev.categorize(event)
                    
                    # Track Meta Key
                    if key_event.keycode == "KEY_LEFTMETA" or key_event.keycode == "KEY_RIGHTMETA":
                        if key_event.keystate == key_event.key_down:
                            self.meta_held = True
                        elif key_event.keystate == key_event.key_up:
                            self.meta_held = False
                            # Safety: If released meta while active, stop
                            if self.active:
                                self.run_handler("stop")
                                self.active = False

                    # Trigger Key: Z
                    if key_event.keycode == "KEY_Z":
                        if key_event.keystate == key_event.key_down:
                            if self.meta_held:
                                print("Start Recording")
                                self.run_handler("start")
                                self.active = True
                        elif key_event.keystate == key_event.key_up:
                            if self.active:
                                print("Stop Recording")
                                self.run_handler("stop")
                                self.active = False
        except KeyboardInterrupt:
            pass
        finally:
            # self.device.ungrab()
            print("Device listener stopped.")

if __name__ == "__main__":
    try:
        listener = KeyboardListener()
        listener.listen()
    except Exception as e:
        print(f"Fatal Error: {e}", file=sys.stderr)
        sys.exit(1)
