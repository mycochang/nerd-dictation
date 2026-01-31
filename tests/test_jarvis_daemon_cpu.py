import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.jarvis_daemon import JarvisDaemon

class TestJarvisDaemonCPU(unittest.TestCase):
    @patch('scripts.jarvis_daemon.WhisperModel')
    @patch('socket.fromfd')
    @patch('os.environ.get', return_value='3') # Simulate socket activation
    @patch('os.chmod')
    def test_daemon_forces_cpu(self, mock_chmod, mock_env, mock_fromfd, MockModel):
        # We need to ensure that WhisperModel is called with device="cpu"
        daemon = JarvisDaemon("/tmp/test.sock")
        
        # Verify WhisperModel was called with device="cpu"
        # Check the first call to WhisperModel
        args, kwargs = MockModel.call_args
        self.assertEqual(kwargs.get('device'), 'cpu', "Daemon must use CPU device")
        self.assertEqual(kwargs.get('compute_type'), 'int8', "Daemon should use int8 for CPU speed")

if __name__ == '__main__':
    unittest.main()
