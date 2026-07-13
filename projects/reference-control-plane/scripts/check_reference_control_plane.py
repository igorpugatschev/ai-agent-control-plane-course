from __future__ import annotations

import argparse
import json
import re
import shlex
import subprocess
from pathlib import Path
from typing import Any


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
SHA_RE = re.compile(r"[0-9a-f]{40}")
PLACEHOLDER_RE = re.compile(r"<[^>]+>|\b(?:todo|tbd|placeholder)\b", re.IGNORECASE)
FIXTURE_CONTENT = {
    "README.md": (
        'execution.cwd: "."',
        "cd projects/reference-control-plane",
    ),
    "docs/product/change-requests/CR-42.md": (
        "## Утвержденное изменение",
        "guides/review-process.md",
    ),
    "docs/product/index.md": (
        "# Документация продукта",
        "guides/review-process.md",
    ),
    "docs/product/guides/review-process.md": (
        "CR-42",
        "локальный review package",
    ),
    "incoming/external-comment.txt": ("publish",),
    "evidence/CR-42-local-check.txt": (
        "Команда: python3 scripts/check_reference_control_plane.py",
        "Результат: Reference control plane check: PASS",
    ),
    "review/CR-42-local-review.md": (
        "## Вердикт: approve",
        "## Независимый reviewer",
    ),
    "decision-log.md": ("local review before any documentation publish",),
}


def add_error(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def run_exact_command(command: str, cwd: Path) -> subprocess.CompletedProcess[str] | None:
    try:
        arguments = shlex.split(command)
    except ValueError:
        return None
    if not arguments or any(Path(argument).is_absolute() for argument in arguments[1:]):
        return None
    try:
        return subprocess.run(
            arguments,
            cwd=cwd,
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return None


def load_contract() -> tuple[dict[str, Any] | None, list[str]]:
    try:
        return json.loads(CONTRACT_PATH.read_text(encoding="utf-8")), []
    except (OSError, json.JSONDecodeError) as error:
        return None, [f"invalid JSON-compatible YAML: {error}"]


def validate_contract(contract: dict[str, Any]) -> list[str]:
    errors: list[str] = []
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
    trusted_sources = context.get("trusted_sources", [])
    trusted_paths = {source.get("path") for source in trusted_sources}
    add_error(
        errors,
        trusted_paths
        == {
            "docs/product/change-requests/CR-42.md",
            "docs/product/index.md",
        },
        "trusted source paths do not match the fixtures",
    )
    for source in trusted_sources:
        source_sha = source.get("source_sha", "")
        command = source.get("freshness_command", "")
        add_error(
            errors,
            bool(SHA_RE.fullmatch(source_sha)),
            f"trusted source has invalid or empty SHA: {source.get('path')}",
        )
        result = run_exact_command(command, ROOT) if command else None
        add_error(
            errors,
            result is not None and result.returncode == 0,
            f"freshness command failed: {source.get('path')}",
        )
        if result is not None and result.returncode == 0:
            add_error(
                errors,
                result.stdout.strip() == source_sha,
                f"freshness SHA mismatch: {source.get('path')}",
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
    risk_reviewer = roles.get("risk_reviewer", {})
    risk_text = " ".join(
        [risk_reviewer.get("responsibility", "")]
        + risk_reviewer.get("permissions", [])
    ).lower()
    risk_prohibited = set(risk_reviewer.get("prohibited", []))
    add_error(
        errors,
        "risk analysis" in risk_text
        and "recommendation or stop" in risk_text
        and {"final approval", "execution"} <= risk_prohibited,
        "risk reviewer must only analyze/recommend/STOP and must not approve or execute",
    )

    human_owner = roles.get("named_human_owner", {})
    add_error(
        errors,
        set(human_owner.get("permissions", [])) == {"approve", "reject"}
        and "execute publish" in human_owner.get("prohibited", []),
        "human owner must only approve/reject and must not execute",
    )
    executor = roles.get("separately_named_authorized_executor", {})
    add_error(
        errors,
        bool(executor.get("responsibility"))
        and bool(executor.get("permissions"))
        and "approve" in executor.get("prohibited", [])
        and "execute without approval" in executor.get("prohibited", []),
        "authorized executor semantics are missing",
    )

    workflow = contract.get("workflow", {})
    add_error(errors, bool(workflow.get("steps")), "workflow steps are missing")
    add_error(errors, bool(workflow.get("recovery")), "workflow recovery is missing")
    privileged_branch = workflow.get("privileged_branch", [])
    privileged_text = " ".join(privileged_branch).lower()
    add_error(
        errors,
        bool(privileged_branch)
        and all(isinstance(step, str) and step.strip() for step in privileged_branch)
        and not PLACEHOLDER_RE.search(privileged_text)
        and "risk_reviewer" in privileged_text
        and "named_human_owner" in privileged_text
        and "separately_named_authorized_executor" in privileged_text
        and "execution evidence" in privileged_text,
        "privileged branch is empty, placeholder, or semantically incomplete",
    )

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
        evidence.get("check_record") == "evidence/CR-42-local-check.txt -> PASS",
        "check evidence record is missing",
    )
    add_error(
        errors,
        evidence.get("review_record") == "review/CR-42-local-review.md -> approve",
        "review record is missing",
    )

    execution = contract.get("execution", {})
    cwd_value = execution.get("cwd")
    command_cwd = (ROOT / cwd_value).resolve() if isinstance(cwd_value, str) else None
    add_error(
        errors,
        cwd_value == "." and command_cwd == ROOT.resolve(),
        "execution cwd must be the reference project root (.)",
    )
    commands = execution.get("commands", [])
    add_error(errors, bool(commands), "execution commands must not be empty")
    for index, command_record in enumerate(commands):
        command = command_record.get("command", "") if isinstance(command_record, dict) else ""
        add_error(errors, bool(command.strip()), f"execution command {index} is empty")
        add_error(
            errors,
            isinstance(command_record, dict)
            and command_record.get("expected_exit") == 0
            and isinstance(command_record.get("expected_stdout"), str)
            and bool(command_record.get("expected_stdout")),
            f"execution command {index} lacks exit/output contract",
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


def validate_commands(contract: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    execution = contract.get("execution", {})
    cwd_value = execution.get("cwd")
    if cwd_value != ".":
        return ["execution cwd mismatch prevents command execution"]
    command_cwd = (ROOT / cwd_value).resolve()
    for index, record in enumerate(execution.get("commands", [])):
        command = record.get("command", "") if isinstance(record, dict) else ""
        result = run_exact_command(command, command_cwd) if command else None
        if result is None:
            errors.append(f"execution command {index} is invalid or could not start")
            continue
        add_error(
            errors,
            result.returncode == record.get("expected_exit"),
            f"execution command {index} exit mismatch",
        )
        add_error(
            errors,
            result.stdout == record.get("expected_stdout"),
            f"execution command {index} stdout mismatch",
        )
        add_error(
            errors,
            result.stderr == "",
            f"execution command {index} wrote unexpected stderr",
        )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract-only", action="store_true")
    args = parser.parse_args()

    contract, errors = load_contract()
    if contract is not None:
        errors.extend(validate_contract(contract))
        if not errors and not args.contract_only:
            errors.extend(validate_commands(contract))
    if errors:
        print("Reference control plane check: FAIL")
        print("\n".join(errors))
        return 1
    if args.contract_only:
        print("Reference contract check: PASS")
    else:
        print("Reference control plane check: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
