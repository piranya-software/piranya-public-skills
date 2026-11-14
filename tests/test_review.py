import json
from pathlib import Path
import tempfile
import unittest

from test_pack import p


class ReviewTests(unittest.TestCase):
    def snapshot(self):
        return p.snapshot(self.root, self.inventory)

    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        skill = self.root / 'skills/demo/SKILL.md'
        skill.parent.mkdir(parents=True)
        skill.write_text('Synthetic review fixture\n')
        self.inventory: dict = {'name': 'demo', 'version': '0.1.0', 'description': 'Synthetic',
                          'skills': {'demo': ['SKILL.md']}, 'connectors': {}}
        self.inventory['connectors'] = {'demo': 'https://mcp.piranya.io/mcp/reporting'}
        self.case: dict = {'description': 'Synthetic check', 'prompt': 'Inspect synthetic data.',
                     'tools_triggered': 'piranya.reporting.get_capabilities',
                     'expected_behavior': 'Return supported definitions without writes.'}
        self.review: dict = {'test_cases': {'positive': [self.case], 'negative': [self.case]}}
        self.inventory['openai_review'] = self.review
        self.inventory['openai_publication'] = {'release_notes': 'Synthetic metadata release.'}

    def test_review_nested_and_provider_isolated(self):
        lock = self.snapshot()
        for provider, path in [('openai', 'plugin.json'), ('claude', '.claude-plugin/plugin.json')]:
            raw = p.build(self.root, self.inventory, lock, provider)
            self.assertEqual(raw, p.build(self.root, self.inventory, lock, provider))
            files = p.inspect(raw)
            manifest = json.loads(files[path])
            if provider == 'openai':
                extension = manifest['extensions']['com.openai']
                self.assertEqual(extension['review'], self.review)
                self.assertEqual(extension['publication'], self.inventory['openai_publication'])
                self.assertNotIn('review', extension.get('interface', {}))
                self.assertEqual(json.loads(files['mcp.json'])['$schema'], p.MCP_ID)
                p.validate(manifest, 'plugin.schema.json')
            else:
                self.assertNotIn('extensions', manifest)
                self.assertNotIn('review', manifest)
            proof = json.loads(files['package-inputs.json'])
            self.assertEqual(proof['files'][path], p.digest(files[path]))
        self.review['test_cases']['positive'][0]['prompt'] = 'Changed'
        with self.assertRaises(ValueError):
            p.build(self.root, self.inventory, lock, 'openai')

    def test_review_fail_closed(self):
        invalid = [None, [], {'invented': True}, {'test_credentials': 'synthetic'},
                   {'reviewer_instructions': 'synthetic'}, {'test_cases': []},
                   {'test_cases': {'unknown': []}}, {'test_cases': {'positive': [self.case] * 6}},
                   {'test_cases': {'negative': [self.case] * 4}},
                   {'test_cases': {'positive': [{}]}},
                   {'test_cases': {'positive': [{**self.case, 'prompt': ' '}]}},
                   {'test_cases': {'positive': [{**self.case, 'description': 'x' * 4001}]}},
                   {'test_cases': {'positive': [{**self.case, 'credentials': 'synthetic'}]}},
                   {'demo_recording_url': 'https://user:pass@public.org/video'},
                   {'demo_recording_url': 'https://public.org/?token=synthetic'}]
        for review in invalid:
            with self.subTest(review=review), self.assertRaises(Exception):
                p.inventory_check({**self.inventory, 'openai_review': review})
        for connectors in ({}, {'one': 'https://mcp.piranya.io/one', 'two': 'https://mcp.piranya.io/two'}):
            with self.assertRaises(ValueError):
                p.inventory_check({**self.inventory, 'connectors': connectors})
        with self.assertRaises(Exception):
            p.inventory_check({**self.inventory, 'openai_publication': {'reviewer_instructions': 'no'}})

    def test_review_optional_fields_and_interface_coexist(self):
        self.inventory['openai_interface'] = {'displayName': 'Synthetic'}
        self.review['demo_recording_url'] = 'https://public.org/synthetic-video'
        self.case['file_attachment_urls'] = ['https://public.org/synthetic.png']
        self.case['expected_output_url'] = 'https://public.org/synthetic-output'
        files = p.inspect(p.build(self.root, self.inventory, self.snapshot(), 'openai'))
        extension = json.loads(files['plugin.json'])['extensions']['com.openai']
        self.assertEqual(set(extension), {'interface', 'review', 'publication'})
        self.assertEqual(extension['review'], self.review)
        for field in ('description', 'prompt', 'tools_triggered', 'expected_behavior'):
            original = self.case[field]
            for invalid in ('', ' ', 3, 'x' * 4001, 'bad\u0000text'):
                self.case[field] = invalid
                with self.subTest(field=field, invalid=invalid), self.assertRaises(Exception):
                    p.inventory_check(self.inventory)
            self.case[field] = original
        for forbidden in ('test_credentials', 'reviewer_instructions'):
            for target in (self.review, self.review['test_cases'], self.case,
                           self.inventory['openai_publication']):
                target[forbidden] = 'synthetic'
                with self.assertRaises(Exception):
                    p.inventory_check(self.inventory)
                del target[forbidden]

    def test_partial_uploads_and_optional_negative_fields(self):
        for cases in ({}, {'positive': []}, {'negative': [{'description': 'Decline', 'prompt': 'Unsupported task'}]}):
            p.inventory_check({**self.inventory, 'openai_review': {'test_cases': cases}})

    def test_offerings_exact_review_inventory(self):
        for name in ('site-management', 'reporting'):
            inv = p.load(p.ROOT / 'packages' / (name + '.json'))
            p.inventory_check(inv)
            self.assertEqual(inv['version'], '0.2.1')
            cases = inv['openai_review']['test_cases']
            self.assertEqual(len(cases['positive']), 5)
            self.assertEqual(len(cases['negative']), 3)
            self.assertNotIn('demo_recording_url', inv['openai_review'])


if __name__ == '__main__':
    unittest.main()
