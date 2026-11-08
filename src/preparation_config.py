"""Explicit private inputs and separate writable preparation outputs."""
import json
from pathlib import Path


def load_preparation_config(repo_root):
    root = Path(repo_root).resolve()
    config_path = root / 'configs' / 'preparation.local.json'
    if not config_path.is_file():
        raise FileNotFoundError('Copy configs/preparation.example.json to configs/preparation.local.json and set source_project_root before preparing data.')
    raw = json.loads(config_path.read_text(encoding='utf-8'))

    def resolve(value):
        p = Path(value).expanduser()
        return p.resolve() if p.is_absolute() else (root / p).resolve()

    project = resolve(raw['source_project_root'])
    output = resolve(raw.get('output_root', 'outputs/preparation'))
    defaults = {
        'raw_filings_dir': project,
        'extraction_dir': project / '10K_competition_lean16_recovered',
        'compustat_source': project / '10K_compustat/raw/fxzpe8jifm2g4jh7.csv.zip',
        'financial_run_dir': project / '10K_compustat/processed/financial_preparation/f210213cef87860ef86d',
        'sec_run_dir': project / '10K_compustat/sec_metadata/runs/20261029T184230_97d76974',
        'embedding_root': project / '10K_three_model_embeddings',
        'minilm_snapshot': project / '10K_three_model_embeddings/minilm/fa8fc124c14a1ca97e34/4bbe3e612630a585888e/latest_snapshot.json',
        'extraction_output_root': output / 'extraction',
        'financial_output_root': output / 'financial/processed/financial_preparation',
        'sec_output_root': output / 'sec_metadata',
        'embedding_output_root': output / 'embeddings',
        'analysis_output_root': output / 'analysis',
    }
    result = {k: resolve(raw[k]) if raw.get(k) else v.resolve() for k, v in defaults.items()}
    # No stage writes into the supplied project or into any configured input.
    inputs = [project, *(result[k] for k in defaults if not k.endswith('_output_root'))]
    destinations = [result[k] for k in defaults if k.endswith('_output_root')]
    # Financial preparation also creates a raw backup two levels above its run root.
    destinations.append(result['financial_output_root'].parent.parent / 'raw')
    for dest in destinations:
        for source in inputs:
            if dest == source or source in dest.parents or (source == project and dest in source.parents):
                raise ValueError(f'Preparation output overlaps a protected input: {dest}')
    return result
