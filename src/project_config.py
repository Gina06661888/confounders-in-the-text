"""Load local paths without storing user-specific locations in the repository."""
from pathlib import Path
import json

def load_project_config(repo_root):
    root = Path(repo_root).resolve()
    path = root/'configs'/'paths.local.json'
    if not path.is_file():
        raise FileNotFoundError('Copy configs/paths.example.json to configs/paths.local.json and set the local input paths before training.')
    raw = json.loads(path.read_text(encoding='utf-8'))
    def resolve(value):
        p = Path(value).expanduser()
        return p.resolve() if p.is_absolute() else (root/p).resolve()
    result = {key:resolve(raw[key]) for key in ('data_root','analysis_data_dir','embedding_root','output_root')}
    if result['output_root'] == result['analysis_data_dir']:
        raise ValueError('Output folder must differ from the frozen input sample folder.')
    if not (result['analysis_data_dir']/'dataset_snapshot.json').is_file():
        raise FileNotFoundError('analysis_data_dir must contain the frozen dataset_snapshot.json receipt.')
    result['expected_corpus_id'] = str(raw['expected_corpus_id'])
    result['embedding_snapshots'] = {k:resolve(v) for k,v in raw.get('embedding_snapshots',{}).items() if v}
    return result
