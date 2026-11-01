"""Draw the 5%-restricted treatment diagnostics from saved aggregate inputs."""
from pathlib import Path
from io import BytesIO
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]

def main():
    with (ROOT / 'results/figure2_treatment_diagnostics.csv').open(newline='', encoding='utf-8') as handle:
        rows = list(csv.DictReader(handle))
    if [r['encoder'] for r in rows] != ['MiniLM', 'Llama', 'OpenAI']:
        raise ValueError('Expected one row for each of the three encoders, in manuscript order.')
    for r in rows:
        if (int(r['reports']), int(r['companies']), int(r['asset_exclusion_pct'])) != (53527, 7679, 5):
            raise ValueError('Figure 2 must use the current 5% main sample.')
    raw = np.array([float(r['raw_h_r2']) for r in rows])
    adjusted = np.array([float(r['adjustment_z_r2']) for r in rows])
    if not np.isfinite(np.r_[raw, adjusted]).all():
        raise ValueError('Diagnostics must be finite.')
    rc = {'font.family':'DejaVu Sans', 'font.size':11, 'pdf.fonttype':42,
          'svg.fonttype':'none', 'axes.spines.top':False, 'axes.spines.right':False}
    with plt.rc_context(rc):
        fig, ax = plt.subplots(figsize=(8.5, 5.3))
        fig.subplots_adjust(left=.12, right=.98, bottom=.23, top=.77)
        x=np.arange(len(rows)); width=.32
        for values, offset, label, color in [
            (raw,-width/2,'Raw embedding (H)','#8798AA'),
            (adjusted,width/2,'Adjustment representation (Z)','#167D9A')]:
            bars=ax.bar(x+offset,values,width,label=label,color=color)
            ax.bar_label(bars,labels=[f'{v:.3f}' for v in values],padding=5)
        ax.set_xticks(x,[r['encoder'] for r in rows])
        ax.set_ylabel('Out-of-fold treatment prediction R²')
        ax.set_ylim(0,.65)
        ax.legend(loc='lower center',bbox_to_anchor=(.5,1.04),ncol=2,frameon=False,fontsize=10)
        ax.set_axisbelow(True);ax.grid(axis='y',alpha=.18)
        fig.text(.12,.95,'Treatment predictability from raw embeddings\nand adjustment representations',
                 ha='left',va='top',fontsize=13,fontweight='bold',linespacing=1.3)
        fig.text(.12,.10,'Company-disjoint cross-fitting; 53,527 reports from 7,679 firms.\nBottom 5% of current-asset observations excluded.\nReduced predictability alone does not establish more accurate causal estimates.',
                 ha='left',va='bottom',fontsize=9,color='#555555',linespacing=1.5)
        target=ROOT/'outputs/figures';target.mkdir(parents=True,exist_ok=True)
        for extension in ('png','pdf','svg'):
            buffer=BytesIO();fig.savefig(buffer,format=extension,dpi=300,bbox_inches='tight',facecolor='white')
            path=target/f'Figure2_Treatment_Predictability.{extension}'
            path.write_bytes(buffer.getvalue());print(f'Saved: {path}')
        plt.close(fig)

if __name__ == '__main__':
    main()
