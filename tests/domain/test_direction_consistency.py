from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from policy_impact.measures.policy_contract import DomainRecord
from policy_impact.analysis.counterfactual import (
    WORSENED, adjusted_effect, equity_summary, observed_gain, persistence, risk_change,
)
from policy_impact.analysis.effect_model import compare, portfolio, record_score
from policy_impact.impact_signal.policy_signal import peer_distribution, policy_signal
from policy_impact.adoption.adoption_gates import decide
from policy_impact.policy_lab import run


FIXTURE = Path(__file__).resolve().parents[2] / "fixtures" / "acceptance.json"


def make(record_id: str, baseline: float, post: float, group: str = "group-a",
         missing: float = 0.1, consultation: float = 0.8, capacity: float = 0.8,
         enforcement: float = 0.5, intensity: float = 120.0) -> DomainRecord:
    return DomainRecord(record_id, {
        "policy_code": "policy", "jurisdiction_level": "national", "measure_type": "audit",
        "covered_entities": 100, "implementation_intensity": intensity,
        "baseline_risk": baseline, "post_risk": post, "missing_rate": missing,
        "enforcement_support": enforcement, "digital_capacity": capacity,
        "affected_group": group, "consultation_coverage": consultation})


class DirectionConsistencyTests(unittest.TestCase):
    """Risk reduction is one business direction everywhere: lower post_risk is improvement."""

    def test_signal_and_effect_agree_on_improvement(self):
        record = make("improved", 60.0, 45.0)
        signal = policy_signal(record.payload)
        effect = adjusted_effect(record)
        self.assertEqual(signal.evidence["direction"], "improved")
        self.assertEqual(effect["direction"], "improved")
        self.assertGreater(risk_change(record), 0.0)
        # The signal's raw improvement and the effect's observed benefit share sign.
        self.assertGreater(signal.evidence["improvement"], 0.0)
        self.assertGreater(observed_gain(record), 0.0)
        self.assertGreater(effect["adjusted"], 0.0)

    def test_signal_and_effect_agree_on_deterioration(self):
        record = make("worsened", 60.0, 75.0)
        signal = policy_signal(record.payload)
        effect = adjusted_effect(record)
        self.assertEqual(signal.evidence["direction"], "worsened")
        self.assertEqual(effect["direction"], "worsened")
        self.assertLess(risk_change(record), 0.0)
        self.assertLess(observed_gain(record), 0.0)
        self.assertLess(effect["adjusted"], 0.0)

    def test_more_relief_always_ranks_as_better(self):
        mild = make("mild", 60.0, 58.0)
        strong = make("strong", 60.0, 30.0)
        self.assertGreater(risk_change(strong), risk_change(mild))
        self.assertGreater(strong and record_score(strong)["score"], record_score(mild)["score"])
        ranked = [row["record_id"] for row in portfolio([mild, strong])["rows"]]
        self.assertEqual(ranked[0], "strong")

    def test_pairwise_comparison_prefers_lower_risk(self):
        better = make("better", 60.0, 45.0)
        worse = make("worse", 60.0, 75.0)
        self.assertEqual(compare(worse, better)["winner"], "better")
        self.assertEqual(compare(better, worse)["winner"], "better")
        self.assertGreater(compare(worse, better)["effect"]["delta"], 0.0)


class WeakEvidenceBoundaryTests(unittest.TestCase):
    """Weak evidence must never be presented as a certain improvement."""

    def weak_improvement(self) -> DomainRecord:
        return make("weak", 60.0, 45.0, missing=0.85, consultation=0.2, capacity=0.2, intensity=10.0)

    def test_weak_improvement_is_not_confirmed(self):
        record = self.weak_improvement()
        signal = policy_signal(record.payload)
        effect = adjusted_effect(record)
        self.assertEqual(signal.evidence["direction"], "improved")
        self.assertEqual(effect["direction"], "improved")
        self.assertFalse(signal.evidence["confirmed"])
        self.assertFalse(effect["confirmed"])
        self.assertEqual(effect["verdict"], "uncertain_improvement")
        self.assertEqual(signal.evidence["claim"], "uncertain_improvement")
        self.assertTrue(effect["weak_evidence"])
        self.assertNotEqual(signal.severity, "info")

    def test_weak_improvement_cannot_be_approved(self):
        decision = decide(self.weak_improvement())
        self.assertNotEqual(decision.outcome, "approve")
        self.assertFalse(any("confirmed_improvement" in reason for reason in decision.reasons))

    def test_weak_improvement_stays_unapproved_even_with_strong_scores(self):
        # Force the numeric scores that would otherwise approve, then confirm
        # the weak-evidence boundary still prevents an approval.
        permissive = {"approve_threshold": 0.0, "review_threshold": 0.0}
        decision = decide(self.weak_improvement(), permissive)
        self.assertNotEqual(decision.outcome, "approve")
        self.assertIn("effect=uncertain_improvement", decision.reasons)

    def test_confirmed_deterioration_blocks_approval(self):
        record = make("worse", 60.0, 75.0)
        self.assertEqual(adjusted_effect(record)["verdict"], "confirmed_worsening")
        self.assertEqual(policy_signal(record.payload).severity, "critical")
        self.assertEqual(decide(record).outcome, "hold")

    def test_uncertain_deterioration_is_never_reported_as_improvement(self):
        record = make("weak-worse", 60.0, 75.0, missing=0.85, consultation=0.2, capacity=0.2, intensity=10.0)
        signal = policy_signal(record.payload)
        self.assertEqual(signal.evidence["direction"], "worsened")
        self.assertIn("worsening", signal.evidence["claim"])
        self.assertNotIn("improvement", signal.evidence["claim"])
        self.assertEqual(decide(record).outcome, "hold")


class GroupConsistencyTests(unittest.TestCase):
    def test_group_summary_keeps_signal_direction(self):
        records = [make("a", 60.0, 45.0, group="x"), make("b", 60.0, 45.0, group="x"),
                   make("c", 60.0, 75.0, group="y")]
        equity = equity_summary(records)
        self.assertGreater(equity["group_effects"]["x"], 0.0)
        self.assertLess(equity["group_effects"]["y"], 0.0)
        self.assertEqual(equity["group_directions"]["x"], ["improved", "improved"])
        self.assertEqual(equity["group_directions"]["y"], ["worsened"])
        self.assertEqual(equity["best_group"], "x")
        self.assertEqual(equity["worst_group"], "y")

        peers = peer_distribution(records)
        self.assertGreater(peers["group_improvements"]["x"], 0.0)
        self.assertLess(peers["group_improvements"]["y"], 0.0)
        self.assertEqual(peers["improved_groups"], 1)
        self.assertEqual(peers["worsened_groups"], 1)

    def test_persistence_direction_matches_mean_effect(self):
        records = [make("a", 60.0, 45.0), make("b", 60.0, 50.0)]
        summary = persistence(records)
        self.assertEqual(summary["direction"], "improved")
        self.assertGreater(summary["mean"], 0.0)
        records = [make("a", 60.0, 75.0), make("b", 60.0, 70.0)]
        self.assertEqual(persistence(records)["direction"], WORSENED)


class BriefingConsistencyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.output = self.root / "output"

    def test_summary_and_records_csv_share_one_direction(self):
        run(FIXTURE, self.root / "state.sqlite3", self.output)
        summary = json.loads((self.output / "summary.json").read_text(encoding="utf-8"))
        with (self.output / "records.csv").open(encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        verdicts = [row["verdict"] for row in rows]
        self.assertEqual(summary["risk_directions"]["improved"], sum(row["direction"] == "improved" for row in rows))
        self.assertEqual(summary["risk_directions"]["worsened"], sum(row["direction"] == "worsened" for row in rows))
        self.assertEqual(summary["confirmed_improvements"],
                         sum(verdict == "confirmed_improvement" for verdict in verdicts))
        # A direction and its verdict can never point in opposite directions.
        for row in rows:
            if row["direction"] == "improved":
                self.assertIn("improvement", row["verdict"])
            elif row["direction"] == "worsened":
                self.assertIn("worsening", row["verdict"])
            else:
                self.assertEqual(row["verdict"], "unchanged")
            if row["direction"] == "worsened":
                self.assertEqual(row["outcome"], "hold")
        self.assertEqual(set(summary["effect_verdicts"]),
                         {verdict for verdict in verdicts})

    def test_uncertain_improvement_is_not_counted_as_confirmed(self):
        fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        fixture["records"] = [{
            "record_id": "policy_measure-weak",
            "payload": {"policy_code": "p", "jurisdiction_level": "n", "measure_type": "a",
                        "covered_entities": 100, "implementation_intensity": 10,
                        "baseline_risk": 60, "post_risk": 45, "missing_rate": 0.85,
                        "enforcement_support": 0.2, "digital_capacity": 0.2,
                        "affected_group": "g", "consultation_coverage": 0.2},
            "state": "registered", "source": "unit-test"}]
        path = self.root / "weak.json"
        path.write_text(json.dumps(fixture), encoding="utf-8")
        run(path, self.root / "weak.sqlite3", self.output)
        summary = json.loads((self.output / "summary.json").read_text(encoding="utf-8"))
        self.assertEqual(summary["confirmed_improvements"], 0)
        self.assertEqual(summary["effect_verdicts"], {"uncertain_improvement": 1})
        self.assertEqual(summary["uncertain_records"], ["policy_measure-weak"])


if __name__ == "__main__":
    unittest.main()
