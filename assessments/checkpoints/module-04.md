# Module 04 checkpoint assessment guide

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
test -f artifacts/module-04/change-brief.md
```
