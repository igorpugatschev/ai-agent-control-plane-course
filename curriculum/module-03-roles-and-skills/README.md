# Модуль 3. Роли, skills, permissions и handoff

Модуль превращает роли из названий в проверяемые контракты. Сквозная задача продолжает работу с учебным `TaskService`: implementer получил запрос одновременно изменить код, удалить старый сценарий и отправить ветку. Эти действия имеют разный риск и не принадлежат одной роли.

К концу модуля вы создадите три связанных артефакта:

1. [Контракт роли агента](lesson-07-agent-role-contract.md) - `artifacts/module-03/role-contracts.md`.
2. [Tools, skills и permissions](lesson-08-tools-skills-permissions.md) - `artifacts/module-03/skill-and-permission-matrix.md`.
3. [Маршрутизация coordinator и handoff](lesson-09-coordinator-handoff.md) - `artifacts/module-03/coordinator-handoff.md`.
4. [Checkpoint 3](checkpoint.md) - проверка STOP и передачи при запросе вне permission implementer-а.

## Обязательный локальный маршрут

Используйте накопленные `artifacts/module-01/control-plane-blueprint.md` и артефакты Module 2, а затем заполняйте локальные Markdown-файлы по шаблонам `templates/agent-role.md`, `templates/skill-contract.md` и `templates/handoff.md`. Обязательный путь не требует API-ключа: уроки содержат подготовленные ответы и локальные проверки. Live prompt разрешен только как черновик; он не создает permission, approval или evidence.

Контракт роли отвечает на вопрос «кто отвечает за результат», skill - «как повторяемо выполнить работу», а tool - «какое отдельное действие технически возможно». Доступность инструмента не является разрешением. Coordinator маршрутизирует работу по contract и evidence, reviewer не редактирует работу автора, implementation не принимает собственный результат, а risk reviewer выполняет risk analysis и ведет approval-gate process.

Final irreversible-action approval дает только named human owner.

## Готовность модуля

Модуль завершен, если:

- у каждой из пяти ролей есть цель, принятые входы, обязательный выход, разрешенные tools, запреты, stop-условия, критерии качества и получатель handoff;
- матрица отделяет tool от skill и permission, выдавая минимально необходимые права;
- handoff содержит scope, статус, evidence, риск, следующего владельца и одно следующее действие;
- coordinator не назначает роль по удобству и не обходит независимый review;
- запрос вне permission приводит к структурированному STOP и handoff, а не к выполнению или ложному завершению.
