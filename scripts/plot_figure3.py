from pathlib import Path
from io import BytesIO
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams["svg.fonttype"] = "none"  # Keep labels editable and searchable.
from matplotlib.lines import Line2D

# Defaults reproduce the frozen proposal summary without local financial inputs.
REPO_ROOT = Path(__file__).resolve().parents[1]
INPUT_CSV = REPO_ROOT / "results" / "simulation_summary.csv"
OUTPUT_DIR = REPO_ROOT / "outputs" / "figures"
TRUE_TAU = 1.0
SHOW_FIGURE = False
SEARCH_ROOT = REPO_ROOT / "results"

SCENARIOS = [
    "low_confounding", "medium_confounding", "high_confounding",
    "high_confounding_no_T_only",
]
SCENARIO_LABELS = ["Low", "Moderate", "High", "High without\nT-only signal"]
METHODS = [
    "W_only-Ridge", "W_only-RF", "NoAdv-Ridge", "NoAdv-RF", "Adjustment-Ridge", "Adjustment-RF",
]
COLORS = {"W_only": "#666666", "NoAdv": "#0072B2", "Adjustment": "#D55E00"}
STYLES = {"Ridge": ("-", "o"), "RF": ("--", "s")}


def select_input():
    if INPUT_CSV is not None:
        path = Path(INPUT_CSV)
        if not path.is_file():
            raise FileNotFoundError(f"Summary CSV not found: {path}")
        return path
    paths = list(SEARCH_ROOT.rglob("simulation_summary.csv")) if SEARCH_ROOT.is_dir() else []
    if not paths:
        raise FileNotFoundError(
            f"No simulation_summary.csv found under {SEARCH_ROOT}. Set INPUT_CSV to its exact path."
        )
    # Selection is by modification time only, never by model performance.
    path = max(paths, key=lambda p: (p.stat().st_mtime_ns, str(p)))
    if len(paths) > 1:
        print(f"Found {len(paths)} summaries; selecting the most recently modified file.")
        print("Set INPUT_CSV explicitly if this is not the intended simulation run.")
    return path


def load_plot_data(path):
    data = pd.read_csv(path)
    required = ["scenario", "true_tau", "method", "replications", "bias",
                "bias_mc_low", "bias_mc_high", "RMSE", "coverage_95"]
    missing = sorted(set(required) - set(data.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    data = data.loc[
        np.isclose(pd.to_numeric(data["true_tau"], errors="coerce"), TRUE_TAU)
        & data["scenario"].isin(SCENARIOS) & data["method"].isin(METHODS)
    ].copy()
    if data.duplicated(["scenario", "method"]).any():
        raise ValueError("Duplicate scenario/method rows; do not combine separate runs in this CSV.")
    expected = pd.MultiIndex.from_product([SCENARIOS, METHODS], names=["scenario", "method"])
    indexed = data.set_index(["scenario", "method"])
    absent = expected.difference(indexed.index)
    if len(absent):
        raise ValueError(f"Missing plotted specifications: {absent.tolist()}")
    data = indexed.reindex(expected).reset_index()
    numeric = required[3:]
    data[numeric] = data[numeric].apply(pd.to_numeric, errors="raise")
    if not np.isfinite(data[numeric].to_numpy()).all():
        raise ValueError("Nonfinite values in the plotted summary.")
    if not data["coverage_95"].between(0, 1).all() or (data["RMSE"] < 0).any():
        raise ValueError("Coverage must be a proportion in [0,1]; RMSE must be nonnegative.")
    if ((data["bias_mc_low"] > data["bias"]) | (data["bias_mc_high"] < data["bias"])).any():
        raise ValueError("Invalid Monte Carlo intervals for bias.")
    if data["replications"].nunique() != 1 or data["replications"].iloc[0] < 2:
        raise ValueError("All plotted specifications must have the same number of replications (at least 2).")
    return data


def plot_figure3(data, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    replications = int(data["replications"].iloc[0])
    rc = {
        "font.family": "DejaVu Sans", "font.size": 10,
        "axes.titlesize": 12, "axes.labelsize": 10,
        "axes.spines.top": False, "axes.spines.right": False,
        "pdf.fonttype": 42, "ps.fonttype": 42,
    }
    with plt.rc_context(rc):
        fig, axes = plt.subplots(1, 3, figsize=(15, 5.4))
        fig.subplots_adjust(left=0.065, right=0.985, top=0.82, bottom=0.29, wspace=0.29)
        x = np.arange(len(SCENARIOS), dtype=float)
        # Small offsets prevent nearly identical NoAdv/Adjustment markers from hiding one another.
        # The underlying values are never changed or rounded before plotting.
        offsets = dict(zip(METHODS, np.linspace(-0.15, 0.15, len(METHODS))))
        handles = []
        for method in METHODS:
            view, learner = method.rsplit("-", 1)
            line, marker = STYLES[learner]
            color = COLORS[view]
            part = data.loc[data["method"].eq(method)].set_index("scenario").reindex(SCENARIOS)
            xx = x + offsets[method]
            kwargs = dict(color=color, linestyle=line, marker=marker, markersize=5,
                          linewidth=1.5, markerfacecolor="white" if learner == "RF" else color,
                          markeredgewidth=1.1, zorder=3)
            bias = part["bias"].to_numpy()
            error = np.vstack([bias - part["bias_mc_low"].to_numpy(),
                               part["bias_mc_high"].to_numpy() - bias])
            axes[0].errorbar(xx, bias, yerr=error, capsize=2.5, elinewidth=1, **kwargs)
            axes[1].plot(xx, part["RMSE"].to_numpy(), **kwargs)
            axes[2].plot(xx, 100 * part["coverage_95"].to_numpy(), **kwargs)
            name = ({"W_only": "W-only", "Adjustment": "Adjustment Z"}.get(view, view)) + " " + learner
            handles.append(Line2D([0], [0], label=name, **{k: v for k, v in kwargs.items() if k != "zorder"}))

        axes[0].axhline(0, color="#222222", linestyle=":", linewidth=1.2, zorder=1)
        axes[1].set_ylim(bottom=0)
        axes[2].axhline(95, color="#222222", linestyle=":", linewidth=1.2, zorder=1)
        axes[2].text(3.22, 95, "95%", ha="right", va="bottom", fontsize=9)
        axes[2].set_ylim(-4, 104)
        axes[2].set_yticks([0, 25, 50, 75, 100])
        for ax, title, ylabel in zip(
            axes,
            ["A. Bias", "B. Root mean squared error", "C. 95% interval coverage"],
            ["Mean estimate minus true effect", "RMSE", "Coverage (%)"],
        ):
            ax.set_title(title, loc="left", fontweight="bold", pad=12)
            ax.set_ylabel(ylabel)
            ax.set_xticks(x)
            ax.set_xticklabels(SCENARIO_LABELS)
            ax.set_xlim(-0.35, 3.35)
            ax.set_xlabel("Simulation scenario", labelpad=8)
            ax.grid(axis="y", color="#E5E5E5", linewidth=0.7, zorder=0)
            ax.set_axisbelow(True)
        fig.suptitle("Figure 3. Semi-synthetic simulation: recovery of a known effect",
                     x=0.065, ha="left", fontsize=15, fontweight="bold", y=0.98)
        fig.text(0.065, 0.895,
                 f"True effect = {TRUE_TAU:g}  |  {replications} replications per scenario  |  Six non-oracle specifications",
                 fontsize=10, color="#555555")
        fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.52, 0.115),
                   ncol=6, frameon=False, handlelength=2.8, columnspacing=1.5)
        fig.text(0.065, 0.055,
                 "Notes: Bias whiskers show 95% Monte Carlo intervals for the mean error, not individual effect-estimate intervals.",
                 fontsize=9, color="#555555")
        fig.text(0.065, 0.020,
                 "Markers are slightly offset horizontally for visibility. Raw-embedding and oracle benchmarks are omitted from this main figure.",
                 fontsize=9, color="#555555")
        for extension in ["png", "pdf", "svg"]:
            path = output_dir / f"Figure3_Simulation.{extension}"
            buffer = BytesIO()
            fig.savefig(buffer, format=extension, dpi=300, bbox_inches="tight", facecolor="white")
            path.write_bytes(buffer.getvalue())
            print("Saved:", path)
        if SHOW_FIGURE:
            plt.show()
        plt.close(fig)


input_path = select_input()
print("Input:", input_path)
plot_data = load_plot_data(input_path)
out_dir = Path(OUTPUT_DIR) if OUTPUT_DIR is not None else input_path.parent / "figure3"
plot_figure3(plot_data, out_dir)
plot_data.to_csv(out_dir / "Figure3_plotted_values.csv", index=False)
print("No simulation was rerun; the figure reads the existing summary only.")
