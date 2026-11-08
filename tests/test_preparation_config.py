from pathlib import Path
import json
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from preparation_config import load_preparation_config


class PreparationConfigurationTests(unittest.TestCase):
    def test_protects_source_project(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'configs').mkdir()
            (root / 'configs/preparation.local.json').write_text(json.dumps({
                'source_project_root': 'private', 'output_root': 'private/overwrite',
            }))
            with self.assertRaises(ValueError):
                load_preparation_config(root)

    def test_new_stage_outputs_can_feed_the_next_stage(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'configs').mkdir()
            config = {'source_project_root': 'private', 'output_root': 'outputs/preparation',
                      'financial_run_dir': 'outputs/preparation/financial/processed/financial_preparation/new-run'}
            (root / 'configs/preparation.local.json').write_text(json.dumps(config))
            result = load_preparation_config(root)
            self.assertEqual(result['financial_run_dir'], root / config['financial_run_dir'])
            self.assertEqual(result['compustat_source'], root / 'private/10K_compustat/raw/fxzpe8jifm2g4jh7.csv.zip')


if __name__ == '__main__':
    unittest.main()
