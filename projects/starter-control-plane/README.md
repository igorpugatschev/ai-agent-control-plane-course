# Starter control plane

Это пустая, но исполнимая заготовка для собственного capstone. Все файлы ниже
содержат только `<student: ...>` prompts: scope, источники, owners, роли, gates
и verdicts студент заполняет собственными фактами. Не используйте reference
project как ответ и не оставляйте placeholder на защите.

## Точное дерево

```text
projects/starter-control-plane/
├── control-plane.yaml
└── artifacts/capstone/
    ├── README.md
    ├── blueprint.md
    ├── source-map.md
    ├── roles.md
    ├── skill-contracts.md
    ├── handoffs.md
    ├── workflow.md
    ├── review-gate.md
    ├── stop-gate.md
    ├── decision-log.md
    ├── evidence-index.md
    ├── run-evidence.md
    ├── corrections.md
    ├── risk-report.md
    ├── final-report.md
    └── defense-notes.md
```

`control-plane.yaml` обязателен: он повторяет field prompts из Markdown в
machine-readable виде. Файл является JSON-compatible YAML, поэтому его можно
проверить Python standard library `json` без PyYAML.

## Обязательное отображение шаблонов

| Шаблон и deliverable | Назначение в пакете |
| --- | --- |
| `templates/control-plane-blueprint.md` -> `artifacts/capstone/blueprint.md` | goal, scope, roles, gates и evidence |
| `templates/context-map.md` -> `artifacts/capstone/source-map.md` | trust, freshness, Source owner и Authority owner |
| `templates/agent-role.md` -> `artifacts/capstone/roles.md` | contracts всех ролей и separation of duties |
| `templates/skill-contract.md` -> `artifacts/capstone/skill-contracts.md` | повторяемые local checks и их rights |
| `templates/handoff.md` -> `artifacts/capstone/handoffs.md` | one receiver и next action |
| `templates/workflow.md` -> `artifacts/capstone/workflow.md` | trigger, branches, recovery и routing |
| `templates/review-gate.md` -> `artifacts/capstone/review-gate.md` | independent review before transition |
| `templates/stop-gate.md` -> `artifacts/capstone/stop-gate.md` | STOP, safe step и resume condition |
| `templates/decision-log.md` -> `artifacts/capstone/decision-log.md` | decisions, evidence и revisit condition |
| `templates/final-report.md` -> `artifacts/capstone/final-report.md` | honest status, concerns и next owner |

`evidence-index.md`, `run-evidence.md`, `corrections.md`, `risk-report.md` и
`defense-notes.md` соединяют template deliverables в проверяемую защиту.

## Следующий локальный шаг

1. Откройте [README пакета capstone](artifacts/capstone/README.md) и замените
   prompts `Goal`, `Scope` и `Intended action` фактами своего проекта.
2. Перенесите эти решения в [blueprint](artifacts/capstone/blueprint.md), сверяясь
   с [шаблоном blueprint](../../templates/control-plane-blueprint.md).
3. Обновите [control-plane.yaml](control-plane.yaml) теми же фактами и выполните
   минимальную локальную проверку ниже.

## Порядок заполнения

1. Замените prompts в `control-plane.yaml` и artifacts только фактами своего домена.
2. Заполните десять mapped deliverables по одноименным шаблонам выше.
3. Назовите trusted sources, untrusted data, freshness command, Source owner и
   Authority owner. Не выводите Authority owner из автора источника.
4. Разделите implementation, reviewer, QA/SDET, coordinator, risk reviewer,
   named human owner и separately named authorized executor. Human owner only
   approves/rejects; executor only performs explicit approved action.
5. Проведите N-01, F-01 stale context, F-02 excess permission и F-03 weak
   evidence. Для failure сохраните STOP, owner, receiver, correction и re-run.

## Минимальная локальная проверка

```bash
cd projects/starter-control-plane
python3 -c "import json; print(json.load(open('control-plane.yaml', encoding='utf-8'))['schema_version'])"
git diff --check
```

Expected output первой команды:

```text
1
```

Успешный parse доказывает только формат starter. Он не заменяет заполненные
decisions, evidence и проверку capstone acceptance.
