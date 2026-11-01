from pathlib import Path
import sys, tempfile, unittest, json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from project_config import load_project_config

class ConfigurationTests(unittest.TestCase):
    def test_missing_configuration_stops(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(FileNotFoundError):
                load_project_config(folder)

    def test_portable_paths_and_local_snapshot(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            (root/'configs').mkdir()
            (root/'data/sample').mkdir(parents=True)
            (root/'data/sample/dataset_snapshot.json').write_text('{}')
            config={'data_root':'data','analysis_data_dir':'data/sample',
                    'embedding_root':'data/embeddings','output_root':'outputs',
                    'expected_corpus_id':'example','embedding_snapshots':{'minilm':None}}
            (root/'configs/paths.local.json').write_text(json.dumps(config))
            result=load_project_config(root)
            self.assertEqual(result['analysis_data_dir'],(root/'data/sample').resolve())
            self.assertEqual(result['embedding_snapshots'],{})

if __name__=='__main__':
    unittest.main()
