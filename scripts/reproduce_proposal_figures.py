"""Recreate Figures 1–3 from the frozen proposal inputs, without retraining."""
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
for name in ['plot_figure1.py','plot_figure2.py','plot_figure3.py']:
    subprocess.run([sys.executable,str(ROOT/'scripts'/name)],cwd=ROOT,check=True)
print('Proposal figures saved to outputs/figures. Model estimation was not rerun.')
