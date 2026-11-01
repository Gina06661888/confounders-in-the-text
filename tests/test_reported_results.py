from pathlib import Path
import unittest
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]

class ReportedResultTests(unittest.TestCase):
    def test_table_population_and_intervals(self):
        data=pd.read_csv(ROOT/'results/table1_full_sample.csv')
        self.assertEqual(len(data),24)
        self.assertTrue(data.reports.eq(56345).all())
        self.assertTrue(data.companies.eq(8094).all())
        self.assertTrue(data.asset_exclusion_pct.eq(0).all())
        self.assertTrue((data.ci_low_roa_pp<0).all())
        self.assertTrue((data.ci_high_roa_pp>0).all())
        self.assertEqual(data.groupby('encoder').size().tolist(),[8,8,8])

    def test_all_simulation_scenarios_and_methods_retained(self):
        data=pd.read_csv(ROOT/'results/simulation_summary.csv')
        self.assertEqual(len(data),40)
        self.assertTrue(data.replications.eq(50).all())
        self.assertTrue(data.true_tau.eq(1).all())
        self.assertEqual(data.groupby('scenario').size().tolist(),[10,10,10,10])
        self.assertTrue(data.coverage_95.between(0,1).all())
        self.assertFalse(data.duplicated(['scenario','method','true_tau']).any())

if __name__=='__main__':unittest.main()
