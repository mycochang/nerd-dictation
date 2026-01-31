import unittest
from unittest.mock import MagicMock, patch, mock_open
import sys
import os
import io

# Add the project root directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.watch_output import watch_and_speak

class TestWatchOutput(unittest.TestCase):
    @patch('scripts.watch_output.speak_text')
    @patch('os.path.exists')
    @patch('time.sleep')
    def test_watch_and_speak_success(self, mock_sleep, mock_exists, mock_speak):
        mock_exists.return_value = True
        
        # We need to mock open and the file handle
        m = mock_open()
        # Mock readline to return a line then empty
        m.return_value.readline.side_effect = ["Hello World\n", "", "", ""]
        
        with patch("builtins.open", m):
            # Run with stop_after=1 to avoid infinite loop
            watch_and_speak("test.log", stop_after=1)
            
            # Verify speak was called
            mock_speak.assert_called_with("Hello World")

    @patch('scripts.watch_output.speak_text')
    @patch('os.path.exists')
    @patch('time.sleep')
    def test_watch_and_speak_wait_for_file(self, mock_sleep, mock_exists, mock_speak):
        # First call False, second call True
        mock_exists.side_effect = [False, True]
        
        m = mock_open()
        m.return_value.readline.side_effect = ["", "", ""]
        
        with patch("builtins.open", m):
            watch_and_speak("test.log", stop_after=1)
            
            # Verify sleep was called at least once
            self.assertTrue(mock_sleep.called)

    @patch('scripts.watch_output.speak_text')
    def test_main_no_args(self, mock_speak):
        from scripts.watch_output import main
        test_args = ["watch_output.py"]
        with patch.object(sys, 'argv', test_args):
            captured_output = io.StringIO()
            sys.stdout = captured_output
            with self.assertRaises(SystemExit):
                main()
            sys.stdout = sys.__stdout__
            self.assertIn("Usage:", captured_output.getvalue())

if __name__ == '__main__':
    unittest.main()