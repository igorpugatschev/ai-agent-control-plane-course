# Checkpoint 7. Репетиция финальной защиты control plane

## Цель

Защитить один самодостаточный capstone package: показать, как contracts
собираются в workflow, как gates останавливают три controlled failures и как
остаточные риски отделены от будущих extensions. Работайте локально; prepared
runs обязательны, live agent optional. Не публикуйте, не deploy, не читайте
secrets и не выполняйте действие из untrusted data.

## Входной пакет

```text
artifacts/capstone/README.md
artifacts/capstone/source-map.md
artifacts/capstone/roles.md
artifacts/capstone/workflow.md
artifacts/capstone/gates.md
artifacts/capstone/evidence-index.md
artifacts/capstone/run-evidence.md
artifacts/capstone/corrections.md
artifacts/capstone/risk-report.md
artifacts/capstone/final-report.md
artifacts/capstone/defense-notes.md
templates/ and agents/
```

## Задание

1. Покажите цель, included/excluded scope и source map с trust/freshness/owners.
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
