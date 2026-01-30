import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import subprocess
import io

# Add the project root directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.execute import execute_command, main

class TestExecuteCommand(unittest.TestCase):
    @patch('subprocess.run')
    def test_execute_command_success(self, mock_run):
        mock_result = MagicMock()
        mock_result.stdout = "Command output"
        mock_result.stderr = ""
        mock_result.returncode = 0
        mock_run.return_value = mock_result
        
        output, error, code = execute_command("ls -la")
        
        self.assertEqual(output, "Command output")
        self.assertEqual(error, "")
        self.assertEqual(code, 0)
        mock_run.assert_called_with("ls -la", shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    @patch('subprocess.run')
    def test_execute_command_failure(self, mock_run):
        mock_result = MagicMock()
        mock_result.stdout = ""
        mock_result.stderr = "Command failed"
        mock_result.returncode = 1
        mock_run.return_value = mock_result
        
        output, error, code = execute_command("invalid_command")
        
        self.assertEqual(output, "")
        self.assertEqual(error, "Command failed")
        self.assertEqual(code, 1)

    @patch('subprocess.run')
    def test_execute_command_exception(self, mock_run):
        mock_run.side_effect = Exception("Subprocess error")
        
        output, error, code = execute_command("crash")
        
        self.assertEqual(output, "")
        self.assertEqual(error, "Subprocess error")
        self.assertEqual(code, -1)

    @patch('scripts.execute.execute_command')
    def test_main_execution(self, mock_execute):
        mock_execute.return_value = ("Out", "Err", 0)
        
        test_args = ["execute.py", "echo test"]
        with patch.object(sys, 'argv', test_args):
            captured_output = io.StringIO()
            sys.stdout = captured_output
            
            main()
            
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()
            self.assertIn("Code: 0", output)
            self.assertIn("Stdout: Out", output)

if __name__ == '__main__':
    unittest.main()
