from pathlib import Path
import sys, tempfile, unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from run_synthetic_demo import run_demo

class SyntheticEstimatorTests(unittest.TestCase):
    def test_known_effect_and_omitted_confounder(self):
        with tempfile.TemporaryDirectory() as folder:
            rows = run_demo(folder)
        observed, oracle = rows
        self.assertGreater(observed['estimated_slope'], 1.3)
        self.assertLess(abs(oracle['estimated_slope']-1), 0.08)
        self.assertLess(oracle['ci_low'], 1)
        self.assertGreater(oracle['ci_high'], 1)

if __name__ == '__main__':
    unittest.main()
