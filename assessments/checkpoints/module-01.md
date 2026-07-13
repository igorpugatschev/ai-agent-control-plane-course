# Module 01 checkpoint assessment guide

## Артефакты

- `artifacts/module-01/control-plane-blueprint.md`.

## Критерии оценки

| Критерий | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Граница задачи | Цель/scope не проверяемы | Есть цель без exclusions/owner | Цель, included/excluded scope, assumptions и owner ограничивают работу |
| Управляющая логика | LLM, agent и control plane смешаны | Части названы без связей | Roles, tools, workflow, gates и approvals связаны с целью |
| Evidence и переходы | Claim без основания | Есть path без owner/проверки | Artifact/command, verdict, owner и next action наблюдаемы |
| STOP и восстановление | Неясный request разрешает реализацию | STOP без выхода | Blocked action, question, receiver и resume condition определены |

## Наблюдаемое evidence

Reviewer проводит одну цепочку intake -> gate -> implementation и видит факт,
assumption, owner и безопасный переход. Дословная терминология не требуется.

## Критические дефекты

- LLM, test output или agent output назван product approval.
- Необратимое действие разрешено без scope и owner.
- Нет evidence, owner или resume condition для STOP.

## Маршрут исправления

Исправьте только blueprint: разделите facts/assumptions, добавьте exclusions,
owner, gate и safe next action; повторите self-check и walkthrough.

## Повторная команда

```bash
test -s artifacts/module-01/control-plane-blueprint.md
grep -Eqi 'Scope|Owner|Evidence|STOP' artifacts/module-01/control-plane-blueprint.md
python3 scripts/validate_course.py curriculum
```
