# Модуль 7. Capstone: сборка, испытание и защита control plane

Capstone соединяет артефакты модулей 1-6 в один проверяемый control plane.
Студент не создает еще один набор теоретических заметок: он собирает пакет,
проводит нормальный и отказные прогоны, затем защищает архитектуру и остаточные
риски.

1. [Сборка и валидация контрактов](lesson-19-assemble-control-plane.md) - полный пакет в `artifacts/capstone/`.
2. [Контрольный запуск и failure injection](lesson-20-failure-injection-improvement.md) - `run-evidence.md` и `corrections.md`.
3. [Аудит, защита и roadmap](lesson-21-audit-defense-roadmap.md) - `risk-report.md` и защита.
4. [Checkpoint 7](checkpoint.md) - репетиция финальной защиты по rubric.

## Обязательный локальный маршрут

Обязательный маршрут работает локально с prepared runs, Markdown, YAML, Git и
pytest; API-ключ, облако и внешний агент не нужны.

## Вход и результат

Используйте собственные проверенные артефакты из модулей 1-6 или начните с
точной структуры [`projects/starter-control-plane/`](../../projects/starter-control-plane/).
Не копируйте [`projects/reference-control-plane/`](../../projects/reference-control-plane/)
как ответ: это независимый пример сопровождения документации, а не решение
для `training-task-app` или вашего capstone.

Готовый capstone содержит цель и scope, source map, contracts ролей, workflow,
переиспользованные templates, gates, evidence четырех прогонов, corrections,
risk report и self-contained theory confirmation. Named human owner может
только approve/reject intended privileged action; отдельный authorized executor
выполняет только уже approved action. Ни coordinator, ни risk reviewer не
становятся human owner или executor по умолчанию.

## Порядок работы

Сначала проверьте freshness источников и полноту contracts. Затем проведите
один normal run и три controlled failures: stale context, excess permission и
weak evidence. Каждый отказ должен завершаться наблюдаемым `STOP`, owner,
receiver, safe next action и resume condition, а не декларацией «агент
остановился». После corrections повторите только затронутый gate и сохраните
до/после evidence для защиты.
