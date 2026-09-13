"""Regression checks for packaging failures the collection promises to catch."""
import json
from pathlib import Path
import tempfile
import unittest

from scripts.validate_skills import validate


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='kk-validator-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.skill = self.root / 'kk-example'
        (self.skill / 'evals').mkdir(parents=True)
        (self.root / 'evals').mkdir()
        (self.root / 'README.md').write_text('[Skill](kk-example/SKILL.md)\n')
        self.entry = self.skill / 'SKILL.md'
        self.entry.write_text('---\nname: kk-example\ndescription: Review an example.\n---\n\n# Example\n')
        self.cases = {'skill_name': 'kk-example', 'evals': [
            {'id': i, 'prompt': 'Review the example.', 'expected_output': 'Concrete findings.',
             'files': [], 'expectations': ['Reports the observed defect.']} for i in range(2)]}
        self.save_cases()
        self.routing = {'cases': [
            {'id': 0, 'prompt': 'Review this example.', 'expected_primary': 'kk-example', 'not_primary': []},
            {'id': 1, 'prompt': 'Say hello.', 'expected_primary': None, 'not_primary': ['kk-example']}]}
        # One-skill fixture: a positive case need not exclude a different skill.
        self.save_routing()

    def save_cases(self):
        (self.skill / 'evals/evals.json').write_text(json.dumps(self.cases))

    def save_routing(self):
        (self.root / 'evals/routing.json').write_text(json.dumps(self.routing))

    def errors(self):
        return '\n'.join(validate(self.root)[0])

    def test_valid_collection(self):
        self.assertEqual(validate(self.root), ([], 1, 2))

    def test_unprefixed_name_is_rejected(self):
        self.entry.write_text(self.entry.read_text().replace('name: kk-example', 'name: example'))
        self.assertIn('name must use the kk- prefix', self.errors())

    def test_missing_expectations_is_rejected(self):
        del self.cases['evals'][0]['expectations']
        self.save_cases()
        self.assertIn('grading expectation', self.errors())

    def test_empty_expectations_is_rejected(self):
        self.cases['evals'][0]['expectations'] = []
        self.save_cases()
        self.assertIn('grading expectation', self.errors())

    def test_missing_fixture_is_rejected(self):
        self.cases['evals'][0]['files'] = ['evals/files/missing.json']
        self.save_cases()
        self.assertIn('missing fixture', self.errors())

    def test_missing_backtick_resource_is_rejected(self):
        self.entry.write_text(self.entry.read_text() + '\nRead `references/missing.md`.\n')
        self.assertIn('missing bundled resource', self.errors())

    def test_broken_markdown_link_is_rejected(self):
        self.entry.write_text(self.entry.read_text() + '\nRead [details](references/missing.md).\n')
        self.assertIn('broken link', self.errors())

    def test_unknown_routing_skill_is_rejected(self):
        self.routing['cases'][0]['expected_primary'] = 'kk-missing'
        self.save_routing()
        self.assertIn('unknown primary skill', self.errors())

    def test_negative_routing_coverage_is_required(self):
        self.routing['cases'].pop()
        self.save_routing()
        self.assertIn('negative routing coverage', self.errors())


if __name__ == '__main__':
    unittest.main()
