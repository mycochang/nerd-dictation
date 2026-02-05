import socket
import os
import sys
import signal
import time
from faster_whisper import WhisperModel

# Configuration
MODEL_SIZE = "Systran/faster-distil-whisper-small.en"
DEVICE = "cpu" 
COMPUTE_TYPE = "int8" 
RUNTIME_DIR = os.environ.get('XDG_RUNTIME_DIR', '/tmp')
SOCKET_PATH = os.path.join(RUNTIME_DIR, "jarvis.sock")
IDLE_TIMEOUT = 3600 # 1 hour in seconds

class JarvisDaemon:
    def __init__(self, socket_path=SOCKET_PATH):
        self.socket_path = socket_path
        self.running = True
        self.model = None
        self.last_active = time.time()
        
        # Load Model
        print(f"Loading {MODEL_SIZE} model on {DEVICE}...")
        try:
            self.model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)
            print("Model loaded.")
        except Exception as e:
            print(f"Failed to load model on {DEVICE}: {e}")
            print("Falling back to CPU...")
            self.model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")

        # Setup Socket
        if os.environ.get('LISTEN_FDS'):
            # Systemd socket activation
            print("Systemd socket activation detected.")
            self.server = socket.fromfd(3, socket.AF_UNIX, socket.SOCK_STREAM)
            # systemd-passed sockets are already bound and listening
        else:
            # Manual startup
            if os.path.exists(self.socket_path):
                os.remove(self.socket_path)
                
            self.server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.server.bind(self.socket_path)
            os.chmod(self.socket_path, 0o600) # Secure permissions
            self.server.listen(1)
            
        self.server.settimeout(10.0) # Check for idle timeout every 10 seconds
        print(f"Listening on {self.socket_path}")

    def handle_client(self, client_socket):
        self.last_active = time.time()
        try:
            # Receive audio file path
            data = client_socket.recv(1024).decode('utf-8').strip()
            if not data:
                return
                
            # Sanitize and Validate Path
            audio_file = os.path.abspath(os.path.expanduser(data))
            
            # Common audio/container extensions supported by ffmpeg
            ALLOWED_EXTENSIONS = {
                '.wav', '.mp3', '.m4a', '.ogg', '.flac', 
                '.aac', '.opus', '.webm', '.mp4', '.m4v', '.mkv'
            }
            _, ext = os.path.splitext(audio_file.lower())
            
            if ext not in ALLOWED_EXTENSIONS:
                print(f"Blocked invalid file type: {audio_file}")
                client_socket.sendall(b"ERROR: Invalid file type. Only audio files allowed.")
                return

            print(f"Transcribing: {audio_file}")
            
            if not os.path.isfile(audio_file):
                client_socket.sendall(b"ERROR: File not found or not a regular file")
                return

            # Transcribe
            segments, _ = self.model.transcribe(audio_file, beam_size=5)
            text = " ".join([s.text for s in segments]).strip()
            
            print(f"Result: {text}")
            client_socket.sendall(text.encode('utf-8'))
            
        except Exception as e:
            print(f"Error handling client: {e}")
            client_socket.sendall(f"ERROR: {str(e)}".encode('utf-8'))
        finally:
            client_socket.close()

    def run(self):
        # Handle signals
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)
        
        print(f"Daemon started. Will exit after {IDLE_TIMEOUT/60} minutes of inactivity.")
        
        while self.running:
            try:
                client, _ = self.server.accept()
                self.handle_client(client)
            except socket.timeout:
                # Check idle timeout
                if time.time() - self.last_active > IDLE_TIMEOUT:
                    print(f"Idle timeout reached ({IDLE_TIMEOUT}s). Shutting down.")
                    self.stop()
            except OSError:
                break
            except Exception as e:
                print(f"Server error: {e}")

    def stop(self, signum=None, frame=None):
        print("Stopping daemon...")
        self.running = False
        try:
            self.server.close()
        except:
            pass
        # Only remove socket if we created it (not systemd)
        if not os.environ.get('LISTEN_FDS') and os.path.exists(self.socket_path):
            os.remove(self.socket_path)
        sys.exit(0)

if __name__ == "__main__":
    daemon = JarvisDaemon()
    daemon.run()
