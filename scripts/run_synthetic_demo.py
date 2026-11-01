"""Fully synthetic CPU demonstration of cross-fitted residual estimation.
This verifies the estimator plumbing, not the learned text representation.
"""
from pathlib import Path
import sys, json
import numpy as np
from sklearn.model_selection import GroupKFold
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from residual_estimation import dml_summary, nuisance_predictions

def run_demo(output_dir=None):
    rng=np.random.default_rng(491)
    n=4000
    w=rng.normal(size=(n,3)); c=rng.normal(size=n)
    treatment=0.6*c+0.3*w[:,0]+rng.normal(size=n)
    outcome=1.0*treatment+c+0.3*w[:,0]+rng.normal(size=n)
    groups=np.repeat(np.arange(n//2),2)
    folds=list(GroupKFold(5).split(w,groups=groups))
    rows=[]
    for name,x in [('Observed_controls',w),('Oracle_observed_confounder',np.column_stack([w,c]))]:
        th=np.empty(n); yh=np.empty(n)
        for fold,(train,test) in enumerate(folds):
            assert set(groups[train]).isdisjoint(groups[test])
            th[test],yh[test]=nuisance_predictions(x[train],x[test],treatment[train],outcome[train],'Ridge',100+fold)
        result=dml_summary(treatment,outcome,th,yh,groups)
        rows.append({'specification':name,'true_slope':1.0,
          'estimated_slope':result['slope_roa_decimal_per_T_pp'],
          'ci_low':result['ci_low_roa_pp']/100,'ci_high':result['ci_high_roa_pp']/100})
    target=Path(output_dir) if output_dir else ROOT/'outputs'/'synthetic_demo'
    target.mkdir(parents=True,exist_ok=True)
    (target/'results.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
    print(json.dumps(rows,indent=2))
    print('Fully synthetic illustration; not empirical results and not an adversarial-method comparison.')
    return rows

if __name__=='__main__':
    run_demo()
