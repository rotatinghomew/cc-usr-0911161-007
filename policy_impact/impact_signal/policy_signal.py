from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

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
    improvement = 0.0 if baseline <= 0 else clamp((baseline-after)/baseline)
    evidence_weight = (1-missing) * (0.5+consultation*0.5)
    score = clamp(improvement*0.38 + enforcement*0.16 + capacity*0.12 + consultation*0.12 + intensity*0.1 + entities*0.04 + evidence_weight*0.08)
    severity = 'critical' if after > baseline and evidence_weight > 0.5 else 'warning' if missing > 0.4 or consultation < 0.3 else 'info'
    return DomainSignal('policy_signal', score, severity, {'improvement': improvement, 'evidence_weight': evidence_weight, 'risk_delta': after-baseline, 'consultation': consultation})

def peer_distribution(records: Iterable[Any], group_field: str = 'affected_group') -> dict[str, Any]:
    groups = {}
    for record in records:
        payload = getattr(record, 'payload', record); groups.setdefault(str(payload.get(group_field,'unknown')),[]).append(policy_signal(payload).score)
    means = {k:sum(v)/len(v) for k,v in groups.items()}; disparity = max(means.values())-min(means.values()) if means else 0.0
    return {'group_effects': means, 'disparity': disparity, 'count': sum(len(v) for v in groups.values())}

def augment_context(record: Any, repository: Any) -> dict[str, Any]:
    signal = policy_signal(record.payload); peers = peer_distribution(repository.list_records())
    return {'domain_signal': signal.score, 'domain_severity': signal.severity, 'policy_disparity': peers['disparity'], 'peer_count': peers['count']}
