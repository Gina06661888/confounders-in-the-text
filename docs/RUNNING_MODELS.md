# Running the research notebooks

## Inputs required locally

1. A frozen authorized analysis sample folder containing `dataset_snapshot.json`, its CSV table, and its aligned reference matrix. Preserve their original filenames and checksums; notebooks follow the receipt.
2. Completed report-level embedding exports for the same corpus, each with `latest_snapshot.json`, its matrix and index, and matching SHA256 checksums. The notebooks join by `doc_id` and stop on missing vectors or text-measure mismatch.

These inputs are not included in the repository. Their upstream construction programs will be integrated separately. Do not substitute different financial samples without recording a new snapshot.

## Setup

Use a separate Python 3.10+ environment for research training. Install the CPU/CUDA-appropriate PyTorch 2.7.1 build, then run:

```bash
python -m pip install -r environment/requirements-models.txt
```

The original runs used PyTorch 2.7.1+cu118, NumPy 2.1.0, pandas 2.2.3, SciPy 1.15.3, scikit-learn 1.6.1, and joblib 1.4.2. Packaging/display dependencies are supporting dependencies, not a verified recreation of the entire original environment.

Copy `configs/paths.example.json` to `configs/paths.local.json`. Set `analysis_data_dir` to the frozen sample folder and `embedding_root` to the existing export root. Relative paths resolve from the repository root. Optional exact snapshot paths can resolve ambiguous model exports. Keep `output_root` separate from original results.

Start Jupyter from the repository root:

```bash
python -m notebook
```

## Notebook selection

| Notebook | Purpose |
|---|---|
| 06a_Benchmarks_MiniLM | All eight specifications using MiniLM |
| 06b_Benchmarks_Llama | Same benchmarks using Llama |
| 06c_Benchmarks_OpenAI | Same benchmarks using already computed OpenAI vectors; no API calls |
| 07_SemiSynthetic_Llama | Four scenarios x 50 replications, using real local inputs |

Run each selected notebook top to bottom. Benchmarks default to the proposal's 5% current-asset restriction, SENSITIVITY_PCTS=[5]. Set SENSITIVITY_PCTS=[0,1,5] to rerun all completed sensitivity comparisons. The default change does not retrain models or verify agreement with saved aggregate results. These are long-running model refits. Avoid simultaneous writers to the same model/run directory. Completed checkpoints are reused; incomplete neural folds or rotations restart. Packaging produces new run identities and does not reuse the original private run hashes.

The additional MiniLM notebook uses the common snapshot-aligning implementation; the original unrestricted MiniLM run used its aligned reference matrix directly. Numerical agreement of the adapted pipeline with the published aggregates has not yet been verified end to end.

## No-data CPU example

```bash
python -m pip install -r requirements-demo.txt
python scripts/run_synthetic_demo.py
```

This generates entirely artificial observations and illustrates cross-fitting and residual estimation with observed vs oracle controls. It does not train the text encoder or validate adversarial adjustment and is not evidence for the paper's reported results.

Industry exploration is a future direction in the current proposal. Its separately preserved implementation is on the `development-industry-extension` branch.
