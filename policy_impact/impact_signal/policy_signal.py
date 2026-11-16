from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from policy_impact.analysis.counterfactual import (
    IMPROVED, UNCHANGED, WORSENED, effect_payload,
)

__all__ = ['DomainSignal', 'IMPROVED', 'UNCHANGED', 'WORSENED', 'augment_context',
           'peer_distribution', 'policy_signal']

@dataclass(frozen=True)
class DomainSignal:
    code: str
    score: float
    severity: str
    evidence: dict[str, Any]

def number(payload: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    try:
        value = float(payload.get(key, default))
    except (TypeError, ValueError):
        return default
    return default if value != value or value in (float('inf'), float('-inf')) else value

def ratio(payload: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    value = number(payload, key, default)
    if value > 1.0:
        value /= 100.0
    return max(0.0, min(1.0, value))

def clamp(value: float) -> float:
    return max(0.0, min(1.0, value))

def policy_signal(payload: Mapping[str, Any]) -> DomainSignal:
    baseline = number(payload, 'baseline_risk')
    after = number(payload, 'post_risk')
    missing = ratio(payload, 'missing_rate')
    enforcement = ratio(payload, 'enforcement_support')
    capacity = ratio(payload, 'digital_capacity')
    consultation = ratio(payload, 'consultation_coverage')
    intensity = min(1.0, number(payload, 'implementation_intensity') / 100.0)
    entities = min(1.0, number(payload, 'covered_entities') / 10000.0)
    improvement = 0.0 if baseline <= 0 else max(-1.0, min(1.0, (baseline-after)/baseline))
    evidence_weight = (1-missing) * (0.5+consultation*0.5)
    score = clamp(max(0.0, improvement)*0.38 + enforcement*0.16 + capacity*0.12 + consultation*0.12 + intensity*0.1 + entities*0.04 + evidence_weight*0.08)
    delta = after - baseline
    # Share the effect model's direction and reliability so monitoring and
    # analysis can never disagree about whether a movement is confirmed.
    claim = effect_payload({'baseline_risk': baseline, 'post_risk': after,
                            'missing_rate': number(payload, 'missing_rate'),
                            'consultation_coverage': number(payload, 'consultation_coverage'),
                            'digital_capacity': number(payload, 'digital_capacity'),
                            'implementation_intensity': number(payload, 'implementation_intensity')})
    direction = claim['direction']
    confirmed = claim['confirmed']
    if direction == WORSENED:
        severity = 'critical' if confirmed else 'warning'
    elif direction == IMPROVED:
        # Weak evidence must never read as a definite improvement.
        severity = 'warning' if (not confirmed or missing > 0.4 or consultation < 0.3) else 'info'
    else:
        severity = 'warning' if missing > 0.4 or consultation < 0.3 else 'info'
    return DomainSignal('policy_signal', score, severity, {
        'improvement': improvement, 'signed_improvement': claim['improvement'],
        'evidence_weight': evidence_weight, 'risk_delta': delta,
        'consultation': consultation, 'direction': claim['direction'], 'confirmed': confirmed,
        'reliability': claim['reliability'], 'claim': claim['verdict']})


def peer_distribution(records: Iterable[Any], group_field: str = 'affected_group') -> dict[str, Any]:
    scores: dict[str, list[float]] = {}
    improvements: dict[str, list[float]] = {}
    directions: dict[str, list[str]] = {}
    for record in records:
        payload = getattr(record, 'payload', record)
        signal = policy_signal(payload)
        key = str(payload.get(group_field, 'unknown'))
        scores.setdefault(key, []).append(signal.score)
        improvements.setdefault(key, []).append(float(signal.evidence['signed_improvement']))
        directions.setdefault(key, []).append(str(signal.evidence['direction']))
    effects = {k: sum(v)/len(v) for k, v in scores.items()}
    group_improvements = {k: sum(v)/len(v) for k, v in improvements.items()}
    disparity = max(effects.values())-min(effects.values()) if effects else 0.0
    improvement_disparity = (max(group_improvements.values())-min(group_improvements.values())
                             if group_improvements else 0.0)
    return {'group_effects': effects, 'group_improvements': group_improvements,
            'group_directions': directions, 'disparity': disparity,
            'improvement_disparity': improvement_disparity,
            'improved_groups': sum(value > 0.0 for value in group_improvements.values()),
            'worsened_groups': sum(value < 0.0 for value in group_improvements.values()),
            'best_group': max(effects, key=effects.get) if effects else '',
            'worst_group': min(effects, key=effects.get) if effects else '',
            'count': sum(len(v) for v in scores.values())}

def augment_context(record: Any, repository: Any) -> dict[str, Any]:
    signal = policy_signal(record.payload); peers = peer_distribution(repository.list_records())
    return {'domain_signal': signal.score, 'domain_severity': signal.severity,
            'policy_disparity': peers['disparity'], 'peer_count': peers['count'],
            'signal_improvement': signal.evidence['signed_improvement'],
            'signal_direction': signal.evidence['direction'],
            'signal_confirmed': signal.evidence['confirmed'],
            'signal_reliability': signal.evidence['reliability'],
            'signal_claim': signal.evidence['claim']}

