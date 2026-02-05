import unittest
import subprocess
import os
import shutil
import tempfile

class TestMonitorResources(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts', 'monitor_resources.sh'))
        self.log_file = os.path.join(self.test_dir, 'test_monitor.log')

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_monitor_script_exists(self):
        """Check if the script exists."""
        self.assertTrue(os.path.exists(self.script_path), "monitor_resources.sh does not exist")

    def test_monitor_script_execution(self):
        """Run the script for a short duration and check log output."""
        # Create a dummy script if it doesn't exist yet (to allow Red phase to run without crashing on missing file)
        # But wait, the task is to create it. So initially it won't exist.
        # The test should fail because the script is missing or doesn't work.
        
        if not os.path.exists(self.script_path):
            self.fail("monitor_resources.sh does not exist")

        # Run for 2 seconds
        cmd = [self.script_path, self.log_file, "2"] 
        env = os.environ.copy()
        env["MONITOR_INTERVAL"] = "1"
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5, env=env)
            self.assertEqual(result.returncode, 0)
            
            # Check log content
            self.assertTrue(os.path.exists(self.log_file))
            with open(self.log_file, 'r') as f:
                content = f.read()
                self.assertIn("CPU", content)
                self.assertIn("MEM", content)
                # GPU might not be present in CI env, but we should handle that gracefully
        except subprocess.TimeoutExpired:
            self.fail("Script timed out")
        except Exception as e:
            self.fail(f"Script failed: {e}")

if __name__ == '__main__':
    unittest.main()
