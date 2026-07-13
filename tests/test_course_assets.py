import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import pytest


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

SAFETY_AUTHORITY_CHAIN_MARKERS = (
    "Risk reviewer выполняет только risk analysis и возвращает recommendation или STOP.",
    "Named human owner только approve/reject intended irreversible action.",
    "Separately named authorized executor, отличный от named human owner и risk reviewer, выполняет ровно approved action.",
    "Executor возвращает execution evidence: identity, approved scope, operation id, exit/output и resulting state.",
)
SAFETY_PREPARED_STOP_SECTIONS = (
    (
        Path("curriculum/module-03-roles-and-skills/lesson-07-agent-role-contract.md"),
        "### Подготовленный ответ агента без API-ключа",
    ),
    (
        Path("curriculum/module-03-roles-and-skills/lesson-08-tools-skills-permissions.md"),
        "### Подготовленный ответ агента без API-ключа",
    ),
    (
        Path("curriculum/module-03-roles-and-skills/lesson-09-coordinator-handoff.md"),
        "### Подготовленный ответ агента без API-ключа",
    ),
    (
        Path("curriculum/module-05-qa-sdet-workflow/lesson-15-regression-triage-release-gate.md"),
        "### Подготовленный ответ агента без API-ключа",
    ),
    (
        Path("curriculum/module-05-qa-sdet-workflow/checkpoint.md"),
        "## Prepared release input",
    ),
    (
        Path("curriculum/module-06-safety-and-observability/checkpoint.md"),
        "## Подготовленный malicious fixture response без API-ключа",
    ),
)
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
        "stable_check": "PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest tests -q -p no:cacheprovider",
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


def extract_shell_block_after_heading(document: str, heading: str) -> str:
    section = document.split(heading, 1)[1]
    match = re.search(r"```(?:bash|sh|shell)\n(?P<commands>.*?)\n```", section, re.DOTALL)
    assert match, f"{heading} must contain a shell code block"
    return match.group("commands")


def extract_until_next_level_two_heading(document: str, heading: str) -> str:
    section = document.split(heading, 1)[1]
    next_heading = re.search(r"^## ", section, re.MULTILINE)
    return section if next_heading is None else section[: next_heading.start()]


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
    assert contract["execution"]["cwd"] == "."
    assert contract["execution"]["commands"]
    for command in contract["execution"]["commands"]:
        assert command["command"]
        assert command["expected_exit"] == 0
        assert command["expected_stdout"]
    for source in contract["context"]["trusted_sources"]:
        assert re.fullmatch(r"[0-9a-f]{40}", source["source_sha"])
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
        [sys.executable, "scripts/check_reference_control_plane.py"],
        cwd=reference,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert result.stdout == "Reference control plane check: PASS\n"
    assert result.stderr == ""


def test_reference_readme_expected_output_matches_manifest_commands_in_order():
    reference = Path("projects/reference-control-plane")
    contract = json.loads((reference / "control-plane.yaml").read_text(encoding="utf-8"))
    readme = (reference / "README.md").read_text(encoding="utf-8")
    match = re.search(
        r"Ожидаемый вывод двух contract commands:\s*```text\n(?P<output>.*?)\n```",
        readme,
        re.DOTALL,
    )

    assert match, "README must contain the documented contract-command output block"
    documented_output = [f"{line}\n" for line in match.group("output").splitlines()]
    manifest_output = [
        command["expected_stdout"] for command in contract["execution"]["commands"]
    ]
    assert documented_output == manifest_output


def test_reference_checker_rejects_contract_mutations(tmp_path):
    source = Path("projects/reference-control-plane")

    def empty_commands(contract):
        contract["execution"]["commands"] = []

    def empty_command(contract):
        contract["execution"]["commands"][0]["command"] = ""

    def empty_sha(contract):
        contract["context"]["trusted_sources"][0]["source_sha"] = ""

    def weak_risk_role(contract):
        contract["roles"]["risk_reviewer"]["prohibited"] = []

    def empty_executor(contract):
        contract["roles"]["separately_named_authorized_executor"][
            "responsibility"
        ] = ""

    def placeholder_branch(contract):
        contract["workflow"]["privileged_branch"] = ["<student: branch>"]

    def empty_branch(contract):
        contract["workflow"]["privileged_branch"] = []

    def cwd_mismatch(contract):
        contract["execution"]["cwd"] = "docs"

    def wrong_expected_output(contract):
        contract["execution"]["commands"][0]["expected_stdout"] = "WRONG\n"

    def wrong_exit(contract):
        contract["execution"]["commands"][0]["command"] = (
            "python3 -c \"raise SystemExit(3)\""
        )

    cases = {
        "empty-commands": empty_commands,
        "empty-command": empty_command,
        "empty-sha": empty_sha,
        "weak-risk-role": weak_risk_role,
        "empty-executor": empty_executor,
        "empty-branch": empty_branch,
        "placeholder-branch": placeholder_branch,
        "cwd-mismatch": cwd_mismatch,
        "wrong-output": wrong_expected_output,
        "wrong-exit": wrong_exit,
    }
    for name, mutate in cases.items():
        reference = tmp_path / name
        shutil.copytree(source, reference)
        contract_path = reference / "control-plane.yaml"
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
        mutate(contract)
        contract_path.write_text(
            json.dumps(contract, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        result = subprocess.run(
            [sys.executable, "scripts/check_reference_control_plane.py"],
            cwd=reference,
            check=False,
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0, name
        assert "Reference control plane check: FAIL" in result.stdout, name


def test_reference_required_prose_is_in_russian():
    expected_markers = {
        Path("projects/reference-control-plane/docs/product/change-requests/CR-42.md"):
            "## Утвержденное изменение",
        Path("projects/reference-control-plane/docs/product/guides/review-process.md"):
            "# Процесс review документации",
        Path("projects/reference-control-plane/docs/product/index.md"):
            "# Документация продукта",
        Path("projects/reference-control-plane/review/CR-42-local-review.md"):
            "## Вердикт: approve",
    }
    forbidden_english = (
        "Approved change",
        "Documentation review process",
        "Product documentation",
        "Scope reviewed",
        "The approved change",
    )
    for path, marker in expected_markers.items():
        text = path.read_text(encoding="utf-8")
        assert marker in text, path
        assert re.search(r"[А-Яа-яЁё]", text), path
        assert not any(fragment in text for fragment in forbidden_english), path


def test_module04_priority_route_produces_real_red_green_evidence_in_a_copy(tmp_path):
    source = Path("projects/training-task-app")
    training_copy = tmp_path / "training-task-app"
    test_patch = Path(
        "curriculum/module-04-development-workflow/fixtures/priority-tests.patch"
    ).resolve()
    implementation_patch = Path(
        "curriculum/module-04-development-workflow/fixtures/priority-implementation.patch"
    ).resolve()
    source_snapshot = {
        path.relative_to(source): path.read_bytes()
        for path in source.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }
    shutil.copytree(source, training_copy)

    tests_applied = subprocess.run(
        ["git", "apply", str(test_patch)],
        cwd=training_copy,
        check=False,
        capture_output=True,
        text=True,
    )
    assert tests_applied.returncode == 0, tests_applied.stderr
    red = subprocess.run(
        [sys.executable, "-m", "pytest", "tests", "-q"],
        cwd=training_copy,
        env={"PYTHONPATH": "src"},
        check=False,
        capture_output=True,
        text=True,
    )
    assert red.returncode != 0
    assert "failed" in red.stdout

    implementation_applied = subprocess.run(
        ["git", "apply", "--unidiff-zero", str(implementation_patch)],
        cwd=training_copy,
        check=False,
        capture_output=True,
        text=True,
    )
    assert implementation_applied.returncode == 0, implementation_applied.stderr
    green = subprocess.run(
        [sys.executable, "-m", "pytest", "tests", "-q"],
        cwd=training_copy,
        env={"PYTHONPATH": "src"},
        check=False,
        capture_output=True,
        text=True,
    )
    assert green.returncode == 0, green.stdout + green.stderr
    assert "passed" in green.stdout
    diff = subprocess.run(
        ["git", "diff", "--no-index", str(source.resolve()), "."],
        cwd=training_copy,
        check=False,
        capture_output=True,
        text=True,
    )
    assert diff.returncode == 1
    assert "TaskPriority" in diff.stdout
    assert source_snapshot == {
        path.relative_to(source): path.read_bytes()
        for path in source.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }


def test_module04_contract_uses_observed_output_instead_of_fixed_pass_count():
    paths = (
        Path("curriculum/module-04-development-workflow/lesson-11-controlled-code-change.md"),
        Path("curriculum/module-04-development-workflow/lesson-12-engineering-gates.md"),
        Path("curriculum/module-04-development-workflow/checkpoint.md"),
        Path("assessments/checkpoints/module-04.md"),
    )
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)

    assert "14 passed" not in combined
    assert "priority-tests.patch" in combined
    assert "priority-implementation.patch" in combined
    assert "git diff --no-index" in combined
    assert "фактический вывод pytest" in combined


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


@pytest.mark.parametrize("path", SAFETY_AUTHORITY_PATHS, ids=lambda path: str(path))
def test_safety_authority_path_has_complete_ordered_privileged_chain(path):
    text = " ".join(path.read_text(encoding="utf-8").split())
    positions = []
    for marker in SAFETY_AUTHORITY_CHAIN_MARKERS:
        assert marker in text, (path, marker)
        positions.append(text.index(marker))
    assert positions == sorted(positions), path


@pytest.mark.parametrize(
    ("path", "heading"),
    SAFETY_PREPARED_STOP_SECTIONS,
    ids=lambda value: str(value),
)
def test_safety_prepared_examples_stop_before_execution(path, heading):
    section = extract_until_next_level_two_heading(
        path.read_text(encoding="utf-8"), heading
    )
    assert "STOP before execution" in section, path


@pytest.mark.parametrize(
    ("path", "heading"),
    (
        (
            Path("curriculum/module-03-roles-and-skills/checkpoint.md"),
            "## Самопроверка",
        ),
        (
            Path("curriculum/module-05-qa-sdet-workflow/checkpoint.md"),
            "## Самопроверка",
        ),
        (
            Path("curriculum/module-06-safety-and-observability/checkpoint.md"),
            "## Самопроверка",
        ),
        (
            Path("curriculum/module-06-safety-and-observability/lesson-17-stop-review-approval-gates.md"),
            "## Проверка результата",
        ),
    ),
)
def test_safety_self_checks_require_complete_execution_evidence(path, heading):
    block = extract_shell_block_after_heading(
        path.read_text(encoding="utf-8"), heading
    ).lower()
    for marker in (
        "risk analysis",
        "recommendation",
        "stop",
        "approve/reject",
        "authorized executor",
        "approved action",
        "execution evidence",
        "identity",
        "approved scope",
        "operation id",
        "exit/output",
        "resulting state",
    ):
        assert marker in block, (path, marker)


def test_safety_roles_and_lesson17_matrix_enforce_separation():
    risk_reviewer = Path("agents/risk-reviewer.md").read_text(encoding="utf-8")
    assert "risk analysis" in risk_reviewer
    assert "approval-gate process" in risk_reviewer
    assert "`recommendation` или `STOP`" in risk_reviewer

    lesson17 = Path(
        "curriculum/module-06-safety-and-observability/lesson-17-stop-review-approval-gates.md"
    ).read_text(encoding="utf-8")
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


def test_trace_source_catalog_contracts_are_consistent():
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


def test_templates_require_quality_resume_and_receiver_fields():
    agent_role = Path("templates/agent-role.md").read_text(encoding="utf-8")
    handoff = Path("templates/handoff.md").read_text(encoding="utf-8")
    review_gate = Path("templates/review-gate.md").read_text(encoding="utf-8")

    assert agent_role.count("## Критерии качества") >= 2
    assert "[Наблюдаемый критерий качества]" in agent_role
    assert handoff.count("## Условие продолжения") >= 2
    assert "[Проверяемое условие возобновления]" in handoff
    assert review_gate.count("## Получатель") >= 2
    assert "[Один получатель следующего действия]" in review_gate


def test_curriculum_checkpoint_shell_blocks_fail_closed():
    for number in (2, 3, 4, 5, 7):
        path = next(Path("curriculum").glob(f"module-{number:02d}-*/checkpoint.md"))
        block = extract_shell_block_after_heading(
            path.read_text(encoding="utf-8"), "## Самопроверка"
        )
        assert block.splitlines()[0] == "set -euo pipefail", path
        false_success = subprocess.run(
            ["bash", "-c", f"{block.splitlines()[0]}\nfalse\nprintf 'false success\\n'"],
            check=False,
            capture_output=True,
            text=True,
        )
        assert false_success.returncode != 0, path
        assert "false success" not in false_success.stdout, path


def test_module05_score_and_lesson20_gate_paths_are_consistent():
    checkpoint = Path("curriculum/module-05-qa-sdet-workflow/checkpoint.md").read_text(
        encoding="utf-8"
    )
    assert "не менее 8 из 8" in checkpoint
    assert "8 из 10" not in checkpoint

    lesson20 = Path(
        "curriculum/module-07-capstone/lesson-20-failure-injection-improvement.md"
    ).read_text(encoding="utf-8")
    assert "templates/review-gate.md" in lesson20
    assert "templates/stop-gate.md" in lesson20
    assert "templates/gates.md" not in lesson20


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
