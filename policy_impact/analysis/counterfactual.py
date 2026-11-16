from __future__ import annotations

import statistics
from collections import defaultdict
from typing import Any, Iterable

from policy_impact.measures.policy_contract import DomainRecord, bounded, finite_number, normalized_text

CONFIDENCE_THRESHOLD = 0.5

IMPROVED = "improved"
WORSENED = "worsened"
UNCHANGED = "unchanged"


def _payload_number(payload, key: str) -> float:
    """Read a numeric payload field, tolerating non-numeric text.

    Numeric strings are parsed; anything unusable contributes zero rather
    than crashing scoring for otherwise valid records.
    """
    value = payload.get(key, 0.0)
    if isinstance(value, bool):
        return float(value)
    if isinstance(value, (int, float)):
        return finite_number(value)
    text = normalized_text(value)
    if not text:
        return 0.0
    try:
        return finite_number(text)
    except (TypeError, ValueError):
        return 0.0


def risk_change_payload(payload) -> float:
    """Signed risk reduction from a raw payload (positive = risk fell)."""
    baseline = _payload_number(payload, "baseline_risk")
    outcome = _payload_number(payload, "post_risk")
    scale = max(1.0, abs(baseline), abs(outcome))
    return (baseline - outcome) / scale


def risk_change(record: DomainRecord) -> float:
    """Signed risk reduction: positive when post_risk is below baseline_risk.

    This is the single business direction used by the monitoring signal, the
    effect model, group summaries and decisions. A positive value always means
    improvement; a negative value always means deterioration.
    """
    return risk_change_payload(record.payload)


def observed_gain(record: DomainRecord) -> float:
    """Observed effect, signed as a benefit (positive = risk fell)."""
    return risk_change(record)


def reliability_payload(payload) -> float:
    """How much a recorded effect can be trusted, in [0, 1].

    Reliability only scales the magnitude of the effect and widens its
    uncertainty band; it never changes the sign of a risk movement.
    """
    missing = bounded(_payload_number(payload, "missing_rate"))
    consent = bounded(_payload_number(payload, "consultation_coverage"))
    digital_capacity = bounded(_payload_number(payload, "digital_capacity"))
    usage = bounded(_payload_number(payload, "implementation_intensity") / 6000.0)
    return bounded((1.0 - missing) * 0.35 + consent * 0.25 + digital_capacity * 0.20 + usage * 0.20)


def reliability_weight(record: DomainRecord) -> float:
    return reliability_payload(record.payload)


def _direction(value: float) -> str:
    if value > 0.0:
        return IMPROVED
    if value < 0.0:
        return WORSENED
    return UNCHANGED


def classify_effect(adjusted: float, reliability: float, lower: float, upper: float) -> dict[str, Any]:
    """Classify an adjusted effect without claiming certainty for weak evidence.

    A movement is only ``confirmed`` when the reliability threshold is met and
    the whole uncertainty band lies on the same side of zero. Otherwise the
    direction is reported as uncertain; in particular a weak-evidence risk
    reduction is never labelled a confirmed improvement.
    """
    direction = _direction(adjusted)
    band_supports_direction = (direction == IMPROVED and lower > 0.0) or (
        direction == WORSENED and upper < 0.0)
    confirmed = direction != UNCHANGED and reliability >= CONFIDENCE_THRESHOLD and band_supports_direction
    if direction == IMPROVED:
        verdict = "confirmed_improvement" if confirmed else "uncertain_improvement"
    elif direction == WORSENED:
        verdict = "confirmed_worsening" if confirmed else "uncertain_worsening"
    else:
        verdict = "unchanged"
    return {"direction": direction, "confirmed": confirmed, "uncertain": direction != UNCHANGED and not confirmed,
            "verdict": verdict, "weak_evidence": reliability < CONFIDENCE_THRESHOLD}


def effect_payload(payload) -> dict[str, Any]:
    """Full effect evaluation for a raw payload (shared by signal and model)."""
    gain = risk_change_payload(payload)
    reliability = reliability_payload(payload)
    shrinkage = 0.35 + reliability * 0.65
    adjusted = gain * shrinkage
    margin = (1.0 - reliability) * 0.12
    lower = adjusted - margin
    upper = adjusted + margin
    return {"observed": gain, "improvement": gain, "risk_delta":
            _payload_number(payload, "post_risk") - _payload_number(payload, "baseline_risk"),
            "reliability": reliability, "adjusted": adjusted, "lower": lower, "upper": upper,
            **classify_effect(adjusted, reliability, lower, upper)}


def adjusted_effect(record: DomainRecord) -> dict[str, Any]:
    return effect_payload(record.payload)


def equity_summary(records: Iterable[DomainRecord]) -> dict[str, Any]:
    groups: dict[str, list[float]] = defaultdict(list)
    group_directions: dict[str, list[str]] = defaultdict(list)
    for record in records:
        key = normalized_text(record.payload.get("affected_group", "unknown"))
        effect = adjusted_effect(record)
        groups[key].append(effect["adjusted"])
        group_directions[key].append(effect["direction"])
    means = {key: statistics.fmean(values) for key, values in groups.items()}
    gap = max(means.values()) - min(means.values()) if means else 0.0
    return {"group_count": float(len(means)), "gap": gap, "fairness": bounded(1.0 - abs(gap)),
            "group_effects": means, "group_directions": dict(group_directions),
            "best_group": max(means, key=means.get) if means else "", "worst_group": min(means, key=means.get) if means else "",
            "improved_groups": float(sum(value > 0.0 for value in means.values())),
            "worsened_groups": float(sum(value < 0.0 for value in means.values()))}


def persistence(records: Iterable[DomainRecord]) -> dict[str, Any]:
    rows = sorted(records, key=lambda row: normalized_text(row.payload.get("policy_code", row.record_id)))
    effects = [adjusted_effect(row)["adjusted"] for row in rows]
    if not effects:
        return {"mean": 0.0, "dispersion": 0.0, "stability": 0.0, "direction": UNCHANGED}
    dispersion = statistics.pstdev(effects) if len(effects) > 1 else 0.0
    mean = statistics.fmean(effects)
    return {"mean": mean, "dispersion": dispersion, "stability": bounded(1.0 - dispersion),
            "direction": _direction(mean)}


def derive_context(record: DomainRecord, repository: Any) -> dict[str, Any]:
    rows = repository.list_records() or [record]
    effect = adjusted_effect(record)
    equity = equity_summary(rows)
    stable = persistence(rows)
    return {"learning_gain_weight": 0.8 + bounded(effect["adjusted"] + 0.5) * 0.4,
            "attrition_bias_weight": 1.2 - effect["reliability"] * 0.4,
            "equity_gap_weight": 0.8 + abs(equity["gap"]) * 0.7,
            "effect_persistence_weight": 0.6 + stable["stability"] * 0.5,
            "scale_readiness_weight": 0.6 + equity["fairness"] * stable["stability"] * 0.6,
            "effect_direction": effect["direction"],
            "effect_verdict": effect["verdict"],
            "effect_confirmed": effect["confirmed"],
            "effect_reliability": effect["reliability"]}

