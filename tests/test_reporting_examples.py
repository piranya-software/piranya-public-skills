import importlib.util
import json
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
SPEC = importlib.util.spec_from_file_location('distribute', ROOT / 'tools/distribute.py')
assert SPEC is not None and SPEC.loader is not None
distribute = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(distribute)


class ReportingExamplesTests(unittest.TestCase):
    def test_time_requests_use_reviewed_selectors_and_grain(self):
        source = (ROOT / 'skills/piranya-sales-reporting/references/scenarios.md').read_text(encoding='utf-8')
        examples = [json.loads(block) for block in re.findall(r'```json\n(.*?)\n```', source, re.S)]
        self.assertEqual(len(examples), 2)
        recurring, chronological = examples
        for request in examples:
            self.assertEqual(request['timestamp_field'], 'expected_fulfillment_time')
            self.assertEqual(request['time_zone'], 'Europe/Copenhagen')
            self.assertEqual(request['measures'], ['order_count'])
            self.assertLess(request['from'], request['to'])
            self.assertNotIn('compare_to', request)
            self.assertNotIn('cursor', request)
        self.assertEqual(recurring['group_by'], ['day_of_week', 'hour_of_day'])
        self.assertNotIn('time_bucket', recurring)
        self.assertNotIn('time_bucket_size', recurring)
        self.assertEqual([key['field'] for key in recurring['sort']], recurring['group_by'])
        self.assertEqual(chronological['group_by'], ['time'])
        self.assertEqual((chronological['time_bucket'], chronological['time_bucket_size']), ('minute', 15))
        self.assertEqual(chronological['sort'], [{'field': 'period_start_at', 'direction': 'asc'}])

    def test_reporting_reference_bytes_reach_both_provider_archives(self):
        outputs = distribute.expected(ROOT)
        for provider in ('claude', 'openai'):
            files = distribute.pack.inspect(outputs[f'dist/reporting-{provider}.zip'])
            for path in (ROOT / 'skills/piranya-sales-reporting').rglob('*.md'):
                relative = path.relative_to(ROOT).as_posix()
                self.assertEqual(files[relative], path.read_bytes().replace(b'\r\n', b'\n'))


if __name__ == '__main__':
    unittest.main()
