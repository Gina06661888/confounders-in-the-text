"""Reproduce the aggregate treatment-predictability figure; no training required."""
from pathlib import Path
from io import BytesIO
import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["svg.fonttype"] = "none"  # Keep labels editable and searchable.

ROOT = Path(__file__).resolve().parents[1]

def main():
    with (ROOT / "results/figure2_treatment_diagnostics.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    labels = [r["encoder"] for r in rows]
    raw = np.array([float(r["raw_h_r2"]) for r in rows])
    adjusted = np.array([float(r["adjustment_z_r2"]) for r in rows])
    if not np.isfinite(np.r_[raw, adjusted]).all():
        raise ValueError("Diagnostics must be finite.")
    plt.rcParams.update({"font.size": 11, "pdf.fonttype": 42, "axes.spines.top": False, "axes.spines.right": False})
    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.arange(len(rows)); width = 0.32
    for values, offset, label, color in [(raw, -width/2, "Raw embedding (H)", "#8798AA"), (adjusted, width/2, "Adjustment Z", "#167D9A")]:
        bars = ax.bar(x+offset, values, width, label=label, color=color)
        ax.bar_label(bars, labels=[f"{v:.3f}" for v in values], padding=5)
    ax.set_xticks(x, labels)
    ax.set_ylabel("Out-of-fold treatment prediction R²")
    ax.set_ylim(0, 0.65)
    ax.set_title("Treatment predictability from raw embeddings and adjustment representations", pad=16)
    ax.legend(frameon=False)
    ax.set_axisbelow(True); ax.grid(axis="y", alpha=0.18)
    fig.text(0.5, 0.025, "Company-disjoint cross-fitting; 56,345 reports from 8,094 firms.\nReduced predictability alone does not establish more accurate causal estimates.", ha="center", va="bottom", fontsize=9, color="#555555")
    fig.tight_layout(rect=(0, 0.12, 1, 1))
    target = ROOT / "outputs/figures"; target.mkdir(parents=True, exist_ok=True)
    for extension in ("png", "pdf", "svg"):
        buffer = BytesIO()
        fig.savefig(buffer, format=extension, dpi=300, bbox_inches="tight", facecolor="white")
        path = target / f"Figure2_Treatment_Predictability.{extension}"
        path.write_bytes(buffer.getvalue()); print(f"Saved: {path}")
    plt.close(fig)

if __name__ == "__main__":
    main()
