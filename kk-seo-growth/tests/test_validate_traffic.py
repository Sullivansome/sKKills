import csv
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/validate_traffic.py'
spec = importlib.util.spec_from_file_location('traffic_validator', SCRIPT)
traffic = importlib.util.module_from_spec(spec)
spec.loader.exec_module(traffic)


class TrafficTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for path in (ROOT / 'examples/traffic-pilot').glob('*.csv'):
            shutil.copy2(path, self.root / path.name)

    def edit(self, name, change):
        path = self.root / name
        with path.open(newline='') as f:
            reader = csv.DictReader(f)
            fields, rows = reader.fieldnames, list(reader)
        change(rows)
        with path.open('w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    def check(self):
        return traffic.validate(self.root/'observations.csv', self.root/'cohorts.csv', self.root/'experiments.csv')

    def test_worked_example_and_cli(self):
        result = self.check()
        self.assertTrue(result['valid'], result)
        self.assertEqual([40, 40], [r['relative_change_percent'] for r in result['comparisons']])
        self.assertEqual([1, 2], [r['page_count'] for r in result['comparisons']])
        cmd = [sys.executable, str(SCRIPT)]
        for flag, name in [('observations','observations.csv'),('cohorts','cohorts.csv'),('experiments','experiments.csv')]:
            cmd.extend(['--'+flag, str(self.root/name)])
        output = subprocess.run(cmd, capture_output=True, text=True, check=True)
        self.assertEqual(result, json.loads(output.stdout))

    def test_duplicate_observation_suppresses_all_calculations(self):
        self.edit('observations.csv', lambda r: r.append(dict(r[0])))
        result = self.check()
        self.assertFalse(result['valid'])
        self.assertEqual([], result['comparisons'])

    def test_missing_and_duplicate_membership(self):
        self.edit('cohorts.csv', lambda r: r.append(dict(r[0])))
        self.assertFalse(self.check()['valid'])
        self.edit('observations.csv', lambda r: r[0].update(cohort_id='unknown'))
        self.assertIn('missing cohort membership', ' '.join(self.check()['errors']))

    def test_mismatched_filters(self):
        self.edit('observations.csv', lambda r: r[1].update(country='GB'))
        self.assertFalse(self.check()['valid'])

    def test_cross_arm_filters_must_match(self):
        self.edit('observations.csv', lambda r: [x.update(country='GB') for x in r if x['arm']=='control'])
        self.assertIn('treatment/control measurement contexts differ', ' '.join(self.check()['errors']))

    def test_overlap_and_unequal_periods(self):
        self.edit('observations.csv', lambda r: r[1].update(period_start='2026-08-24'))
        errors = ' '.join(self.check()['errors'])
        self.assertIn('overlap', errors)
        self.assertIn('unequal', errors)

    def test_ambiguous_zero_rejected_and_missing_preserved(self):
        self.edit('observations.csv', lambda r: r[0].update(value='0'))
        self.assertIn('zero is unverified', ' '.join(self.check()['errors']))
        self.edit('observations.csv', lambda r: r[0].update(value='', data_status='missing', notes='raw zero may represent unavailable'))
        result = self.check()
        self.assertTrue(result['valid'], result)
        self.assertTrue(result['warnings'])
        self.assertEqual(['control'], [x['arm'] for x in result['comparisons']])

    def test_verified_zero_has_no_relative_lift(self):
        self.edit('observations.csv', lambda r: r[0].update(value='0', zero_evidence='observed', zero_evidence_ref='synthetic-source-confirmation'))
        result = self.check()
        self.assertTrue(result['valid'], result)
        self.assertIsNone(result['comparisons'][0]['relative_change_percent'])

    def test_partial_withheld(self):
        self.edit('observations.csv', lambda r: r[1].update(data_status='partial'))
        result = self.check()
        self.assertTrue(result['valid'], result)
        self.assertEqual(1, len(result['comparisons']))

    def test_unavailable_numeric_value_rejected(self):
        self.edit('observations.csv', lambda r: r[0].update(data_status='missing'))
        self.assertFalse(self.check()['valid'])

    def test_invalid_number_and_timestamp_rejected(self):
        self.edit('observations.csv', lambda r: r[0].update(value='NaN',extracted_at='2026-10-06T12:00:00'))
        self.assertFalse(self.check()['valid'])

    def test_new_page_false_baseline_rejected(self):
        self.edit('cohorts.csv', lambda r: r[0].update(first_published_at='2026-08-31'))
        self.assertIn('full pre-existing baseline', ' '.join(self.check()['errors']))

    def test_wrong_deployment_and_changed_fingerprint_rejected(self):
        self.edit('experiments.csv', lambda r: r[0].update(release_at='2026-10-02T08:00:00+08:00',skill_sha256='b'*64))
        errors = ' '.join(self.check()['errors'])
        self.assertIn('release date',errors)
        self.assertIn('mismatched skill_sha256',errors)


if __name__ == '__main__':
    unittest.main()
