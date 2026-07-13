# Starter control plane

Это пустая, но исполнимая заготовка для собственного capstone. Она задает
точные каталоги, поля и команды, но не принимает решения за студента: scope,
источники, owners, roles, permissions, gates и verdicts остаются незаполненными.
Не используйте reference project как шаблон ответа: сначала сформулируйте свой
домен и bounded intended action.

## Структура, которую нужно создать в своем проекте

```text
artifacts/capstone/
├── README.md                 # goal, scope, intended action
├── source-map.md             # sources, trust, freshness, Source/Authority owner
├── roles.md                  # contracts всех ролей
├── workflow.md               # trigger, steps, branches, recovery
├── gates.md                  # review/stop/approval conditions
├── evidence-index.md         # paths, commands, outputs, decision IDs
├── run-evidence.md           # N-01, F-01, F-02, F-03
├── corrections.md            # failed gate -> correction -> re-run
├── risk-report.md            # residual risks and owners
├── final-report.md           # status, evidence, concerns, next owner
└── defense-notes.md          # rubric scores and theory confirmation
control-plane.yaml            # machine-readable field prompts
```

## Порядок заполнения

1. Скопируйте `templates/context-map.md`, `agent-role.md`, `workflow.md`,
   `review-gate.md`, `stop-gate.md`, `decision-log.md` и `final-report.md` в
   назначенные artifacts.
2. Заполните `control-plane.yaml` и Markdown только фактами своего домена.
3. Назовите trusted sources, untrusted data, freshness command, Source owner и
   Authority owner. Не выводите Authority owner из автора источника.
4. Разделите implementation, reviewer, QA/SDET, coordinator, risk reviewer,
   named human owner и separately named authorized executor. Human owner only
   approves/rejects; executor only performs explicit approved action.
5. Проведите N-01, F-01 stale context, F-02 excess permission и F-03 weak
   evidence. Для failure сохраните STOP, owner, receiver, correction и re-run.

## Минимальная локальная проверка

```bash
python3 -c "from pathlib import Path; print(Path('control-plane.yaml').is_file())"
git diff --check
```

YAML синтаксически валиден, когда его можно разобрать YAML parser-ом; Markdown
содержит обязательное объяснение и evidence. Поля-подсказки в starter не
являются готовыми decisions и должны быть заменены перед защитой.
