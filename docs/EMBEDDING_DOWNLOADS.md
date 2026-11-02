# Downloading the report embeddings

## Archive and current access status

[Report embedding archive](https://www.dropbox.com/scl/fo/q124t6ty6jc7hhv7yv5te/AGuSuXWJ6tzK4TIF-qTp-8U?rlkey=dvrrshgw5x286ei0rrw8ujnl9&dl=0)

The three matrices, anonymous report index and model receipts have been staged in this archive. **Public link access is not yet enabled.** The current link is view-only, permits downloads, and is restricted to people with existing access. It must not be described as a publicly accessible download until the owner changes the link audience in Dropbox and access is checked without an authorized session.

No company-level financial records, credentials, raw text archives, checkpoint databases or paragraph vector matrices are included.

## Contents

| Model | Matrix filename | Shape | File size in bytes |
|---|---|---|---:|
| MiniLM | `minilm/report_vectors_c3cd192fca42.npy` | 106,877 × 384 | 164,163,200 |
| Llama-based | `llama/report_vectors_af6b69086662.npy` | 106,877 × 512 | 218,884,224 |
| OpenAI | `openai/report_vectors_6d97282a499e.npy` | 106,877 × 512 | 218,884,224 |

The archive also contains `report_index.csv`, `manifest.json`, `README.txt`, and one `latest_snapshot.json` in each model folder. Report matrices are float32. Their corpus ID is `fa8fc124c14a1ca97e34`.

The report index describes the full accepted corpus. It is not the 53,527-report main analysis table. Use stable `doc_id` values to join to the authorized financial analysis sample. Never match records by assumed row order across independent exports.

## Anonymization

The index's personal `source_path` column was removed; document IDs, embedding rows, text counts and competition measures are unchanged. The shared anonymous index has its own checksum. Receipts point to `../report_index.csv` and contain the updated checksum. Personal `corpus_database` paths were removed. Numerical vector files remain unchanged.

The files in `data/embedding_metadata/` duplicate the small anonymous receipts and manifest for inspection. They do not include the matrices or index; use the complete external archive for validation and model inputs.

## Download and validate

1. Once link access is enabled, download the entire archive and extract it while preserving the `minilm`, `llama`, and `openai` subfolders.
2. Install NumPy in the environment used for validation.
3. From the repository root, run:

```bash
python scripts/verify_embedding_package.py --root "/path/to/downloaded/embeddings"
```

The staged matrices and anonymous index have passed these checks; the checksum record is in `data/embedding_metadata/VERIFICATION.json`. The script verifies matrix and index SHA256 checksums, report IDs, row indexes, corpus agreement, dimensions, dtype and finite values. It does not train models or call an embedding API.

## Configure research notebooks

In the ignored local file `configs/paths.local.json`, set `embedding_root` to the downloaded embeddings folder and provide explicit `embedding_snapshots` entries for each model. Use the absolute local paths to `minilm/latest_snapshot.json`, `llama/latest_snapshot.json`, and `openai/latest_snapshot.json`. The configuration loader resolves relative paths from the repository root, not automatically from the embedding folder.

The original automatic corpus-directory search is unnecessary when explicit snapshot paths are supplied.

## Separate financial inputs

Precomputed embeddings remove the need to repeat paragraph encoding. They do not replace the financial analysis table, its frozen dataset receipt, or the reference matrix currently expected by the research notebooks. Those inputs require authorized Compustat access. Upstream financial reconstruction remains under integration; the external embedding archive alone is not a complete input-to-paper replication package.

The semi-synthetic research notebook also uses real observed financial characteristics. It is distinct from the fully artificial CPU quick-start example.
