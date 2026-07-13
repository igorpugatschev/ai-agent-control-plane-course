from pathlib import Path


TEMPLATES = (
    "control-plane-blueprint.md",
    "context-map.md",
    "agent-role.md",
    "skill-contract.md",
    "handoff.md",
    "workflow.md",
    "review-gate.md",
    "stop-gate.md",
    "decision-log.md",
    "final-report.md",
)

# Compatibility name for consumers of the task brief's asset contract.
REQUIRED_ASSETS = TEMPLATES

TERMS = (
    "LLM",
    "prompt",
    "agent",
    "control plane",
    "context",
    "evidence",
    "role",
    "skill",
    "tool",
    "workflow",
    "handoff",
    "gate",
    "stop-gate",
    "review-gate",
    "evaluation",
    "tracing",
    "prompt injection",
)

SAFETY_AUTHORITY_PATHS = (
    Path("agents/coordinator.md"),
    Path("agents/risk-reviewer.md"),
    Path("agents/README.md"),
    Path("curriculum/module-03-roles-and-skills/README.md"),
    Path("curriculum/module-03-roles-and-skills/checkpoint.md"),
    Path("curriculum/module-03-roles-and-skills/lesson-07-agent-role-contract.md"),
    Path("curriculum/module-03-roles-and-skills/lesson-08-tools-skills-permissions.md"),
    Path("curriculum/module-03-roles-and-skills/lesson-09-coordinator-handoff.md"),
    Path("curriculum/module-05-qa-sdet-workflow/lesson-15-regression-triage-release-gate.md"),
    Path("curriculum/module-05-qa-sdet-workflow/checkpoint.md"),
    Path("curriculum/module-06-safety-and-observability/lesson-17-stop-review-approval-gates.md"),
    Path("curriculum/module-06-safety-and-observability/checkpoint.md"),
)

FINAL_APPROVAL_POLICY = "Final irreversible-action approval дает только named human owner."


def test_required_assets_alias_matches_templates():
    assert REQUIRED_ASSETS == TEMPLATES


def test_all_templates_exist_and_have_acceptance_criteria():
    for name in TEMPLATES:
        path = Path("templates") / name
        assert path.is_file(), path
        assert "## Критерии готовности" in path.read_text(encoding="utf-8")


def test_glossary_defines_required_terms():
    text = Path("glossary/terms.md").read_text(encoding="utf-8").lower()
    for term in TERMS:
        assert term.lower() in text, term


def test_safety_authority_and_trace_source_contracts_are_consistent():
    for path in SAFETY_AUTHORITY_PATHS:
        text = " ".join(path.read_text(encoding="utf-8").split())
        assert FINAL_APPROVAL_POLICY in text, path

    risk_reviewer = Path("agents/risk-reviewer.md").read_text(encoding="utf-8")
    assert "risk analysis" in risk_reviewer
    assert "approval-gate process" in risk_reviewer
    assert "`recommendation` или `STOP`" in risk_reviewer

    trace_lesson = Path(
        "curriculum/module-06-safety-and-observability/lesson-18-evaluation-tracing-decision-log.md"
    ).read_text(encoding="utf-8")
    catalog = Path("docs/source-catalog.md").read_text(encoding="utf-8")
    canonical_url = "https://github.com/open-telemetry/semantic-conventions-genai"
    obsolete_url = "https://opentelemetry.io" + "/docs/specs/semconv/gen-ai/"
    assert canonical_url in trace_lesson
    assert canonical_url in catalog
    assert obsolete_url not in trace_lesson
    assert obsolete_url not in catalog
    for source in ("NIST AI RMF Core", "OWASP LLM01:2025 Prompt Injection"):
        assert source in catalog
    assert catalog.count("Checked: 2026-07-13.") >= 3
