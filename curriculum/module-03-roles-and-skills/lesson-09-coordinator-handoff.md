# Урок 9. Coordinator, routing и handoff

## Результат урока

Вы создадите `artifacts/module-03/coordinator-handoff.md`: маршрут coordinator-а и structured handoff packages для normal review, test failure и запроса необратимого действия.

## Зачем это инженеру

Много ролей без маршрутизации создают очередь случайных сообщений. Implementation не знает, кому передавать падение теста; reviewer получает просьбу исправить код; опасный запрос прячется в обычном handoff. Coordinator нужен не для работы за всех, а чтобы выбрать следующий contract по состоянию, evidence и risk.

Хороший handoff сохраняет причинную цепочку: что запрошено, что сделано, какие источники и команды это подтверждают, что заблокировано и кто вправе продолжить. Без него новая роль повторяет исследование или принимает недоказанный вывод.

## Теория

### Routing по состоянию, а не по названию агента

Coordinator принимает только пакет с input schema: `task_id`, `goal`, `scope`, `sources`, `current_owner`, `status`, `evidence`, `risk`, `requested_next_action`. Он проверяет completeness и выбирает одну ветку:

```text
incomplete input -> STOP -> sender
approved implementation evidence -> reviewer
test failure -> implementation or QA/SDET, depending on failure owner
review finding -> implementation
request for irreversible action -> risk reviewer
risk recommendation -> named human owner for final irreversible-action approval
```

Coordinator не выдает product approval, не пишет изменения и не закрывает задачу на основании статуса `passed`. Он владеет корректной маршрутизацией и видимостью failure ownership.

### Handoff package и failure ownership

Используйте `templates/handoff.md` и добавьте: receiver, status, scope, changed/untouched files, evidence, known risks, failure owner, stop status, next action. Failure owner не означает виновника: это роль, ответственная за безопасный следующий анализ или correction. Тест падает из-за output implementation - owner correction implementation; окружение недоступно - owner triage QA/SDET; approval на удаление отсутствует - risk reviewer владеет analysis и gate process, а named human owner - final approval.

### STOP как результат

Structured STOP не равен «задача завершена» и не равен «ничего не сделано». Он содержит blocked action, observable condition, risk, preserved evidence, safe next action, receiver и resume condition. Coordinator передает STOP owner-у, который вправе снять блокировку. После risk recommendation coordinator все равно не запускает действие: он направляет recommendation named human owner, затем назначает разрешенного исполнителя и прикладывает final approval как evidence.

### Независимость review

После implementation coordinator маршрутизирует package reviewer-у, а не назад author-у с просьбой «самому проверить». Reviewer возвращает `approve`, `changes requested` или `STOP`; findings принадлежат implementation для correction. Если reviewer видит рискованное действие, он не редактирует результат и не выдает risk approval: он создает handoff risk reviewer-у через coordinator.

## Ключевые термины

- **Coordinator (координатор)** - роль, маршрутизирующая пакеты между contracts по status, evidence и risk.
- **Routing (маршрутизация)** - выбор следующего владельца и действия по проверяемому правилу.
- **Handoff package (пакет передачи)** - структура состояния, scope, evidence, рисков и следующего действия.
- **Failure ownership (владение обработкой сбоя)** - роль следующего безопасного correction или decision, а не виновник.
- **Resume condition (условие возобновления)** - наблюдаемый факт, после которого STOP может быть снят.
- **Independent review (независимое review)** - проверка ролью, не вносившей author change.
- **Irreversible action (необратимое действие)** - действие с высокой ценой отката, требующее отдельного approval.

## Рабочий пример

Implementation передает зеленый локальный тест и просит «заодно удалить stale-сценарий и сделать push». Coordinator видит, что request выходит за implementation contract. Он не направляет его reviewer-у: review не дает approval удаления или push. Он создает STOP handoff risk reviewer-у с diff, test output, файлами и вопросом: есть ли recommendation или STOP для named human owner перед final approval?

### Подготовленный ответ агента без API-ключа

```text
Handoff: TASK-03 / запрос необратимого действия
Получатель: risk reviewer.
Статус: STOP, реализация не считается завершенной.
Scope: TaskService и tests проверены; stale-сценарий не изменялся.
Evidence: git diff согласованных файлов; exact pytest command; exit code 0.
Риск: удаление лишит команды учебного конфликтного входа; push меняет общую ветку.
Failure owner: risk reviewer владеет risk analysis и approval-gate process.
Следующее действие: вернуть recommendation или STOP с conditions named human owner.
Условие возобновления: final approval named human owner и назначенный исполнитель.
```

Пакет не говорит «все готово». Даже после recommendation coordinator направляет ее named human owner; только его final approval позволяет передать действие разрешенному исполнителю.

## Практика

Создайте артефакт:

```bash
mkdir -p artifacts/module-03
printf '# Coordinator routing и handoff\n' > artifacts/module-03/coordinator-handoff.md
```

1. Скопируйте поля `templates/handoff.md` и добавьте `Task ID`, `Failure owner`, `Stop status`, `Resume condition`, `Requested next action`.
2. Опишите input schema coordinator-а: task ID, goal, scope, sources, current owner, status, evidence, risk и requested next action. Неполный пакет возвращайте sender-у с STOP.
3. Нарисуйте routing table для шести веток: implementation -> reviewer; finding -> implementation; test failure -> implementation/QA-SDET; irreversible request -> risk reviewer; risk recommendation -> named human owner; final approval -> assigned executor.
4. Создайте три заполненных packages: normal review, test failure и request удалить `scenarios/stale-documentation.md`/выполнить `git push`.
5. В risk package укажите, что risk reviewer владеет analysis и approval-gate process, возвращает recommendation или STOP, но не выполняет действие и не дает final approval; reviewer не редактирует author diff; implementation не принимает свой результат.
6. Для каждой ветки добавьте failure owner, evidence, один receiver и resume condition.

### Необязательный prompt для живого агента

```text
Не меняй файлы, не запускай команды и не выполняй необратимые действия.
Собери Markdown-черновик coordinator routing и трех handoff packages для
TaskService: normal review, test failure, request удалить stale-сценарий и
выполнить git push. Используй input schema task_id, goal, scope, sources,
current_owner, status, evidence, risk, requested_next_action. Верни failure
owner, stop status, receiver, next action и resume condition. Reviewer не
редактирует, implementation не self-approves, risk reviewer владеет analysis и
approval-gate process, а named human owner дает final approval.
```

Сопоставьте ответ с role contracts. Routing нельзя принять, если он отправляет review author-у, дает coordinator-у approval или объявляет STOP завершением.

## Проверка результата

```bash
test -f artifacts/module-03/coordinator-handoff.md
for term in "Task ID" "Получатель" "Текущий статус" Scope Evidence \
  "Failure owner" "Stop status" "Resume condition" "Следующее действие"; do
  grep -qi "$term" artifacts/module-03/coordinator-handoff.md || exit 1
done
for branch in reviewer implementation "QA/SDET" "risk reviewer" "human owner"; do
  grep -qi "$branch" artifacts/module-03/coordinator-handoff.md || exit 1
done
grep -qi "scenarios/stale-documentation.md" artifacts/module-03/coordinator-handoff.md
grep -qi "git push" artifacts/module-03/coordinator-handoff.md
```

Проведите walkthrough: пакет implementation с просьбой удалить stale-сценарий должен идти `STOP -> coordinator -> risk reviewer -> recommendation or STOP -> named human owner final approval -> assigned executor`; reviewer не выдает approval, implementation не завершает задачу.

Наблюдаемые критерии приемки:

- coordinator routing использует schema, status, evidence и risk;
- у каждого handoff один receiver и одно следующее действие;
- normal review, risk recommendation/STOP и final approval различены;
- failure owner назван для test failure и risk request;
- STOP содержит resume condition;
- final acceptance остается у human owner после independent review.

Локальный маршрут исправления: если walkthrough требует догадки, добавьте к ветке condition, receiver и resume condition. Если есть два receiver, разделите пакет на два handoff с разными goals. Если risk reviewer или coordinator выполняет действие вместо analysis/recommendation, удалите это право, направьте recommendation named human owner и final approval - назначенному исполнителю.

## Типичные ошибки

- **Coordinator становится super-agent.** Исправление: оставьте ему routing и полноту пакета, не implementation или approval.
- **Failure owner назван виновником.** Исправление: назовите владельца следующего безопасного шага.
- **Handoff содержит только «тесты прошли».** Исправление: добавьте scope, command, output, risk и receiver.
- **STOP передан всем сразу.** Исправление: назначьте единственного owner, способного снять condition.
- **Approval рискованного действия подменен review.** Исправление: создайте отдельный package risk reviewer-у.

Final irreversible-action approval дает только named human owner.

## Контрольные вопросы

1. По каким полям coordinator выбирает receiver?
2. Почему `passed` не является final acceptance?
3. Чем failure ownership отличается от поиска виновного?
4. Какой маршрут у запроса на удаление файла после зеленого теста?
5. Почему один handoff должен иметь одного receiver?
6. Что должно появиться до возобновления после STOP?

## Официальные источники

- [OpenAI Agents guide](https://developers.openai.com/api/docs/guides/agents) - официальный обзор orchestration и handoff patterns; урок задает vendor-neutral routing без SDK.
- [OpenAI Agents SDK for Python: handoffs](https://openai.github.io/openai-agents-python/handoffs/) - provider-specific пример передачи между agents, используемый только как дополнительная реализация.
- [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework) - официальный источник о governance и управлении рисками; схема handoff изложена в уроке.
