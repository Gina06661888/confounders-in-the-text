"""Validate the downloaded report-vector package; no training or API calls."""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import numpy as np

def sha256(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(8*1024*1024),b''):h.update(block)
    return h.hexdigest()

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,required=True,help='Downloaded embeddings folder')
    args=parser.parse_args();root=args.root.resolve()
    manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    index=root/'report_index.csv'
    if sha256(index)!=manifest['index_sha256']:raise ValueError('Index checksum mismatch')
    with index.open(newline='',encoding='utf-8-sig') as f:
        reader=csv.DictReader(f)
        if 'source_path' in reader.fieldnames:raise ValueError('Expected the anonymous index')
        rows=list(reader)
    n=len(rows)
    if n!=manifest['reports']:raise ValueError('Wrong report count')
    if len({r['doc_id'] for r in rows})!=n:raise ValueError('Duplicate document IDs')
    if sorted(int(r['embedding_row']) for r in rows)!=list(range(n)):raise ValueError('Invalid embedding rows')
    if {r['corpus_id'] for r in rows}!={manifest['corpus_id']}:raise ValueError('Corpus mismatch')
    for model,entry in manifest['models'].items():
        receipt_path=root/entry['snapshot'];receipt=json.loads(receipt_path.read_text())
        matrix=root/entry['matrix']
        if matrix.stat().st_size!=entry['matrix_size_bytes']:raise ValueError(f'{model}: wrong file size')
        if sha256(matrix)!=entry['matrix_sha256']:raise ValueError(f'{model}: matrix checksum mismatch')
        if (receipt_path.parent/receipt['report_index']).resolve()!=index:raise ValueError(f'{model}: wrong index path')
        if receipt['report_index_sha256']!=manifest['index_sha256']:raise ValueError(f'{model}: receipt index mismatch')
        if receipt['report_matrix_sha256']!=entry['matrix_sha256']:raise ValueError(f'{model}: receipt matrix mismatch')
        arr=np.load(matrix,mmap_mode='r',allow_pickle=False)
        if arr.shape!=(n,entry['dimension']) or arr.dtype!=np.float32:raise ValueError(f'{model}: wrong matrix shape or dtype')
        for start in range(0,n,4096):
            if not np.isfinite(arr[start:start+4096]).all():raise ValueError(f'{model}: nonfinite vectors')
        print(f"PASS {model}: {n:,} reports x {entry['dimension']} dimensions; SHA256 verified")
    print('Embedding package verified. Financial analysis inputs are separate and require authorized access.')

if __name__=='__main__':main()
