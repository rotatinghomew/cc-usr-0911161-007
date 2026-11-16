from __future__ import annotations

import unittest
from policy_impact.measures.policy_contract import DomainRecord
from policy_impact.analysis.counterfactual import adjusted_effect, equity_summary, observed_gain, persistence


class BiasAdjustmentTests(unittest.TestCase):
    def record(self, key, language="a", outcome=75):
        return DomainRecord(key, {"policy_code": key, "jurisdiction_level": "g5", "measure_type": "math", "covered_entities": 100,
            "implementation_intensity": 1200, "baseline_risk": 60, "post_risk": outcome, "missing_rate": .05,
            "enforcement_support": .4, "digital_capacity": .9, "affected_group": language, "consultation_coverage": .95})

    def test_adjustment_shrinks_observed_magnitude(self):
        record = self.record("a")
        self.assertLess(abs(adjusted_effect(record)["adjusted"]), abs(observed_gain(record)))

    def test_equity_and_persistence(self):
        rows = [self.record("a", "x", 80), self.record("b", "y", 65)]
        self.assertGreater(equity_summary(rows)["gap"], 0.0)
        self.assertTrue(0.0 <= persistence(rows)["stability"] <= 1.0)
