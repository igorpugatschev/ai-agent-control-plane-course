# Module 03 checkpoint assessment guide

## Артефакты

- `artifacts/module-03/role-contracts.md`.
- `artifacts/module-03/skill-and-permission-matrix.md`.
- `artifacts/module-03/coordinator-handoff.md`.

## Критерии оценки

| Критерий | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Role contracts | Roles/prohibitions нет | Нет inputs/outputs/receiver | Duties, rights, STOP и handoff разделены |
| Skills и permissions | Tool/skill/permission смешаны | Definitions без scope | Role, procedure, tool, action, scope и evidence связаны |
| Независимость review | Author self-accepts/reviewer edits | Review без verdict | Findings/verdict независимы, correction идет implementation |
| Routing и authority | Coordinator/risk reviewer исполняет | STOP без receiver | One receiver; recommendation, approval и execution разделены |

## Наблюдаемое evidence

Walkthrough показывает, что implementation не публикует и не удаляет, reviewer
не меняет diff, а неполный package возвращается sender-у.

## Критические дефекты

- Implementation получает self-approval, push/delete или scope expansion.
- Reviewer правит author work; coordinator/risk reviewer дает final approval.
- STOP без blocked action, evidence, receiver или resume condition.

## Маршрут исправления

Уберите опасное permission, восстановите независимого receiver-а и bounded STOP
package; повторите walkthrough без запрещенного действия.

## Повторная команда

```bash
test -s artifacts/module-03/role-contracts.md
test -s artifacts/module-03/skill-and-permission-matrix.md
test -s artifacts/module-03/coordinator-handoff.md
grep -Eqi 'reviewer|permission|STOP|receiver' artifacts/module-03/role-contracts.md
grep -Eqi 'tool|skill|permission|scope|evidence' artifacts/module-03/skill-and-permission-matrix.md
grep -Eqi 'receiver|STOP|recommendation|approval|execution' artifacts/module-03/coordinator-handoff.md
python3 scripts/validate_course.py curriculum
```
