import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import subprocess
import io

# Add the project root directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.type_input import type_text, main


class TestTypeInput(unittest.TestCase):
    @patch("subprocess.run")
    def test_type_text_success(self, mock_run):
        # Mock subprocess.run
        mock_run.return_value = MagicMock(returncode=0)

        type_text("Hello Jarvis")

        # Verify ydotool type was called with --next-delay 0 for speed
        mock_run.assert_called_with(
            ["ydotool", "type", "--next-delay", "0", "Hello Jarvis"],
            env=unittest.mock.ANY,
            check=True,
        )

    def test_type_text_empty(self):
        with patch("subprocess.run") as mock_run:
            type_text("")
            mock_run.assert_not_called()

            type_text("   ")
            mock_run.assert_not_called()

    @patch("subprocess.run")
    def test_type_text_exception(self, mock_run):
        mock_run.side_effect = Exception("Typing Failed")

        # Capture stderr
        captured_stderr = io.StringIO()
        sys.stderr = captured_stderr

        type_text("Hello")

        sys.stderr = sys.__stderr__
        self.assertIn("Typing Error: Typing Failed", captured_stderr.getvalue())

    @patch("scripts.type_input.type_text")
    def test_main_execution(self, mock_type):
        test_args = ["type_input.py", "Hello World"]
        with patch.object(sys, "argv", test_args):
            main()
            mock_type.assert_called_with("Hello World")

    def test_main_no_args(self):
        test_args = ["type_input.py"]
        with patch.object(sys, "argv", test_args):
            captured_output = io.StringIO()
            sys.stdout = captured_output

            with self.assertRaises(SystemExit):
                main()

            sys.stdout = sys.__stdout__
            self.assertIn("Usage:", captured_output.getvalue())


if __name__ == "__main__":
    unittest.main()
