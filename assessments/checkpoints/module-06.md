# Module 06 checkpoint assessment guide

## Артефакты

- `artifacts/module-06/threat-model.md`.
- `artifacts/module-06/approval-matrix.md`.
- `artifacts/module-06/evaluation-dataset.md`.
- `artifacts/module-06/trace-record.md`.
- `artifacts/module-06/decision-log.md`.

## Критерии оценки

| Критерий | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Threat boundary | Нет assets/actors/boundary | Injection без controls | Boundary, assets, actors, tools, least privilege, controls и owner связаны |
| Gates и authority | Review/recommendation = approval | STOP без intended action/resume | STOP, review, recommendation, human approval и execution различены |
| Evaluation и trace | Только prose | Case/trace не полны | Expected/forbidden outcome, hard metric, redaction, trace/decision linkage есть |
| Injection response | Payload исполнен/одобрен | Отказ без event | Data only, zero unsafe actions, event, STOP и trusted resume есть |

## Наблюдаемое evidence

Reviewer находит `SAFE-CHK-006`, `trace_id`, source/trust, digest/redaction и
подтверждает отсутствие tool call, scope или approval из malicious text.

## Критические дефекты

- Injection выполнен/одобрен или расширил credential, tool, permission либо scope.
- Trace/log содержит secret, PII или полный payload без protected store.
- Safety claim без event, gate, owner или resume condition.

## Маршрут исправления

Остановите unsafe branch, уберите execution, восстановите least privilege и
замените payload digest/safe summary; свяжите event, trace, decision и re-run.

## Повторная команда

```bash
test -s artifacts/module-06/threat-model.md
test -s artifacts/module-06/approval-matrix.md
test -s artifacts/module-06/evaluation-dataset.md
test -s artifacts/module-06/trace-record.md
test -s artifacts/module-06/decision-log.md
grep -Eqi 'untrusted|least privilege|owner|control' artifacts/module-06/threat-model.md
grep -Eqi 'STOP|recommendation|approval|execution' artifacts/module-06/approval-matrix.md
grep -Eqi 'SAFE-CHK-006|expected|forbidden|redaction' artifacts/module-06/evaluation-dataset.md
grep -Eqi 'trace_id|source|trust|redaction' artifacts/module-06/trace-record.md
grep -Eqi 'event|gate|owner|resume' artifacts/module-06/decision-log.md
python3 projects/reference-control-plane/scripts/check_reference_control_plane.py
```
