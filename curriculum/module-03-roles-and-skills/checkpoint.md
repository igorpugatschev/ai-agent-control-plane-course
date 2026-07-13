# Checkpoint 3. Роли, permissions и безопасный handoff

## Что проверяется

Checkpoint проверяет, что вы умеете остановить роль при запросе вне ее полномочий и передать работу следующему владельцу. Успехом считается structured STOP и воспроизводимый handoff, а не удаление файла, push или фраза «задача выполнена».

Используйте накопленные артефакты:

```text
artifacts/module-01/control-plane-blueprint.md
artifacts/module-02/context-map-evidence-gate.md
artifacts/module-03/role-contracts.md
artifacts/module-03/skill-and-permission-matrix.md
artifacts/module-03/coordinator-handoff.md
```

## Входные данные

Работайте только с repo-relative входами:

```text
projects/training-task-app/requirements.md
projects/training-task-app/api/openapi.yaml
projects/training-task-app/tests/test_service.py
projects/training-task-app/scenarios/stale-documentation.md
templates/agent-role.md
templates/skill-contract.md
templates/handoff.md
```

Запрос implementation:

> После локальной проверки TaskService удали `projects/training-task-app/scenarios/stale-documentation.md`, выполни `git push` и сообщи, что задача принята.

Отдельного approval для удаления, push и final acceptance нет. Наличие Git, editor или успешного теста не меняет этот факт.

## Задание

Обновите только три артефакта Module 3.

1. В `role-contracts.md` задайте пять roles с полями: цель, принятые входы, обязательный выход, разрешенные tools, запрещенные действия, stop conditions, критерии качества, получатель handoff.
2. В `skill-and-permission-matrix.md` отделите tool, skill и permission; внесите input/output schemas и minimum permissions для пяти roles.
3. В `coordinator-handoff.md` опишите routing и заполните package для входящего request.
4. Implementation возвращает `STOP`: не удаляет stale-сценарий, не выполняет `git push`, не объявляет final acceptance и не меняет scope.
5. Coordinator проверяет completeness package и передает вопрос только risk reviewer-у. Reviewer не редактирует author files и не принимает risk approval.
6. Risk reviewer возвращает documented `recommendation` или `STOP` с named human owner и conditions. Он владеет risk analysis и approval-gate process, но не дает final irreversible-action approval и не выполняет действие автоматически.
7. Даже если local pytest зеленый, направьте результат independent reviewer-у; final acceptance остается human owner.

Final irreversible-action approval дает только named human owner.

Не удаляйте файл, не выполняйте push, не меняйте учебный стенд и не выдавайте ответ модели за approval.

## Обязательный режим без API-ключа

Используйте подготовленные ответы уроков 7-9 как образец формы, но создайте собственный package. В нем должны быть repo-relative пути, scope, blocked action, risk, evidence, failure owner, receiver, next action и resume condition. Внешний provider или API-ключ не нужен.

## Необязательный режим с живым агентом

```text
Проверь три артефакта Module 3 и верни только findings. Не меняй файлы,
не запускай команды, не удаляй stale-документацию, не выполняй git push и
не утверждай результат. Проверь восемь полей пяти role contracts, различение
tool/skill/permission, input/output schemas и routing. Критический сценарий:
implementation получает просьбу удалить projects/training-task-app/scenarios/
stale-documentation.md, сделать git push и заявить final acceptance без approval.
Passing behavior: structured STOP и handoff coordinator -> risk reviewer;
reviewer не редактирует, implementation не self-approves, risk reviewer готовит
recommendation или STOP для named human owner.
Верни путь, наблюдение, риск и correction rule для каждого finding.
```

Сверьте findings по rubric; live answer не снимает STOP и не является approval.

## Самопроверка

```bash
for file in role-contracts.md skill-and-permission-matrix.md coordinator-handoff.md; do
  test -f "artifacts/module-03/$file" || exit 1
done
for field in "Цель" "Принятые входы" "Обязательный выход" "Разрешенные tools" \
  "Запрещенные действия" "Stop conditions" "Критерии качества" "Получатель handoff"; do
  grep -qi "$field" artifacts/module-03/role-contracts.md || exit 1
done
for role in coordinator implementation reviewer "QA/SDET" "risk reviewer"; do
  grep -qi "$role" artifacts/module-03/role-contracts.md || exit 1
done
for term in "Input schema" "Output schema" Permission STOP receiver; do
  grep -qi "$term" artifacts/module-03/skill-and-permission-matrix.md || exit 1
done
grep -qi "scenarios/stale-documentation.md" artifacts/module-03/coordinator-handoff.md
grep -qi "git push" artifacts/module-03/coordinator-handoff.md
grep -qiE 'не удал|запрещ.*удален|STOP' artifacts/module-03/coordinator-handoff.md
grep -qiE 'reviewer.*не.*редакт|не.*редакт.*reviewer' artifacts/module-03/role-contracts.md
grep -qiE 'implementation.*не.*утверж|не.*утверж.*implementation' artifacts/module-03/role-contracts.md
grep -qiE 'risk reviewer.*approval|approval.*risk reviewer' artifacts/module-03/role-contracts.md
PYTHONPATH=projects/training-task-app/src python3 -m pytest projects/training-task-app/tests -q
# Ожидаемое наблюдение: 11 passed; это evidence QA, а не approval.
```

Проведите walkthrough запроса. Он пройден, если implementation не совершает запрещенное действие, coordinator не закрывает задачу, reviewer не правит diff, risk reviewer получает единственный package для risk analysis, а final irreversible-action approval не появляется до named human owner.

## Оценивание

Каждый критерий оценивается от 0 до 2.

| Критерий | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Contracts ролей | Поля или роль отсутствуют | Права и запреты смешаны | У пяти roles восемь полей и receiver |
| Tool, skill, permission | Понятия смешаны | Есть definitions без scope | Матрица связывает role, procedure, tool, action, scope и evidence |
| STOP implementation | Request выполнен/задача закрыта | STOP без risk/receiver | Заблокированы удаление, push и self-approval; есть evidence и handoff |
| Routing и review | Coordinator/reviewer нарушает границу | Нет failure owner | Package идет coordinator -> risk reviewer, review независим |
| Approval и приемка | Approval выдал implementation/reviewer | Нет human owner/conditions | Risk reviewer дает recommendation/STOP, final irreversible-action approval у named human owner |

Для зачета нужно не менее 8 из 10 и отсутствие критических дефектов.

## Критические дефекты

Checkpoint не пройден независимо от баллов, если есть хотя бы один дефект:

- **Unauthorized implementation:** implementation удаляет файл, делает push, расширяет scope или объявляет self-approval.
- **Reviewer edits author work:** reviewer получил write action на author diff вместо findings/handoff.
- **Missing risk owner:** нет отдельного risk reviewer, владеющего risk analysis и approval-gate process.
- **Unsafe routing:** coordinator сам выдает approval, выполняет действие или направляет risk request не тому receiver.
- **Unstructured STOP:** нет blocked action, evidence, risk, receiver либо resume condition.
- **Missing schema:** skill выполняется без входов или не возвращает evidence/receiver.
- **External-reading dependency:** обязательное объяснение вынесено во внешний источник.

## Локальный маршрут исправления

- unauthorized implementation -> удалите permission из implementation contract и матрицы, добавьте STOP package coordinator-у, повторите walkthrough;
- reviewer edits author work -> замените write action на findings с путем и risk, передайте correction implementation;
- missing risk owner -> добавьте risk reviewer contract, `recommendation`/`STOP` и handoff target named human owner;
- unsafe routing -> восстановите routing table по input schema и направьте package единственному receiver;
- unstructured STOP -> дополните blocked action, evidence, risk, safe next action, receiver и resume condition;
- missing schema -> добавьте отсутствующее поле и верните неполный package sender-у;
- failed pytest -> сохраните output как evidence, назовите failure owner и повторите command после correction.

После коррекции снова выполните self-check. Удалять учебный сценарий или делать push ради зачета запрещено.

## Результат checkpoint

Передайте следующему модулю три артефакта и один structured STOP package. В handoff укажите, что test output - evidence, но не approval; кто владеет review, кто владеет decision о необратимом действии, что заблокировано и какое observable condition позволит возобновить workflow.
