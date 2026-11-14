import json
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
import unittest

from test_pack import p


class ReportingFixtureTests(unittest.TestCase):
    def setUp(self):
        self.inventory = p.load(p.ROOT / 'packages/reporting.json')
        self.cases = self.inventory['openai_review']['test_cases']
        self.docs = (p.ROOT / 'docs/review-cases.md').read_text(encoding='utf-8')

    def test_fixed_totals_and_comparison(self):
        a = tuple(map(Decimal, ('4', '11', '496.80', '621.00')))
        b = tuple(map(Decimal, ('5', '21', '963.20', '1204.00')))
        total = tuple(map(Decimal, ('9', '32', '1460.00', '1825.00')))
        self.assertEqual(tuple(x + y for x, y in zip(a, b)), total)
        percentages = tuple(((y - x) / x * 100).quantize(Decimal('.01'), rounding=ROUND_HALF_UP) for x, y in zip(a, b))
        self.assertEqual(percentages, tuple(map(Decimal, ('25.00', '90.91', '93.88', '93.88'))))
        text = self.cases['positive'][1]['expected_behavior']
        for expected in ('(9, 32, 1460.00, 1825.00)', '(4, 11, 496.80, 621.00)', '(5, 21, 963.20, 1204.00)', '25%', '90.91%', '93.88%', 'group_by []'):
            self.assertIn(expected, text)

    def test_recurring_rows_and_chronological_totals(self):
        rows = [('5', '16', '836.80', '1046.00'), ('1', '4', '294.40', '368.00'), ('1', '4', '96.00', '120.00')]
        self.assertEqual(tuple(sum(Decimal(row[i]) for row in rows) for i in range(4)), tuple(map(Decimal, ('7', '24', '1227.20', '1534.00'))))
        recurring = self.cases['positive'][3]['expected_behavior']
        for key, row in zip(('4/9', '1/14', '4/10'), rows):
            expected = key + ' => (' + ', '.join(row) + ')'
            self.assertIn(expected, recurring)
            self.assertIn(expected, self.docs)
        for case in self.cases['positive'][2:]:
            self.assertIn('(7, 24, 1227.20, 1534.00)', case['expected_behavior'])
        chronological = self.cases['positive'][4]['expected_behavior']
        self.assertIn('4, 7 and 5 nonempty rows', chronological)
        self.assertIn('exact subhour rows are not specified', chronological)
        for start in ('2026-10-01T07:00:00Z', '2026-10-01T08:00:00Z', '2026-10-08T07:00:00Z', '2026-10-12T12:00:00Z'):
            self.assertIn(start, chronological)
            self.assertIn(start, self.docs)

    def test_windows_currency_scope_and_tools(self):
        for case in self.cases['positive'][1:]:
            for value in ('2026-09-30T22:00:00Z', '2026-10-31T23:00:00Z', 'Europe/Copenhagen', 'DKK', 'all_accessible'):
                self.assertIn(value, case['prompt'])
            self.assertEqual(case['tools_triggered'], 'piranya.deployments.list, piranya.reporting.get_capabilities, piranya.reporting.run_report')
        aggregate = self.cases['positive'][1]['expected_behavior']
        for boundary in ('2026-10-07T22:00:00Z', '2026-10-14T22:00:00Z'):
            self.assertIn(boundary, aggregate)
            self.assertIn(boundary, self.docs)
        start = datetime.fromisoformat('2026-09-30T22:00:00+00:00')
        end = datetime.fromisoformat('2026-10-31T23:00:00+00:00')
        self.assertGreater(end, start)
        serialized = json.dumps(self.cases)
        for stale in ('2026-09-14', 'Review Sandbox', 'group_by [product]'):
            self.assertNotIn(stale, serialized)
        for case in self.cases['positive'] + self.cases['negative']:
            self.assertIn('synthetic reviewer installation', case['prompt'])

    def test_negative_gates_and_evidence_limits(self):
        case = self.cases['negative'][1]
        self.assertIn('10-minute', case['prompt'])
        self.assertNotIn('run_report', case['tools_triggered'])
        for value in ('do not call run_report', 'rebucket', 'ask permission', 'sole accessible department'):
            self.assertIn(value, case['expected_behavior'])
        for value in ('November', 'cancelled', 'not separately', 'OWNER-REPORTED', 'tool trace', 'all site-management cases are **NOT RUN**'):
            self.assertIn(value, self.docs)
        self.assertIn('without requesting order-editing access', self.cases['negative'][0]['expected_behavior'])
        self.assertIn('exports have no implemented delivery contract', self.cases['negative'][2]['expected_behavior'])
        self.assertNotIn('demo_recording_url', self.inventory['openai_review'])


if __name__ == '__main__':
    unittest.main()
