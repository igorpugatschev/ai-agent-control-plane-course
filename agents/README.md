# Agents

Эта директория содержит исполнимые учебные контракты Module 3. Агент здесь не «отдельная нейросеть», а инженерный исполнитель с явной целью, входами, output, permissions, запретами, stop conditions, quality criteria и handoff target.

## Нормативная privileged chain

- Risk reviewer выполняет только risk analysis и возвращает recommendation или STOP.
- Named human owner только approve/reject intended irreversible action.
- Separately named authorized executor, отличный от named human owner и risk reviewer, выполняет ровно approved action.
- Executor возвращает execution evidence: identity, approved scope, operation id, exit/output и resulting state.
- `STOP`/reject завершает ветку до execution; approve не является execution evidence.

## Ролевые контракты

- [Coordinator](coordinator.md) - проверяет полноту пакета и маршрутизирует следующего владельца; не пишет код и не выдает approval.
- [Implementation](implementation.md) - вносит согласованное обратимое изменение и готовит evidence; не утверждает собственный результат.
- [Reviewer](reviewer.md) - независимо сопоставляет scope, diff и evidence; не редактирует работу автора.
- [QA/SDET](qa-sdet.md) - воспроизводимо запускает согласованную проверку и владеет test evidence, а не final acceptance.
- [Risk reviewer](risk-reviewer.md) - владеет risk analysis и approval-gate process,
  возвращает recommendation или `STOP`, но не final irreversible-action approval.

## Правила взаимодействия

1. Coordinator принимает только полный package: task ID, goal, scope, sources, owner, status, evidence, risk и requested next action.
2. Implementation передает diff и local evidence reviewer-у; зеленый тест не является self-approval.
3. Reviewer возвращает `approve`, `changes requested` или `STOP`; findings уходят implementation, а reviewer не исправляет author files.
4. QA/SDET передает command, environment assumptions, output и failure owner coordinator-у; test verdict не является product acceptance.
5. Запрос на delete, deploy, publish или `git push` останавливается и идет через coordinator к risk reviewer. Risk reviewer возвращает recommendation или `STOP` с conditions, а coordinator направляет recommendation named human owner.
6. Final acceptance принадлежит human owner после независимого review и нужных approvals.

Final irreversible-action approval дает только named human owner.

Формы contracts и packages находятся в [templates/agent-role.md](../templates/agent-role.md), [templates/skill-contract.md](../templates/skill-contract.md) и [templates/handoff.md](../templates/handoff.md). Module 3 объясняет правила на русском и не требует API-ключа: [маршрут модуля](../curriculum/module-03-roles-and-skills/README.md).

Следующее действие студента: после заполнения role, skill и handoff contracts
пройдите [checkpoint 3](../curriculum/module-03-roles-and-skills/checkpoint.md),
затем продолжайте [Module 4](../curriculum/module-04-development-workflow/README.md).
