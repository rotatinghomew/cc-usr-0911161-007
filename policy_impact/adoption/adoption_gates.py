from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping

from policy_impact.measures.policy_contract import ContractError, Decision, DomainRecord, RuleResult, bounded
from policy_impact.analysis.effect_model import grouped_metrics, record_score
from policy_impact.comparability.evidence_gate import evaluate

STATES = ['registered', 'baselined', 'modeled', 'consulted', 'adopted', 'reviewed']
TRANSITIONS = {state: tuple(STATES[i + 1:i + 3]) for i, state in enumerate(STATES)}

@dataclass(frozen=True)
class TransitionPlan:
    from_state: str
    to_state: str
    allowed: bool
    reasons: tuple[str, ...]
    score: float

def allowed_targets(state: str) -> tuple[str, ...]:
    if state not in TRANSITIONS:
        raise ContractError('unknown workflow state')
    return TRANSITIONS[state]

def plan_transition(record: DomainRecord, target: str, context: Mapping[str, Any] | None = None) -> TransitionPlan:
    context = context or {}
    if target not in STATES:
        raise ContractError('unknown target state')
    impact_brief = record_score(record, context)
    reasons: list[str] = []
    structurally_allowed = target in allowed_targets(record.state)
    if not structurally_allowed:
        reasons.append('transition is not adjacent in the lifecycle')
    threshold = float(context.get('transition_threshold', 0.42))
    if impact_brief['score'] < threshold:
        reasons.append('record score is below the transition threshold')
    return TransitionPlan(record.state, target, structurally_allowed and not reasons, tuple(reasons or ['eligible']), impact_brief['score'])

def apply_transition(record: DomainRecord, target: str, context: Mapping[str, Any] | None = None) -> DomainRecord:
    plan = plan_transition(record, target, context)
    if not plan.allowed:
        raise ContractError('; '.join(plan.reasons))
    return record.with_state(target)

def guard_policy_code_learning_gain_01(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('learning_gain', 0.0)
    floor = float(context.get('guard_policy_code_learning_gain_01_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('baselined')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_policy_code_learning_gain_01' + (':passed' if allowed else ':blocked')

def guard_jurisdiction_level_engagement_comparability_02(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('engagement_comparability', 0.0)
    floor = float(context.get('guard_jurisdiction_level_engagement_comparability_02_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('modeled')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_jurisdiction_level_engagement_comparability_02' + (':passed' if allowed else ':blocked')

def guard_measure_type_attrition_bias_03(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('attrition_bias', 0.0)
    floor = float(context.get('guard_measure_type_attrition_bias_03_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('consulted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_measure_type_attrition_bias_03' + (':passed' if allowed else ':blocked')

def guard_covered_entities_equity_gap_04(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('equity_gap', 0.0)
    floor = float(context.get('guard_covered_entities_equity_gap_04_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('adopted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_covered_entities_equity_gap_04' + (':passed' if allowed else ':blocked')

def guard_implementation_intensity_teacher_dependency_05(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('teacher_dependency', 0.0)
    floor = float(context.get('guard_implementation_intensity_teacher_dependency_05_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('reviewed')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_implementation_intensity_teacher_dependency_05' + (':passed' if allowed else ':blocked')

def guard_baseline_risk_digital_capacity_resilience_06(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('digital_capacity_resilience', 0.0)
    floor = float(context.get('guard_baseline_risk_digital_capacity_resilience_06_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('baselined')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_baseline_risk_digital_capacity_resilience_06' + (':passed' if allowed else ':blocked')

def guard_post_risk_effect_persistence_07(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('effect_persistence', 0.0)
    floor = float(context.get('guard_post_risk_effect_persistence_07_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('modeled')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_post_risk_effect_persistence_07' + (':passed' if allowed else ':blocked')

def guard_missing_rate_scale_readiness_08(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('scale_readiness', 0.0)
    floor = float(context.get('guard_missing_rate_scale_readiness_08_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('consulted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_missing_rate_scale_readiness_08' + (':passed' if allowed else ':blocked')

def guard_enforcement_support_learning_gain_09(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('learning_gain', 0.0)
    floor = float(context.get('guard_enforcement_support_learning_gain_09_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('adopted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_enforcement_support_learning_gain_09' + (':passed' if allowed else ':blocked')

def guard_digital_capacity_engagement_comparability_10(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('engagement_comparability', 0.0)
    floor = float(context.get('guard_digital_capacity_engagement_comparability_10_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('reviewed')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_digital_capacity_engagement_comparability_10' + (':passed' if allowed else ':blocked')

def guard_affected_group_attrition_bias_11(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('attrition_bias', 0.0)
    floor = float(context.get('guard_affected_group_attrition_bias_11_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('baselined')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_affected_group_attrition_bias_11' + (':passed' if allowed else ':blocked')

def guard_consultation_coverage_equity_gap_12(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('equity_gap', 0.0)
    floor = float(context.get('guard_consultation_coverage_equity_gap_12_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('modeled')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_consultation_coverage_equity_gap_12' + (':passed' if allowed else ':blocked')

def guard_policy_code_teacher_dependency_13(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('teacher_dependency', 0.0)
    floor = float(context.get('guard_policy_code_teacher_dependency_13_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('consulted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_policy_code_teacher_dependency_13' + (':passed' if allowed else ':blocked')

def guard_jurisdiction_level_digital_capacity_resilience_14(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('digital_capacity_resilience', 0.0)
    floor = float(context.get('guard_jurisdiction_level_digital_capacity_resilience_14_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('adopted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_jurisdiction_level_digital_capacity_resilience_14' + (':passed' if allowed else ':blocked')

def guard_measure_type_effect_persistence_15(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('effect_persistence', 0.0)
    floor = float(context.get('guard_measure_type_effect_persistence_15_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('reviewed')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_measure_type_effect_persistence_15' + (':passed' if allowed else ':blocked')

def guard_covered_entities_scale_readiness_16(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('scale_readiness', 0.0)
    floor = float(context.get('guard_covered_entities_scale_readiness_16_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('baselined')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_covered_entities_scale_readiness_16' + (':passed' if allowed else ':blocked')

def guard_implementation_intensity_learning_gain_17(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('learning_gain', 0.0)
    floor = float(context.get('guard_implementation_intensity_learning_gain_17_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('modeled')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_implementation_intensity_learning_gain_17' + (':passed' if allowed else ':blocked')

def guard_baseline_risk_engagement_comparability_18(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('engagement_comparability', 0.0)
    floor = float(context.get('guard_baseline_risk_engagement_comparability_18_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('consulted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_baseline_risk_engagement_comparability_18' + (':passed' if allowed else ':blocked')

def guard_post_risk_attrition_bias_19(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('attrition_bias', 0.0)
    floor = float(context.get('guard_post_risk_attrition_bias_19_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('adopted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_post_risk_attrition_bias_19' + (':passed' if allowed else ':blocked')

def guard_missing_rate_equity_gap_20(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('equity_gap', 0.0)
    floor = float(context.get('guard_missing_rate_equity_gap_20_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('reviewed')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_missing_rate_equity_gap_20' + (':passed' if allowed else ':blocked')

def guard_enforcement_support_teacher_dependency_21(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('teacher_dependency', 0.0)
    floor = float(context.get('guard_enforcement_support_teacher_dependency_21_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('baselined')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_enforcement_support_teacher_dependency_21' + (':passed' if allowed else ':blocked')

def guard_digital_capacity_digital_capacity_resilience_22(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('digital_capacity_resilience', 0.0)
    floor = float(context.get('guard_digital_capacity_digital_capacity_resilience_22_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('modeled')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_digital_capacity_digital_capacity_resilience_22' + (':passed' if allowed else ':blocked')

def guard_affected_group_effect_persistence_23(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('effect_persistence', 0.0)
    floor = float(context.get('guard_affected_group_effect_persistence_23_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('consulted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_affected_group_effect_persistence_23' + (':passed' if allowed else ':blocked')

def guard_consultation_coverage_scale_readiness_24(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('scale_readiness', 0.0)
    floor = float(context.get('guard_consultation_coverage_scale_readiness_24_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('adopted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_consultation_coverage_scale_readiness_24' + (':passed' if allowed else ':blocked')

def guard_policy_code_learning_gain_25(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('learning_gain', 0.0)
    floor = float(context.get('guard_policy_code_learning_gain_25_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('reviewed')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_policy_code_learning_gain_25' + (':passed' if allowed else ':blocked')

def guard_jurisdiction_level_engagement_comparability_26(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('engagement_comparability', 0.0)
    floor = float(context.get('guard_jurisdiction_level_engagement_comparability_26_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('baselined')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_jurisdiction_level_engagement_comparability_26' + (':passed' if allowed else ':blocked')

def guard_measure_type_attrition_bias_27(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('attrition_bias', 0.0)
    floor = float(context.get('guard_measure_type_attrition_bias_27_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('modeled')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_measure_type_attrition_bias_27' + (':passed' if allowed else ':blocked')

def guard_covered_entities_equity_gap_28(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('equity_gap', 0.0)
    floor = float(context.get('guard_covered_entities_equity_gap_28_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('consulted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_covered_entities_equity_gap_28' + (':passed' if allowed else ':blocked')

def guard_implementation_intensity_teacher_dependency_29(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('teacher_dependency', 0.0)
    floor = float(context.get('guard_implementation_intensity_teacher_dependency_29_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('adopted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_implementation_intensity_teacher_dependency_29' + (':passed' if allowed else ':blocked')

def guard_baseline_risk_digital_capacity_resilience_30(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('digital_capacity_resilience', 0.0)
    floor = float(context.get('guard_baseline_risk_digital_capacity_resilience_30_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('reviewed')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_baseline_risk_digital_capacity_resilience_30' + (':passed' if allowed else ':blocked')

def guard_post_risk_effect_persistence_31(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('effect_persistence', 0.0)
    floor = float(context.get('guard_post_risk_effect_persistence_31_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('baselined')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_post_risk_effect_persistence_31' + (':passed' if allowed else ':blocked')

def guard_missing_rate_scale_readiness_32(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('scale_readiness', 0.0)
    floor = float(context.get('guard_missing_rate_scale_readiness_32_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('modeled')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_missing_rate_scale_readiness_32' + (':passed' if allowed else ':blocked')

def guard_enforcement_support_learning_gain_33(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('learning_gain', 0.0)
    floor = float(context.get('guard_enforcement_support_learning_gain_33_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('consulted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_enforcement_support_learning_gain_33' + (':passed' if allowed else ':blocked')

def guard_digital_capacity_engagement_comparability_34(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('engagement_comparability', 0.0)
    floor = float(context.get('guard_digital_capacity_engagement_comparability_34_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('adopted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_digital_capacity_engagement_comparability_34' + (':passed' if allowed else ':blocked')

def guard_affected_group_attrition_bias_35(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('attrition_bias', 0.0)
    floor = float(context.get('guard_affected_group_attrition_bias_35_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('reviewed')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_affected_group_attrition_bias_35' + (':passed' if allowed else ':blocked')

def guard_consultation_coverage_equity_gap_36(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('equity_gap', 0.0)
    floor = float(context.get('guard_consultation_coverage_equity_gap_36_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('baselined')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_consultation_coverage_equity_gap_36' + (':passed' if allowed else ':blocked')

def guard_policy_code_teacher_dependency_37(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('teacher_dependency', 0.0)
    floor = float(context.get('guard_policy_code_teacher_dependency_37_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('modeled')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_policy_code_teacher_dependency_37' + (':passed' if allowed else ':blocked')

def guard_jurisdiction_level_digital_capacity_resilience_38(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('digital_capacity_resilience', 0.0)
    floor = float(context.get('guard_jurisdiction_level_digital_capacity_resilience_38_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('consulted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_jurisdiction_level_digital_capacity_resilience_38' + (':passed' if allowed else ':blocked')

def guard_measure_type_effect_persistence_39(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('effect_persistence', 0.0)
    floor = float(context.get('guard_measure_type_effect_persistence_39_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('adopted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_measure_type_effect_persistence_39' + (':passed' if allowed else ':blocked')

def guard_covered_entities_scale_readiness_40(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('scale_readiness', 0.0)
    floor = float(context.get('guard_covered_entities_scale_readiness_40_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('reviewed')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_covered_entities_scale_readiness_40' + (':passed' if allowed else ':blocked')

def guard_implementation_intensity_learning_gain_41(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('learning_gain', 0.0)
    floor = float(context.get('guard_implementation_intensity_learning_gain_41_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('baselined')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_implementation_intensity_learning_gain_41' + (':passed' if allowed else ':blocked')

def guard_baseline_risk_engagement_comparability_42(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('engagement_comparability', 0.0)
    floor = float(context.get('guard_baseline_risk_engagement_comparability_42_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('modeled')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_baseline_risk_engagement_comparability_42' + (':passed' if allowed else ':blocked')

def guard_post_risk_attrition_bias_43(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('attrition_bias', 0.0)
    floor = float(context.get('guard_post_risk_attrition_bias_43_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('consulted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_post_risk_attrition_bias_43' + (':passed' if allowed else ':blocked')

def guard_missing_rate_equity_gap_44(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('equity_gap', 0.0)
    floor = float(context.get('guard_missing_rate_equity_gap_44_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('adopted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_missing_rate_equity_gap_44' + (':passed' if allowed else ':blocked')

def guard_enforcement_support_teacher_dependency_45(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('teacher_dependency', 0.0)
    floor = float(context.get('guard_enforcement_support_teacher_dependency_45_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('reviewed')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_enforcement_support_teacher_dependency_45' + (':passed' if allowed else ':blocked')

def guard_digital_capacity_digital_capacity_resilience_46(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('digital_capacity_resilience', 0.0)
    floor = float(context.get('guard_digital_capacity_digital_capacity_resilience_46_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('baselined')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_digital_capacity_digital_capacity_resilience_46' + (':passed' if allowed else ':blocked')

def guard_affected_group_effect_persistence_47(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('effect_persistence', 0.0)
    floor = float(context.get('guard_affected_group_effect_persistence_47_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('modeled')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_affected_group_effect_persistence_47' + (':passed' if allowed else ':blocked')

def guard_consultation_coverage_scale_readiness_48(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('scale_readiness', 0.0)
    floor = float(context.get('guard_consultation_coverage_scale_readiness_48_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('consulted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_consultation_coverage_scale_readiness_48' + (':passed' if allowed else ':blocked')

def guard_policy_code_learning_gain_49(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('learning_gain', 0.0)
    floor = float(context.get('guard_policy_code_learning_gain_49_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('adopted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_policy_code_learning_gain_49' + (':passed' if allowed else ':blocked')

def guard_jurisdiction_level_engagement_comparability_50(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('engagement_comparability', 0.0)
    floor = float(context.get('guard_jurisdiction_level_engagement_comparability_50_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('reviewed')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_jurisdiction_level_engagement_comparability_50' + (':passed' if allowed else ':blocked')

def guard_measure_type_attrition_bias_51(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('attrition_bias', 0.0)
    floor = float(context.get('guard_measure_type_attrition_bias_51_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('baselined')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_measure_type_attrition_bias_51' + (':passed' if allowed else ':blocked')

def guard_covered_entities_equity_gap_52(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('equity_gap', 0.0)
    floor = float(context.get('guard_covered_entities_equity_gap_52_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('modeled')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_covered_entities_equity_gap_52' + (':passed' if allowed else ':blocked')

def guard_implementation_intensity_teacher_dependency_53(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('teacher_dependency', 0.0)
    floor = float(context.get('guard_implementation_intensity_teacher_dependency_53_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('consulted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_implementation_intensity_teacher_dependency_53' + (':passed' if allowed else ':blocked')

def guard_baseline_risk_digital_capacity_resilience_54(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('digital_capacity_resilience', 0.0)
    floor = float(context.get('guard_baseline_risk_digital_capacity_resilience_54_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('adopted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_baseline_risk_digital_capacity_resilience_54' + (':passed' if allowed else ':blocked')

def guard_post_risk_effect_persistence_55(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('effect_persistence', 0.0)
    floor = float(context.get('guard_post_risk_effect_persistence_55_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('reviewed')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_post_risk_effect_persistence_55' + (':passed' if allowed else ':blocked')

def guard_missing_rate_scale_readiness_56(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('scale_readiness', 0.0)
    floor = float(context.get('guard_missing_rate_scale_readiness_56_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('baselined')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_missing_rate_scale_readiness_56' + (':passed' if allowed else ':blocked')

def guard_enforcement_support_learning_gain_57(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('learning_gain', 0.0)
    floor = float(context.get('guard_enforcement_support_learning_gain_57_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('modeled')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_enforcement_support_learning_gain_57' + (':passed' if allowed else ':blocked')

def guard_digital_capacity_engagement_comparability_58(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('engagement_comparability', 0.0)
    floor = float(context.get('guard_digital_capacity_engagement_comparability_58_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('consulted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_digital_capacity_engagement_comparability_58' + (':passed' if allowed else ':blocked')

def guard_affected_group_attrition_bias_59(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('attrition_bias', 0.0)
    floor = float(context.get('guard_affected_group_attrition_bias_59_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('adopted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_affected_group_attrition_bias_59' + (':passed' if allowed else ':blocked')

def guard_consultation_coverage_equity_gap_60(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('equity_gap', 0.0)
    floor = float(context.get('guard_consultation_coverage_equity_gap_60_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('reviewed')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_consultation_coverage_equity_gap_60' + (':passed' if allowed else ':blocked')

def guard_policy_code_teacher_dependency_61(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('teacher_dependency', 0.0)
    floor = float(context.get('guard_policy_code_teacher_dependency_61_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('baselined')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_policy_code_teacher_dependency_61' + (':passed' if allowed else ':blocked')

def guard_jurisdiction_level_digital_capacity_resilience_62(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('digital_capacity_resilience', 0.0)
    floor = float(context.get('guard_jurisdiction_level_digital_capacity_resilience_62_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('modeled')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_jurisdiction_level_digital_capacity_resilience_62' + (':passed' if allowed else ':blocked')

def guard_measure_type_effect_persistence_63(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('effect_persistence', 0.0)
    floor = float(context.get('guard_measure_type_effect_persistence_63_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('consulted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_measure_type_effect_persistence_63' + (':passed' if allowed else ':blocked')

def guard_covered_entities_scale_readiness_64(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('scale_readiness', 0.0)
    floor = float(context.get('guard_covered_entities_scale_readiness_64_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('adopted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_covered_entities_scale_readiness_64' + (':passed' if allowed else ':blocked')

def guard_implementation_intensity_learning_gain_65(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('learning_gain', 0.0)
    floor = float(context.get('guard_implementation_intensity_learning_gain_65_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('reviewed')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_implementation_intensity_learning_gain_65' + (':passed' if allowed else ':blocked')

def guard_baseline_risk_engagement_comparability_66(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('engagement_comparability', 0.0)
    floor = float(context.get('guard_baseline_risk_engagement_comparability_66_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('baselined')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_baseline_risk_engagement_comparability_66' + (':passed' if allowed else ':blocked')

def guard_post_risk_attrition_bias_67(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('attrition_bias', 0.0)
    floor = float(context.get('guard_post_risk_attrition_bias_67_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('modeled')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_post_risk_attrition_bias_67' + (':passed' if allowed else ':blocked')

def guard_missing_rate_equity_gap_68(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('equity_gap', 0.0)
    floor = float(context.get('guard_missing_rate_equity_gap_68_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('consulted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_missing_rate_equity_gap_68' + (':passed' if allowed else ':blocked')

def guard_enforcement_support_teacher_dependency_69(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('teacher_dependency', 0.0)
    floor = float(context.get('guard_enforcement_support_teacher_dependency_69_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('adopted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_enforcement_support_teacher_dependency_69' + (':passed' if allowed else ':blocked')

def guard_digital_capacity_digital_capacity_resilience_70(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('digital_capacity_resilience', 0.0)
    floor = float(context.get('guard_digital_capacity_digital_capacity_resilience_70_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('reviewed')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_digital_capacity_digital_capacity_resilience_70' + (':passed' if allowed else ':blocked')

def guard_affected_group_effect_persistence_71(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('effect_persistence', 0.0)
    floor = float(context.get('guard_affected_group_effect_persistence_71_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('baselined')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_affected_group_effect_persistence_71' + (':passed' if allowed else ':blocked')

def guard_consultation_coverage_scale_readiness_72(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('scale_readiness', 0.0)
    floor = float(context.get('guard_consultation_coverage_scale_readiness_72_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('modeled')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_consultation_coverage_scale_readiness_72' + (':passed' if allowed else ':blocked')

def guard_policy_code_learning_gain_73(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('learning_gain', 0.0)
    floor = float(context.get('guard_policy_code_learning_gain_73_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('consulted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_policy_code_learning_gain_73' + (':passed' if allowed else ':blocked')

def guard_jurisdiction_level_engagement_comparability_74(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('engagement_comparability', 0.0)
    floor = float(context.get('guard_jurisdiction_level_engagement_comparability_74_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('adopted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_jurisdiction_level_engagement_comparability_74' + (':passed' if allowed else ':blocked')

def guard_measure_type_attrition_bias_75(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('attrition_bias', 0.0)
    floor = float(context.get('guard_measure_type_attrition_bias_75_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('reviewed')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_measure_type_attrition_bias_75' + (':passed' if allowed else ':blocked')

def guard_covered_entities_equity_gap_76(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('equity_gap', 0.0)
    floor = float(context.get('guard_covered_entities_equity_gap_76_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('baselined')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_covered_entities_equity_gap_76' + (':passed' if allowed else ':blocked')

def guard_implementation_intensity_teacher_dependency_77(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('teacher_dependency', 0.0)
    floor = float(context.get('guard_implementation_intensity_teacher_dependency_77_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('modeled')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_implementation_intensity_teacher_dependency_77' + (':passed' if allowed else ':blocked')

def guard_baseline_risk_digital_capacity_resilience_78(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('digital_capacity_resilience', 0.0)
    floor = float(context.get('guard_baseline_risk_digital_capacity_resilience_78_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('consulted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_baseline_risk_digital_capacity_resilience_78' + (':passed' if allowed else ':blocked')

def guard_post_risk_effect_persistence_79(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('effect_persistence', 0.0)
    floor = float(context.get('guard_post_risk_effect_persistence_79_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('adopted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_post_risk_effect_persistence_79' + (':passed' if allowed else ':blocked')

def guard_missing_rate_scale_readiness_80(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('scale_readiness', 0.0)
    floor = float(context.get('guard_missing_rate_scale_readiness_80_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('reviewed')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_missing_rate_scale_readiness_80' + (':passed' if allowed else ':blocked')

def guard_enforcement_support_learning_gain_81(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('learning_gain', 0.0)
    floor = float(context.get('guard_enforcement_support_learning_gain_81_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('baselined')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_enforcement_support_learning_gain_81' + (':passed' if allowed else ':blocked')

def guard_digital_capacity_engagement_comparability_82(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('engagement_comparability', 0.0)
    floor = float(context.get('guard_digital_capacity_engagement_comparability_82_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('modeled')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_digital_capacity_engagement_comparability_82' + (':passed' if allowed else ':blocked')

def guard_affected_group_attrition_bias_83(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('attrition_bias', 0.0)
    floor = float(context.get('guard_affected_group_attrition_bias_83_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('consulted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_affected_group_attrition_bias_83' + (':passed' if allowed else ':blocked')

def guard_consultation_coverage_equity_gap_84(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('equity_gap', 0.0)
    floor = float(context.get('guard_consultation_coverage_equity_gap_84_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('adopted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_consultation_coverage_equity_gap_84' + (':passed' if allowed else ':blocked')

def guard_policy_code_teacher_dependency_85(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('teacher_dependency', 0.0)
    floor = float(context.get('guard_policy_code_teacher_dependency_85_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('reviewed')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_policy_code_teacher_dependency_85' + (':passed' if allowed else ':blocked')

def guard_jurisdiction_level_digital_capacity_resilience_86(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('digital_capacity_resilience', 0.0)
    floor = float(context.get('guard_jurisdiction_level_digital_capacity_resilience_86_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('baselined')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_jurisdiction_level_digital_capacity_resilience_86' + (':passed' if allowed else ':blocked')

def guard_measure_type_effect_persistence_87(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('effect_persistence', 0.0)
    floor = float(context.get('guard_measure_type_effect_persistence_87_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('modeled')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_measure_type_effect_persistence_87' + (':passed' if allowed else ':blocked')

def guard_covered_entities_scale_readiness_88(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('scale_readiness', 0.0)
    floor = float(context.get('guard_covered_entities_scale_readiness_88_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('consulted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_covered_entities_scale_readiness_88' + (':passed' if allowed else ':blocked')

def guard_implementation_intensity_learning_gain_89(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('learning_gain', 0.0)
    floor = float(context.get('guard_implementation_intensity_learning_gain_89_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('adopted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_implementation_intensity_learning_gain_89' + (':passed' if allowed else ':blocked')

def guard_baseline_risk_engagement_comparability_90(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('engagement_comparability', 0.0)
    floor = float(context.get('guard_baseline_risk_engagement_comparability_90_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('reviewed')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_baseline_risk_engagement_comparability_90' + (':passed' if allowed else ':blocked')

def guard_post_risk_attrition_bias_91(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('attrition_bias', 0.0)
    floor = float(context.get('guard_post_risk_attrition_bias_91_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('baselined')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_post_risk_attrition_bias_91' + (':passed' if allowed else ':blocked')

def guard_missing_rate_equity_gap_92(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('equity_gap', 0.0)
    floor = float(context.get('guard_missing_rate_equity_gap_92_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('modeled')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_missing_rate_equity_gap_92' + (':passed' if allowed else ':blocked')

def guard_enforcement_support_teacher_dependency_93(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('teacher_dependency', 0.0)
    floor = float(context.get('guard_enforcement_support_teacher_dependency_93_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('consulted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_enforcement_support_teacher_dependency_93' + (':passed' if allowed else ':blocked')

def guard_digital_capacity_digital_capacity_resilience_94(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('digital_capacity_resilience', 0.0)
    floor = float(context.get('guard_digital_capacity_digital_capacity_resilience_94_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('adopted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_digital_capacity_digital_capacity_resilience_94' + (':passed' if allowed else ':blocked')

def guard_affected_group_effect_persistence_95(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('effect_persistence', 0.0)
    floor = float(context.get('guard_affected_group_effect_persistence_95_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('reviewed')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_affected_group_effect_persistence_95' + (':passed' if allowed else ':blocked')

def guard_consultation_coverage_scale_readiness_96(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('scale_readiness', 0.0)
    floor = float(context.get('guard_consultation_coverage_scale_readiness_96_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('baselined')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_consultation_coverage_scale_readiness_96' + (':passed' if allowed else ':blocked')

def guard_policy_code_learning_gain_97(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('learning_gain', 0.0)
    floor = float(context.get('guard_policy_code_learning_gain_97_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('modeled')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_policy_code_learning_gain_97' + (':passed' if allowed else ':blocked')

def guard_jurisdiction_level_engagement_comparability_98(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('engagement_comparability', 0.0)
    floor = float(context.get('guard_jurisdiction_level_engagement_comparability_98_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('consulted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_jurisdiction_level_engagement_comparability_98' + (':passed' if allowed else ':blocked')

def guard_measure_type_attrition_bias_99(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('attrition_bias', 0.0)
    floor = float(context.get('guard_measure_type_attrition_bias_99_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('adopted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_measure_type_attrition_bias_99' + (':passed' if allowed else ':blocked')

def guard_covered_entities_equity_gap_100(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('equity_gap', 0.0)
    floor = float(context.get('guard_covered_entities_equity_gap_100_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('reviewed')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_covered_entities_equity_gap_100' + (':passed' if allowed else ':blocked')

def guard_implementation_intensity_teacher_dependency_101(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('teacher_dependency', 0.0)
    floor = float(context.get('guard_implementation_intensity_teacher_dependency_101_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('baselined')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_implementation_intensity_teacher_dependency_101' + (':passed' if allowed else ':blocked')

def guard_baseline_risk_digital_capacity_resilience_102(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('digital_capacity_resilience', 0.0)
    floor = float(context.get('guard_baseline_risk_digital_capacity_resilience_102_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('modeled')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_baseline_risk_digital_capacity_resilience_102' + (':passed' if allowed else ':blocked')

def guard_post_risk_effect_persistence_103(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('effect_persistence', 0.0)
    floor = float(context.get('guard_post_risk_effect_persistence_103_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('consulted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_post_risk_effect_persistence_103' + (':passed' if allowed else ':blocked')

def guard_missing_rate_scale_readiness_104(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('scale_readiness', 0.0)
    floor = float(context.get('guard_missing_rate_scale_readiness_104_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('adopted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_missing_rate_scale_readiness_104' + (':passed' if allowed else ':blocked')

def guard_enforcement_support_learning_gain_105(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('learning_gain', 0.0)
    floor = float(context.get('guard_enforcement_support_learning_gain_105_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('reviewed')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_enforcement_support_learning_gain_105' + (':passed' if allowed else ':blocked')

def guard_digital_capacity_engagement_comparability_106(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('engagement_comparability', 0.0)
    floor = float(context.get('guard_digital_capacity_engagement_comparability_106_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('baselined')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_digital_capacity_engagement_comparability_106' + (':passed' if allowed else ':blocked')

def guard_affected_group_attrition_bias_107(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('attrition_bias', 0.0)
    floor = float(context.get('guard_affected_group_attrition_bias_107_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('modeled')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_affected_group_attrition_bias_107' + (':passed' if allowed else ':blocked')

def guard_consultation_coverage_equity_gap_108(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('equity_gap', 0.0)
    floor = float(context.get('guard_consultation_coverage_equity_gap_108_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('consulted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_consultation_coverage_equity_gap_108' + (':passed' if allowed else ':blocked')

def guard_policy_code_teacher_dependency_109(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('teacher_dependency', 0.0)
    floor = float(context.get('guard_policy_code_teacher_dependency_109_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('adopted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_policy_code_teacher_dependency_109' + (':passed' if allowed else ':blocked')

def guard_jurisdiction_level_digital_capacity_resilience_110(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('digital_capacity_resilience', 0.0)
    floor = float(context.get('guard_jurisdiction_level_digital_capacity_resilience_110_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('reviewed')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_jurisdiction_level_digital_capacity_resilience_110' + (':passed' if allowed else ':blocked')

def guard_measure_type_effect_persistence_111(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('effect_persistence', 0.0)
    floor = float(context.get('guard_measure_type_effect_persistence_111_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('baselined')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_measure_type_effect_persistence_111' + (':passed' if allowed else ':blocked')

def guard_covered_entities_scale_readiness_112(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('scale_readiness', 0.0)
    floor = float(context.get('guard_covered_entities_scale_readiness_112_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('modeled')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_covered_entities_scale_readiness_112' + (':passed' if allowed else ':blocked')

def guard_implementation_intensity_learning_gain_113(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('learning_gain', 0.0)
    floor = float(context.get('guard_implementation_intensity_learning_gain_113_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('consulted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_implementation_intensity_learning_gain_113' + (':passed' if allowed else ':blocked')

def guard_baseline_risk_engagement_comparability_114(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('engagement_comparability', 0.0)
    floor = float(context.get('guard_baseline_risk_engagement_comparability_114_floor', 0.32))
    state_ok = STATES.index(record.state) <= STATES.index('adopted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_baseline_risk_engagement_comparability_114' + (':passed' if allowed else ':blocked')

def guard_post_risk_attrition_bias_115(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('attrition_bias', 0.0)
    floor = float(context.get('guard_post_risk_attrition_bias_115_floor', 0.39))
    state_ok = STATES.index(record.state) <= STATES.index('reviewed')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_post_risk_attrition_bias_115' + (':passed' if allowed else ':blocked')

def guard_missing_rate_equity_gap_116(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('equity_gap', 0.0)
    floor = float(context.get('guard_missing_rate_equity_gap_116_floor', 0.46))
    state_ok = STATES.index(record.state) <= STATES.index('baselined')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_missing_rate_equity_gap_116' + (':passed' if allowed else ':blocked')

def guard_enforcement_support_teacher_dependency_117(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('teacher_dependency', 0.0)
    floor = float(context.get('guard_enforcement_support_teacher_dependency_117_floor', 0.53))
    state_ok = STATES.index(record.state) <= STATES.index('modeled')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_enforcement_support_teacher_dependency_117' + (':passed' if allowed else ':blocked')

def guard_digital_capacity_digital_capacity_resilience_118(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('digital_capacity_resilience', 0.0)
    floor = float(context.get('guard_digital_capacity_digital_capacity_resilience_118_floor', 0.6000000000000001))
    state_ok = STATES.index(record.state) <= STATES.index('consulted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_digital_capacity_digital_capacity_resilience_118' + (':passed' if allowed else ':blocked')

def guard_affected_group_effect_persistence_119(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('effect_persistence', 0.0)
    floor = float(context.get('guard_affected_group_effect_persistence_119_floor', 0.67))
    state_ok = STATES.index(record.state) <= STATES.index('adopted')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_affected_group_effect_persistence_119' + (':passed' if allowed else ':blocked')

def guard_consultation_coverage_scale_readiness_120(record: DomainRecord, context: Mapping[str, Any]) -> tuple[bool, str]:
    metrics = context.get('_metrics') or grouped_metrics(record, context)
    value = metrics.get('scale_readiness', 0.0)
    floor = float(context.get('guard_consultation_coverage_scale_readiness_120_floor', 0.25))
    state_ok = STATES.index(record.state) <= STATES.index('reviewed')
    allowed = state_ok and value >= min(1.0, floor)
    return allowed, 'guard_consultation_coverage_scale_readiness_120' + (':passed' if allowed else ':blocked')

GUARDS: tuple[Callable[[DomainRecord, Mapping[str, Any]], tuple[bool, str]], ...] = (
    guard_policy_code_learning_gain_01,
    guard_jurisdiction_level_engagement_comparability_02,
    guard_measure_type_attrition_bias_03,
    guard_covered_entities_equity_gap_04,
    guard_implementation_intensity_teacher_dependency_05,
    guard_baseline_risk_digital_capacity_resilience_06,
    guard_post_risk_effect_persistence_07,
    guard_missing_rate_scale_readiness_08,
    guard_enforcement_support_learning_gain_09,
    guard_digital_capacity_engagement_comparability_10,
    guard_affected_group_attrition_bias_11,
    guard_consultation_coverage_equity_gap_12,
    guard_policy_code_teacher_dependency_13,
    guard_jurisdiction_level_digital_capacity_resilience_14,
    guard_measure_type_effect_persistence_15,
    guard_covered_entities_scale_readiness_16,
    guard_implementation_intensity_learning_gain_17,
    guard_baseline_risk_engagement_comparability_18,
    guard_post_risk_attrition_bias_19,
    guard_missing_rate_equity_gap_20,
    guard_enforcement_support_teacher_dependency_21,
    guard_digital_capacity_digital_capacity_resilience_22,
    guard_affected_group_effect_persistence_23,
    guard_consultation_coverage_scale_readiness_24,
    guard_policy_code_learning_gain_25,
    guard_jurisdiction_level_engagement_comparability_26,
    guard_measure_type_attrition_bias_27,
    guard_covered_entities_equity_gap_28,
    guard_implementation_intensity_teacher_dependency_29,
    guard_baseline_risk_digital_capacity_resilience_30,
    guard_post_risk_effect_persistence_31,
    guard_missing_rate_scale_readiness_32,
    guard_enforcement_support_learning_gain_33,
    guard_digital_capacity_engagement_comparability_34,
    guard_affected_group_attrition_bias_35,
    guard_consultation_coverage_equity_gap_36,
    guard_policy_code_teacher_dependency_37,
    guard_jurisdiction_level_digital_capacity_resilience_38,
    guard_measure_type_effect_persistence_39,
    guard_covered_entities_scale_readiness_40,
    guard_implementation_intensity_learning_gain_41,
    guard_baseline_risk_engagement_comparability_42,
    guard_post_risk_attrition_bias_43,
    guard_missing_rate_equity_gap_44,
    guard_enforcement_support_teacher_dependency_45,
    guard_digital_capacity_digital_capacity_resilience_46,
    guard_affected_group_effect_persistence_47,
    guard_consultation_coverage_scale_readiness_48,
    guard_policy_code_learning_gain_49,
    guard_jurisdiction_level_engagement_comparability_50,
    guard_measure_type_attrition_bias_51,
    guard_covered_entities_equity_gap_52,
    guard_implementation_intensity_teacher_dependency_53,
    guard_baseline_risk_digital_capacity_resilience_54,
    guard_post_risk_effect_persistence_55,
    guard_missing_rate_scale_readiness_56,
    guard_enforcement_support_learning_gain_57,
    guard_digital_capacity_engagement_comparability_58,
    guard_affected_group_attrition_bias_59,
    guard_consultation_coverage_equity_gap_60,
    guard_policy_code_teacher_dependency_61,
    guard_jurisdiction_level_digital_capacity_resilience_62,
    guard_measure_type_effect_persistence_63,
    guard_covered_entities_scale_readiness_64,
    guard_implementation_intensity_learning_gain_65,
    guard_baseline_risk_engagement_comparability_66,
    guard_post_risk_attrition_bias_67,
    guard_missing_rate_equity_gap_68,
    guard_enforcement_support_teacher_dependency_69,
    guard_digital_capacity_digital_capacity_resilience_70,
    guard_affected_group_effect_persistence_71,
    guard_consultation_coverage_scale_readiness_72,
    guard_policy_code_learning_gain_73,
    guard_jurisdiction_level_engagement_comparability_74,
    guard_measure_type_attrition_bias_75,
    guard_covered_entities_equity_gap_76,
    guard_implementation_intensity_teacher_dependency_77,
    guard_baseline_risk_digital_capacity_resilience_78,
    guard_post_risk_effect_persistence_79,
    guard_missing_rate_scale_readiness_80,
    guard_enforcement_support_learning_gain_81,
    guard_digital_capacity_engagement_comparability_82,
    guard_affected_group_attrition_bias_83,
    guard_consultation_coverage_equity_gap_84,
    guard_policy_code_teacher_dependency_85,
    guard_jurisdiction_level_digital_capacity_resilience_86,
    guard_measure_type_effect_persistence_87,
    guard_covered_entities_scale_readiness_88,
    guard_implementation_intensity_learning_gain_89,
    guard_baseline_risk_engagement_comparability_90,
    guard_post_risk_attrition_bias_91,
    guard_missing_rate_equity_gap_92,
    guard_enforcement_support_teacher_dependency_93,
    guard_digital_capacity_digital_capacity_resilience_94,
    guard_affected_group_effect_persistence_95,
    guard_consultation_coverage_scale_readiness_96,
    guard_policy_code_learning_gain_97,
    guard_jurisdiction_level_engagement_comparability_98,
    guard_measure_type_attrition_bias_99,
    guard_covered_entities_equity_gap_100,
    guard_implementation_intensity_teacher_dependency_101,
    guard_baseline_risk_digital_capacity_resilience_102,
    guard_post_risk_effect_persistence_103,
    guard_missing_rate_scale_readiness_104,
    guard_enforcement_support_learning_gain_105,
    guard_digital_capacity_engagement_comparability_106,
    guard_affected_group_attrition_bias_107,
    guard_consultation_coverage_equity_gap_108,
    guard_policy_code_teacher_dependency_109,
    guard_jurisdiction_level_digital_capacity_resilience_110,
    guard_measure_type_effect_persistence_111,
    guard_covered_entities_scale_readiness_112,
    guard_implementation_intensity_learning_gain_113,
    guard_baseline_risk_engagement_comparability_114,
    guard_post_risk_attrition_bias_115,
    guard_missing_rate_equity_gap_116,
    guard_enforcement_support_teacher_dependency_117,
    guard_digital_capacity_digital_capacity_resilience_118,
    guard_affected_group_effect_persistence_119,
    guard_consultation_coverage_scale_readiness_120,
)

def guard_report(record: DomainRecord, context: Mapping[str, Any] | None = None) -> dict[str, Any]:
    context = dict(context or {})
    context['_metrics'] = grouped_metrics(record, context)
    results = [guard(record, context) for guard in GUARDS]
    return {'passed': sum(item[0] for item in results), 'failed': sum(not item[0] for item in results),
            'messages': [item[1] for item in results]}

def decide(record: DomainRecord, context: Mapping[str, Any] | None = None) -> Decision:
    context = context or {}
    rules = evaluate(record, context)
    impact_brief = record_score(record, context)
    guards = guard_report(record, context)
    effective_score = impact_brief['score'] * 0.65 + float(context.get('domain_signal', 0.5)) * 0.35 - min(0.2, float(context.get('policy_disparity', 0.0)) * 0.25)
    critical = sum(item.severity == 'critical' for item in rules)
    if context.get('domain_severity') == 'critical':
        outcome = 'hold'
    elif critical:
        outcome = 'hold'
    elif effective_score >= float(context.get('approve_threshold', 0.62)) and guards['passed'] >= guards['failed']:
        outcome = 'approve'
    elif effective_score >= float(context.get('review_threshold', 0.38)):
        outcome = 'review'
    else:
        outcome = 'reject'
    reasons = (f"score={impact_brief['score']:.6f}", f"critical={critical}",
               f"guards={guards['passed']}/{guards['passed'] + guards['failed']}")
    return Decision(record.record_id, outcome, effective_score, reasons, rules, impact_brief['metrics'])

def advance_for_outcome(record: DomainRecord, decision: Decision) -> DomainRecord:
    current = STATES.index(record.state)
    if decision.outcome == 'approve' and current + 1 < len(STATES):
        return record.with_state(STATES[current + 1])
    if decision.outcome == 'hold' and STATES[-1] != record.state:
        return record.with_state(STATES[-1])
    return record
