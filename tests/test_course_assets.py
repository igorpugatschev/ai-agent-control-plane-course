import json
import subprocess
import sys
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

CANONICAL_TEMPLATE_MAPPING = (
    {"template": "templates/control-plane-blueprint.md", "artifact": "artifacts/capstone/blueprint.md"},
    {"template": "templates/context-map.md", "artifact": "artifacts/capstone/source-map.md"},
    {"template": "templates/agent-role.md", "artifact": "artifacts/capstone/roles.md"},
    {"template": "templates/skill-contract.md", "artifact": "artifacts/capstone/skill-contracts.md"},
    {"template": "templates/handoff.md", "artifact": "artifacts/capstone/handoffs.md"},
    {"template": "templates/workflow.md", "artifact": "artifacts/capstone/workflow.md"},
    {"template": "templates/review-gate.md", "artifact": "artifacts/capstone/review-gate.md"},
    {"template": "templates/stop-gate.md", "artifact": "artifacts/capstone/stop-gate.md"},
    {"template": "templates/decision-log.md", "artifact": "artifacts/capstone/decision-log.md"},
    {"template": "templates/final-report.md", "artifact": "artifacts/capstone/final-report.md"},
)

CAPSTONE_MAPPING_PATHS = (
    Path("curriculum/module-07-capstone/lesson-19-assemble-control-plane.md"),
    Path("projects/starter-control-plane/README.md"),
    Path("projects/capstone.md"),
    Path("curriculum/module-07-capstone/checkpoint.md"),
    Path("curriculum/module-07-capstone/lesson-21-audit-defense-roadmap.md"),
)

CAPSTONE_PACKAGE_MANIFEST_PATHS = (
    Path("curriculum/module-07-capstone/lesson-19-assemble-control-plane.md"),
    Path("projects/capstone.md"),
    Path("curriculum/module-07-capstone/checkpoint.md"),
)

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
CAPSTONE_CWD_DOC_PATHS = (
    Path("projects/capstone.md"),
    Path("curriculum/module-07-capstone/checkpoint.md"),
)
CAPSTONE_ROOT_CWD_MARKER = "# Run from the course repository root."
CAPSTONE_ROOT_COMMANDS = (
    'python3 -c "import json; json.load(open(\'projects/starter-control-plane/control-plane.yaml\', encoding=\'utf-8\'))"',
    "python3 scripts/validate_course.py curriculum",
    "python3 -m pytest tests/test_course_structure.py -q",
    "PYTHONPATH=projects/training-task-app/src python3 -m pytest projects/training-task-app/tests -q",
    "git diff --check",
)
AUTHORIZED_EXECUTOR_POLICY = (
    "A separately named authorized executor, distinct from the named human owner "
    "and risk reviewer, executes the approved action."
)
HUMAN_OWNER_DECISION_POLICY = "The named human owner may only approve or reject the intended action."
FORBIDDEN_OWNER_AS_EXECUTOR_PHRASE = "implementation или human owner через coordinator"
PRIVILEGED_ACTION_ROW_PREFIX = "| Publish/deploy/delete/read secret |"
EXPECTED_PRIVILEGED_MATRIX_CELLS = (
    "Publish/deploy/delete/read secret",
    "Привилегированно",
    "STOP + risk analysis + human approval",
    "Impact, rollback, risk recommendation",
    "named human owner: only approve/reject",
    "separately named authorized executor, not human owner or risk reviewer",
    "Выполнить только approved action",
    "Explicit approval intended action",
)

CATALOG_SECTIONS = {
    "NIST AI RMF Core": {
        "role": "vendor-neutral Tier 1 framework для управления AI risks.",
        "scope": "функции Govern, Map, Measure и Manage; распределение ответственности,\n  оценка и управление рисками в Module 6.",
        "url": "https://airc.nist.gov/airmf-resources/airmf/5-sec-core/",
    },
    "OWASP LLM01:2025 Prompt Injection": {
        "role": "Tier 1 security guidance для угрозы prompt injection.",
        "scope": "direct и indirect prompt injection, untrusted inputs, least privilege\n  и boundaries в Module 6.",
        "url": "https://genai.owasp.org/llmrisk/llm01-prompt-injection/",
    },
    "OpenTelemetry GenAI semantic conventions": {
        "role": "Tier 1 specification для trace conventions и attributes GenAI telemetry.",
        "scope": "trace conventions и attributes для Module 6 trace record; не redaction\n  policy и не разрешения на запись payload.",
        "url": "https://github.com/open-telemetry/semantic-conventions-genai",
    },
}


def extract_catalog_section(catalog: str, title: str) -> str:
    marker = f"### {title}"
    start = catalog.index(marker)
    next_heading = catalog.find("\n### ", start + len(marker))
    return catalog[start:] if next_heading == -1 else catalog[start:next_heading]


def test_required_assets_alias_matches_templates():
    assert REQUIRED_ASSETS == TEMPLATES


def test_all_templates_exist_and_have_acceptance_criteria():
    for name in TEMPLATES:
        path = Path("templates") / name
        assert path.is_file(), path
        assert "## Критерии готовности" in path.read_text(encoding="utf-8")


def test_reference_control_plane_is_self_contained_and_rerunnable():
    reference = Path("projects/reference-control-plane")
    contract = json.loads((reference / "control-plane.yaml").read_text(encoding="utf-8"))

    assert contract["project"]["name"] == "product-documentation-maintenance"
    assert contract["evidence"]["local_check"] == (
        "python3 scripts/check_reference_control_plane.py -> exit 0"
    )
    for path in (
        "docs/product/change-requests/CR-42.md",
        "docs/product/index.md",
        "docs/product/guides/review-process.md",
        "incoming/external-comment.txt",
        "evidence/CR-42-local-check.txt",
        "review/CR-42-local-review.md",
        "decision-log.md",
        "scripts/check_reference_control_plane.py",
    ):
        assert (reference / path).is_file(), path

    result = subprocess.run(
        [sys.executable, str(reference / "scripts/check_reference_control_plane.py")],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert result.stdout == "Reference control plane check: PASS\n"
    assert result.stderr == ""


def test_starter_and_capstone_map_every_template_to_a_required_deliverable():
    starter = Path("projects/starter-control-plane")
    starter_contract = json.loads((starter / "control-plane.yaml").read_text(encoding="utf-8"))
    assert starter_contract["project"]["name"].startswith("<student:")
    assert starter_contract["template_mapping"] == list(CANONICAL_TEMPLATE_MAPPING)

    for mapping_entry in CANONICAL_TEMPLATE_MAPPING:
        template = mapping_entry["template"]
        artifact = mapping_entry["artifact"]
        mapping = f"`{template}` -> `{artifact}`"
        for path in CAPSTONE_MAPPING_PATHS:
            assert mapping in path.read_text(encoding="utf-8"), (path, mapping)

        starter_artifact = starter / artifact
        assert starter_artifact.is_file(), starter_artifact
        assert "<student:" in starter_artifact.read_text(encoding="utf-8")

    for path in CAPSTONE_MAPPING_PATHS:
        text = path.read_text(encoding="utf-8")
        assert "`control-plane.yaml`" in text, path

    for path in CAPSTONE_CWD_DOC_PATHS:
        text = path.read_text(encoding="utf-8")
        assert CAPSTONE_ROOT_CWD_MARKER in text, path
        for command in CAPSTONE_ROOT_COMMANDS:
            assert command in text, (path, command)

    repository_root = Path(__file__).parent.parent
    for command in CAPSTONE_ROOT_COMMANDS:
        result = subprocess.run(
            command,
            cwd=repository_root,
            shell=True,
            check=False,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, (command, result.stdout, result.stderr)


def test_capstone_manifest_keeps_the_package_readme():
    for path in CAPSTONE_PACKAGE_MANIFEST_PATHS:
        assert "artifacts/capstone/README.md" in path.read_text(encoding="utf-8"), path


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

    lesson17 = Path(
        "curriculum/module-06-safety-and-observability/lesson-17-stop-review-approval-gates.md"
    ).read_text(encoding="utf-8")
    assert AUTHORIZED_EXECUTOR_POLICY in lesson17
    assert HUMAN_OWNER_DECISION_POLICY in lesson17
    assert FORBIDDEN_OWNER_AS_EXECUTOR_PHRASE not in lesson17

    privileged_row = next(
        line for line in lesson17.splitlines() if line.startswith(PRIVILEGED_ACTION_ROW_PREFIX)
    )
    privileged_cells = tuple(
        cell.strip() for cell in privileged_row.strip().strip("|").split("|")
    )
    assert privileged_cells == EXPECTED_PRIVILEGED_MATRIX_CELLS

    decision_owner = privileged_cells[4]
    authorized_executor = privileged_cells[5]
    assert decision_owner == "named human owner: only approve/reject"
    executor_role, separator, executor_exclusions = authorized_executor.partition(", not ")
    assert executor_role == "separately named authorized executor"
    assert separator
    assert executor_exclusions == "human owner or risk reviewer"
    assert "human owner" not in executor_role
    assert "risk reviewer" not in executor_role

    forbidden_actions = risk_reviewer.split("## Запрещенные действия", 1)[1].split(
        "## Stop conditions", 1
    )[0]
    forbidden_actions = " ".join(forbidden_actions.split())
    for forbidden_term in (
        "не удалять",
        "не публиковать",
        "не делать deploy",
        "не выполнять `git push`",
        "не выдавать final irreversible-action approval",
    ):
        assert forbidden_term in forbidden_actions

    implementation = " ".join(Path("agents/implementation.md").read_text(encoding="utf-8").split())
    assert (
        "не делать deploy, release или `git push` без отдельного documented approval и нового назначения."
        in implementation
    )

    trace_lesson = Path(
        "curriculum/module-06-safety-and-observability/lesson-18-evaluation-tracing-decision-log.md"
    ).read_text(encoding="utf-8")
    catalog = Path("docs/source-catalog.md").read_text(encoding="utf-8")
    obsolete_url = "https://opentelemetry.io" + "/docs/specs/semconv/gen-ai/"
    assert CATALOG_SECTIONS["OpenTelemetry GenAI semantic conventions"]["url"] in trace_lesson
    assert obsolete_url not in trace_lesson
    assert obsolete_url not in catalog
    for title, expected in CATALOG_SECTIONS.items():
        section = extract_catalog_section(catalog, title)
        assert f"- Роль: {expected['role']}" in section
        assert f"- Scope: {expected['scope']}" in section
        assert f"]({expected['url']})" in section
        assert "- Checked: 2026-07-13." in section
