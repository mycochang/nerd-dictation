import unittest
import subprocess
import os
import shutil
import tempfile
import time

class TestPTTHandler(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts', 'jarvis_ptt_handler.sh'))
        self.pid_file = os.path.join(tempfile.gettempdir(), 'jarvis_ptt_test.pid')
        # We need to override the PID file path in the script, or mock it.
        # Since it's a bash script, environment variables are the best way.
        self.env = os.environ.copy()
        self.env["PID_FILE"] = self.pid_file
        self.env["AUDIO_FILE"] = os.path.join(self.test_dir, "test_audio.wav")
        self.env["PYTHON_INTERPRETER"] = "python3"
        # Mock parecord and other tools if necessary, or just check logic flow.
        
    def tearDown(self):
        shutil.rmtree(self.test_dir)
        if os.path.exists(self.pid_file):
            os.remove(self.pid_file)

    def test_handler_script_exists(self):
        self.assertTrue(os.path.exists(self.script_path), "jarvis_ptt_handler.sh does not exist")

    def test_start_stop_logic(self):
        if not os.path.exists(self.script_path):
            self.fail("Script missing")

        # Test START
        # We need to mock parecord to just sleep or run in background
        # We can create a fake parecord in the test_dir and add to PATH
        fake_bin_dir = os.path.join(self.test_dir, 'bin')
        os.makedirs(fake_bin_dir)
        self.env["PATH"] = f"{fake_bin_dir}:{self.env['PATH']}"
        
        with open(os.path.join(fake_bin_dir, 'parecord'), 'w') as f:
            f.write("#!/bin/bash\nsleep 10\n")
        os.chmod(os.path.join(fake_bin_dir, 'parecord'), 0o755)
        
        # Also mock aplay and notify-send to avoid noise
        with open(os.path.join(fake_bin_dir, 'aplay'), 'w') as f:
            f.write("#!/bin/bash\nexit 0\n")
        os.chmod(os.path.join(fake_bin_dir, 'aplay'), 0o755)
        
        with open(os.path.join(fake_bin_dir, 'notify-send'), 'w') as f:
            f.write("#!/bin/bash\nexit 0\n")
        os.chmod(os.path.join(fake_bin_dir, 'notify-send'), 0o755)

        # START
        subprocess.run([self.script_path, "start"], env=self.env, check=True)
        self.assertTrue(os.path.exists(self.pid_file), "PID file should exist after start")
        
        # Verify process is running
        with open(self.pid_file, 'r') as f:
            pid = int(f.read().strip())
        try:
            os.kill(pid, 0)
        except OSError:
            self.fail("Recording process not running")

        # STOP
        # We need to mock the python scripts it calls too (transcribe/type)
        with open(os.path.join(fake_bin_dir, 'python3'), 'w') as f:
            f.write("#!/bin/bash\nexit 0\n") # Dummy python
        os.chmod(os.path.join(fake_bin_dir, 'python3'), 0o755)

        subprocess.run([self.script_path, "stop"], env=self.env, check=True)
        self.assertFalse(os.path.exists(self.pid_file), "PID file should be gone after stop")

if __name__ == '__main__':
    unittest.main()
