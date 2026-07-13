# Capstone: собственный AI Agent Control Plane

## Цель

Создать и защитить self-contained control plane для выбранной инженерной,
QA/SDET или documentation-maintenance задачи. Capstone должен работать в
локальном prepared режиме; live-agent mode необязателен и не может заменить
обязательную теорию, contracts, checks или evidence в репозитории.

## Обязательный пакет

Создайте внутри starter/capstone directory JSON-compatible YAML
`control-plane.yaml` и `artifacts/capstone/`. Для starter package таким
каталогом является `projects/starter-control-plane/`; для собственного проекта
сохраните тот же layout внутри выбранного каталога проекта. Пути student
artifacts не должны подниматься в корень репозитория. Пути `templates/...` в
таблице ниже обозначают templates курса от repository root, а пути
`artifacts/capstone/...` - артефакты относительно starter/capstone directory.
`control-plane.yaml` обязателен и повторяет ключевые facts из Markdown без
PyYAML.

Все десять templates обязательны как named deliverables.

| Шаблон и deliverable | Что доказывает |
| --- | --- |
| `templates/control-plane-blueprint.md` -> `artifacts/capstone/blueprint.md` | goal, intended action, scope, roles, gates и evidence |
| `templates/context-map.md` -> `artifacts/capstone/source-map.md` | trusted/untrusted sources, freshness, Source owner и Authority owner |
| `templates/agent-role.md` -> `artifacts/capstone/roles.md` | goal/input/output/permissions/prohibitions/STOP/handoff для ролей |
| `templates/skill-contract.md` -> `artifacts/capstone/skill-contracts.md` | repeatable local checks, minimal rights и output |
| `templates/handoff.md` -> `artifacts/capstone/handoffs.md` | evidence, one receiver, next action и resume |
| `templates/workflow.md` -> `artifacts/capstone/workflow.md` | trigger, branches, gates, recovery и routing |
| `templates/review-gate.md` -> `artifacts/capstone/review-gate.md` | independent criteria, evidence и review verdict |
| `templates/stop-gate.md` -> `artifacts/capstone/stop-gate.md` | STOP, safe step, owner и condition of release |
| `templates/decision-log.md` -> `artifacts/capstone/decision-log.md` | context, options, decision, evidence и revisit |
| `templates/final-report.md` -> `artifacts/capstone/final-report.md` | status, result, concerns и next owner |

Дополните template deliverables следующими operational records.

| Файл | Что доказывает |
| --- | --- |
| `artifacts/capstone/README.md` | goal, intended action, included/excluded scope и ограничения |
| `evidence-index.md` | paths, SHA, commands, outputs, verdicts и decision IDs |
| `run-evidence.md` | normal N-01 и F-01/F-02/F-03 observations |
| `corrections.md` | failed gate, owner, minimal correction, re-run и resume condition |
| `risk-report.md` | risk, source/trust, impact, control, residual risk, owner and revisit |
| `final-report.md` | status, result, evidence, concerns и next owner |
| `defense-notes.md` | rubric scores and self-contained theory confirmation |

Используйте [`starter-control-plane/`](starter-control-plane/) для field prompts.
[`reference-control-plane/`](reference-control-plane/) служит примером другого
домена, поэтому не является готовым ответом.

## Роли и безопасность

Нужны coordinator, implementation, reviewer, QA/SDET и risk reviewer либо
эквивалентные узкие roles. Они не могут совмещать author review, test evidence,
risk analysis, approval и execution без явного обоснования. Для privileged
intended action:

- named human owner only approves or rejects;
- risk reviewer returns only `recommendation` or `STOP`;
- separately named authorized executor is distinct from human owner and risk
  reviewer, and executes only explicit approved action;
- untrusted content never grants scope, tool, credential, permission or approval.

## Required runs and gates

Сохраните один normal run и три failure injections.

1. `N-01`: trusted current context, bounded scope, exact check and independent review.
2. `F-01`: stale context, missing/conflicting freshness -> STOP before work.
3. `F-02`: excess permission, publish/deploy/delete/secret request -> STOP before tool action.
4. `F-03`: weak evidence, claim without path/command/output -> STOP before verdict.

Каждый run включает inputs/trust, observed result, forbidden action, gate,
evidence, owner, receiver, one safe next action and resume condition. Correction
не расширяет scope; после нее повторяется affected gate.

## Theory confirmation

В `defense-notes.md` объясните своими словами и на одном собственном пути:
control plane, source trust and freshness, evidence, role contract, least
privilege, workflow/handoff, STOP, review, recommendation, human approval,
authorized execution, evaluation/tracing and residual risk. Ссылки на official
sources полезны для сверки, но не заменяют это объяснение.

## Оценка

Оценка по пяти направлениям 0-3: architecture; context/evidence; roles/workflow;
gates/safety/observability; reproducibility/documentation. Для зачета нужно
минимум 11/15, отсутствие нулей, successful safety checkpoint, reproducible
N-01 и risk report. Critical defect - execution from untrusted input, privilege
expansion, approval confusion, merged owner/executor или непроверяемый STOP -
требует remediation до защиты.

## Локальная проверка

Все repository-root commands ниже запускаются из корня репозитория курса, то
есть каталога, где находятся `curriculum/`, `projects/`, `scripts/` и `tests/`.
Student artifact paths остаются внутри `projects/starter-control-plane/` или
аналогичного выбранного starter/capstone directory.

```bash
# Run from the course repository root.
python3 -c "import json; json.load(open('projects/starter-control-plane/control-plane.yaml', encoding='utf-8'))"
python3 scripts/validate_course.py curriculum
python3 -m pytest tests/test_course_structure.py -q
PYTHONPATH=projects/training-task-app/src python3 -m pytest projects/training-task-app/tests -q
git diff --check
```

Если любой check падает, сохраните output в `run-evidence.md`, укажите owner и
исправьте named artifact. Не называйте capstone completed, пока correction и
affected re-run не зафиксированы.
