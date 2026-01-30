import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import subprocess
import io

# Add the project root directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.speak import speak_text, main, PIPER_MODEL

class TestSpeakText(unittest.TestCase):
    @patch('subprocess.Popen')
    @patch('subprocess.run')
    def test_speak_text_success(self, mock_run, mock_popen):
        # Mock Popen for echo and piper
        mock_process_1 = MagicMock()
        mock_process_1.stdout = MagicMock()
        
        mock_process_2 = MagicMock()
        mock_process_2.stdout = MagicMock()
        
        mock_popen.side_effect = [mock_process_1, mock_process_2]
        
        speak_text("Hello")
        
        # Verify echo was called
        mock_popen.assert_any_call(["echo", "Hello"], stdout=subprocess.PIPE)
        
        # Verify piper was called
        mock_popen.assert_any_call(
            ["piper-tts", "--model", PIPER_MODEL, "--output-raw"],
            stdin=mock_process_1.stdout,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )
        
        # Verify aplay was called
        mock_run.assert_called_with(
            ["aplay", "-q", "-r", "22050", "-f", "S16_LE", "-t", "raw"],
            stdin=mock_process_2.stdout
        )

    def test_speak_text_empty(self):
        with patch('subprocess.Popen') as mock_popen:
            speak_text("")
            mock_popen.assert_not_called()
            
            speak_text("   ")
            mock_popen.assert_not_called()

    @patch('subprocess.Popen')
    def test_speak_text_exception(self, mock_popen):
        mock_popen.side_effect = Exception("TTS Failed")
        
        # Capture stderr to verify error logging
        captured_stderr = io.StringIO()
        sys.stderr = captured_stderr
        
        speak_text("Hello")
        
        sys.stderr = sys.__stderr__
        self.assertIn("TTS Error: TTS Failed", captured_stderr.getvalue())

    @patch('scripts.speak.speak_text')
    def test_main_execution(self, mock_speak):
        test_args = ["speak.py", "Hello World"]
        with patch.object(sys, 'argv', test_args):
            main()
            mock_speak.assert_called_with("Hello World")

    def test_main_no_args(self):
        test_args = ["speak.py"]
        with patch.object(sys, 'argv', test_args):
            captured_output = io.StringIO()
            sys.stdout = captured_output
            
            with self.assertRaises(SystemExit):
                main()
            
            sys.stdout = sys.__stdout__
            self.assertIn("Usage:", captured_output.getvalue())

if __name__ == '__main__':
    unittest.main()