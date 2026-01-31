import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import socket

# Add the project root directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.transcribe import transcribe_audio_client

class TestTranscribeClient(unittest.TestCase):
    @patch('os.path.exists')
    @patch('socket.socket')
    def test_transcribe_audio_client_success(self, mock_socket_class, mock_exists):
        mock_exists.return_value = True
        
        # Configure context manager
        mock_sock_instance = MagicMock()
        mock_socket_class.return_value = mock_sock_instance
        mock_client = mock_sock_instance.__enter__.return_value
        
        # Mock server response
        mock_client.recv.return_value = b"Hello Daemon"
        
        result = transcribe_audio_client("/tmp/audio.wav")
        
        # Verify connection
        mock_client.connect.assert_called_with("/tmp/jarvis.sock")
        
        # Verify data sent
        mock_client.sendall.assert_called_with(b"/tmp/audio.wav")
        
        self.assertEqual(result, "Hello Daemon")

    @patch('os.path.exists')
    @patch('socket.socket')
    def test_transcribe_audio_client_connection_refused(self, mock_socket_class, mock_exists):
        mock_exists.return_value = True
        
        mock_sock_instance = MagicMock()
        mock_socket_class.return_value = mock_sock_instance
        
        # Connect raises exception on the instance (or __enter__ depending on where connect is called)
        # connect is called on the instance BEFORE enter in some patterns, but here:
        # with socket.socket(...) as client: client.connect() -> No, it is:
        # with socket.socket(...) as client: client.connect()
        # Wait, usually it is: s = socket.socket(); s.connect(); with s: ...
        # My code: with socket.socket(...) as client: client.connect()
        
        # So connect is called on the object returned by __enter__? No, client is bound to __enter__ return.
        # But if I use `as client`, `client` is what `__enter__` returns.
        # Check code: `with socket.socket(...) as client: client.connect(...)`
        # So I should mock `connect` on the object returned by `__enter__`.
        
        mock_client = mock_sock_instance.__enter__.return_value
        mock_client.connect.side_effect = ConnectionRefusedError("Daemon not running")
        
        with self.assertRaises(ConnectionRefusedError):
            transcribe_audio_client("/tmp/audio.wav")

if __name__ == '__main__':
    unittest.main()
