from __future__ import annotations

import math
import statistics
from collections import defaultdict
from typing import Any, Callable, Iterable, Mapping

from policy_impact.measures.policy_contract import DomainRecord, bounded, finite_number, normalized_text, stable_hash
from policy_impact.comparability.evidence_gate import evaluate, summarize
from policy_impact.analysis.counterfactual import adjusted_effect

MetricFunction = Callable[[DomainRecord, Mapping[str, Any]], float]

def _value(record: DomainRecord, field: str) -> float:
    value = record.payload.get(field)
    if isinstance(value, bool):
        return float(value)
    if isinstance(value, (int, float)):
        return finite_number(value)
    text = normalized_text(value)
    return float(sum((index + 1) * ord(ch) for index, ch in enumerate(text)) % 997) / 10.0

def _signal(record: DomainRecord, fields: tuple[str, ...], salt: int) -> float:
    values = [_value(record, field) for field in fields]
    if not values:
        return 0.0
    center = statistics.fmean(values)
    spread = statistics.pstdev(values) if len(values) > 1 else 0.0
    harmonic = sum(math.sin(value / (salt + 1)) + math.cos(value * (salt + 1) / 17.0) for value in values)
    return bounded(0.5 + math.tanh((center - spread + harmonic) / (30.0 + salt)) / 2.0)

def metric_learning_gain_01(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('policy_code', 'covered_entities', 'post_risk', 'digital_capacity'), 1)
    weight = finite_number(context.get('learning_gain_weight', 0.7))
    offset = finite_number(context.get('metric_learning_gain_01_offset', -0.08))
    return bounded(base * weight + offset)

def metric_learning_gain_02(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('jurisdiction_level', 'implementation_intensity', 'missing_rate', 'affected_group'), 2)
    weight = finite_number(context.get('learning_gain_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_learning_gain_02_offset', -0.06))
    return bounded(base * weight + offset)

def metric_learning_gain_03(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('measure_type', 'baseline_risk', 'enforcement_support', 'consultation_coverage'), 3)
    weight = finite_number(context.get('learning_gain_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_learning_gain_03_offset', -0.04))
    return bounded(base * weight + offset)

def metric_learning_gain_04(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('covered_entities', 'post_risk', 'digital_capacity', 'policy_code'), 4)
    weight = finite_number(context.get('learning_gain_weight', 1.0))
    offset = finite_number(context.get('metric_learning_gain_04_offset', -0.02))
    return bounded(base * weight + offset)

def metric_learning_gain_05(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('implementation_intensity', 'missing_rate', 'affected_group', 'jurisdiction_level'), 5)
    weight = finite_number(context.get('learning_gain_weight', 0.7))
    offset = finite_number(context.get('metric_learning_gain_05_offset', 0.0))
    return bounded(base * weight + offset)

def metric_learning_gain_06(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('baseline_risk', 'enforcement_support', 'consultation_coverage', 'measure_type'), 6)
    weight = finite_number(context.get('learning_gain_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_learning_gain_06_offset', 0.02))
    return bounded(base * weight + offset)

def metric_learning_gain_07(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('post_risk', 'digital_capacity', 'policy_code', 'covered_entities'), 7)
    weight = finite_number(context.get('learning_gain_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_learning_gain_07_offset', 0.04))
    return bounded(base * weight + offset)

def metric_learning_gain_08(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('missing_rate', 'affected_group', 'jurisdiction_level', 'implementation_intensity'), 8)
    weight = finite_number(context.get('learning_gain_weight', 1.0))
    offset = finite_number(context.get('metric_learning_gain_08_offset', 0.06))
    return bounded(base * weight + offset)

def metric_learning_gain_09(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('enforcement_support', 'consultation_coverage', 'measure_type', 'baseline_risk'), 9)
    weight = finite_number(context.get('learning_gain_weight', 0.7))
    offset = finite_number(context.get('metric_learning_gain_09_offset', 0.08))
    return bounded(base * weight + offset)

def metric_learning_gain_10(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('digital_capacity', 'policy_code', 'covered_entities', 'post_risk'), 10)
    weight = finite_number(context.get('learning_gain_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_learning_gain_10_offset', 0.1))
    return bounded(base * weight + offset)

def metric_engagement_comparability_01(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('jurisdiction_level', 'implementation_intensity', 'missing_rate', 'affected_group'), 2)
    weight = finite_number(context.get('engagement_comparability_weight', 0.7))
    offset = finite_number(context.get('metric_engagement_comparability_01_offset', -0.08))
    return bounded(base * weight + offset)

def metric_engagement_comparability_02(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('measure_type', 'baseline_risk', 'enforcement_support', 'consultation_coverage'), 3)
    weight = finite_number(context.get('engagement_comparability_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_engagement_comparability_02_offset', -0.06))
    return bounded(base * weight + offset)

def metric_engagement_comparability_03(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('covered_entities', 'post_risk', 'digital_capacity', 'policy_code'), 4)
    weight = finite_number(context.get('engagement_comparability_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_engagement_comparability_03_offset', -0.04))
    return bounded(base * weight + offset)

def metric_engagement_comparability_04(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('implementation_intensity', 'missing_rate', 'affected_group', 'jurisdiction_level'), 5)
    weight = finite_number(context.get('engagement_comparability_weight', 1.0))
    offset = finite_number(context.get('metric_engagement_comparability_04_offset', -0.02))
    return bounded(base * weight + offset)

def metric_engagement_comparability_05(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('baseline_risk', 'enforcement_support', 'consultation_coverage', 'measure_type'), 6)
    weight = finite_number(context.get('engagement_comparability_weight', 0.7))
    offset = finite_number(context.get('metric_engagement_comparability_05_offset', 0.0))
    return bounded(base * weight + offset)

def metric_engagement_comparability_06(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('post_risk', 'digital_capacity', 'policy_code', 'covered_entities'), 7)
    weight = finite_number(context.get('engagement_comparability_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_engagement_comparability_06_offset', 0.02))
    return bounded(base * weight + offset)

def metric_engagement_comparability_07(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('missing_rate', 'affected_group', 'jurisdiction_level', 'implementation_intensity'), 8)
    weight = finite_number(context.get('engagement_comparability_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_engagement_comparability_07_offset', 0.04))
    return bounded(base * weight + offset)

def metric_engagement_comparability_08(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('enforcement_support', 'consultation_coverage', 'measure_type', 'baseline_risk'), 9)
    weight = finite_number(context.get('engagement_comparability_weight', 1.0))
    offset = finite_number(context.get('metric_engagement_comparability_08_offset', 0.06))
    return bounded(base * weight + offset)

def metric_engagement_comparability_09(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('digital_capacity', 'policy_code', 'covered_entities', 'post_risk'), 10)
    weight = finite_number(context.get('engagement_comparability_weight', 0.7))
    offset = finite_number(context.get('metric_engagement_comparability_09_offset', 0.08))
    return bounded(base * weight + offset)

def metric_engagement_comparability_10(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('affected_group', 'jurisdiction_level', 'implementation_intensity', 'missing_rate'), 11)
    weight = finite_number(context.get('engagement_comparability_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_engagement_comparability_10_offset', 0.1))
    return bounded(base * weight + offset)

def metric_attrition_bias_01(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('measure_type', 'baseline_risk', 'enforcement_support', 'consultation_coverage'), 3)
    weight = finite_number(context.get('attrition_bias_weight', 0.7))
    offset = finite_number(context.get('metric_attrition_bias_01_offset', -0.08))
    return bounded(base * weight + offset)

def metric_attrition_bias_02(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('covered_entities', 'post_risk', 'digital_capacity', 'policy_code'), 4)
    weight = finite_number(context.get('attrition_bias_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_attrition_bias_02_offset', -0.06))
    return bounded(base * weight + offset)

def metric_attrition_bias_03(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('implementation_intensity', 'missing_rate', 'affected_group', 'jurisdiction_level'), 5)
    weight = finite_number(context.get('attrition_bias_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_attrition_bias_03_offset', -0.04))
    return bounded(base * weight + offset)

def metric_attrition_bias_04(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('baseline_risk', 'enforcement_support', 'consultation_coverage', 'measure_type'), 6)
    weight = finite_number(context.get('attrition_bias_weight', 1.0))
    offset = finite_number(context.get('metric_attrition_bias_04_offset', -0.02))
    return bounded(base * weight + offset)

def metric_attrition_bias_05(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('post_risk', 'digital_capacity', 'policy_code', 'covered_entities'), 7)
    weight = finite_number(context.get('attrition_bias_weight', 0.7))
    offset = finite_number(context.get('metric_attrition_bias_05_offset', 0.0))
    return bounded(base * weight + offset)

def metric_attrition_bias_06(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('missing_rate', 'affected_group', 'jurisdiction_level', 'implementation_intensity'), 8)
    weight = finite_number(context.get('attrition_bias_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_attrition_bias_06_offset', 0.02))
    return bounded(base * weight + offset)

def metric_attrition_bias_07(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('enforcement_support', 'consultation_coverage', 'measure_type', 'baseline_risk'), 9)
    weight = finite_number(context.get('attrition_bias_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_attrition_bias_07_offset', 0.04))
    return bounded(base * weight + offset)

def metric_attrition_bias_08(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('digital_capacity', 'policy_code', 'covered_entities', 'post_risk'), 10)
    weight = finite_number(context.get('attrition_bias_weight', 1.0))
    offset = finite_number(context.get('metric_attrition_bias_08_offset', 0.06))
    return bounded(base * weight + offset)

def metric_attrition_bias_09(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('affected_group', 'jurisdiction_level', 'implementation_intensity', 'missing_rate'), 11)
    weight = finite_number(context.get('attrition_bias_weight', 0.7))
    offset = finite_number(context.get('metric_attrition_bias_09_offset', 0.08))
    return bounded(base * weight + offset)

def metric_attrition_bias_10(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('consultation_coverage', 'measure_type', 'baseline_risk', 'enforcement_support'), 12)
    weight = finite_number(context.get('attrition_bias_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_attrition_bias_10_offset', 0.1))
    return bounded(base * weight + offset)

def metric_equity_gap_01(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('covered_entities', 'post_risk', 'digital_capacity', 'policy_code'), 4)
    weight = finite_number(context.get('equity_gap_weight', 0.7))
    offset = finite_number(context.get('metric_equity_gap_01_offset', -0.08))
    return bounded(base * weight + offset)

def metric_equity_gap_02(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('implementation_intensity', 'missing_rate', 'affected_group', 'jurisdiction_level'), 5)
    weight = finite_number(context.get('equity_gap_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_equity_gap_02_offset', -0.06))
    return bounded(base * weight + offset)

def metric_equity_gap_03(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('baseline_risk', 'enforcement_support', 'consultation_coverage', 'measure_type'), 6)
    weight = finite_number(context.get('equity_gap_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_equity_gap_03_offset', -0.04))
    return bounded(base * weight + offset)

def metric_equity_gap_04(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('post_risk', 'digital_capacity', 'policy_code', 'covered_entities'), 7)
    weight = finite_number(context.get('equity_gap_weight', 1.0))
    offset = finite_number(context.get('metric_equity_gap_04_offset', -0.02))
    return bounded(base * weight + offset)

def metric_equity_gap_05(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('missing_rate', 'affected_group', 'jurisdiction_level', 'implementation_intensity'), 8)
    weight = finite_number(context.get('equity_gap_weight', 0.7))
    offset = finite_number(context.get('metric_equity_gap_05_offset', 0.0))
    return bounded(base * weight + offset)

def metric_equity_gap_06(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('enforcement_support', 'consultation_coverage', 'measure_type', 'baseline_risk'), 9)
    weight = finite_number(context.get('equity_gap_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_equity_gap_06_offset', 0.02))
    return bounded(base * weight + offset)

def metric_equity_gap_07(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('digital_capacity', 'policy_code', 'covered_entities', 'post_risk'), 10)
    weight = finite_number(context.get('equity_gap_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_equity_gap_07_offset', 0.04))
    return bounded(base * weight + offset)

def metric_equity_gap_08(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('affected_group', 'jurisdiction_level', 'implementation_intensity', 'missing_rate'), 11)
    weight = finite_number(context.get('equity_gap_weight', 1.0))
    offset = finite_number(context.get('metric_equity_gap_08_offset', 0.06))
    return bounded(base * weight + offset)

def metric_equity_gap_09(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('consultation_coverage', 'measure_type', 'baseline_risk', 'enforcement_support'), 12)
    weight = finite_number(context.get('equity_gap_weight', 0.7))
    offset = finite_number(context.get('metric_equity_gap_09_offset', 0.08))
    return bounded(base * weight + offset)

def metric_equity_gap_10(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('policy_code', 'covered_entities', 'post_risk', 'digital_capacity'), 13)
    weight = finite_number(context.get('equity_gap_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_equity_gap_10_offset', 0.1))
    return bounded(base * weight + offset)

def metric_teacher_dependency_01(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('implementation_intensity', 'missing_rate', 'affected_group', 'jurisdiction_level'), 5)
    weight = finite_number(context.get('teacher_dependency_weight', 0.7))
    offset = finite_number(context.get('metric_teacher_dependency_01_offset', -0.08))
    return bounded(base * weight + offset)

def metric_teacher_dependency_02(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('baseline_risk', 'enforcement_support', 'consultation_coverage', 'measure_type'), 6)
    weight = finite_number(context.get('teacher_dependency_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_teacher_dependency_02_offset', -0.06))
    return bounded(base * weight + offset)

def metric_teacher_dependency_03(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('post_risk', 'digital_capacity', 'policy_code', 'covered_entities'), 7)
    weight = finite_number(context.get('teacher_dependency_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_teacher_dependency_03_offset', -0.04))
    return bounded(base * weight + offset)

def metric_teacher_dependency_04(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('missing_rate', 'affected_group', 'jurisdiction_level', 'implementation_intensity'), 8)
    weight = finite_number(context.get('teacher_dependency_weight', 1.0))
    offset = finite_number(context.get('metric_teacher_dependency_04_offset', -0.02))
    return bounded(base * weight + offset)

def metric_teacher_dependency_05(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('enforcement_support', 'consultation_coverage', 'measure_type', 'baseline_risk'), 9)
    weight = finite_number(context.get('teacher_dependency_weight', 0.7))
    offset = finite_number(context.get('metric_teacher_dependency_05_offset', 0.0))
    return bounded(base * weight + offset)

def metric_teacher_dependency_06(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('digital_capacity', 'policy_code', 'covered_entities', 'post_risk'), 10)
    weight = finite_number(context.get('teacher_dependency_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_teacher_dependency_06_offset', 0.02))
    return bounded(base * weight + offset)

def metric_teacher_dependency_07(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('affected_group', 'jurisdiction_level', 'implementation_intensity', 'missing_rate'), 11)
    weight = finite_number(context.get('teacher_dependency_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_teacher_dependency_07_offset', 0.04))
    return bounded(base * weight + offset)

def metric_teacher_dependency_08(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('consultation_coverage', 'measure_type', 'baseline_risk', 'enforcement_support'), 12)
    weight = finite_number(context.get('teacher_dependency_weight', 1.0))
    offset = finite_number(context.get('metric_teacher_dependency_08_offset', 0.06))
    return bounded(base * weight + offset)

def metric_teacher_dependency_09(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('policy_code', 'covered_entities', 'post_risk', 'digital_capacity'), 13)
    weight = finite_number(context.get('teacher_dependency_weight', 0.7))
    offset = finite_number(context.get('metric_teacher_dependency_09_offset', 0.08))
    return bounded(base * weight + offset)

def metric_teacher_dependency_10(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('jurisdiction_level', 'implementation_intensity', 'missing_rate', 'affected_group'), 14)
    weight = finite_number(context.get('teacher_dependency_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_teacher_dependency_10_offset', 0.1))
    return bounded(base * weight + offset)

def metric_digital_capacity_resilience_01(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('baseline_risk', 'enforcement_support', 'consultation_coverage', 'measure_type'), 6)
    weight = finite_number(context.get('digital_capacity_resilience_weight', 0.7))
    offset = finite_number(context.get('metric_digital_capacity_resilience_01_offset', -0.08))
    return bounded(base * weight + offset)

def metric_digital_capacity_resilience_02(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('post_risk', 'digital_capacity', 'policy_code', 'covered_entities'), 7)
    weight = finite_number(context.get('digital_capacity_resilience_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_digital_capacity_resilience_02_offset', -0.06))
    return bounded(base * weight + offset)

def metric_digital_capacity_resilience_03(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('missing_rate', 'affected_group', 'jurisdiction_level', 'implementation_intensity'), 8)
    weight = finite_number(context.get('digital_capacity_resilience_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_digital_capacity_resilience_03_offset', -0.04))
    return bounded(base * weight + offset)

def metric_digital_capacity_resilience_04(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('enforcement_support', 'consultation_coverage', 'measure_type', 'baseline_risk'), 9)
    weight = finite_number(context.get('digital_capacity_resilience_weight', 1.0))
    offset = finite_number(context.get('metric_digital_capacity_resilience_04_offset', -0.02))
    return bounded(base * weight + offset)

def metric_digital_capacity_resilience_05(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('digital_capacity', 'policy_code', 'covered_entities', 'post_risk'), 10)
    weight = finite_number(context.get('digital_capacity_resilience_weight', 0.7))
    offset = finite_number(context.get('metric_digital_capacity_resilience_05_offset', 0.0))
    return bounded(base * weight + offset)

def metric_digital_capacity_resilience_06(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('affected_group', 'jurisdiction_level', 'implementation_intensity', 'missing_rate'), 11)
    weight = finite_number(context.get('digital_capacity_resilience_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_digital_capacity_resilience_06_offset', 0.02))
    return bounded(base * weight + offset)

def metric_digital_capacity_resilience_07(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('consultation_coverage', 'measure_type', 'baseline_risk', 'enforcement_support'), 12)
    weight = finite_number(context.get('digital_capacity_resilience_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_digital_capacity_resilience_07_offset', 0.04))
    return bounded(base * weight + offset)

def metric_digital_capacity_resilience_08(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('policy_code', 'covered_entities', 'post_risk', 'digital_capacity'), 13)
    weight = finite_number(context.get('digital_capacity_resilience_weight', 1.0))
    offset = finite_number(context.get('metric_digital_capacity_resilience_08_offset', 0.06))
    return bounded(base * weight + offset)

def metric_digital_capacity_resilience_09(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('jurisdiction_level', 'implementation_intensity', 'missing_rate', 'affected_group'), 14)
    weight = finite_number(context.get('digital_capacity_resilience_weight', 0.7))
    offset = finite_number(context.get('metric_digital_capacity_resilience_09_offset', 0.08))
    return bounded(base * weight + offset)

def metric_digital_capacity_resilience_10(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('measure_type', 'baseline_risk', 'enforcement_support', 'consultation_coverage'), 15)
    weight = finite_number(context.get('digital_capacity_resilience_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_digital_capacity_resilience_10_offset', 0.1))
    return bounded(base * weight + offset)

def metric_effect_persistence_01(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('post_risk', 'digital_capacity', 'policy_code', 'covered_entities'), 7)
    weight = finite_number(context.get('effect_persistence_weight', 0.7))
    offset = finite_number(context.get('metric_effect_persistence_01_offset', -0.08))
    return bounded(base * weight + offset)

def metric_effect_persistence_02(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('missing_rate', 'affected_group', 'jurisdiction_level', 'implementation_intensity'), 8)
    weight = finite_number(context.get('effect_persistence_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_effect_persistence_02_offset', -0.06))
    return bounded(base * weight + offset)

def metric_effect_persistence_03(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('enforcement_support', 'consultation_coverage', 'measure_type', 'baseline_risk'), 9)
    weight = finite_number(context.get('effect_persistence_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_effect_persistence_03_offset', -0.04))
    return bounded(base * weight + offset)

def metric_effect_persistence_04(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('digital_capacity', 'policy_code', 'covered_entities', 'post_risk'), 10)
    weight = finite_number(context.get('effect_persistence_weight', 1.0))
    offset = finite_number(context.get('metric_effect_persistence_04_offset', -0.02))
    return bounded(base * weight + offset)

def metric_effect_persistence_05(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('affected_group', 'jurisdiction_level', 'implementation_intensity', 'missing_rate'), 11)
    weight = finite_number(context.get('effect_persistence_weight', 0.7))
    offset = finite_number(context.get('metric_effect_persistence_05_offset', 0.0))
    return bounded(base * weight + offset)

def metric_effect_persistence_06(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('consultation_coverage', 'measure_type', 'baseline_risk', 'enforcement_support'), 12)
    weight = finite_number(context.get('effect_persistence_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_effect_persistence_06_offset', 0.02))
    return bounded(base * weight + offset)

def metric_effect_persistence_07(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('policy_code', 'covered_entities', 'post_risk', 'digital_capacity'), 13)
    weight = finite_number(context.get('effect_persistence_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_effect_persistence_07_offset', 0.04))
    return bounded(base * weight + offset)

def metric_effect_persistence_08(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('jurisdiction_level', 'implementation_intensity', 'missing_rate', 'affected_group'), 14)
    weight = finite_number(context.get('effect_persistence_weight', 1.0))
    offset = finite_number(context.get('metric_effect_persistence_08_offset', 0.06))
    return bounded(base * weight + offset)

def metric_effect_persistence_09(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('measure_type', 'baseline_risk', 'enforcement_support', 'consultation_coverage'), 15)
    weight = finite_number(context.get('effect_persistence_weight', 0.7))
    offset = finite_number(context.get('metric_effect_persistence_09_offset', 0.08))
    return bounded(base * weight + offset)

def metric_effect_persistence_10(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('covered_entities', 'post_risk', 'digital_capacity', 'policy_code'), 16)
    weight = finite_number(context.get('effect_persistence_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_effect_persistence_10_offset', 0.1))
    return bounded(base * weight + offset)

def metric_scale_readiness_01(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('missing_rate', 'affected_group', 'jurisdiction_level', 'implementation_intensity'), 8)
    weight = finite_number(context.get('scale_readiness_weight', 0.7))
    offset = finite_number(context.get('metric_scale_readiness_01_offset', -0.08))
    return bounded(base * weight + offset)

def metric_scale_readiness_02(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('enforcement_support', 'consultation_coverage', 'measure_type', 'baseline_risk'), 9)
    weight = finite_number(context.get('scale_readiness_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_scale_readiness_02_offset', -0.06))
    return bounded(base * weight + offset)

def metric_scale_readiness_03(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('digital_capacity', 'policy_code', 'covered_entities', 'post_risk'), 10)
    weight = finite_number(context.get('scale_readiness_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_scale_readiness_03_offset', -0.04))
    return bounded(base * weight + offset)

def metric_scale_readiness_04(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('affected_group', 'jurisdiction_level', 'implementation_intensity', 'missing_rate'), 11)
    weight = finite_number(context.get('scale_readiness_weight', 1.0))
    offset = finite_number(context.get('metric_scale_readiness_04_offset', -0.02))
    return bounded(base * weight + offset)

def metric_scale_readiness_05(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('consultation_coverage', 'measure_type', 'baseline_risk', 'enforcement_support'), 12)
    weight = finite_number(context.get('scale_readiness_weight', 0.7))
    offset = finite_number(context.get('metric_scale_readiness_05_offset', 0.0))
    return bounded(base * weight + offset)

def metric_scale_readiness_06(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('policy_code', 'covered_entities', 'post_risk', 'digital_capacity'), 13)
    weight = finite_number(context.get('scale_readiness_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_scale_readiness_06_offset', 0.02))
    return bounded(base * weight + offset)

def metric_scale_readiness_07(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('jurisdiction_level', 'implementation_intensity', 'missing_rate', 'affected_group'), 14)
    weight = finite_number(context.get('scale_readiness_weight', 0.8999999999999999))
    offset = finite_number(context.get('metric_scale_readiness_07_offset', 0.04))
    return bounded(base * weight + offset)

def metric_scale_readiness_08(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('measure_type', 'baseline_risk', 'enforcement_support', 'consultation_coverage'), 15)
    weight = finite_number(context.get('scale_readiness_weight', 1.0))
    offset = finite_number(context.get('metric_scale_readiness_08_offset', 0.06))
    return bounded(base * weight + offset)

def metric_scale_readiness_09(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('covered_entities', 'post_risk', 'digital_capacity', 'policy_code'), 16)
    weight = finite_number(context.get('scale_readiness_weight', 0.7))
    offset = finite_number(context.get('metric_scale_readiness_09_offset', 0.08))
    return bounded(base * weight + offset)

def metric_scale_readiness_10(record: DomainRecord, context: Mapping[str, Any]) -> float:
    base = _signal(record, ('implementation_intensity', 'missing_rate', 'affected_group', 'jurisdiction_level'), 17)
    weight = finite_number(context.get('scale_readiness_weight', 0.7999999999999999))
    offset = finite_number(context.get('metric_scale_readiness_10_offset', 0.1))
    return bounded(base * weight + offset)

METRICS: dict[str, MetricFunction] = {
    'metric_learning_gain_01': metric_learning_gain_01,
    'metric_learning_gain_02': metric_learning_gain_02,
    'metric_learning_gain_03': metric_learning_gain_03,
    'metric_learning_gain_04': metric_learning_gain_04,
    'metric_learning_gain_05': metric_learning_gain_05,
    'metric_learning_gain_06': metric_learning_gain_06,
    'metric_learning_gain_07': metric_learning_gain_07,
    'metric_learning_gain_08': metric_learning_gain_08,
    'metric_learning_gain_09': metric_learning_gain_09,
    'metric_learning_gain_10': metric_learning_gain_10,
    'metric_engagement_comparability_01': metric_engagement_comparability_01,
    'metric_engagement_comparability_02': metric_engagement_comparability_02,
    'metric_engagement_comparability_03': metric_engagement_comparability_03,
    'metric_engagement_comparability_04': metric_engagement_comparability_04,
    'metric_engagement_comparability_05': metric_engagement_comparability_05,
    'metric_engagement_comparability_06': metric_engagement_comparability_06,
    'metric_engagement_comparability_07': metric_engagement_comparability_07,
    'metric_engagement_comparability_08': metric_engagement_comparability_08,
    'metric_engagement_comparability_09': metric_engagement_comparability_09,
    'metric_engagement_comparability_10': metric_engagement_comparability_10,
    'metric_attrition_bias_01': metric_attrition_bias_01,
    'metric_attrition_bias_02': metric_attrition_bias_02,
    'metric_attrition_bias_03': metric_attrition_bias_03,
    'metric_attrition_bias_04': metric_attrition_bias_04,
    'metric_attrition_bias_05': metric_attrition_bias_05,
    'metric_attrition_bias_06': metric_attrition_bias_06,
    'metric_attrition_bias_07': metric_attrition_bias_07,
    'metric_attrition_bias_08': metric_attrition_bias_08,
    'metric_attrition_bias_09': metric_attrition_bias_09,
    'metric_attrition_bias_10': metric_attrition_bias_10,
    'metric_equity_gap_01': metric_equity_gap_01,
    'metric_equity_gap_02': metric_equity_gap_02,
    'metric_equity_gap_03': metric_equity_gap_03,
    'metric_equity_gap_04': metric_equity_gap_04,
    'metric_equity_gap_05': metric_equity_gap_05,
    'metric_equity_gap_06': metric_equity_gap_06,
    'metric_equity_gap_07': metric_equity_gap_07,
    'metric_equity_gap_08': metric_equity_gap_08,
    'metric_equity_gap_09': metric_equity_gap_09,
    'metric_equity_gap_10': metric_equity_gap_10,
    'metric_teacher_dependency_01': metric_teacher_dependency_01,
    'metric_teacher_dependency_02': metric_teacher_dependency_02,
    'metric_teacher_dependency_03': metric_teacher_dependency_03,
    'metric_teacher_dependency_04': metric_teacher_dependency_04,
    'metric_teacher_dependency_05': metric_teacher_dependency_05,
    'metric_teacher_dependency_06': metric_teacher_dependency_06,
    'metric_teacher_dependency_07': metric_teacher_dependency_07,
    'metric_teacher_dependency_08': metric_teacher_dependency_08,
    'metric_teacher_dependency_09': metric_teacher_dependency_09,
    'metric_teacher_dependency_10': metric_teacher_dependency_10,
    'metric_digital_capacity_resilience_01': metric_digital_capacity_resilience_01,
    'metric_digital_capacity_resilience_02': metric_digital_capacity_resilience_02,
    'metric_digital_capacity_resilience_03': metric_digital_capacity_resilience_03,
    'metric_digital_capacity_resilience_04': metric_digital_capacity_resilience_04,
    'metric_digital_capacity_resilience_05': metric_digital_capacity_resilience_05,
    'metric_digital_capacity_resilience_06': metric_digital_capacity_resilience_06,
    'metric_digital_capacity_resilience_07': metric_digital_capacity_resilience_07,
    'metric_digital_capacity_resilience_08': metric_digital_capacity_resilience_08,
    'metric_digital_capacity_resilience_09': metric_digital_capacity_resilience_09,
    'metric_digital_capacity_resilience_10': metric_digital_capacity_resilience_10,
    'metric_effect_persistence_01': metric_effect_persistence_01,
    'metric_effect_persistence_02': metric_effect_persistence_02,
    'metric_effect_persistence_03': metric_effect_persistence_03,
    'metric_effect_persistence_04': metric_effect_persistence_04,
    'metric_effect_persistence_05': metric_effect_persistence_05,
    'metric_effect_persistence_06': metric_effect_persistence_06,
    'metric_effect_persistence_07': metric_effect_persistence_07,
    'metric_effect_persistence_08': metric_effect_persistence_08,
    'metric_effect_persistence_09': metric_effect_persistence_09,
    'metric_effect_persistence_10': metric_effect_persistence_10,
    'metric_scale_readiness_01': metric_scale_readiness_01,
    'metric_scale_readiness_02': metric_scale_readiness_02,
    'metric_scale_readiness_03': metric_scale_readiness_03,
    'metric_scale_readiness_04': metric_scale_readiness_04,
    'metric_scale_readiness_05': metric_scale_readiness_05,
    'metric_scale_readiness_06': metric_scale_readiness_06,
    'metric_scale_readiness_07': metric_scale_readiness_07,
    'metric_scale_readiness_08': metric_scale_readiness_08,
    'metric_scale_readiness_09': metric_scale_readiness_09,
    'metric_scale_readiness_10': metric_scale_readiness_10,
}

def metric_vector(record: DomainRecord, context: Mapping[str, Any] | None = None) -> dict[str, float]:
    context = context or {}
    return {name: function(record, context) for name, function in METRICS.items()}

def grouped_metrics(record: DomainRecord, context: Mapping[str, Any] | None = None) -> dict[str, float]:
    vector = metric_vector(record, context)
    groups: dict[str, list[float]] = defaultdict(list)
    for name, value in vector.items():
        key = name.rsplit('_', 1)[0].removeprefix('metric_')
        groups[key].append(value)
    return {key: statistics.fmean(values) for key, values in groups.items()}

def record_score(record: DomainRecord, context: Mapping[str, Any] | None = None) -> dict[str, Any]:
    context = context or {}
    rules = evaluate(record, context)
    rule_summary = summarize(rules)
    metrics = grouped_metrics(record, context)
    metric_score = statistics.fmean(metrics.values()) if metrics else 0.0
    effect = adjusted_effect(record)
    effect_component = bounded(0.5 + effect['adjusted'] * 0.5)
    combined = bounded(rule_summary['score'] * 0.45 + metric_score * 0.35 + effect_component * 0.20)
    return {'score': combined, 'rule_summary': rule_summary, 'metrics': metrics, 'effect': effect,
            'fingerprint': stable_hash({'record': record.fingerprint, 'metrics': metrics,
                                        'rules': rule_summary, 'effect': effect['adjusted'],
                                        'effect_verdict': effect['verdict']})}

def portfolio(records: Iterable[DomainRecord], context: Mapping[str, Any] | None = None) -> dict[str, Any]:
    rows = [record_score(record, context) | {'record_id': record.record_id} for record in records]
    if not rows:
        return {'count': 0, 'average': 0.0, 'minimum': 0.0, 'maximum': 0.0, 'rows': []}
    scores = [row['score'] for row in rows]
    return {'count': len(rows), 'average': statistics.fmean(scores),
            'minimum': min(scores), 'maximum': max(scores), 'rows': sorted(rows, key=lambda row: (-row['score'], row['record_id']))}

def compare(left: DomainRecord, right: DomainRecord, context: Mapping[str, Any] | None = None) -> dict[str, Any]:
    left_metrics = grouped_metrics(left, context)
    right_metrics = grouped_metrics(right, context)
    delta = {key: right_metrics.get(key, 0.0) - left_metrics.get(key, 0.0) for key in sorted(set(left_metrics) | set(right_metrics))}
    left_effect = adjusted_effect(left)
    right_effect = adjusted_effect(right)
    effect_delta = right_effect['adjusted'] - left_effect['adjusted']
    return {'left': left.record_id, 'right': right.record_id, 'delta': delta,
            'effect': {'left': left_effect, 'right': right_effect, 'delta': effect_delta},
            'winner': right.record_id if effect_delta >= 0 else left.record_id,
            'direction': right_effect['direction'], 'confirmed': right_effect['confirmed']}
