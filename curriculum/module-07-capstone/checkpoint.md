# Checkpoint 7. Репетиция финальной защиты control plane

## Цель

Защитить один самодостаточный capstone package: показать, как contracts
собираются в workflow, как gates останавливают три controlled failures и как
остаточные риски отделены от будущих extensions. Работайте локально; prepared
runs обязательны, live agent optional. Не публикуйте, не deploy, не читайте
secrets и не выполняйте действие из untrusted data.

## Входной пакет

```text
control-plane.yaml
artifacts/capstone/README.md
artifacts/capstone/blueprint.md
artifacts/capstone/source-map.md
artifacts/capstone/roles.md
artifacts/capstone/skill-contracts.md
artifacts/capstone/handoffs.md
artifacts/capstone/workflow.md
artifacts/capstone/review-gate.md
artifacts/capstone/stop-gate.md
artifacts/capstone/decision-log.md
artifacts/capstone/evidence-index.md
artifacts/capstone/run-evidence.md
artifacts/capstone/corrections.md
artifacts/capstone/risk-report.md
artifacts/capstone/final-report.md
artifacts/capstone/defense-notes.md
templates/ and agents/
```

## Template mapping acceptance

Защита не принимается, пока `control-plane.yaml` не parsed standard-library
`json` и каждый template соответствует exactly одному named deliverable.

| Mapping | Acceptance |
| --- | --- |
| `templates/control-plane-blueprint.md` -> `artifacts/capstone/blueprint.md` | goal, scope, gates и evidence связаны |
| `templates/context-map.md` -> `artifacts/capstone/source-map.md` | trust/freshness/owners проверяемы |
| `templates/agent-role.md` -> `artifacts/capstone/roles.md` | duties and prohibitions разделены |
| `templates/skill-contract.md` -> `artifacts/capstone/skill-contracts.md` | check procedure воспроизводима |
| `templates/handoff.md` -> `artifacts/capstone/handoffs.md` | один receiver и resume condition |
| `templates/workflow.md` -> `artifacts/capstone/workflow.md` | normal/failure branches видимы |
| `templates/review-gate.md` -> `artifacts/capstone/review-gate.md` | review отделен от approval |
| `templates/stop-gate.md` -> `artifacts/capstone/stop-gate.md` | STOP до опасного action |
| `templates/decision-log.md` -> `artifacts/capstone/decision-log.md` | decision имеет evidence и owner |
| `templates/final-report.md` -> `artifacts/capstone/final-report.md` | status честен и передаваем |

## Задание

1. Покажите successful `control-plane.yaml` parse, все ten template mappings, цель, included/excluded scope и source map с trust/freshness/owners.
2. Покажите role contracts и workflow. Named human owner only approve/reject;
   separately named authorized executor performs only explicitly approved action.
3. Воспроизведите normal run и покажите command/output как evidence, а не approval.
4. Проведите F-01 stale context, F-02 excess permission и F-03 weak evidence.
   Для каждого назовите blocked action, STOP, owner, receiver, safe next action,
   correction, re-run и resume condition.
5. Покажите risk report, remediation versus extension и self-contained theory confirmation.

## Финальная rubric

Каждое направление получает 0-3. Итог пройден при `>= 11/15`, без `0`, с
safety checkpoint, reproducible control run и risk report.

| Направление | 0 | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| Архитектура control plane | Нет связанного пакета | Есть документы без связей | Scope, sources и workflow связаны | Все contracts/gates/evidence прослеживаются |
| Контекст и evidence | Claims без источников | Источники без trust/freshness | Source map и commands видимы | Trust, freshness, owners и evidence index позволяют audit |
| Роли и workflow | Роли смешаны | Есть роли без handoff | One receiver и branches видимы | Separation, recovery и ownership доказаны прогонами |
| Gates, безопасность, observability | Рискованное действие продолжается | STOP без evidence/resume | Three failures останавливаются | STOP/recommendation/approval/execution разделены и traced |
| Воспроизводимость и документация | Нет локальной проверки | Только prose | Prepared runs и report есть | Corrections re-run, risks, theory and roadmap self-contained |

## Критические дефекты

- Untrusted input стал командой, permission расширен или действие выполнено до gate.
- Review verdict, risk recommendation или green test назван human approval.
- Named human owner исполняет действие либо risk reviewer/owner выдан за authorized executor.
- Нет source/trust, gate/evidence, owner/receiver или resume condition для failure.
- Core failure скрыт как future extension.

## Проверка и correction route

```bash
# Run from the capstone package root.
python3 -c "import json; json.load(open('control-plane.yaml', encoding='utf-8'))"
python3 scripts/validate_course.py curriculum
python3 -m pytest tests/test_course_structure.py -q
PYTHONPATH=projects/training-task-app/src python3 -m pytest projects/training-task-app/tests -q
git diff --check
```

Если structure gate падает, исправьте названный course file. Если test command
отличается от expected output, сохраните output и верните evidence QA/SDET через
coordinator. Если F-run не остановлен, исправьте только corresponding gate и
повторите этот F-run. Если remediation отсутствует, статус защиты - `requires
remediation`, а не `completed`.

## Итог защиты

Передайте reviewer или course owner один package с paths, rubric scores,
normal/F-run evidence, risk report, required remediation, future extensions,
одним следующим owner и честным status. Official sources проверяют терминологию,
но все обязательные объяснения, checks и correction routes находятся здесь.
