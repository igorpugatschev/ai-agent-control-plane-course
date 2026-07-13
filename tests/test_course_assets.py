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
