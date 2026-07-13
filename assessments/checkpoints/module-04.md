# Module 04 checkpoint assessment guide

[Все checkpoint guides](README.md)

## Артефакты

- `artifacts/module-04/change-brief.md`.
- `artifacts/module-04/controlled-change-plan.md`.
- `artifacts/module-04/change-review-gate.md`.

## Критерии оценки

| Критерий | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Intake и acceptance | Нет owner/criteria | Request без exclusions/impact | Owner, criteria, impact и boundaries подтверждены |
| Test-first plan | Tests нет/после кода | Tests без red/green route | Focused tests, guards, impact и red/green evidence связаны |
| Review evidence | Green test = acceptance | Diff/review не проверяемы | Author/reviewer разделены, diff/output/sync/verdict доступны |
| Scope и commit boundary | Drift/self-approval принят | Correction без границы | Changes requested с path/risk/receiver; commit после review |

## Наблюдаемое evidence

Reviewer находит changed/untouched paths, повторяет focused test и видит, почему
scope drift возвращает revision, а не commit.

## Критические дефекты

- Лишнее behavior принято без request, или requirements/README/OpenAPI рассинхронизированы.
- Нет exact test command/output, implementation self-approves или pushes.

## Маршрут исправления

Сузьте plan, синхронизируйте contract paths, зафиксируйте red/green evidence и
направьте finding implementation receiver-у; повторите review-gate.

## Повторная команда

```bash
set -euo pipefail
test -s artifacts/module-04/change-brief.md
test -s artifacts/module-04/controlled-change-plan.md
test -s artifacts/module-04/change-review-gate.md
grep -Eqi 'acceptance|owner|exclusions|impact' artifacts/module-04/change-brief.md
grep -Eqi 'focused|red|green|regression' artifacts/module-04/controlled-change-plan.md
grep -Eqi 'review|verdict|diff|receiver' artifacts/module-04/change-review-gate.md
PYTHONPATH=projects/training-task-app/src python3 -m pytest projects/training-task-app/tests -q
```
