from __future__ import annotations

import math
from typing import Any, Callable, Mapping

from policy_impact.measures.policy_contract import DomainRecord, RuleResult, bounded, finite_number, normalized_text

RuleFunction = Callable[[DomainRecord, Mapping[str, Any]], RuleResult]

def _number(record: DomainRecord, field: str) -> float:
    value = record.payload.get(field)
    if isinstance(value, bool):
        return 1.0 if value else 0.0
    if isinstance(value, (int, float)):
        return finite_number(value)
    text = normalized_text(value)
    if not text:
        return 0.0
    try:
        return finite_number(text)
    except ValueError:
        return float(sum(ord(ch) for ch in text) % 101)

def _context_number(context: Mapping[str, Any], key: str, default: float) -> float:
    try:
        return finite_number(context.get(key, default))
    except ValueError:
        return default

def _result(code: str, value: float, threshold: float, higher_is_better: bool, message: str, evidence: dict[str, Any]) -> RuleResult:
    distance = (value - threshold) if higher_is_better else (threshold - value)
    passed = distance >= 0
    scale = max(1.0, abs(threshold))
    score = bounded(0.5 + distance / (2.0 * scale))
    severity = 'info' if passed else ('critical' if score < 0.2 else 'error')
    return RuleResult(code, passed, score, severity, message, evidence)

def check_policy_code_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'policy_code')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_policy_code_presence_threshold', 10.333)
    return _result('check_policy_code_presence', adjusted, threshold, True, 'validates policy_code presence',
                   {'field': 'policy_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_policy_code_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'policy_code')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_policy_code_range_threshold', 12.667)
    return _result('check_policy_code_range', adjusted, threshold, True, 'validates policy_code range',
                   {'field': 'policy_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_policy_code_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'policy_code')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_policy_code_stability_threshold', 15.0)
    return _result('check_policy_code_stability', adjusted, threshold, False, 'validates policy_code stability',
                   {'field': 'policy_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_policy_code_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'policy_code')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_policy_code_freshness_threshold', 17.333)
    return _result('check_policy_code_freshness', adjusted, threshold, True, 'validates policy_code freshness',
                   {'field': 'policy_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_policy_code_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'policy_code')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_policy_code_coverage_threshold', 19.667)
    return _result('check_policy_code_coverage', adjusted, threshold, True, 'validates policy_code coverage',
                   {'field': 'policy_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_policy_code_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'policy_code')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_policy_code_consistency_threshold', 22.0)
    return _result('check_policy_code_consistency', adjusted, threshold, False, 'validates policy_code consistency',
                   {'field': 'policy_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_policy_code_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'policy_code')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_policy_code_risk_threshold', 24.333)
    return _result('check_policy_code_risk', adjusted, threshold, True, 'validates policy_code risk',
                   {'field': 'policy_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_policy_code_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'policy_code')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_policy_code_confidence_threshold', 26.667)
    return _result('check_policy_code_confidence', adjusted, threshold, True, 'validates policy_code confidence',
                   {'field': 'policy_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_policy_code_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'policy_code')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_policy_code_dependency_threshold', 29.0)
    return _result('check_policy_code_dependency', adjusted, threshold, False, 'validates policy_code dependency',
                   {'field': 'policy_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_policy_code_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'policy_code')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_policy_code_readiness_threshold', 31.333)
    return _result('check_policy_code_readiness', adjusted, threshold, True, 'validates policy_code readiness',
                   {'field': 'policy_code', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_jurisdiction_level_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'jurisdiction_level')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_jurisdiction_level_presence_threshold', 9.333)
    return _result('check_jurisdiction_level_presence', adjusted, threshold, True, 'validates jurisdiction_level presence',
                   {'field': 'jurisdiction_level', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_jurisdiction_level_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'jurisdiction_level')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_jurisdiction_level_range_threshold', 11.667)
    return _result('check_jurisdiction_level_range', adjusted, threshold, False, 'validates jurisdiction_level range',
                   {'field': 'jurisdiction_level', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_jurisdiction_level_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'jurisdiction_level')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_jurisdiction_level_stability_threshold', 14.0)
    return _result('check_jurisdiction_level_stability', adjusted, threshold, True, 'validates jurisdiction_level stability',
                   {'field': 'jurisdiction_level', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_jurisdiction_level_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'jurisdiction_level')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_jurisdiction_level_freshness_threshold', 16.333)
    return _result('check_jurisdiction_level_freshness', adjusted, threshold, True, 'validates jurisdiction_level freshness',
                   {'field': 'jurisdiction_level', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_jurisdiction_level_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'jurisdiction_level')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_jurisdiction_level_coverage_threshold', 18.667)
    return _result('check_jurisdiction_level_coverage', adjusted, threshold, False, 'validates jurisdiction_level coverage',
                   {'field': 'jurisdiction_level', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_jurisdiction_level_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'jurisdiction_level')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_jurisdiction_level_consistency_threshold', 21.0)
    return _result('check_jurisdiction_level_consistency', adjusted, threshold, True, 'validates jurisdiction_level consistency',
                   {'field': 'jurisdiction_level', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_jurisdiction_level_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'jurisdiction_level')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_jurisdiction_level_risk_threshold', 23.333)
    return _result('check_jurisdiction_level_risk', adjusted, threshold, True, 'validates jurisdiction_level risk',
                   {'field': 'jurisdiction_level', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_jurisdiction_level_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'jurisdiction_level')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_jurisdiction_level_confidence_threshold', 25.667)
    return _result('check_jurisdiction_level_confidence', adjusted, threshold, False, 'validates jurisdiction_level confidence',
                   {'field': 'jurisdiction_level', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_jurisdiction_level_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'jurisdiction_level')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_jurisdiction_level_dependency_threshold', 28.0)
    return _result('check_jurisdiction_level_dependency', adjusted, threshold, True, 'validates jurisdiction_level dependency',
                   {'field': 'jurisdiction_level', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_jurisdiction_level_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'jurisdiction_level')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_jurisdiction_level_readiness_threshold', 30.333)
    return _result('check_jurisdiction_level_readiness', adjusted, threshold, True, 'validates jurisdiction_level readiness',
                   {'field': 'jurisdiction_level', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_measure_type_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'measure_type')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_measure_type_presence_threshold', 8.333)
    return _result('check_measure_type_presence', adjusted, threshold, False, 'validates measure_type presence',
                   {'field': 'measure_type', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_measure_type_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'measure_type')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_measure_type_range_threshold', 10.667)
    return _result('check_measure_type_range', adjusted, threshold, True, 'validates measure_type range',
                   {'field': 'measure_type', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_measure_type_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'measure_type')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_measure_type_stability_threshold', 13.0)
    return _result('check_measure_type_stability', adjusted, threshold, True, 'validates measure_type stability',
                   {'field': 'measure_type', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_measure_type_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'measure_type')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_measure_type_freshness_threshold', 15.333)
    return _result('check_measure_type_freshness', adjusted, threshold, False, 'validates measure_type freshness',
                   {'field': 'measure_type', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_measure_type_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'measure_type')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_measure_type_coverage_threshold', 17.667)
    return _result('check_measure_type_coverage', adjusted, threshold, True, 'validates measure_type coverage',
                   {'field': 'measure_type', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_measure_type_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'measure_type')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_measure_type_consistency_threshold', 20.0)
    return _result('check_measure_type_consistency', adjusted, threshold, True, 'validates measure_type consistency',
                   {'field': 'measure_type', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_measure_type_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'measure_type')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_measure_type_risk_threshold', 22.333)
    return _result('check_measure_type_risk', adjusted, threshold, False, 'validates measure_type risk',
                   {'field': 'measure_type', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_measure_type_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'measure_type')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_measure_type_confidence_threshold', 24.667)
    return _result('check_measure_type_confidence', adjusted, threshold, True, 'validates measure_type confidence',
                   {'field': 'measure_type', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_measure_type_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'measure_type')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_measure_type_dependency_threshold', 27.0)
    return _result('check_measure_type_dependency', adjusted, threshold, True, 'validates measure_type dependency',
                   {'field': 'measure_type', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_measure_type_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'measure_type')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_measure_type_readiness_threshold', 29.333)
    return _result('check_measure_type_readiness', adjusted, threshold, False, 'validates measure_type readiness',
                   {'field': 'measure_type', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_covered_entities_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'covered_entities')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_covered_entities_presence_threshold', 31.667)
    return _result('check_covered_entities_presence', adjusted, threshold, True, 'validates covered_entities presence',
                   {'field': 'covered_entities', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_covered_entities_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'covered_entities')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_covered_entities_range_threshold', 9.667)
    return _result('check_covered_entities_range', adjusted, threshold, True, 'validates covered_entities range',
                   {'field': 'covered_entities', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_covered_entities_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'covered_entities')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_covered_entities_stability_threshold', 12.0)
    return _result('check_covered_entities_stability', adjusted, threshold, False, 'validates covered_entities stability',
                   {'field': 'covered_entities', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_covered_entities_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'covered_entities')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_covered_entities_freshness_threshold', 14.333)
    return _result('check_covered_entities_freshness', adjusted, threshold, True, 'validates covered_entities freshness',
                   {'field': 'covered_entities', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_covered_entities_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'covered_entities')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_covered_entities_coverage_threshold', 16.667)
    return _result('check_covered_entities_coverage', adjusted, threshold, True, 'validates covered_entities coverage',
                   {'field': 'covered_entities', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_covered_entities_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'covered_entities')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_covered_entities_consistency_threshold', 19.0)
    return _result('check_covered_entities_consistency', adjusted, threshold, False, 'validates covered_entities consistency',
                   {'field': 'covered_entities', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_covered_entities_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'covered_entities')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_covered_entities_risk_threshold', 21.333)
    return _result('check_covered_entities_risk', adjusted, threshold, True, 'validates covered_entities risk',
                   {'field': 'covered_entities', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_covered_entities_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'covered_entities')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_covered_entities_confidence_threshold', 23.667)
    return _result('check_covered_entities_confidence', adjusted, threshold, True, 'validates covered_entities confidence',
                   {'field': 'covered_entities', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_covered_entities_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'covered_entities')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_covered_entities_dependency_threshold', 26.0)
    return _result('check_covered_entities_dependency', adjusted, threshold, False, 'validates covered_entities dependency',
                   {'field': 'covered_entities', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_covered_entities_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'covered_entities')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_covered_entities_readiness_threshold', 28.333)
    return _result('check_covered_entities_readiness', adjusted, threshold, True, 'validates covered_entities readiness',
                   {'field': 'covered_entities', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_implementation_intensity_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'implementation_intensity')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_implementation_intensity_presence_threshold', 30.667)
    return _result('check_implementation_intensity_presence', adjusted, threshold, True, 'validates implementation_intensity presence',
                   {'field': 'implementation_intensity', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_implementation_intensity_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'implementation_intensity')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_implementation_intensity_range_threshold', 8.667)
    return _result('check_implementation_intensity_range', adjusted, threshold, False, 'validates implementation_intensity range',
                   {'field': 'implementation_intensity', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_implementation_intensity_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'implementation_intensity')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_implementation_intensity_stability_threshold', 11.0)
    return _result('check_implementation_intensity_stability', adjusted, threshold, True, 'validates implementation_intensity stability',
                   {'field': 'implementation_intensity', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_implementation_intensity_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'implementation_intensity')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_implementation_intensity_freshness_threshold', 13.333)
    return _result('check_implementation_intensity_freshness', adjusted, threshold, True, 'validates implementation_intensity freshness',
                   {'field': 'implementation_intensity', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_implementation_intensity_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'implementation_intensity')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_implementation_intensity_coverage_threshold', 15.667)
    return _result('check_implementation_intensity_coverage', adjusted, threshold, False, 'validates implementation_intensity coverage',
                   {'field': 'implementation_intensity', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_implementation_intensity_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'implementation_intensity')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_implementation_intensity_consistency_threshold', 18.0)
    return _result('check_implementation_intensity_consistency', adjusted, threshold, True, 'validates implementation_intensity consistency',
                   {'field': 'implementation_intensity', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_implementation_intensity_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'implementation_intensity')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_implementation_intensity_risk_threshold', 20.333)
    return _result('check_implementation_intensity_risk', adjusted, threshold, True, 'validates implementation_intensity risk',
                   {'field': 'implementation_intensity', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_implementation_intensity_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'implementation_intensity')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_implementation_intensity_confidence_threshold', 22.667)
    return _result('check_implementation_intensity_confidence', adjusted, threshold, False, 'validates implementation_intensity confidence',
                   {'field': 'implementation_intensity', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_implementation_intensity_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'implementation_intensity')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_implementation_intensity_dependency_threshold', 25.0)
    return _result('check_implementation_intensity_dependency', adjusted, threshold, True, 'validates implementation_intensity dependency',
                   {'field': 'implementation_intensity', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_implementation_intensity_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'implementation_intensity')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_implementation_intensity_readiness_threshold', 27.333)
    return _result('check_implementation_intensity_readiness', adjusted, threshold, True, 'validates implementation_intensity readiness',
                   {'field': 'implementation_intensity', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_baseline_risk_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'baseline_risk')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_baseline_risk_presence_threshold', 29.667)
    return _result('check_baseline_risk_presence', adjusted, threshold, False, 'validates baseline_risk presence',
                   {'field': 'baseline_risk', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_baseline_risk_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'baseline_risk')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_baseline_risk_range_threshold', 32.0)
    return _result('check_baseline_risk_range', adjusted, threshold, True, 'validates baseline_risk range',
                   {'field': 'baseline_risk', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_baseline_risk_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'baseline_risk')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_baseline_risk_stability_threshold', 10.0)
    return _result('check_baseline_risk_stability', adjusted, threshold, True, 'validates baseline_risk stability',
                   {'field': 'baseline_risk', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_baseline_risk_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'baseline_risk')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_baseline_risk_freshness_threshold', 12.333)
    return _result('check_baseline_risk_freshness', adjusted, threshold, False, 'validates baseline_risk freshness',
                   {'field': 'baseline_risk', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_baseline_risk_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'baseline_risk')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_baseline_risk_coverage_threshold', 14.667)
    return _result('check_baseline_risk_coverage', adjusted, threshold, True, 'validates baseline_risk coverage',
                   {'field': 'baseline_risk', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_baseline_risk_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'baseline_risk')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_baseline_risk_consistency_threshold', 17.0)
    return _result('check_baseline_risk_consistency', adjusted, threshold, True, 'validates baseline_risk consistency',
                   {'field': 'baseline_risk', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_baseline_risk_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'baseline_risk')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_baseline_risk_risk_threshold', 19.333)
    return _result('check_baseline_risk_risk', adjusted, threshold, False, 'validates baseline_risk risk',
                   {'field': 'baseline_risk', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_baseline_risk_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'baseline_risk')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_baseline_risk_confidence_threshold', 21.667)
    return _result('check_baseline_risk_confidence', adjusted, threshold, True, 'validates baseline_risk confidence',
                   {'field': 'baseline_risk', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_baseline_risk_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'baseline_risk')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_baseline_risk_dependency_threshold', 24.0)
    return _result('check_baseline_risk_dependency', adjusted, threshold, True, 'validates baseline_risk dependency',
                   {'field': 'baseline_risk', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_baseline_risk_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'baseline_risk')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_baseline_risk_readiness_threshold', 26.333)
    return _result('check_baseline_risk_readiness', adjusted, threshold, False, 'validates baseline_risk readiness',
                   {'field': 'baseline_risk', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_post_risk_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'post_risk')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_post_risk_presence_threshold', 28.667)
    return _result('check_post_risk_presence', adjusted, threshold, True, 'validates post_risk presence',
                   {'field': 'post_risk', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_post_risk_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'post_risk')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_post_risk_range_threshold', 31.0)
    return _result('check_post_risk_range', adjusted, threshold, True, 'validates post_risk range',
                   {'field': 'post_risk', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_post_risk_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'post_risk')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_post_risk_stability_threshold', 9.0)
    return _result('check_post_risk_stability', adjusted, threshold, False, 'validates post_risk stability',
                   {'field': 'post_risk', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_post_risk_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'post_risk')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_post_risk_freshness_threshold', 11.333)
    return _result('check_post_risk_freshness', adjusted, threshold, True, 'validates post_risk freshness',
                   {'field': 'post_risk', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_post_risk_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'post_risk')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_post_risk_coverage_threshold', 13.667)
    return _result('check_post_risk_coverage', adjusted, threshold, True, 'validates post_risk coverage',
                   {'field': 'post_risk', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_post_risk_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'post_risk')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_post_risk_consistency_threshold', 16.0)
    return _result('check_post_risk_consistency', adjusted, threshold, False, 'validates post_risk consistency',
                   {'field': 'post_risk', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_post_risk_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'post_risk')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_post_risk_risk_threshold', 18.333)
    return _result('check_post_risk_risk', adjusted, threshold, True, 'validates post_risk risk',
                   {'field': 'post_risk', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_post_risk_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'post_risk')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_post_risk_confidence_threshold', 20.667)
    return _result('check_post_risk_confidence', adjusted, threshold, True, 'validates post_risk confidence',
                   {'field': 'post_risk', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_post_risk_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'post_risk')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_post_risk_dependency_threshold', 23.0)
    return _result('check_post_risk_dependency', adjusted, threshold, False, 'validates post_risk dependency',
                   {'field': 'post_risk', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_post_risk_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'post_risk')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_post_risk_readiness_threshold', 25.333)
    return _result('check_post_risk_readiness', adjusted, threshold, True, 'validates post_risk readiness',
                   {'field': 'post_risk', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_missing_rate_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'missing_rate')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_missing_rate_presence_threshold', 27.667)
    return _result('check_missing_rate_presence', adjusted, threshold, True, 'validates missing_rate presence',
                   {'field': 'missing_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_missing_rate_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'missing_rate')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_missing_rate_range_threshold', 30.0)
    return _result('check_missing_rate_range', adjusted, threshold, False, 'validates missing_rate range',
                   {'field': 'missing_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_missing_rate_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'missing_rate')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_missing_rate_stability_threshold', 8.0)
    return _result('check_missing_rate_stability', adjusted, threshold, True, 'validates missing_rate stability',
                   {'field': 'missing_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_missing_rate_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'missing_rate')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_missing_rate_freshness_threshold', 10.333)
    return _result('check_missing_rate_freshness', adjusted, threshold, True, 'validates missing_rate freshness',
                   {'field': 'missing_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_missing_rate_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'missing_rate')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_missing_rate_coverage_threshold', 12.667)
    return _result('check_missing_rate_coverage', adjusted, threshold, False, 'validates missing_rate coverage',
                   {'field': 'missing_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_missing_rate_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'missing_rate')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_missing_rate_consistency_threshold', 15.0)
    return _result('check_missing_rate_consistency', adjusted, threshold, True, 'validates missing_rate consistency',
                   {'field': 'missing_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_missing_rate_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'missing_rate')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_missing_rate_risk_threshold', 17.333)
    return _result('check_missing_rate_risk', adjusted, threshold, True, 'validates missing_rate risk',
                   {'field': 'missing_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_missing_rate_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'missing_rate')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_missing_rate_confidence_threshold', 19.667)
    return _result('check_missing_rate_confidence', adjusted, threshold, False, 'validates missing_rate confidence',
                   {'field': 'missing_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_missing_rate_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'missing_rate')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_missing_rate_dependency_threshold', 22.0)
    return _result('check_missing_rate_dependency', adjusted, threshold, True, 'validates missing_rate dependency',
                   {'field': 'missing_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_missing_rate_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'missing_rate')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_missing_rate_readiness_threshold', 24.333)
    return _result('check_missing_rate_readiness', adjusted, threshold, True, 'validates missing_rate readiness',
                   {'field': 'missing_rate', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_enforcement_support_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'enforcement_support')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_enforcement_support_presence_threshold', 26.667)
    return _result('check_enforcement_support_presence', adjusted, threshold, False, 'validates enforcement_support presence',
                   {'field': 'enforcement_support', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_enforcement_support_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'enforcement_support')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_enforcement_support_range_threshold', 29.0)
    return _result('check_enforcement_support_range', adjusted, threshold, True, 'validates enforcement_support range',
                   {'field': 'enforcement_support', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_enforcement_support_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'enforcement_support')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_enforcement_support_stability_threshold', 31.333)
    return _result('check_enforcement_support_stability', adjusted, threshold, True, 'validates enforcement_support stability',
                   {'field': 'enforcement_support', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_enforcement_support_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'enforcement_support')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_enforcement_support_freshness_threshold', 9.333)
    return _result('check_enforcement_support_freshness', adjusted, threshold, False, 'validates enforcement_support freshness',
                   {'field': 'enforcement_support', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_enforcement_support_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'enforcement_support')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_enforcement_support_coverage_threshold', 11.667)
    return _result('check_enforcement_support_coverage', adjusted, threshold, True, 'validates enforcement_support coverage',
                   {'field': 'enforcement_support', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_enforcement_support_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'enforcement_support')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_enforcement_support_consistency_threshold', 14.0)
    return _result('check_enforcement_support_consistency', adjusted, threshold, True, 'validates enforcement_support consistency',
                   {'field': 'enforcement_support', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_enforcement_support_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'enforcement_support')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_enforcement_support_risk_threshold', 16.333)
    return _result('check_enforcement_support_risk', adjusted, threshold, False, 'validates enforcement_support risk',
                   {'field': 'enforcement_support', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_enforcement_support_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'enforcement_support')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_enforcement_support_confidence_threshold', 18.667)
    return _result('check_enforcement_support_confidence', adjusted, threshold, True, 'validates enforcement_support confidence',
                   {'field': 'enforcement_support', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_enforcement_support_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'enforcement_support')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_enforcement_support_dependency_threshold', 21.0)
    return _result('check_enforcement_support_dependency', adjusted, threshold, True, 'validates enforcement_support dependency',
                   {'field': 'enforcement_support', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_enforcement_support_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'enforcement_support')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_enforcement_support_readiness_threshold', 23.333)
    return _result('check_enforcement_support_readiness', adjusted, threshold, False, 'validates enforcement_support readiness',
                   {'field': 'enforcement_support', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_digital_capacity_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'digital_capacity')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_digital_capacity_presence_threshold', 25.667)
    return _result('check_digital_capacity_presence', adjusted, threshold, True, 'validates digital_capacity presence',
                   {'field': 'digital_capacity', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_digital_capacity_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'digital_capacity')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_digital_capacity_range_threshold', 28.0)
    return _result('check_digital_capacity_range', adjusted, threshold, True, 'validates digital_capacity range',
                   {'field': 'digital_capacity', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_digital_capacity_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'digital_capacity')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_digital_capacity_stability_threshold', 30.333)
    return _result('check_digital_capacity_stability', adjusted, threshold, False, 'validates digital_capacity stability',
                   {'field': 'digital_capacity', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_digital_capacity_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'digital_capacity')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_digital_capacity_freshness_threshold', 8.333)
    return _result('check_digital_capacity_freshness', adjusted, threshold, True, 'validates digital_capacity freshness',
                   {'field': 'digital_capacity', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_digital_capacity_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'digital_capacity')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_digital_capacity_coverage_threshold', 10.667)
    return _result('check_digital_capacity_coverage', adjusted, threshold, True, 'validates digital_capacity coverage',
                   {'field': 'digital_capacity', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_digital_capacity_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'digital_capacity')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_digital_capacity_consistency_threshold', 13.0)
    return _result('check_digital_capacity_consistency', adjusted, threshold, False, 'validates digital_capacity consistency',
                   {'field': 'digital_capacity', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_digital_capacity_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'digital_capacity')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_digital_capacity_risk_threshold', 15.333)
    return _result('check_digital_capacity_risk', adjusted, threshold, True, 'validates digital_capacity risk',
                   {'field': 'digital_capacity', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_digital_capacity_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'digital_capacity')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_digital_capacity_confidence_threshold', 17.667)
    return _result('check_digital_capacity_confidence', adjusted, threshold, True, 'validates digital_capacity confidence',
                   {'field': 'digital_capacity', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_digital_capacity_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'digital_capacity')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_digital_capacity_dependency_threshold', 20.0)
    return _result('check_digital_capacity_dependency', adjusted, threshold, False, 'validates digital_capacity dependency',
                   {'field': 'digital_capacity', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_digital_capacity_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'digital_capacity')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_digital_capacity_readiness_threshold', 22.333)
    return _result('check_digital_capacity_readiness', adjusted, threshold, True, 'validates digital_capacity readiness',
                   {'field': 'digital_capacity', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_affected_group_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'affected_group')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_affected_group_presence_threshold', 24.667)
    return _result('check_affected_group_presence', adjusted, threshold, True, 'validates affected_group presence',
                   {'field': 'affected_group', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_affected_group_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'affected_group')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_affected_group_range_threshold', 27.0)
    return _result('check_affected_group_range', adjusted, threshold, False, 'validates affected_group range',
                   {'field': 'affected_group', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_affected_group_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'affected_group')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_affected_group_stability_threshold', 29.333)
    return _result('check_affected_group_stability', adjusted, threshold, True, 'validates affected_group stability',
                   {'field': 'affected_group', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_affected_group_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'affected_group')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_affected_group_freshness_threshold', 31.667)
    return _result('check_affected_group_freshness', adjusted, threshold, True, 'validates affected_group freshness',
                   {'field': 'affected_group', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_affected_group_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'affected_group')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_affected_group_coverage_threshold', 9.667)
    return _result('check_affected_group_coverage', adjusted, threshold, False, 'validates affected_group coverage',
                   {'field': 'affected_group', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_affected_group_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'affected_group')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_affected_group_consistency_threshold', 12.0)
    return _result('check_affected_group_consistency', adjusted, threshold, True, 'validates affected_group consistency',
                   {'field': 'affected_group', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_affected_group_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'affected_group')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_affected_group_risk_threshold', 14.333)
    return _result('check_affected_group_risk', adjusted, threshold, True, 'validates affected_group risk',
                   {'field': 'affected_group', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_affected_group_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'affected_group')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_affected_group_confidence_threshold', 16.667)
    return _result('check_affected_group_confidence', adjusted, threshold, False, 'validates affected_group confidence',
                   {'field': 'affected_group', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_affected_group_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'affected_group')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_affected_group_dependency_threshold', 19.0)
    return _result('check_affected_group_dependency', adjusted, threshold, True, 'validates affected_group dependency',
                   {'field': 'affected_group', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_affected_group_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'affected_group')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 0.0
    threshold = _context_number(context, 'check_affected_group_readiness_threshold', 21.333)
    return _result('check_affected_group_readiness', adjusted, threshold, True, 'validates affected_group readiness',
                   {'field': 'affected_group', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_consultation_coverage_presence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'consultation_coverage')
    weight = _context_number(context, 'presence_weight', 1.1)
    adjusted = raw * weight + 0.17
    threshold = _context_number(context, 'check_consultation_coverage_presence_threshold', 23.667)
    return _result('check_consultation_coverage_presence', adjusted, threshold, False, 'validates consultation_coverage presence',
                   {'field': 'consultation_coverage', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_consultation_coverage_range(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'consultation_coverage')
    weight = _context_number(context, 'range_weight', 1.2)
    adjusted = raw * weight + 0.34
    threshold = _context_number(context, 'check_consultation_coverage_range_threshold', 26.0)
    return _result('check_consultation_coverage_range', adjusted, threshold, True, 'validates consultation_coverage range',
                   {'field': 'consultation_coverage', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_consultation_coverage_stability(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'consultation_coverage')
    weight = _context_number(context, 'stability_weight', 1.3)
    adjusted = raw * weight + 0.51
    threshold = _context_number(context, 'check_consultation_coverage_stability_threshold', 28.333)
    return _result('check_consultation_coverage_stability', adjusted, threshold, True, 'validates consultation_coverage stability',
                   {'field': 'consultation_coverage', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_consultation_coverage_freshness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'consultation_coverage')
    weight = _context_number(context, 'freshness_weight', 1.4)
    adjusted = raw * weight + 0.68
    threshold = _context_number(context, 'check_consultation_coverage_freshness_threshold', 30.667)
    return _result('check_consultation_coverage_freshness', adjusted, threshold, False, 'validates consultation_coverage freshness',
                   {'field': 'consultation_coverage', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_consultation_coverage_coverage(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'consultation_coverage')
    weight = _context_number(context, 'coverage_weight', 1.0)
    adjusted = raw * weight + 0.8500000000000001
    threshold = _context_number(context, 'check_consultation_coverage_coverage_threshold', 8.667)
    return _result('check_consultation_coverage_coverage', adjusted, threshold, True, 'validates consultation_coverage coverage',
                   {'field': 'consultation_coverage', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_consultation_coverage_consistency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'consultation_coverage')
    weight = _context_number(context, 'consistency_weight', 1.1)
    adjusted = raw * weight + 1.02
    threshold = _context_number(context, 'check_consultation_coverage_consistency_threshold', 11.0)
    return _result('check_consultation_coverage_consistency', adjusted, threshold, True, 'validates consultation_coverage consistency',
                   {'field': 'consultation_coverage', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_consultation_coverage_risk(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'consultation_coverage')
    weight = _context_number(context, 'risk_weight', 1.2)
    adjusted = raw * weight + 1.1900000000000002
    threshold = _context_number(context, 'check_consultation_coverage_risk_threshold', 13.333)
    return _result('check_consultation_coverage_risk', adjusted, threshold, False, 'validates consultation_coverage risk',
                   {'field': 'consultation_coverage', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_consultation_coverage_confidence(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'consultation_coverage')
    weight = _context_number(context, 'confidence_weight', 1.3)
    adjusted = raw * weight + 1.36
    threshold = _context_number(context, 'check_consultation_coverage_confidence_threshold', 15.667)
    return _result('check_consultation_coverage_confidence', adjusted, threshold, True, 'validates consultation_coverage confidence',
                   {'field': 'consultation_coverage', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_consultation_coverage_dependency(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'consultation_coverage')
    weight = _context_number(context, 'dependency_weight', 1.4)
    adjusted = raw * weight + 1.53
    threshold = _context_number(context, 'check_consultation_coverage_dependency_threshold', 18.0)
    return _result('check_consultation_coverage_dependency', adjusted, threshold, True, 'validates consultation_coverage dependency',
                   {'field': 'consultation_coverage', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

def check_consultation_coverage_readiness(record: DomainRecord, context: Mapping[str, Any]) -> RuleResult:
    raw = _number(record, 'consultation_coverage')
    weight = _context_number(context, 'readiness_weight', 1.0)
    adjusted = raw * weight + 1.7000000000000002
    threshold = _context_number(context, 'check_consultation_coverage_readiness_threshold', 20.333)
    return _result('check_consultation_coverage_readiness', adjusted, threshold, False, 'validates consultation_coverage readiness',
                   {'field': 'consultation_coverage', 'raw': raw, 'weight': weight, 'adjusted': adjusted, 'threshold': threshold})

RULES: tuple[RuleFunction, ...] = (
    check_policy_code_presence,
    check_policy_code_range,
    check_policy_code_stability,
    check_policy_code_freshness,
    check_policy_code_coverage,
    check_policy_code_consistency,
    check_policy_code_risk,
    check_policy_code_confidence,
    check_policy_code_dependency,
    check_policy_code_readiness,
    check_jurisdiction_level_presence,
    check_jurisdiction_level_range,
    check_jurisdiction_level_stability,
    check_jurisdiction_level_freshness,
    check_jurisdiction_level_coverage,
    check_jurisdiction_level_consistency,
    check_jurisdiction_level_risk,
    check_jurisdiction_level_confidence,
    check_jurisdiction_level_dependency,
    check_jurisdiction_level_readiness,
    check_measure_type_presence,
    check_measure_type_range,
    check_measure_type_stability,
    check_measure_type_freshness,
    check_measure_type_coverage,
    check_measure_type_consistency,
    check_measure_type_risk,
    check_measure_type_confidence,
    check_measure_type_dependency,
    check_measure_type_readiness,
    check_covered_entities_presence,
    check_covered_entities_range,
    check_covered_entities_stability,
    check_covered_entities_freshness,
    check_covered_entities_coverage,
    check_covered_entities_consistency,
    check_covered_entities_risk,
    check_covered_entities_confidence,
    check_covered_entities_dependency,
    check_covered_entities_readiness,
    check_implementation_intensity_presence,
    check_implementation_intensity_range,
    check_implementation_intensity_stability,
    check_implementation_intensity_freshness,
    check_implementation_intensity_coverage,
    check_implementation_intensity_consistency,
    check_implementation_intensity_risk,
    check_implementation_intensity_confidence,
    check_implementation_intensity_dependency,
    check_implementation_intensity_readiness,
    check_baseline_risk_presence,
    check_baseline_risk_range,
    check_baseline_risk_stability,
    check_baseline_risk_freshness,
    check_baseline_risk_coverage,
    check_baseline_risk_consistency,
    check_baseline_risk_risk,
    check_baseline_risk_confidence,
    check_baseline_risk_dependency,
    check_baseline_risk_readiness,
    check_post_risk_presence,
    check_post_risk_range,
    check_post_risk_stability,
    check_post_risk_freshness,
    check_post_risk_coverage,
    check_post_risk_consistency,
    check_post_risk_risk,
    check_post_risk_confidence,
    check_post_risk_dependency,
    check_post_risk_readiness,
    check_missing_rate_presence,
    check_missing_rate_range,
    check_missing_rate_stability,
    check_missing_rate_freshness,
    check_missing_rate_coverage,
    check_missing_rate_consistency,
    check_missing_rate_risk,
    check_missing_rate_confidence,
    check_missing_rate_dependency,
    check_missing_rate_readiness,
    check_enforcement_support_presence,
    check_enforcement_support_range,
    check_enforcement_support_stability,
    check_enforcement_support_freshness,
    check_enforcement_support_coverage,
    check_enforcement_support_consistency,
    check_enforcement_support_risk,
    check_enforcement_support_confidence,
    check_enforcement_support_dependency,
    check_enforcement_support_readiness,
    check_digital_capacity_presence,
    check_digital_capacity_range,
    check_digital_capacity_stability,
    check_digital_capacity_freshness,
    check_digital_capacity_coverage,
    check_digital_capacity_consistency,
    check_digital_capacity_risk,
    check_digital_capacity_confidence,
    check_digital_capacity_dependency,
    check_digital_capacity_readiness,
    check_affected_group_presence,
    check_affected_group_range,
    check_affected_group_stability,
    check_affected_group_freshness,
    check_affected_group_coverage,
    check_affected_group_consistency,
    check_affected_group_risk,
    check_affected_group_confidence,
    check_affected_group_dependency,
    check_affected_group_readiness,
    check_consultation_coverage_presence,
    check_consultation_coverage_range,
    check_consultation_coverage_stability,
    check_consultation_coverage_freshness,
    check_consultation_coverage_coverage,
    check_consultation_coverage_consistency,
    check_consultation_coverage_risk,
    check_consultation_coverage_confidence,
    check_consultation_coverage_dependency,
    check_consultation_coverage_readiness,
)

RULE_INDEX = {rule.__name__: rule for rule in RULES}

def evaluate(record: DomainRecord, context: Mapping[str, Any] | None = None) -> tuple[RuleResult, ...]:
    context = context or {}
    return tuple(rule(record, context) for rule in RULES)

def summarize(results: tuple[RuleResult, ...]) -> dict[str, Any]:
    if not results:
        return {'score': 0.0, 'passed': 0, 'failed': 0, 'critical': 0}
    return {'score': sum(item.score for item in results) / len(results),
            'passed': sum(item.passed for item in results),
            'failed': sum(not item.passed for item in results),
            'critical': sum(item.severity == 'critical' for item in results)}
