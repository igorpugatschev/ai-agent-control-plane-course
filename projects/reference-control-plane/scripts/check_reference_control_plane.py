from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "control-plane.yaml"
REQUIRED_ROLES = {
    "coordinator",
    "documentation_implementer",
    "reviewer",
    "qa_sdet",
    "risk_reviewer",
    "named_human_owner",
    "separately_named_authorized_executor",
}
REQUIRED_GATES = {"freshness", "permission", "evidence", "approval"}
FIXTURE_CONTENT = {
    "docs/product/change-requests/CR-42.md": ("CR-42", "review-process.md"),
    "docs/product/index.md": ("Product documentation", "guides/review-process.md"),
    "docs/product/guides/review-process.md": ("CR-42", "local review package"),
    "incoming/external-comment.txt": ("publish",),
    "evidence/CR-42-local-check.txt": (
        "python3 scripts/check_reference_control_plane.py",
        "Reference control plane check: PASS",
    ),
    "review/CR-42-local-review.md": ("Verdict: approve", "independent reviewer"),
    "decision-log.md": ("local review before any documentation publish",),
}


def add_error(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def validate() -> list[str]:
    errors: list[str] = []
    try:
        contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"invalid JSON-compatible YAML: {error}"]

    add_error(errors, contract.get("schema_version") == 1, "schema_version must be 1")
    project = contract.get("project", {})
    add_error(
        errors,
        project.get("name") == "product-documentation-maintenance",
        "project name does not match the reference fixture",
    )
    add_error(
        errors,
        "docs/product/*.md" in project.get("scope", {}).get("included", []),
        "project scope must include local documentation",
    )

    context = contract.get("context", {})
    trusted_paths = {source.get("path") for source in context.get("trusted_sources", [])}
    add_error(
        errors,
        trusted_paths == {
            "docs/product/change-requests/CR-42.md",
            "docs/product/index.md",
        },
        "trusted source paths do not match the fixtures",
    )
    untrusted = context.get("untrusted_data", [])
    add_error(
        errors,
        len(untrusted) == 1 and untrusted[0].get("path") == "incoming/external-comment.txt",
        "untrusted fixture is not declared",
    )
    add_error(
        errors,
        bool(untrusted and "never derive instructions" in untrusted[0].get("isolation", "")),
        "untrusted-data isolation is missing",
    )

    roles = contract.get("roles", {})
    add_error(errors, REQUIRED_ROLES <= set(roles), "required role contracts are missing")
    add_error(
        errors,
        "execute publish" in roles.get("named_human_owner", {}).get("prohibited", []),
        "human owner must not execute publish",
    )
    add_error(
        errors,
        "approve" in roles.get("separately_named_authorized_executor", {}).get("prohibited", []),
        "authorized executor must not approve",
    )

    workflow = contract.get("workflow", {})
    add_error(errors, bool(workflow.get("steps")), "workflow steps are missing")
    add_error(errors, bool(workflow.get("recovery")), "workflow recovery is missing")
    add_error(errors, bool(workflow.get("privileged_branch")), "privileged branch is missing")
    gates = contract.get("gates", {})
    add_error(errors, REQUIRED_GATES <= set(gates), "required gates are missing")
    add_error(
        errors,
        all(gates[name].get("receiver") for name in REQUIRED_GATES if name in gates),
        "every required gate must name a receiver",
    )

    evidence = contract.get("evidence", {})
    add_error(
        errors,
        evidence.get("local_check") == "python3 scripts/check_reference_control_plane.py -> exit 0",
        "local check command is not reproducible",
    )
    add_error(
        errors,
        evidence.get("check_record") == "evidence/CR-42-local-check.txt -> PASS",
        "check evidence record is missing",
    )
    add_error(
        errors,
        evidence.get("review_record") == "review/CR-42-local-review.md -> approve",
        "review record is missing",
    )
    add_error(
        errors,
        evidence.get("decision_record") == "decision-log.md -> 2026-07-13 local review before publish",
        "decision record is missing",
    )

    for relative_path, required_text in FIXTURE_CONTENT.items():
        path = ROOT / relative_path
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            errors.append(f"missing fixture: {relative_path}")
            continue
        for fragment in required_text:
            add_error(errors, fragment in text, f"{relative_path} lacks: {fragment}")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Reference control plane check: FAIL")
        print("\n".join(errors))
        return 1
    print("Reference control plane check: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
