"""Compare supplied original aggregate outputs with the review-package CSVs.

This checks exported numbers, not a model refit. Pass the private project's
10K_compustat/processed folder. No individual financial observations are read.
"""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
COMPARISONS = {
    'MiniLM': ('geni_benchmarks', 'comparison_a60d6cffe5884ca3'),
    'Llama': ('geni_benchmarks_llama', 'comparison_e78d3603a1f62008'),
    'OpenAI': ('geni_benchmarks_openai', 'comparison_4fa0514c7545692b'),
}


def original_model(row):
    spec = 'GENI' if row.specification == 'Adjustment Z' else row.specification
    return f'{spec}-{row.learner}'


def verify(processed):
    processed = Path(processed)
    comparisons, probes = {}, {}
    for encoder, (folder, comparison) in COMPARISONS.items():
        d = processed / folder / 'asset_sensitivity' / comparison
        comparisons[encoder] = pd.read_csv(d / 'benchmark_comparison.csv')
        probes[encoder] = pd.read_csv(d / 'probe_comparison.csv')
    checked = {}
    for name in ['table1_asset_restricted.csv', 'table1_full_sample.csv', 'asset_sensitivity_adjustment.csv']:
        table = pd.read_csv(ROOT / 'results' / name)
        decimals = 2 if name == 'table1_full_sample.csv' else 4
        for row in table.itertuples(index=False):
            source = comparisons[row.encoder]
            match = source.loc[(source.model == original_model(row)) &
                               (source.excluded_bottom_assets_pct == row.asset_exclusion_pct)]
            if len(match) != 1:
                raise AssertionError(f'{name}: missing or duplicate result for {row.encoder}/{original_model(row)}')
            original = match.iloc[0]
            for field in ['effect_roa_pp_per_T_pp', 'ci_low_roa_pp', 'ci_high_roa_pp']:
                if not np.isclose(round(float(original[field]), decimals), getattr(row, field), atol=1e-10, rtol=0):
                    raise AssertionError(f'{name}: {row.encoder}/{original_model(row)} differs in {field}')
            assert int(original.N) == row.reports and int(original.companies) == row.companies
        checked[name] = len(table)
    for name in ['figure2_treatment_diagnostics.csv', 'figure2_treatment_diagnostics_unrestricted.csv']:
        table = pd.read_csv(ROOT / 'results' / name)
        for row in table.itertuples(index=False):
            source = probes[row.encoder]
            for field, probe in [('raw_h_r2', 'T_from_H'), ('adjustment_z_r2', 'T_from_Z')]:
                exclusion = getattr(row, 'asset_exclusion_pct', 0)
                match = source.loc[(source.probe == probe) & (source.excluded_bottom_assets_pct == exclusion)]
                assert len(match) == 1, (name, row.encoder, probe)
                value = float(match.iloc[0].R2_oof)
                if exclusion == 5:
                    value = round(value, 6)
                assert np.isclose(value, getattr(row, field), atol=1e-10, rtol=0), (name, row.encoder, probe)
        checked[name] = len(table)
    source = pd.read_csv(processed / 'geni_semisynthetic_llama/0bb6c425603e03fcdf94/simulation_summary.csv')
    source['method'] = source.method.str.replace('GENI-', 'Adjustment-', regex=False)
    package = pd.read_csv(ROOT / 'results/simulation_summary.csv')
    pd.testing.assert_frame_equal(source, package, check_exact=False, rtol=1e-10, atol=1e-12)
    checked['simulation_summary.csv'] = len(package)
    return {'status': 'passed', 'scope': 'comparison of original saved aggregate outputs; no neural retraining', 'checked_rows': checked}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--processed-root', required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.processed_root), indent=2))
