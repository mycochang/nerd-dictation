import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import io
import socket

# Add the project root directory to the path so we can import the module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.transcribe import transcribe_audio, transcribe_audio_client, main

class TestTranscribeWhisper(unittest.TestCase):
    @patch('scripts.transcribe.WhisperModel')
    def test_transcribe_audio_success(self, MockModel):
        mock_model_instance = MockModel.return_value
        Segment = MagicMock()
        Segment.text = "Hello world"
        mock_model_instance.transcribe.return_value = ([Segment], None)
        
        # Patch os.path.exists for this test specifically
        with patch('os.path.exists', return_value=True):
            result = transcribe_audio("dummy_audio.wav")
            self.assertEqual(result, "Hello world")

    def test_transcribe_audio_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            transcribe_audio("non_existent_file.wav")

    @patch('scripts.transcribe.transcribe_audio_client')
    def test_main_execution_client_success(self, mock_client):
        mock_client.return_value = "Client Output"
        
        test_args = ["transcribe.py", "test.wav"]
        with patch.object(sys, 'argv', test_args):
            captured_output = io.StringIO()
            sys.stdout = captured_output
            
            main()
            
            sys.stdout = sys.__stdout__
            self.assertEqual(captured_output.getvalue().strip(), "Client Output")

    @patch('scripts.transcribe.transcribe_audio_client')
    @patch('scripts.transcribe.transcribe_audio')
    def test_main_execution_fallback(self, mock_transcribe, mock_client):
        # Simulate client failure
        mock_client.side_effect = ConnectionRefusedError("Daemon down")
        mock_transcribe.return_value = "Fallback Output"
        
        test_args = ["transcribe.py", "test.wav"]
        with patch.object(sys, 'argv', test_args):
            captured_output = io.StringIO()
            sys.stdout = captured_output
            
            main()
            
            sys.stdout = sys.__stdout__
            self.assertEqual(captured_output.getvalue().strip(), "Fallback Output")

    @patch('os.path.exists')
    @patch('socket.socket')
    def test_transcribe_audio_client_success(self, mock_socket_class, mock_exists):
        mock_exists.return_value = True
        
        mock_sock_instance = MagicMock()
        mock_socket_class.return_value = mock_sock_instance
        mock_client = mock_sock_instance.__enter__.return_value
        
        mock_client.recv.return_value = b"Hello Daemon"
        
        result = transcribe_audio_client("/tmp/audio.wav")
        self.assertEqual(result, "Hello Daemon")

    def test_main_no_args(self):
        test_args = ["transcribe.py"]
        with patch.object(sys, 'argv', test_args):
            captured_output = io.StringIO()
            sys.stdout = captured_output
            
            with self.assertRaises(SystemExit):
                main()
            
            sys.stdout = sys.__stdout__

if __name__ == '__main__':
    unittest.main()