import subprocess
import os
import sys

def type_text(text):
    """
    Simulates keyboard input using ydotool.
    """
    if not text or not text.strip():
        return
    
    text = text.strip()
    
    try:
        # Ensure YDOTOOL_SOCKET is set
        env = os.environ.copy()
        if "YDOTOOL_SOCKET" not in env:
            runtime_dir = os.environ.get("XDG_RUNTIME_DIR", "/tmp")
            env["YDOTOOL_SOCKET"] = os.path.join(runtime_dir, ".ydotool_socket")
            
        print(f"DEBUG: Typing '{text}' using socket {env['YDOTOOL_SOCKET']}", file=sys.stderr)
            
        # Type the text
        subprocess.run(["ydotool", "type", text], env=env, check=True)
        
    except Exception as e:
        print(f"Typing Error: {e}", file=sys.stderr)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 type_input.py <text>")
        sys.exit(1)
    
    type_text(sys.argv[1])

if __name__ == "__main__":
    main()
