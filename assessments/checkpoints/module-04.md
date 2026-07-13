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
scope drift возвращает revision, а не commit. Red/green evidence получено в
отдельной копии стенда через `priority-tests.patch` и
`priority-implementation.patch`; канонический stand остается неизменным.

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
grep -Eqi 'фактический вывод pytest|pytest output' artifacts/module-04/change-review-gate.md
repo_root=$PWD
workdir=$(mktemp -d)
cp -R projects/training-task-app "$workdir/training-task-app"
cd "$workdir/training-task-app"
git apply "$repo_root/curriculum/module-04-development-workflow/fixtures/priority-tests.patch"
set +e
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest tests -q -p no:cacheprovider \
  > "$workdir/red.txt" 2>&1
red_status=$?
set -e
test "$red_status" -ne 0
git apply --unidiff-zero "$repo_root/curriculum/module-04-development-workflow/fixtures/priority-implementation.patch"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest tests -q -p no:cacheprovider \
  | tee "$workdir/green.txt"
diff_status=0
git diff --no-index "$repo_root/projects/training-task-app" . \
  > "$workdir/priority.diff" || diff_status=$?
test "$diff_status" -eq 1
test -s "$workdir/red.txt"
test -s "$workdir/green.txt"
test -s "$workdir/priority.diff"
grep -q 'TaskPriority' "$workdir/priority.diff"
```
