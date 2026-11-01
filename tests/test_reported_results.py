from pathlib import Path
import unittest
import json
import pandas as pd
import numpy as np

ROOT=Path(__file__).resolve().parents[1]

class ReportedResultTests(unittest.TestCase):
    def test_main_table_and_sensitivity_provenance(self):
        data=pd.read_csv(ROOT/'results/table1_asset_restricted.csv')
        self.assertEqual(len(data),24)
        self.assertTrue(data.reports.eq(53527).all())
        self.assertTrue(data.companies.eq(7679).all())
        self.assertTrue(data.asset_exclusion_pct.eq(5).all())
        self.assertFalse(data.duplicated(['encoder','specification','learner']).any())
        self.assertEqual(data.groupby('encoder').size().tolist(),[8,8,8])
        self.assertTrue((data.ci_low_roa_pp<=data.effect_roa_pp_per_T_pp).all())
        self.assertTrue((data.effect_roa_pp_per_T_pp<=data.ci_high_roa_pp).all())
        adj=data.loc[data.specification.eq('Adjustment Z')]
        self.assertEqual(len(adj),6)
        self.assertTrue(adj.ci_low_roa_pp.gt(0).all())
        self.assertEqual(float(data.loc[data.encoder.eq('OpenAI')&data.specification.eq('Raw_H')&data.learner.eq('RF'),'ci_low_roa_pp'].iloc[0]),.0002)
        for _,g in data.loc[data.specification.eq('W_only')].groupby('learner'):
            self.assertEqual(g.effect_roa_pp_per_T_pp.nunique(),1)
        sens=pd.read_csv(ROOT/'results/asset_sensitivity_adjustment.csv')
        self.assertEqual(len(sens),18)
        self.assertEqual(set(sens.asset_exclusion_pct),{0,1,5})
        low=sens.loc[sens.asset_exclusion_pct.isin([0,1])]
        self.assertTrue(low.ci_low_roa_pp.lt(0).all())
        self.assertTrue(low.ci_high_roa_pp.gt(0).all())
        keys=['encoder','specification','learner']
        a=adj.set_index(keys).sort_index()
        b=sens.loc[sens.asset_exclusion_pct.eq(5)].set_index(keys).sort_index()
        np.testing.assert_allclose(a[['effect_roa_pp_per_T_pp','ci_low_roa_pp','ci_high_roa_pp']],b[['effect_roa_pp_per_T_pp','ci_low_roa_pp','ci_high_roa_pp']])
        old=pd.read_csv(ROOT/'results/table1_full_sample.csv')
        self.assertEqual(len(old),24)
        self.assertTrue(old.asset_exclusion_pct.eq(0).all())
        self.assertTrue(old.reports.eq(56345).all())

    def test_figure2_uses_main_population_and_correct_probes(self):
        data=pd.read_csv(ROOT/'results/figure2_treatment_diagnostics.csv')
        self.assertEqual(data.encoder.tolist(),['MiniLM','Llama','OpenAI'])
        self.assertTrue(data.asset_exclusion_pct.eq(5).all())
        self.assertTrue(data.reports.eq(53527).all())
        np.testing.assert_allclose(data.raw_h_r2,[.454216,.546029,.553073])
        np.testing.assert_allclose(data.adjustment_z_r2,[.191111,.196419,.171278])

    def test_notebook_defaults_and_manifest(self):
        import hashlib,ast,re
        manifest=json.loads((ROOT/'docs/PACKAGE_MANIFEST.json').read_text())
        for rec in manifest['notebooks']:
            p=ROOT/rec['artifact'];nb=json.loads(p.read_text())
            self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),rec['sha256'])
            for c in nb['cells']:
                if c['cell_type']=='code':ast.parse(c['source']);self.assertFalse(c.get('outputs'))
            if p.name.startswith('06'):
                source='\n'.join(c['source'] for c in nb['cells'] if c['cell_type']=='code')
                self.assertIn('SENSITIVITY_PCTS=[5]',source)
                normalized=re.sub(r'^CODE_DIGEST\s*=.*$',"CODE_DIGEST='<normalized>'",source,flags=re.M)
                self.assertEqual(hashlib.sha256(normalized.encode()).hexdigest(),rec['code_identity'])

    def test_all_simulation_scenarios_and_methods_retained(self):
        data=pd.read_csv(ROOT/'results/simulation_summary.csv')
        self.assertEqual(len(data),40)
        self.assertTrue(data.replications.eq(50).all())
        self.assertTrue(data.true_tau.eq(1).all())
        self.assertEqual(data.groupby('scenario').size().tolist(),[10,10,10,10])
        self.assertTrue(data.coverage_95.between(0,1).all())
        self.assertFalse(data.duplicated(['scenario','method','true_tau']).any())

if __name__=='__main__':unittest.main()
