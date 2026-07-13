# Agents

Эта директория содержит исполнимые учебные контракты Module 3. Агент здесь не «отдельная нейросеть», а инженерный исполнитель с явной целью, входами, output, permissions, запретами, stop conditions, quality criteria и handoff target.

## Ролевые контракты

- [Coordinator](coordinator.md) - проверяет полноту пакета и маршрутизирует следующего владельца; не пишет код и не выдает approval.
- [Implementation](implementation.md) - вносит согласованное обратимое изменение и готовит evidence; не утверждает собственный результат.
- [Reviewer](reviewer.md) - независимо сопоставляет scope, diff и evidence; не редактирует работу автора.
- [QA/SDET](qa-sdet.md) - воспроизводимо запускает согласованную проверку и владеет test evidence, а не final acceptance.
- [Risk reviewer](risk-reviewer.md) - единственный владелец decision об approval необратимого действия; по умолчанию не выполняет это действие сам.

## Правила взаимодействия

1. Coordinator принимает только полный package: task ID, goal, scope, sources, owner, status, evidence, risk и requested next action.
2. Implementation передает diff и local evidence reviewer-у; зеленый тест не является self-approval.
3. Reviewer возвращает `approve`, `changes requested` или `STOP`; findings уходят implementation, а reviewer не исправляет author files.
4. QA/SDET передает command, environment assumptions, output и failure owner coordinator-у; test verdict не является product acceptance.
5. Запрос на delete, deploy, publish или `git push` останавливается и идет через coordinator к risk reviewer. Risk reviewer возвращает decision с conditions, а coordinator назначает отдельного разрешенного исполнителя.
6. Final acceptance принадлежит human owner после независимого review и нужных approvals.

Формы contracts и packages находятся в [templates/agent-role.md](../templates/agent-role.md), [templates/skill-contract.md](../templates/skill-contract.md) и [templates/handoff.md](../templates/handoff.md). Module 3 объясняет правила на русском и не требует API-ключа: [маршрут модуля](../curriculum/module-03-roles-and-skills/README.md).
