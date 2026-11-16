from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

from policy_impact.measures.policy_contract import Decision, DomainRecord, canonical_json, stable_hash, utc_now
from policy_impact.analysis.counterfactual import adjusted_effect, equity_summary, persistence


def ensure_output(path: str | Path) -> Path:
    output = Path(path)
    output.mkdir(parents=True, exist_ok=True)
    return output


def write_json(path: Path, value: Any) -> str:
    body = json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2)
    path.write_text(body + "\n", encoding="utf-8")
    return stable_hash(value)


def write_records(path: Path, records: Iterable[DomainRecord], decisions: Mapping[str, Decision]) -> int:
    rows = []
    for record in records:
        decision = decisions.get(record.record_id)
        effect = adjusted_effect(record)
        rows.append({"record_id": record.record_id, "state": record.state, "version": record.version,
                     "source": record.source, "fingerprint": record.fingerprint,
                     "outcome": decision.outcome if decision else "", "score": decision.score if decision else "",
                     "direction": effect["direction"], "verdict": effect["verdict"],
                     "risk_delta": effect["risk_delta"], "reliability": effect["reliability"]})
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["record_id", "state", "version", "source", "fingerprint",
                                                    "outcome", "score", "direction", "verdict", "risk_delta",
                                                    "reliability"])
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def write_rules(path: Path, decisions: Mapping[str, Decision]) -> int:
    count = 0
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["record_id", "code", "passed", "score", "severity", "message"])
        writer.writeheader()
        for record_id, decision in sorted(decisions.items()):
            for result in decision.rule_results:
                writer.writerow({"record_id": record_id, "code": result.code, "passed": result.passed,
                                 "score": result.score, "severity": result.severity, "message": result.message})
                count += 1
    return count


def build_summary(records: list[DomainRecord], decisions: Mapping[str, Decision], snapshot: Mapping[str, Any]) -> dict[str, Any]:
    outcomes: dict[str, int] = {}
    for decision in decisions.values():
        outcomes[decision.outcome] = outcomes.get(decision.outcome, 0) + 1
    scores = [decision.score for decision in decisions.values()]
    effects = [(record.record_id, adjusted_effect(record)) for record in records]
    directions = {"improved": 0, "worsened": 0, "unchanged": 0}
    verdicts: dict[str, int] = {}
    for _, effect in effects:
        directions[effect["direction"]] += 1
        verdicts[effect["verdict"]] = verdicts.get(effect["verdict"], 0) + 1
    equity = equity_summary(records)
    stability = persistence(records)
    return {"product": '人工智能治理政策版本影响评估平台', "entity": 'policy_measure', "generated_at": utc_now(),
            "record_count": len(records), "decision_count": len(decisions), "outcomes": outcomes,
            "average_score": sum(scores) / len(scores) if scores else 0.0,
            "minimum_score": min(scores) if scores else 0.0, "maximum_score": max(scores) if scores else 0.0,
            "risk_directions": directions, "effect_verdicts": verdicts,
            "confirmed_improvements": sum(1 for _, effect in effects if effect["verdict"] == "confirmed_improvement"),
            "confirmed_worsenings": sum(1 for _, effect in effects if effect["verdict"] == "confirmed_worsening"),
            "uncertain_records": [record_id for record_id, effect in effects if effect["uncertain"]],
            "group_summary": equity, "persistence": stability,
            "repository": snapshot}


def export_bundle(output: str | Path, records: list[DomainRecord], decisions: Mapping[str, Decision],
                  snapshot: Mapping[str, Any], events: list[dict[str, Any]]) -> dict[str, Any]:
    root = ensure_output(output)
    summary = build_summary(records, decisions, snapshot)
    record_count = write_records(root / "records.csv", records, decisions)
    rule_count = write_rules(root / "rules.csv", decisions)
    summary_hash = write_json(root / "summary.json", summary)
    decision_hash = write_json(root / "decisions.json", [value.as_dict() for _, value in sorted(decisions.items())])
    event_hash = write_json(root / "audit-events.json", events)
    manifest = {"files": {"summary.json": summary_hash, "decisions.json": decision_hash,
                           "audit-events.json": event_hash}, "record_rows": record_count,
                "rule_rows": rule_count, "created_at": utc_now()}
    manifest["manifest_hash"] = stable_hash(manifest)
    write_json(root / "manifest.json", manifest)
    return manifest


def verify_bundle(output: str | Path) -> list[str]:
    root = Path(output)
    errors: list[str] = []
    manifest_path = root / "manifest.json"
    if not manifest_path.is_file():
        return ["manifest.json is missing"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected_manifest_hash = manifest.pop("manifest_hash", "")
    if stable_hash(manifest) != expected_manifest_hash:
        errors.append("manifest hash mismatch")
    for name, expected in manifest.get("files", {}).items():
        path = root / name
        if not path.is_file():
            errors.append(f"{name} is missing")
            continue
        value = json.loads(path.read_text(encoding="utf-8"))
        if stable_hash(value) != expected:
            errors.append(f"{name} hash mismatch")
    return errors
