# Compact AI Agent Control Plane Course Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Создать полный самодостаточный русскоязычный курс из 21 урока, семи checkpoints, учебного Python-стенда, шаблонов, assessment-материалов и capstone-проекта.

**Architecture:** Курс строится artifact-first: каждый модуль добавляет проверяемые артефакты к одному control plane. Сначала создаются автоматические структурные проверки и локальный учебный стенд, затем семь модулей, после чего материалы связываются сквозной навигацией и итоговой rubric.

**Tech Stack:** Markdown, YAML, Python 3.11+, pytest, Git, стандартная библиотека Python.

## Global Constraints

- Курс содержит ровно 21 обязательный урок в семи модулях.
- Ориентировочная продолжительность основного маршрута: 50-70 часов.
- Целевая аудитория уже владеет базовыми Python и Git.
- Весь обязательный материал написан на русском языке.
- Теория, задания, критерии готовности и маршруты исправления находятся в репозитории.
- Внешние ссылки подтверждают материал, но не заменяют его.
- Официальная документация имеет приоритет над официальными курсами и примерами.
- Обязательный маршрут можно пройти без платного API-ключа и облачной платформы.
- Каждый урок создаёт один основной инженерный артефакт.
- Checkpoint не считается отдельным уроком.
- Безопасность, проверка результата и необходимые базовые навыки нельзя исключать ради сокращения.
- Основной стек ограничен Python 3.11+, Git, Markdown, YAML и pytest.
- Docker, Kubernetes, production deployment, fine-tuning и глубокая математика нейросетей остаются вне обязательного маршрута.

---

## File Map

- `scripts/validate_course.py` — проверяет количество модулей, уроков, checkpoints, обязательные разделы и источники.
- `tests/test_course_structure.py` — фиксирует структурный контракт курса.
- `tests/test_course_assets.py` — проверяет glossary, templates, assessments и проекты.
- `curriculum/README.md` — маршрут студента, prerequisites и правила двух режимов практики.
- `curriculum/module-*/` — семь модулей по три урока и одному checkpoint.
- `glossary/terms.md` — обязательная русская терминология.
- `templates/*.md` — десять переиспользуемых инженерных шаблонов.
- `projects/training-task-app/` — локальный Python-стенд и контролируемые сценарии.
- `projects/starter-control-plane/` — рабочая заготовка студента.
- `projects/reference-control-plane/` — законченный пример из другой предметной области.
- `projects/capstone.md` — постановка итогового проекта.
- `assessments/` — checkpoint-правила, итоговая rubric и ориентиры ответов.

---

### Task 1: Structural Validator and Course Entry Point

**Files:**
- Create: `scripts/validate_course.py`
- Create: `tests/test_course_structure.py`
- Create: `curriculum/README.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: утверждённую спецификацию `docs/superpowers/specs/2026-07-13-compact-course-content-design.md`.
- Produces: `validate_lesson(path) -> list[str]`, `validate_module(path) -> list[str]`, `validate_course(root) -> list[str]` и единый формат урока для Tasks 4-10.

- [ ] **Step 1: Write validator tests that define the course contract**

Создать `tests/test_course_structure.py` с проверками:

```python
from scripts.validate_course import REQUIRED_SECTIONS, validate_lesson


def test_required_sections_match_approved_lesson_format():
    assert REQUIRED_SECTIONS == (
        "## Результат урока",
        "## Зачем это инженеру",
        "## Теория",
        "## Ключевые термины",
        "## Рабочий пример",
        "## Практика",
        "## Проверка результата",
        "## Типичные ошибки",
        "## Контрольные вопросы",
        "## Официальные источники",
    )


def test_lesson_requires_official_https_source(tmp_path):
    lesson = tmp_path / "lesson.md"
    lesson.write_text("\n".join(REQUIRED_SECTIONS), encoding="utf-8")
    assert "нет ссылки на официальный источник" in validate_lesson(lesson)
```

- [ ] **Step 2: Run tests and confirm the structural gate is red**

Run: `python3 -m pytest tests/test_course_structure.py -q`

Expected: collection fails because `scripts.validate_course` does not exist.

- [ ] **Step 3: Implement the validator**

Создать `scripts/validate_course.py`:

```python
from __future__ import annotations

import argparse
import re
from pathlib import Path


REQUIRED_SECTIONS = (
    "## Результат урока",
    "## Зачем это инженеру",
    "## Теория",
    "## Ключевые термины",
    "## Рабочий пример",
    "## Практика",
    "## Проверка результата",
    "## Типичные ошибки",
    "## Контрольные вопросы",
    "## Официальные источники",
)


def validate_lesson(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors = [f"{path}: нет раздела {section}" for section in REQUIRED_SECTIONS if section not in text]
    if "https://" not in text:
        errors.append("нет ссылки на официальный источник")
    if re.search(r"[А-Яа-яЁё]", text) is None:
        errors.append(f"{path}: нет русскоязычного объяснения")
    return errors


def validate_module(path: Path) -> list[str]:
    errors: list[str] = []
    lessons = sorted(path.glob("lesson-*.md"))
    if not (path / "README.md").is_file():
        errors.append(f"{path}: нет README.md")
    if not (path / "checkpoint.md").is_file():
        errors.append(f"{path}: нет checkpoint.md")
    if len(lessons) != 3:
        errors.append(f"{path}: ожидалось 3 урока, найдено {len(lessons)}")
    for lesson in lessons:
        errors.extend(validate_lesson(lesson))
    return errors


def validate_course(root: Path) -> list[str]:
    if root.name.startswith("module-"):
        return validate_module(root)
    modules = sorted(path for path in root.glob("module-*") if path.is_dir())
    errors: list[str] = []
    if len(modules) != 7:
        errors.append(f"{root}: ожидалось 7 модулей, найдено {len(modules)}")
    for module in modules:
        errors.extend(validate_module(module))
    lesson_count = sum(len(list(module.glob("lesson-*.md"))) for module in modules)
    if lesson_count != 21:
        errors.append(f"{root}: ожидался 21 урок, найдено {lesson_count}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Проверяет структуру курса")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    errors = validate_course(args.path)
    if errors:
        print("\n".join(errors))
        return 1
    print("Курс проверен: ошибок нет")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Write the course entry page**

`curriculum/README.md` must contain: prerequisites, 50-70 hour estimate, seven-module table, artifact-first flow, mandatory offline/no-key mode, optional live-agent mode, checkpoint rules and links to every module.

Update `README.md` so the primary call to action points to `curriculum/README.md`.

- [ ] **Step 5: Run focused verification**

Run: `python3 -m pytest tests/test_course_structure.py::test_required_sections_match_approved_lesson_format tests/test_course_structure.py::test_lesson_requires_official_https_source -q`

Expected: `2 passed`.

- [ ] **Step 6: Commit the validator foundation**

```bash
git add README.md curriculum/README.md scripts/validate_course.py tests/test_course_structure.py
git commit -m "feat: add course structure validator"
```

---

### Task 2: Glossary and Reusable Artifact Templates

**Files:**
- Create: `glossary/terms.md`
- Create: `templates/control-plane-blueprint.md`
- Create: `templates/context-map.md`
- Create: `templates/agent-role.md`
- Create: `templates/skill-contract.md`
- Create: `templates/handoff.md`
- Create: `templates/workflow.md`
- Create: `templates/review-gate.md`
- Create: `templates/stop-gate.md`
- Create: `templates/decision-log.md`
- Create: `templates/final-report.md`
- Create: `tests/test_course_assets.py`
- Modify: `templates/README.md`

**Interfaces:**
- Consumes: lesson format and artifact names from Task 1.
- Produces: canonical templates referenced by all modules and `REQUIRED_ASSETS` in `tests/test_course_assets.py`.

- [ ] **Step 1: Write the asset existence test**

Создать `tests/test_course_assets.py`:

```python
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


def test_all_templates_exist_and_have_acceptance_criteria():
    for name in TEMPLATES:
        path = Path("templates") / name
        assert path.is_file(), path
        assert "## Критерии готовности" in path.read_text(encoding="utf-8")


def test_glossary_defines_required_terms():
    text = Path("glossary/terms.md").read_text(encoding="utf-8").lower()
    for term in TERMS:
        assert term.lower() in text, term
```

- [ ] **Step 2: Run the asset test and confirm it fails**

Run: `python3 -m pytest tests/test_course_assets.py -q`

Expected: failures list missing glossary and template files.

- [ ] **Step 3: Create the glossary**

For every required term provide: Russian name, original English term, concise definition, one engineering example and a contrast with the nearest confusing term. Link definitions to the official source catalog without making external reading mandatory.

- [ ] **Step 4: Create the ten templates**

Every template must contain:

- purpose and when to use it;
- copy-ready Markdown fields;
- one short filled example;
- `## Критерии готовности`;
- a warning against the main misuse of that artifact.

The blueprint fields are: goal, scope, context sources, roles, workflow, tools, gates, approvals, evidence, risks. The agent-role fields are: goal, inputs, outputs, permissions, forbidden actions, stop conditions, handoff. The workflow fields are: trigger, preconditions, steps, branches, gates, output and recovery.

- [ ] **Step 5: Verify and commit reusable assets**

Run: `python3 -m pytest tests/test_course_assets.py -q`

Expected: all asset tests pass.

```bash
git add glossary templates tests/test_course_assets.py
git commit -m "docs: add course glossary and artifact templates"
```

---

### Task 3: Self-Contained Python Training Stand

**Files:**
- Create: `projects/training-task-app/README.md`
- Create: `projects/training-task-app/requirements.md`
- Create: `projects/training-task-app/api/openapi.yaml`
- Create: `projects/training-task-app/src/task_app/__init__.py`
- Create: `projects/training-task-app/src/task_app/models.py`
- Create: `projects/training-task-app/src/task_app/service.py`
- Create: `projects/training-task-app/tests/test_service.py`
- Create: `projects/training-task-app/scenarios/ambiguous-change.md`
- Create: `projects/training-task-app/scenarios/defect-report.md`
- Create: `projects/training-task-app/scenarios/flaky-run.log`
- Create: `projects/training-task-app/scenarios/stale-documentation.md`
- Modify: `projects/README.md`

**Interfaces:**
- Consumes: Python 3.11+ and pytest.
- Produces: `Task`, `TaskStatus`, `TaskService.create_task()`, `TaskService.complete_task()` and deterministic evidence used by modules 2, 4, 5 and 6.

- [ ] **Step 1: Write stable service tests**

Создать `projects/training-task-app/tests/test_service.py`:

```python
import pytest

from task_app import TaskService, TaskStatus


def test_create_task_assigns_integer_id():
    task = TaskService().create_task("Проверить контракт")
    assert task.id == 1
    assert task.status is TaskStatus.OPEN


def test_empty_title_is_rejected():
    with pytest.raises(ValueError, match="Название задачи не может быть пустым"):
        TaskService().create_task("   ")


def test_duplicate_active_title_is_rejected():
    service = TaskService()
    service.create_task("Проверить контракт")
    with pytest.raises(ValueError, match="Активная задача с таким названием уже существует"):
        service.create_task("проверить КОНТРАКТ")


def test_unknown_task_cannot_be_completed():
    with pytest.raises(KeyError, match="Задача 99 не найдена"):
        TaskService().complete_task(99)


def test_complete_task_records_done_status():
    service = TaskService()
    task = service.create_task("Проверить контракт")
    completed = service.complete_task(task.id)
    assert completed.status is TaskStatus.DONE
```

- [ ] **Step 2: Run the stand tests and confirm failure**

Run: `PYTHONPATH=projects/training-task-app/src python3 -m pytest projects/training-task-app/tests -q`

Expected: import fails because `task_app` is not implemented.

- [ ] **Step 3: Implement the minimal domain model and service**

Создать `projects/training-task-app/src/task_app/models.py`:

```python
from dataclasses import dataclass
from enum import StrEnum


class TaskStatus(StrEnum):
    OPEN = "open"
    DONE = "done"


@dataclass(slots=True)
class Task:
    id: int
    title: str
    status: TaskStatus = TaskStatus.OPEN
```

Создать `projects/training-task-app/src/task_app/service.py`:

```python
from .models import Task, TaskStatus


class TaskService:
    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id = 1

    def create_task(self, title: str) -> Task:
        normalized = title.strip()
        if not normalized:
            raise ValueError("Название задачи не может быть пустым")
        if any(
            task.status is TaskStatus.OPEN and task.title.casefold() == normalized.casefold()
            for task in self._tasks.values()
        ):
            raise ValueError("Активная задача с таким названием уже существует")
        task = Task(id=self._next_id, title=normalized)
        self._tasks[task.id] = task
        self._next_id += 1
        return task

    def list_tasks(self) -> list[Task]:
        return [self._tasks[task_id] for task_id in sorted(self._tasks)]

    def complete_task(self, task_id: int) -> Task:
        if task_id not in self._tasks:
            raise KeyError(f"Задача {task_id} не найдена")
        self._tasks[task_id].status = TaskStatus.DONE
        return self._tasks[task_id]
```

Создать `projects/training-task-app/src/task_app/__init__.py`:

```python
from .models import Task, TaskStatus
from .service import TaskService

__all__ = ["Task", "TaskService", "TaskStatus"]
```

- [ ] **Step 4: Add documentation and controlled scenarios**

The requirements define create/list/complete behavior. `openapi.yaml` expresses the same contract. The four scenario files respectively contain: an ambiguous request, a reproducible defect, a recorded flaky history and documentation that conflicts with the current requirement. None of these scenarios may make the default pytest suite flaky or failing.

- [ ] **Step 5: Verify and commit the training stand**

Run: `PYTHONPATH=projects/training-task-app/src python3 -m pytest projects/training-task-app/tests -q`

Expected: all stand tests pass.

```bash
git add projects
git commit -m "feat: add self-contained training task app"
```

---

### Task 4: Module 1 - Control Plane Foundations

**Files:**
- Create: `curriculum/module-01-foundations/README.md`
- Create: `curriculum/module-01-foundations/lesson-01-chat-to-control-plane.md`
- Create: `curriculum/module-01-foundations/lesson-02-task-boundaries.md`
- Create: `curriculum/module-01-foundations/lesson-03-blueprint-v1.md`
- Create: `curriculum/module-01-foundations/checkpoint.md`

**Interfaces:**
- Consumes: `templates/control-plane-blueprint.md`, glossary and source catalog.
- Produces: `control-plane-blueprint.md` student artifact used by every later module.

- [ ] **Step 1: Write the three lessons using the canonical ten sections**

Lesson 1 explains LLM, prompt, agent, workflow and control plane through one change-request example. Lesson 2 teaches goal, scope, assumptions, permissions, irreversible actions and human ownership. Lesson 3 builds blueprint v1 with context, roles, workflow, gates and risks.

- [ ] **Step 2: Add practical outputs and local correction routes**

The three outputs are: comparison table, task boundary contract and blueprint v1. Each lesson includes a no-key prepared agent response, an optional live-agent prompt, observable acceptance criteria and corrections for common failures.

- [ ] **Step 3: Create checkpoint 1**

The student receives the ambiguous change scenario from the training app and must produce a bounded blueprint. The checkpoint rejects missing owner, missing stop condition, unspecified evidence or external-reading dependencies.

- [ ] **Step 4: Validate and commit module 1**

Run: `python3 scripts/validate_course.py curriculum/module-01-foundations`

Expected: `Курс проверен: ошибок нет`.

```bash
git add curriculum/module-01-foundations
git commit -m "docs: add control plane foundations module"
```

---

### Task 5: Module 2 - Context and Evidence

**Files:**
- Create: `curriculum/module-02-context/README.md`
- Create: `curriculum/module-02-context/lesson-04-source-hierarchy.md`
- Create: `curriculum/module-02-context/lesson-05-context-packet.md`
- Create: `curriculum/module-02-context/lesson-06-context-map-evidence-gate.md`
- Create: `curriculum/module-02-context/checkpoint.md`

**Interfaces:**
- Consumes: training app requirements, API contract, stale documentation scenario and `templates/context-map.md`.
- Produces: context map, context packet and evidence gate used by roles and workflows.

- [ ] **Step 1: Write lessons 4-6**

Cover source-of-truth hierarchy, fact versus assumption, live state, freshness metadata, minimal context packets, conflicting sources, citations, evidence sufficiency and stop behavior. Use the stale documentation scenario as the running example.

- [ ] **Step 2: Create checkpoint 2**

The student must detect the conflict between requirements and stale documentation, identify the authoritative source, record uncertainty and stop before unsupported implementation. Acceptance requires source owner, check date, confidence and reproducible evidence.

- [ ] **Step 3: Validate and commit module 2**

Run: `python3 scripts/validate_course.py curriculum/module-02-context`

Expected: no validation errors.

```bash
git add curriculum/module-02-context
git commit -m "docs: add context and evidence module"
```

---

### Task 6: Module 3 - Roles, Skills, Permissions and Handoff

**Files:**
- Create: `curriculum/module-03-roles-and-skills/README.md`
- Create: `curriculum/module-03-roles-and-skills/lesson-07-agent-role-contract.md`
- Create: `curriculum/module-03-roles-and-skills/lesson-08-tools-skills-permissions.md`
- Create: `curriculum/module-03-roles-and-skills/lesson-09-coordinator-handoff.md`
- Create: `curriculum/module-03-roles-and-skills/checkpoint.md`
- Create: `agents/coordinator.md`
- Create: `agents/implementation.md`
- Create: `agents/reviewer.md`
- Create: `agents/qa-sdet.md`
- Create: `agents/risk-reviewer.md`
- Modify: `agents/README.md`

**Interfaces:**
- Consumes: blueprint, context map, `templates/agent-role.md`, `templates/skill-contract.md` and `templates/handoff.md`.
- Produces: five role contracts and one coordinator handoff flow.

- [ ] **Step 1: Write lessons 7-9**

Explain role contracts, least privilege, tools versus skills, permission boundaries, input/output schemas, stop conditions, handoff packages, coordinator routing and failure ownership. Compare provider-specific implementations only after the vendor-neutral contract is clear.

- [ ] **Step 2: Create reusable example roles**

Every role file must specify goal, accepted inputs, required output, allowed tools, forbidden actions, stop conditions, quality criteria and handoff target. The reviewer cannot edit implementation; the implementation role cannot approve its own result; the risk reviewer owns risk analysis and the approval-gate process, while only the named human owner grants final irreversible-action approval.

- [ ] **Step 3: Create checkpoint 3 and verify**

The checkpoint injects a request that exceeds implementation permissions. Passing behavior is a structured stop and handoff, not task completion.

Run: `python3 scripts/validate_course.py curriculum/module-03-roles-and-skills`

Expected: no validation errors.

```bash
git add curriculum/module-03-roles-and-skills agents
git commit -m "docs: add agent roles and handoff module"
```

---

### Task 7: Module 4 - Development Workflow

**Files:**
- Create: `curriculum/module-04-development-workflow/README.md`
- Create: `curriculum/module-04-development-workflow/lesson-10-task-intake.md`
- Create: `curriculum/module-04-development-workflow/lesson-11-controlled-code-change.md`
- Create: `curriculum/module-04-development-workflow/lesson-12-engineering-gates.md`
- Create: `curriculum/module-04-development-workflow/checkpoint.md`

**Interfaces:**
- Consumes: training app, role contracts, context packet, `templates/workflow.md` and `templates/review-gate.md`.
- Produces: development workflow from intake through commit handoff.

- [ ] **Step 1: Write lessons 10-12**

Teach task intake, acceptance criteria, impact analysis, plan boundaries, small changes, test-first reasoning, diff review, documentation sync, commit evidence and separation of implementation from approval.

- [ ] **Step 2: Build the development practice**

Use a change requiring a new task priority field. The student must trace requirement -> affected code -> tests -> documentation -> review evidence without requiring a live model.

- [ ] **Step 3: Create checkpoint 4 and verify**

The checkpoint includes an implementation response that changes unrelated behavior. The control plane must reject scope drift and request a bounded revision.

Run: `python3 scripts/validate_course.py curriculum/module-04-development-workflow`

Expected: no validation errors.

```bash
git add curriculum/module-04-development-workflow
git commit -m "docs: add controlled development workflow module"
```

---

### Task 8: Module 5 - QA and SDET Workflow

**Files:**
- Create: `curriculum/module-05-qa-sdet-workflow/README.md`
- Create: `curriculum/module-05-qa-sdet-workflow/lesson-13-requirements-to-checks.md`
- Create: `curriculum/module-05-qa-sdet-workflow/lesson-14-api-ui-test-agents.md`
- Create: `curriculum/module-05-qa-sdet-workflow/lesson-15-regression-triage-release-gate.md`
- Create: `curriculum/module-05-qa-sdet-workflow/checkpoint.md`

**Interfaces:**
- Consumes: requirements, OpenAPI contract, pytest suite, defect and flaky fixtures.
- Produces: traceability matrix, test-agent workflow, defect evidence package and release gate.

- [ ] **Step 1: Write lessons 13-15**

Teach testable conditions, risk-based selection, API contract checks, UI checks as an optional extension, deterministic evidence, regression scope, flaky classification, defect reproduction, severity versus priority and release decisions.

- [ ] **Step 2: Add executable commands**

Every relevant lesson uses the stable command:

```bash
PYTHONPATH=projects/training-task-app/src python3 -m pytest projects/training-task-app/tests -q
```

The expected output is stated in the lesson. UI automation remains an optional Playwright example with a complete conceptual explanation in the core text.

- [ ] **Step 3: Create checkpoint 5 and verify**

The checkpoint asks the student to classify evidence from one defect report and one flaky log, select regression scope and produce a release gate. A release decision without traceability fails.

Run: `python3 scripts/validate_course.py curriculum/module-05-qa-sdet-workflow`

Expected: no validation errors.

```bash
git add curriculum/module-05-qa-sdet-workflow
git commit -m "docs: add QA and SDET workflow module"
```

---

### Task 9: Module 6 - Safety, Evaluation and Observability

**Files:**
- Create: `curriculum/module-06-safety-and-observability/README.md`
- Create: `curriculum/module-06-safety-and-observability/lesson-16-threat-model-prompt-injection.md`
- Create: `curriculum/module-06-safety-and-observability/lesson-17-stop-review-approval-gates.md`
- Create: `curriculum/module-06-safety-and-observability/lesson-18-evaluation-tracing-decision-log.md`
- Create: `curriculum/module-06-safety-and-observability/checkpoint.md`

**Interfaces:**
- Consumes: `templates/stop-gate.md`, `templates/review-gate.md`, `templates/decision-log.md`, NIST AI RMF, OWASP GenAI, provider safety docs and OpenTelemetry GenAI conventions.
- Produces: threat model, approval matrix, evaluation dataset, trace record and decision log.

- [ ] **Step 1: Write lessons 16-18**

Cover assets, actors, trust boundaries, indirect prompt injection, untrusted tool output, least privilege, reversible actions, human approval, stop versus review gates, evaluation cases, outcome metrics, traces, redaction and decision logging.

- [ ] **Step 2: Create checkpoint 6**

Inject an untrusted instruction into a documentation fixture. Passing behavior requires treating it as data, preventing privilege expansion, recording the event and requesting approval only for the intended action.

- [ ] **Step 3: Validate and commit module 6**

Run: `python3 scripts/validate_course.py curriculum/module-06-safety-and-observability`

Expected: no validation errors.

```bash
git add curriculum/module-06-safety-and-observability
git commit -m "docs: add safety and observability module"
```

#### Task 9 safety-review report

- Authority: risk reviewer owns risk analysis and the approval-gate process,
  returning a recommendation or `STOP`; only the named human owner grants final
  irreversible-action approval.
- Sources: added Tier 1 catalog entries for NIST AI RMF Core, OWASP LLM01:2025
  Prompt Injection and OpenTelemetry GenAI semantic conventions, all checked
  `2026-07-13`; the OpenTelemetry source is limited to trace conventions and
  attributes, while redaction remains local course safety policy.
- Regression guard: `tests/test_course_assets.py` checks the authority contract,
  canonical GenAI URL and Tier 1 catalog coverage.
- Verification: Module 3 and Module 6 validators, root pytest and the training
  stand pass. The root course validator remains blocked by the pre-Task-10
  baseline of six modules and 18 lessons, so Module 7 is deliberately out of
  scope for this Task 9 fix.
- Final fix: a separately named authorized executor, distinct from the named
  human owner and risk reviewer, executes an approved action; the human owner
  may only approve or reject, while the risk reviewer retains risk analysis,
  approval-gate ownership and recommendation/`STOP`. The regression test now
  checks this separation and validates role, scope, exact canonical URL and
  checked date independently for each NIST, OWASP and OpenTelemetry section.

---

### Task 10: Module 7, Starter Project, Reference Project and Capstone

**Files:**
- Create: `curriculum/module-07-capstone/README.md`
- Create: `curriculum/module-07-capstone/lesson-19-assemble-control-plane.md`
- Create: `curriculum/module-07-capstone/lesson-20-failure-injection-improvement.md`
- Create: `curriculum/module-07-capstone/lesson-21-audit-defense-roadmap.md`
- Create: `curriculum/module-07-capstone/checkpoint.md`
- Create: `projects/starter-control-plane/README.md`
- Create: `projects/starter-control-plane/control-plane.yaml`
- Create: `projects/reference-control-plane/README.md`
- Create: `projects/reference-control-plane/control-plane.yaml`
- Create: `projects/reference-control-plane/decision-log.md`
- Create: `projects/capstone.md`

**Interfaces:**
- Consumes: every required template and all artifacts from modules 1-6.
- Produces: complete student project contract, independent reference example and final defense package.

- [ ] **Step 1: Write lessons 19-21**

Lesson 19 assembles and validates all contracts. Lesson 20 runs a normal scenario and three failure injections: stale context, excess permission and weak evidence. Lesson 21 performs audit, prepares a defense and separates required remediation from future extensions.

- [ ] **Step 2: Create starter and reference projects**

The starter contains the exact directory structure and field prompts but no completed decisions. The reference project models a documentation-maintenance control plane, not the task application, and includes context, roles, workflow, gates, evidence and a decision log.

- [ ] **Step 3: Create capstone contract and checkpoint 7**

The capstone requires README, source map, role contracts, workflow, templates, gates, run evidence, risk report and self-contained theory confirmation. Checkpoint 7 is the defense rehearsal using the final rubric.

- [ ] **Step 4: Run the full structure gate**

Обновить import в `tests/test_course_structure.py` и добавить проверку полного дерева:

```python
from pathlib import Path

from scripts.validate_course import REQUIRED_SECTIONS, validate_course, validate_lesson


def test_complete_course_has_no_structure_errors():
    assert validate_course(Path("curriculum")) == []
```

Run: `python3 scripts/validate_course.py curriculum`

Expected: 7 modules, 21 lessons, 7 checkpoints and no errors.

Run: `python3 -m pytest tests/test_course_structure.py -q`

Expected: all structure tests pass.

- [ ] **Step 5: Commit module 7 and projects**

```bash
git add curriculum/module-07-capstone projects/starter-control-plane projects/reference-control-plane projects/capstone.md
git commit -m "docs: add capstone module and project tracks"
```

---

### Task 11: Assessments, Source Traceability and Answer Guidance

**Files:**
- Create: `assessments/README.md`
- Create: `assessments/final-rubric.md`
- Create: `assessments/answer-guidelines.md`
- Create: `assessments/checkpoints/README.md`
- Create: `assessments/checkpoints/module-01.md`
- Create: `assessments/checkpoints/module-02.md`
- Create: `assessments/checkpoints/module-03.md`
- Create: `assessments/checkpoints/module-04.md`
- Create: `assessments/checkpoints/module-05.md`
- Create: `assessments/checkpoints/module-06.md`
- Create: `assessments/checkpoints/module-07.md`
- Create: `docs/lesson-source-matrix.md`
- Modify: `docs/source-catalog.md`

**Interfaces:**
- Consumes: all lessons, module checkpoints and `docs/source-catalog.md`.
- Produces: consistent 0-2 checkpoint scoring, 0-3 capstone scoring and lesson-to-source traceability.

- [ ] **Step 1: Write checkpoint scoring guides**

Each module guide lists evaluated artifacts, four criteria, observable evidence, critical defects, correction route and repeat command. The guidance must evaluate reasoning and evidence rather than exact wording.

- [ ] **Step 2: Write the final rubric**

Score architecture, context/evidence, roles/workflow, safety/observability and reproducibility from 0 to 3. Passing requires at least 11/15, no zero, passed safety checkpoint, reproducible run and risk report.

- [ ] **Step 3: Create source traceability matrix**

For lessons 1-21 list: primary Tier 1 source, supporting Tier 2/3 source when used, checked date, exact topic supported and vendor-specific limitation. Add DeepSeek, Qwen, NIST AI RMF, OWASP GenAI, MCP specification, A2A, OpenTelemetry GenAI, OpenAPI, JSON Schema, GitHub Actions and current ADK docs where relevant. Add the same verified sources to `docs/source-catalog.md` under the correct trust tier.

- [ ] **Step 4: Verify and commit assessments**

Run: `python3 scripts/validate_course.py curriculum`

Expected: no validation errors.

```bash
git add assessments docs/lesson-source-matrix.md docs/source-catalog.md
git commit -m "docs: add course assessments and source traceability"
```

---

### Task 12: Navigation, Full Verification and Course-Wide Review

**Files:**
- Modify: `README.md`
- Modify: `docs/repository-structure.md`
- Modify: `curriculum/README.md`
- Modify: `agents/README.md`
- Modify: `projects/README.md`
- Modify: `templates/README.md`
- Modify: `scripts/validate_course.py`
- Modify: `tests/test_course_structure.py`
- Modify: `tests/test_course_assets.py`

**Interfaces:**
- Consumes: every artifact produced by Tasks 1-11.
- Produces: one navigable, validated and self-contained course release.

- [ ] **Step 1: Complete navigation**

Every top-level README must point to the next student action. Add links among lessons, checkpoints, templates, training stand, assessments and capstone. Avoid duplicate theory in navigation pages.

- [ ] **Step 2: Extend automated checks**

Добавить в `tests/test_course_assets.py`:

```python
import re


LINK_RE = re.compile(r"\[[^]]+\]\(([^)]+)\)")


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
            target = raw_target.split("#", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            assert (path.parent / target).resolve().exists(), f"{path}: {raw_target}"


def test_source_matrix_contains_all_21_lessons():
    text = Path("docs/lesson-source-matrix.md").read_text(encoding="utf-8")
    rows = re.findall(r"^\|\s*(?:[1-9]|1[0-9]|2[01])\s*\|", text, flags=re.MULTILINE)
    assert len(rows) == 21


def test_seven_checkpoint_guides_exist():
    guides = sorted(Path("assessments/checkpoints").glob("module-*.md"))
    assert len(guides) == 7


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
```

- [ ] **Step 3: Run all automated verification**

Run:

```bash
python3 scripts/validate_course.py curriculum
python3 -m pytest tests -q
PYTHONPATH=projects/training-task-app/src python3 -m pytest projects/training-task-app/tests -q
git diff --check
```

Expected: validator exits `0`; both pytest commands report zero failures; `git diff --check` prints nothing.

- [ ] **Step 4: Perform course-wide content review**

For each lesson confirm: one primary outcome, one artifact, complete theory, local correction route, Russian explanations, official sources, no mandatory external reading and no dependency on a paid key. For each checkpoint confirm that it integrates prior artifacts and includes at least one failure path.

- [ ] **Step 5: Commit the completed course**

```bash
git add README.md docs curriculum agents projects templates assessments glossary scripts tests
git commit -m "docs: complete compact AI agent control plane course"
```

---

## Final Acceptance Gate

The implementation is complete only when all of these statements are proven by the commands in Task 12:

- the repository contains exactly 21 valid lessons and seven valid checkpoints;
- all required theory is in Russian and available locally;
- every lesson creates a named artifact and cites official sources;
- the training stand and course tests pass;
- starter, reference and capstone tracks are navigable;
- safety checkpoint and final rubric enforce critical-stop conditions;
- no mandatory task requires an API key, cloud account or external literature.

## Task 11 Correction Report (2026-07-13)

- Matrix rows 1-21 now carry exactly one Tier 1 primary URL that occurs in the
  corresponding lesson's `## Официальные источники`; unsupported catalog
  extensions are explicitly excluded from lesson dependencies.
- Added the complete Tier 1 record for the primary OpenAI Agents guide and
  retained DeepSeek, Qwen, A2A, GitHub Actions and ADK as catalog-only
  extensions when no lesson uses their URLs.
- Checkpoint self-checks now require nonempty listed artifacts, required
  evidence fields and a relevant stable validator, pytest or reference check.
  Module 7 additionally checks all ten mappings, N-01/F-01/F-02/F-03 evidence,
  safety authority and risk evidence.
- The repository baseline does not contain completed student artifacts, so
  student-artifact self-check commands were intentionally not executed during
  this correction; their presence and required checks are enforced by tests.
- Verification: `python3 scripts/validate_course.py curriculum` completed with
  no errors; focused assets tests passed 10, root course tests passed 13,
  training stand tests passed 11 and the reference control-plane check passed.
