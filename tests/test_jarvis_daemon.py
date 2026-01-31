import unittest
from unittest.mock import MagicMock, patch, mock_open
import sys
import os
import socket
import threading
import time
import signal

# Add the project root directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.jarvis_daemon import JarvisDaemon

class TestJarvisDaemon(unittest.TestCase):
    @patch('scripts.jarvis_daemon.WhisperModel')
    @patch('socket.socket')
    @patch('os.remove')
    @patch('os.path.exists')
    @patch('os.chmod')
    def test_daemon_initialization(self, mock_chmod, mock_exists, mock_remove, mock_socket, mock_model):
        mock_exists.return_value = False
        daemon = JarvisDaemon("/tmp/test.sock")
        
        # Verify model loaded
        mock_model.assert_called_once()
        
        # Verify socket created
        mock_socket.assert_called_with(socket.AF_UNIX, socket.SOCK_STREAM)
        
        # Verify chmod called
        mock_chmod.assert_called_with("/tmp/test.sock", 0o600)

    @patch('scripts.jarvis_daemon.WhisperModel')
    @patch('socket.socket')
    @patch('os.chmod')
    def test_handle_client(self, mock_chmod, mock_socket, mock_model):
        daemon = JarvisDaemon("/tmp/test.sock")
        
        # Mock client socket
        mock_client = MagicMock()
        mock_client.recv.return_value = b"/tmp/audio.wav"
        
        # Mock transcription result
        mock_model_instance = mock_model.return_value
        Segment = MagicMock()
        Segment.text = "Hello"
        mock_model_instance.transcribe.return_value = ([Segment], None)
        
        # Mock file exists for the audio file check
        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = True
            # Run handler
            daemon.handle_client(mock_client)
        
        # Verify transcribe called
        mock_model_instance.transcribe.assert_called_with("/tmp/audio.wav", beam_size=5)
        
        # Verify response sent
        mock_client.sendall.assert_called_with(b"Hello")

    @patch('scripts.jarvis_daemon.WhisperModel')
    @patch('socket.socket')
    @patch('os.chmod')
    def test_handle_client_error(self, mock_chmod, mock_socket, mock_model):
        daemon = JarvisDaemon("/tmp/test.sock")
        
        mock_client = MagicMock()
        mock_client.recv.side_effect = Exception("Receive Error")
        
        daemon.handle_client(mock_client)
        
        mock_client.sendall.assert_called_with(b"ERROR: Receive Error")

    @patch('scripts.jarvis_daemon.WhisperModel')
    @patch('socket.socket')
    @patch('os.chmod')
    def test_run_loop(self, mock_chmod, mock_socket, mock_model):
        daemon = JarvisDaemon("/tmp/test.sock")
        daemon.server = MagicMock()
        
        # Mock accept to return a client once, then raise OSError to break loop
        client = MagicMock()
        daemon.server.accept.side_effect = [(client, "addr"), OSError("Stop")]
        
        # Mock handle_client to avoid actual logic
        daemon.handle_client = MagicMock()
        
        daemon.run()
        
        daemon.handle_client.assert_called_once_with(client)

    @patch('scripts.jarvis_daemon.WhisperModel')
    @patch('socket.socket')
    @patch('os.chmod')
    @patch('sys.exit')
    def test_stop(self, mock_exit, mock_chmod, mock_socket, mock_model):
        daemon = JarvisDaemon("/tmp/test.sock")
        
        with patch('os.path.exists') as mock_exists, patch('os.remove') as mock_remove:
            mock_exists.return_value = True
            daemon.stop()
            
            mock_remove.assert_called_with("/tmp/test.sock")
            mock_exit.assert_called_with(0)

if __name__ == '__main__':
    unittest.main()