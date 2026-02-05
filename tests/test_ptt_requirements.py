import unittest
import shutil

class TestPTTRequirements(unittest.TestCase):
    def test_input_remapper_installed(self):
        """Check if input-remapper-control is in the PATH."""
        executable = shutil.which("input-remapper-control")
        self.assertIsNotNone(executable, "input-remapper-control not found in PATH")

if __name__ == '__main__':
    unittest.main()
