# Module 07 checkpoint assessment guide

## Артефакты

- `control-plane.yaml` и десять mapped `artifacts/capstone/` deliverables.
- `artifacts/capstone/evidence-index.md`, `run-evidence.md`, `corrections.md`.
- `artifacts/capstone/risk-report.md`, `final-report.md`, `defense-notes.md`.

## Критерии оценки

| Критерий | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Связанный package | YAML/mappings отсутствуют | Документы без связей | Scope, sources, roles, workflow, gates и evidence index прослеживаются |
| Reproducible runs | Нет command/output | Есть N-01 без failures | N-01 и F-01/F-02/F-03 имеют result, owner, receiver, correction, re-run и resume |
| Safety authority | Approval/execution смешаны | STOP без separation | Untrusted input inert; recommendation, approval и execution разделены |
| Audit и remediation | Только prose/extension скрывает defect | Risks без owner/re-run | Risk report, residual risk, remediation, extensions и status связаны evidence |

## Наблюдаемое evidence

Reviewer parses `control-plane.yaml`, проверяет mappings, повторяет N-01 и один
F-run, где STOP произошел до action, а correction не расширяет scope.

## Критические дефекты

- Untrusted input стал command, permission расширен либо action выполнен до gate.
- Review/risk recommendation/green test названы human approval.
- Human owner/risk reviewer стал executor-ом, либо F-run не имеет owner/receiver/resume.

## Маршрут исправления

Исправьте затронутый contract/gate/evidence record, верните status к `requires
remediation`, выполните affected re-run и только потом обновите audit.

## Повторная команда

```bash
python3 scripts/validate_course.py curriculum
```
