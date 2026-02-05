import subprocess
import os
import sys
import time

def paste_text(text):
    """
    Pastes text using wl-copy and ydotool (Primary + Clipboard Fix).
    """
    if not text:
        return
    
    text = text.strip()
    
    try:
        # Force Environment for Systemd/Wayland
        env = os.environ.copy()
        uid = os.getuid()
        env["WAYLAND_DISPLAY"] = "wayland-0"
        env["XDG_RUNTIME_DIR"] = f"/run/user/{uid}"
        
        # 1. Copy to Clipboard AND Primary Selection
        if subprocess.run(["which", "wl-copy"], stdout=subprocess.DEVNULL).returncode == 0:
            # Update standard clipboard (Ctrl+V)
            subprocess.run(["wl-copy", text], env=env, check=True)
            # Update primary selection (Shift+Insert / Middle-click)
            subprocess.run(["wl-copy", "--primary", text], env=env, check=True)
            
            # Tiny sleep to let clipboard sync
            time.sleep(0.1) 
        else:
            print("Error: wl-copy not found.", file=sys.stderr)
            return

        # 2. Simulate Paste (Shift+Insert)
        env["YDOTOOL_SOCKET"] = os.path.join(env["XDG_RUNTIME_DIR"], ".ydotool_socket")
            
        print(f"DEBUG: Pasting '{text}' to Clipboard and Primary...", file=sys.stderr)
            
        # Shift(42) Down, Insert(110) Down, Insert Up, Shift Up
        subprocess.run(["ydotool", "key", "42:1", "110:1", "110:0", "42:0"], env=env, check=True)
        
    except Exception as e:
        print(f"Pasting Error: {e}", file=sys.stderr)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 paste_input.py <text>")
        sys.exit(1)
    
    paste_text(sys.argv[1])

if __name__ == "__main__":
    main()
