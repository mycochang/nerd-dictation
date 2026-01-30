import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import io

# Add the project root directory to the path so we can import the module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.transcribe import transcribe_audio, main

class TestTranscribeWhisper(unittest.TestCase):
    @patch('scripts.transcribe.WhisperModel')
    def test_transcribe_audio_success(self, MockModel):
        mock_model_instance = MockModel.return_value
        Segment = MagicMock()
        Segment.text = "Hello world"
        mock_model_instance.transcribe.return_value = ([Segment], None)
        
        result = transcribe_audio("dummy_audio.wav")
        self.assertEqual(result, "Hello world")

    def test_transcribe_audio_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            transcribe_audio("non_existent_file.wav")

    @patch('scripts.transcribe.transcribe_audio')
    def test_main_execution(self, mock_transcribe):
        mock_transcribe.return_value = "Test Output"
        
        test_args = ["transcribe.py", "test.wav"]
        with patch.object(sys, 'argv', test_args):
            captured_output = io.StringIO()
            sys.stdout = captured_output
            
            main()
            
            sys.stdout = sys.__stdout__
            self.assertEqual(captured_output.getvalue().strip(), "Test Output")

    def test_main_no_args(self):
        test_args = ["transcribe.py"]
        with patch.object(sys, 'argv', test_args):
            captured_output = io.StringIO()
            sys.stdout = captured_output
            
            with self.assertRaises(SystemExit):
                main()
            
            sys.stdout = sys.__stdout__
            # self.assertIn("Usage:", captured_output.getvalue()) # Simple check

if __name__ == '__main__':
    unittest.main()
