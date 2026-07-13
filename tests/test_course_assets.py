import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


LINK_RE = re.compile(r"\[[^]]+\]\(([^)]+)\)")


def local_markdown_path(raw_target: str) -> str | None:
    parsed = urlsplit(raw_target)
    if parsed.scheme or parsed.netloc:
        return None
    return unquote(parsed.path) or None


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

TASK11_SOURCE_RECORDS = {
    "OpenAI Agents guide": "https://developers.openai.com/api/docs/guides/agents",
    "DeepSeek API documentation": "https://api-docs.deepseek.com/",
    "Qwen documentation": "https://qwen.readthedocs.io/en/stable/getting_started/quickstart.html",
    "Model Context Protocol specification": "https://modelcontextprotocol.io/specification/latest",
    "A2A Protocol specification": "https://a2a-protocol.org/latest/specification/",
    "NIST AI RMF Core": "https://airc.nist.gov/airmf-resources/airmf/5-sec-core/",
    "OWASP LLM01:2025 Prompt Injection": "https://genai.owasp.org/llmrisk/llm01-prompt-injection/",
    "OpenTelemetry GenAI semantic conventions": "https://github.com/open-telemetry/semantic-conventions-genai",
    "OpenAPI Specification": "https://spec.openapis.org/oas/latest.html",
    "JSON Schema specification": "https://json-schema.org/specification",
    "GitHub Actions documentation": "https://docs.github.com/en/actions/reference",
    "Google Agent Development Kit documentation": "https://adk.dev/",
}

CANONICAL_LESSON_SOURCE_MAPPING = {
    1: ("https://developers.openai.com/api/docs/guides/agents", "Различие model, tools и управляемого agent workflow"),
    2: ("https://developers.openai.com/api/docs/guides/agents", "Instructions, tools и управляющий workflow как границы задачи"),
    3: ("https://developers.openai.com/api/docs/guides/agents", "Agent workflows, tools и blueprint components"),
    4: ("https://spec.openapis.org/oas/latest.html", "Formal API contract в source hierarchy"),
    5: ("https://modelcontextprotocol.io/docs/getting-started/intro", "Ограниченный context packet и внешние tools"),
    6: ("https://developers.openai.com/api/docs/guides/agents", "Ограничения и checks в управляемых agent actions"),
    7: ("https://developers.openai.com/api/docs/guides/agents", "Roles, tools и управляемый workflow в role contract"),
    8: ("https://openai.github.io/openai-agents-python/", "Tools, handoffs и guardrails как пример реализации"),
    9: ("https://developers.openai.com/api/docs/guides/agents", "Orchestration и handoff patterns для coordinator routing"),
    10: ("https://spec.openapis.org/oas/latest.html", "API contract для intake и acceptance impact"),
    11: ("https://spec.openapis.org/oas/latest.html", "Contract-aware controlled code change"),
    12: ("https://git-scm.com/docs", "Commit и diff evidence в engineering gates"),
    13: ("https://spec.openapis.org/oas/latest.html", "HTTP contract как source для testable conditions"),
    14: ("https://spec.openapis.org/oas/latest.html", "Paths, operations, responses и schemas для API checks"),
    15: ("https://docs.pytest.org/", "Collection и report output для regression evidence"),
    16: ("https://genai.owasp.org/llmrisk/llm01-prompt-injection/", "Direct/indirect injection, untrusted input и least privilege"),
    17: ("https://airc.nist.gov/airmf-resources/airmf/5-sec-core/", "Govern, Map, Measure и Manage для gates и authority"),
    18: ("https://github.com/open-telemetry/semantic-conventions-genai", "GenAI trace conventions и attributes для evaluation evidence"),
    19: ("https://airc.nist.gov/airmf-resources/airmf/5-sec-core/", "Risk ownership при сборке capstone control plane"),
    20: ("https://airc.nist.gov/airmf-resources/playbook/", "Measured failure, correction и re-run"),
    21: ("https://github.com/open-telemetry/semantic-conventions-genai", "Trace terminology для audit и observability"),
}

CATALOG_ONLY_EXTENSION_URLS = (
    "https://api-docs.deepseek.com/",
    "https://qwen.readthedocs.io/en/stable/getting_started/quickstart.html",
    "https://a2a-protocol.org/latest/specification/",
    "https://docs.github.com/en/actions/reference",
    "https://adk.dev/",
)

CHECKPOINT_SELF_CHECK_REQUIREMENTS = {
    "module-01.md": {
        "artifacts": ("artifacts/module-01/control-plane-blueprint.md",),
        "markers": ("Scope", "Owner", "Evidence", "STOP"),
        "stable_check": "python3 scripts/validate_course.py curriculum",
    },
    "module-02.md": {
        "artifacts": (
            "artifacts/module-02/source-register.md",
            "artifacts/module-02/context-packet.md",
            "artifacts/module-02/context-map-evidence-gate.md",
        ),
        "markers": ("Source owner", "Authority owner", "Evidence gate", "STOP"),
        "stable_check": "python3 scripts/validate_course.py curriculum",
    },
    "module-03.md": {
        "artifacts": (
            "artifacts/module-03/role-contracts.md",
            "artifacts/module-03/skill-and-permission-matrix.md",
            "artifacts/module-03/coordinator-handoff.md",
        ),
        "markers": ("receiver", "STOP", "permission", "reviewer"),
        "stable_check": "python3 scripts/validate_course.py curriculum",
    },
    "module-04.md": {
        "artifacts": (
            "artifacts/module-04/change-brief.md",
            "artifacts/module-04/controlled-change-plan.md",
            "artifacts/module-04/change-review-gate.md",
        ),
        "markers": ("acceptance", "focused", "review", "verdict"),
        "stable_check": "PYTHONPATH=projects/training-task-app/src python3 -m pytest projects/training-task-app/tests -q",
    },
    "module-05.md": {
        "artifacts": (
            "artifacts/module-05/traceability-matrix.md",
            "artifacts/module-05/test-agent-workflow.md",
            "artifacts/module-05/triage-and-release-gate.md",
        ),
        "markers": ("source", "check", "output", "STOP"),
        "stable_check": "PYTHONPATH=projects/training-task-app/src python3 -m pytest projects/training-task-app/tests -q",
    },
    "module-06.md": {
        "artifacts": (
            "artifacts/module-06/threat-model.md",
            "artifacts/module-06/approval-matrix.md",
            "artifacts/module-06/evaluation-dataset.md",
            "artifacts/module-06/trace-record.md",
            "artifacts/module-06/decision-log.md",
        ),
        "markers": ("SAFE-CHK-006", "trace_id", "redaction", "STOP"),
        "stable_check": "python3 projects/reference-control-plane/scripts/check_reference_control_plane.py",
    },
}


def extract_catalog_section(catalog: str, title: str) -> str:
    marker = f"### {title}"
    start = catalog.index(marker)
    next_heading = catalog.find("\n### ", start + len(marker))
    return catalog[start:] if next_heading == -1 else catalog[start:next_heading]


def extract_lesson_source_section(lesson: str) -> str:
    return lesson.split("## Официальные источники", 1)[1]


def extract_self_check_block(guide: str) -> str:
    section = guide.split("## Повторная команда", 1)[1]
    match = re.search(r"```(?:bash|sh|shell)\n(?P<commands>.*?)\n```", section, re.DOTALL)
    assert match, "repeat command must be a shell code block"
    return match.group("commands")


def has_complete_tier_1_record(catalog: str, url: str) -> bool:
    for section in re.split(r"(?=^### )", catalog, flags=re.MULTILINE):
        if f"]({url})" not in section:
            continue
        if all(
            marker in section
            for marker in (
                "- Роль:",
                "Tier 1",
                "- Scope:",
                "- Canonical URL:",
                "- Checked: 2026-07-13.",
                "Ограничения:",
            )
        ):
            return True
    return False


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


def test_task11_assessment_assets_are_complete_and_scored_consistently():
    guides = sorted(Path("assessments/checkpoints").glob("module-*.md"))
    assert [path.name for path in guides] == [
        f"module-{number:02d}.md" for number in range(1, 8)
    ]

    for guide in guides:
        text = guide.read_text(encoding="utf-8")
        assert "## Артефакты" in text
        assert "## Критерии оценки" in text
        assert "## Наблюдаемое evidence" in text
        assert "## Критические дефекты" in text
        assert "## Маршрут исправления" in text
        assert "## Повторная команда" in text
        rows = [
            line
            for line in text.splitlines()
            if line.startswith("|")
            and not line.startswith("| Критерий")
            and not line.startswith("| ---")
            and line.count("|") == 5
        ]
        assert len(rows) == 4, guide

        self_check = extract_self_check_block(text)
        assert self_check.splitlines()[0] == "set -euo pipefail"
        assert "test -s" in self_check
        assert "grep -Eq" in self_check
        assert re.search(
            r"(?m)^(?:grep -Eq|grep -Eqi|python3 .*validate_course|.*pytest|python3 .*check_reference_control_plane)",
            self_check,
        )

        if guide.name != "module-07.md":
            requirements = CHECKPOINT_SELF_CHECK_REQUIREMENTS[guide.name]
            for artifact in requirements["artifacts"]:
                assert artifact in self_check, (guide, artifact)
            for marker in requirements["markers"]:
                assert marker in self_check, (guide, marker)
            assert requirements["stable_check"] in self_check, guide

    rubric = Path("assessments/final-rubric.md").read_text(encoding="utf-8")
    assert "11/15" in rubric
    assert "без нулей" in rubric
    assert "safety checkpoint" in rubric
    assert "reproducible" in rubric
    assert "risk report" in rubric


def test_task11_lesson_source_matrix_and_catalog_are_traceable():
    matrix = Path("docs/lesson-source-matrix.md").read_text(encoding="utf-8")
    rows = [
        line
        for line in matrix.splitlines()
        if re.match(r"^\|\s*(?:[1-9]|1[0-9]|2[01])\s*\|", line)
    ]
    assert len(rows) == 21
    lesson_sources = {
        int(match.group(1)): path
        for path in Path("curriculum").glob("module-*/lesson-*.md")
        if (match := re.search(r"lesson-(\d+)-", path.name))
    }
    assert set(lesson_sources) == set(range(1, 22))
    parsed_mapping = {}
    for row in rows:
        cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
        lesson_number = int(cells[0])
        primary_urls = re.findall(r"https?://[^)\s]+", cells[1])
        supporting_urls = re.findall(r"https?://[^)\s]+", cells[2])
        assert len(primary_urls) == 1, row
        assert "Tier 1" in cells[1] and "2026-07-13" in cells[3], row
        parsed_mapping[lesson_number] = (primary_urls[0], cells[4])
        lesson_text = lesson_sources[lesson_number].read_text(encoding="utf-8")
        lesson_source_section = extract_lesson_source_section(lesson_text)
        assert primary_urls[0] in lesson_text, row
        assert primary_urls[0] in lesson_source_section, row
        for url in supporting_urls:
            assert url in lesson_source_section, row

    assert parsed_mapping == CANONICAL_LESSON_SOURCE_MAPPING
    assert "Поддерживающий Tier 2/3" in matrix
    assert "Ограничение вендора" in matrix
    assert "только URL, который указан в `## Официальные источники`" in matrix
    assert "catalog extensions" in matrix

    catalog = Path("docs/source-catalog.md").read_text(encoding="utf-8")
    assert has_complete_tier_1_record(
        catalog, "https://developers.openai.com/api/docs/guides/agents"
    )
    tier_1_start = re.search(r"^## Tier 1:", catalog, re.MULTILINE).start()
    tier_2_start = re.search(r"^## Tier 2:", catalog, re.MULTILINE).start()
    tier_1_region = catalog[tier_1_start:tier_2_start]
    for url, _topic in CANONICAL_LESSON_SOURCE_MAPPING.values():
        assert url in tier_1_region or has_complete_tier_1_record(catalog, url), url
    all_lesson_text = "\n".join(
        path.read_text(encoding="utf-8") for path in lesson_sources.values()
    )
    for url in CATALOG_ONLY_EXTENSION_URLS:
        assert url not in all_lesson_text, url
        assert url not in matrix, url
        assert url in catalog, url

    catalog_urls = []
    for title, url in TASK11_SOURCE_RECORDS.items():
        section = extract_catalog_section(catalog, title)
        assert catalog.count(f"### {title}") == 1
        assert "- Роль:" in section
        assert "Tier 1" in section
        assert "- Scope:" in section
        canonical_url = re.search(
            r"^- Canonical URL: \[[^]]+\]\((https?://[^)]+)\)$",
            section,
            re.MULTILINE,
        )
        assert canonical_url and canonical_url.group(1) == url
        assert "- Checked: 2026-07-13." in section
        assert "Ограничения:" in section
        catalog_urls.append(url)
    assert len(catalog_urls) == len(set(catalog_urls))


def test_task11_module07_self_check_covers_mappings_runs_and_safety_evidence():
    guide = Path("assessments/checkpoints/module-07.md").read_text(encoding="utf-8")
    self_check = extract_self_check_block(guide)

    assert self_check.splitlines()[0] == "set -euo pipefail"
    assert "test -s" in self_check
    assert "grep -Eq" in self_check
    assert "python3 -c" in self_check
    for mapping_entry in CANONICAL_TEMPLATE_MAPPING:
        assert mapping_entry["template"] in self_check
        assert mapping_entry["artifact"] in self_check
    for artifact in (
        "artifacts/capstone/evidence-index.md",
        "artifacts/capstone/run-evidence.md",
        "artifacts/capstone/corrections.md",
        "artifacts/capstone/risk-report.md",
        "artifacts/capstone/final-report.md",
        "artifacts/capstone/defense-notes.md",
    ):
        assert artifact in self_check
    for marker in (
        "N-01",
        "F-01",
        "F-02",
        "F-03",
        "STOP",
        "owner",
        "receiver",
        "correction",
        "re-run",
        "resume",
        "untrusted",
        "least privilege",
        "residual risk",
    ):
        assert marker in self_check


def test_internal_markdown_links_resolve():
    roots = (
        Path("README.md"),
        Path("docs"),
        Path("curriculum"),
        Path("agents"),
        Path("projects"),
        Path("templates"),
        Path("assessments"),
        Path("glossary"),
    )
    files = [roots[0]]
    for root in roots[1:]:
        files.extend(root.rglob("*.md"))
    for path in files:
        text = path.read_text(encoding="utf-8")
        for raw_target in LINK_RE.findall(text):
            target = local_markdown_path(raw_target)
            if target is None:
                continue
            assert (path.parent / target).resolve().exists(), f"{path}: {raw_target}"


def test_local_markdown_path_strips_query_and_fragment_from_relative_path():
    assert local_markdown_path("../README.md?via=checkpoint#result") == "../README.md"


def test_local_markdown_path_skips_external_schemes_and_network_locations():
    for target in (
        "http://example.com/guide.md",
        "https://example.com/guide.md",
        "mailto:course@example.com",
        "ftp://example.com/guide.md",
        "//example.com/guide.md",
    ):
        assert local_markdown_path(target) is None


def test_source_matrix_contains_all_21_lessons():
    text = Path("docs/lesson-source-matrix.md").read_text(encoding="utf-8")
    rows = re.findall(r"^\|\s*(?:[1-9]|1[0-9]|2[01])\s*\|", text, flags=re.MULTILINE)
    assert len(rows) == 21


def test_seven_checkpoint_guides_exist():
    guides = sorted(Path("assessments/checkpoints").glob("module-*.md"))
    assert len(guides) == 7


def test_checkpoint_index_links_each_module_guide_and_each_guide_links_back():
    index = Path("assessments/checkpoints/README.md").read_text(encoding="utf-8")
    for number in range(1, 8):
        guide = Path(f"assessments/checkpoints/module-{number:02d}.md")
        assert f"](module-{number:02d}.md)" in index
        assert "](README.md)" in guide.read_text(encoding="utf-8")


def test_student_project_tracks_exist():
    required = (
        Path("projects/starter-control-plane/control-plane.yaml"),
        Path("projects/reference-control-plane/control-plane.yaml"),
        Path("projects/reference-control-plane/decision-log.md"),
        Path("projects/capstone.md"),
    )
    assert all(path.is_file() for path in required)


def test_curriculum_has_no_unresolved_authoring_markers():
    markers = ("TO" + "DO", "TB" + "D", "FIX" + "ME")
    for path in Path("curriculum").rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        assert not any(marker in text for marker in markers), path
