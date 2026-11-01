"""Benchmark residual slope and nuisance helpers; no neural dependencies."""
import numpy as np
import pandas as pd
from scipy.stats import t as student_t
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
CPU_THREADS=1
CFG={"ridge_alpha":10.0,"rf_n_estimators":100,"rf_max_depth":8,"rf_min_samples_leaf":10,"rf_max_features":0.5}

def r2_np(actual, predicted):
    denom = np.sum((actual - np.mean(actual)) ** 2)
    return float(1 - np.sum((actual - predicted) ** 2) / denom) if denom > 1e-12 else np.nan

def make_learner(kind, seed):
    if kind == "Ridge":
        return make_pipeline(StandardScaler(), Ridge(alpha=CFG["ridge_alpha"], solver="svd"))
    if kind == "RF":
        return RandomForestRegressor(
            n_estimators=CFG["rf_n_estimators"], max_depth=CFG["rf_max_depth"],
            min_samples_leaf=CFG["rf_min_samples_leaf"],
            random_state=seed, n_jobs=CPU_THREADS, max_features=CFG["rf_max_features"],
        )
    raise ValueError(kind)

def nuisance_predictions(xtr, xte, ttr, ytr, learner, seed):
    treatment_model = make_learner(learner, seed)
    outcome_model = make_learner(learner, seed + 1000)
    treatment_model.fit(xtr, ttr)
    outcome_model.fit(xtr, ytr)
    return treatment_model.predict(xte), outcome_model.predict(xte)

def dml_summary(t, y, that, yhat, cluster_ids):
    u, v = t - that, y - yhat
    denom = float(np.mean(u ** 2))
    if denom < 1e-12:
        raise ValueError("Treatment residual variation is essentially zero.")
    theta = float(np.mean(u * v) / denom)
    influence = u * (v - theta * u) / denom
    sums = pd.DataFrame({"g": cluster_ids, "psi": influence}).groupby("g")["psi"].sum()
    n, G = len(t), len(sums)
    assert G > 1
    se = float(np.sqrt((G / (G - 1)) * np.sum(sums.to_numpy() ** 2) / n ** 2))
    critical = student_t.ppf(0.975, df=G - 1)
    p = float(2 * student_t.sf(abs(theta / se), df=G - 1)) if se > 0 else np.nan
    return {
        "N": n, "companies": G,
        "slope_roa_decimal_per_T_pp": theta,
        "effect_roa_pp_per_T_pp": 100 * theta,
        "se_roa_pp": 100 * se,
        "ci_low_roa_pp": 100 * (theta - critical * se),
        "ci_high_roa_pp": 100 * (theta + critical * se),
        "p_value_approx": p,
        "R2_T_oof": r2_np(t, that), "R2_Y_oof": r2_np(y, yhat),
        "t_resid_mse": denom,
        "residual_mse_to_T_variance": denom / float(np.var(t)),
        "low_abs_residual_share": float(np.mean(np.abs(u) < 0.05 * np.std(t))),
    }

