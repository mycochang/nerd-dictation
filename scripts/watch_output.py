import time
import os
import sys
from scripts.speak import speak_text

def watch_and_speak(filepath, poll_interval=0.5, stop_after=None):
    """
    Watches a file for new lines and speaks them.
    stop_after is for testing (number of iterations).
    """
    if not os.path.exists(filepath):
        # Wait for file to be created
        while not os.path.exists(filepath):
            if stop_after is not None and stop_after <= 0:
                return
            time.sleep(poll_interval)
            if stop_after is not None: stop_after -= 1

    with open(filepath, 'r') as f:
        # Move to end of file initially? 
        # For a screen reader, maybe we want to start from now.
        f.seek(0, os.SEEK_END)
        
        count = 0
        while True:
            line = f.readline()
            if not line:
                if stop_after is not None and count >= stop_after:
                    break
                time.sleep(poll_interval)
                count += 1
                continue
            
            # Clean and speak
            text = line.strip()
            if text:
                print(f"Reading: {text}")
                speak_text(text)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 watch_output.py <logfile>")
        sys.exit(1)
    
    watch_and_speak(sys.argv[1])

if __name__ == "__main__":
    main()
