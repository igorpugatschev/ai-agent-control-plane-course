# Module 05 checkpoint assessment guide

## Артефакты

- `artifacts/module-05/traceability-matrix.md`.
- `artifacts/module-05/test-agent-workflow.md`.
- `artifacts/module-05/triage-and-release-gate.md`.

## Критерии оценки

| Критерий | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Traceability | Claim не связан с source/check | Tests без risk/observation | Condition, source, check, output, risk и gap прослеживаются |
| API/UI workflow | Layers смешаны | Command без environment/output | Schema, service и applicable UI branches имеют routing |
| Triage reasoning | Fixture/flaky выдан за root cause | Label без facts/owner | Classification, runs, unknown cause, pinned gap, scope и owner доказуемы |
| Release gate | Green text = release | Checklist без STOP/recovery | Matrix, output, disposition, risk/rollback и owner блокируют release |

## Наблюдаемое evidence

Reviewer проходит одну matrix row до command/output и видит отдельные маршруты
для `not reproduced` и flaky без выдуманной причины.

## Критические дефекты

- Release/go выдан без source-to-check matrix и observed evidence.
- Historical fixture выдан за current defect, или flaky скрыт green retries.
- QA/SDET self-approves release либо test layer выдан за другой layer.

## Маршрут исправления

Добавьте missing source/check/output, верните verdict к STOP, сохраните runs и
честно обозначьте unknown; передайте решение coordinator-у.

## Повторная команда

```bash
test -f artifacts/module-05/traceability-matrix.md
```
