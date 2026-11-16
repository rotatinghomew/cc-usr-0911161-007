from __future__ import annotations
import unittest
from policy_impact.impact_signal.policy_signal import policy_signal, peer_distribution
class Record:
    def __init__(self, payload): self.payload = payload
class SignalTests(unittest.TestCase):
    def setUp(self): self.payload = {'policy_code': 'policy-a', 'jurisdiction_level': 'national', 'measure_type': 'audit', 'covered_entities': 5000, 'implementation_intensity': 70, 'baseline_risk': 80, 'post_risk': 45, 'missing_rate': 0.08, 'enforcement_support': 0.78, 'digital_capacity': 0.7, 'affected_group': 'small-enterprise', 'consultation_coverage': 0.72}
    def test_signal_is_bounded_and_explainable(self):
        signal = policy_signal(self.payload)
        self.assertGreaterEqual(signal.score, 0.0)
        self.assertLessEqual(signal.score, 1.0)
        self.assertIn(signal.severity, {'info', 'warning', 'critical'})
        self.assertTrue({'improvement', 'risk_delta', 'evidence_weight'}.issubset(signal.evidence))
    def test_peer_distribution_uses_business_group(self):
        other = dict(self.payload); other['affected_group'] = 'group-b'
        result = peer_distribution([Record(self.payload), Record(other)])
        self.assertEqual(result['count'], 2)
        self.assertIn('group_effects', result)
    def test_material_business_change_is_observable(self):
        changed = dict(self.payload); changed['post_risk'] = 90
        self.assertNotEqual(policy_signal(changed).score, policy_signal(self.payload).score)
    def test_business_variant_1(self):
        changed = dict(self.payload)
        changed['measure_type'] = self.payload['measure_type']
        signal = policy_signal(changed)
        self.assertGreaterEqual(signal.score, 0.0)
        self.assertLessEqual(signal.score, 1.0)

    def test_business_variant_2(self):
        changed = dict(self.payload)
        changed['covered_entities'] = self.payload['covered_entities']
        signal = policy_signal(changed)
        self.assertGreaterEqual(signal.score, 0.0)
        self.assertLessEqual(signal.score, 1.0)

    def test_business_variant_3(self):
        changed = dict(self.payload)
        changed['implementation_intensity'] = self.payload['implementation_intensity']
        signal = policy_signal(changed)
        self.assertGreaterEqual(signal.score, 0.0)
        self.assertLessEqual(signal.score, 1.0)

    def test_business_variant_4(self):
        changed = dict(self.payload)
        changed['baseline_risk'] = self.payload['baseline_risk']
        signal = policy_signal(changed)
        self.assertGreaterEqual(signal.score, 0.0)
        self.assertLessEqual(signal.score, 1.0)

if __name__ == '__main__': unittest.main()
