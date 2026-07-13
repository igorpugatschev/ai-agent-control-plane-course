# Урок 14. API/UI automation, тестовые агенты и детерминированное evidence

## Результат урока

Вы создадите `artifacts/module-05/test-agent-workflow.md`: workflow QA/SDET для service tests, API-contract review, optional UI-check и передачи детерминированного evidence coordinator-у.

## Зачем это инженеру

Automation полезна, только когда следующий исполнитель понимает, что именно запускалось и что означает результат. Агент, который меняет тесты во время независимой проверки, или browser script без product UI, создает видимость качества. Для учебного стенда есть Python library и OpenAPI, но нет HTTP-сервера и web-интерфейса; поэтому обязательный путь обязан оставаться честным и воспроизводимым без Playwright.

QA/SDET workflow разделяет четыре уровня: требования, service behavior, HTTP contract и UI behavior. Их evidence различается. Стабильная команда подтверждает только текущий Python suite; schema review подтверждает описание API; UI check возможен лишь когда появятся URL, browser state и утвержденный UI scope.

## Теория

### API contract checks

Локальный `api/openapi.yaml` требует `POST /tasks` с `title`, ответы `201`/`400`, `GET /tasks` с массивом `Task` и `POST /tasks/{task_id}/complete` с `200`/`404`. Проверка контракта сверяет пути, методы, required fields, типы, enum `open`/`done`, error schema и documented status codes. Она не вызывает сеть: в стенде HTTP-сервер отсутствует. Service tests наблюдают близкие правила через `TaskService`, но не доказывают serialization, routing или actual HTTP status.

### UI как необязательное расширение

Playwright управляет браузером и проверяет user-visible behavior: загрузку страницы, ввод, действие, сообщение и доступный результат. Когда появится утвержденный UI, сценарий должен иметь base URL, test data, selector policy, ожидание observable state, cleanup и artifact при failure. Для текущего стенда эти входы отсутствуют, поэтому не запускайте выдуманный browser test. Core теория и workflow все равно нужны: UI check - отдельный слой evidence, не замена API/service tests.

### Детерминированное evidence и test agent

QA/SDET получает approved scope, локальные sources, exact command и changed paths. Output включает command, cwd, Python/environment assumptions, exit code, полный observed result, failed node/trace при failure, SHA/diff state, confidence, failure owner и receiver. Повторный запуск без изменения command/source создает данные для flaky classification, но сам по себе не доказывает root cause. QA/SDET не правит implementation, не принимает release и не выполняет deploy/push.

## Ключевые термины

- **API contract check** - сверка поведения или схемы с формальным API-контрактом.
- **Schema review** - проверка локального OpenAPI-документа без сетевого вызова.
- **UI check** - наблюдение пользовательского поведения через интерфейс.
- **Selector** - устойчивый способ найти элемент UI; предпочтителен semantic/role locator.
- **Deterministic evidence** - evidence с достаточными условиями для повторения результата.
- **Test agent** - ограниченная роль, запускающая согласованные checks и передающая evidence.
- **Confidence** - обоснованная степень доверия к наблюдению, не замена output.

## Рабочий пример

```md
# QA/SDET workflow: TaskService

Trigger: implementation handoff с approved service/API scope.
Preconditions: доступны requirements, OpenAPI, tests, exact command, changed paths.
Steps:
1. QA/SDET сверяет traceability и schema: `/tasks`, `title`, 201/400/404, Task/Error.
2. QA/SDET запускает stable pytest command из корня репозитория.
3. QA/SDET фиксирует cwd, Python 3.11+, exit code, output, SHA/diff и confidence.
Branches:
- service test failed -> coordinator -> implementation, приложить node/trace;
- schema и requirement расходятся -> STOP -> Product owner через coordinator;
- UI scope/URL отсутствуют -> UI check `not applicable`, не fail и не pass.
Output: QA/SDET handoff coordinator-у; green evidence не является release approval.
Recovery: повторить неизмененную command; при разном outcome сохранить runs и начать flaky triage.
```

### Подготовленный ответ агента без API-ключа

```text
QA/SDET report: command выполнена из repository root с PYTHONPATH, exit code 0,
observed result 11 passed. Confidence high для Python service suite. OpenAPI
проверен как schema review: пути и ответы прочитаны, но HTTP server не запущен.
UI status: not applicable, потому что нет URL и UI scope. Receiver: coordinator.
Release verdict не выдаю; для него нужны traceability и отдельный decision owner.
```

Это prepared output. Подставьте фактические SHA, время и output своей проверки; не переносите текст как evidence без запуска.

## Практика

1. Создайте `artifacts/module-05/test-agent-workflow.md` по `templates/workflow.md`.
2. Заполните trigger, preconditions, steps, branches, gates, output и recovery. Назовите QA/SDET, coordinator, implementation и Product owner.
3. Добавьте API schema checklist для `/tasks`, `/tasks/{task_id}/complete`, `CreateTaskRequest`, `Task`, `Error`, 201/400/404 и enum `open`/`done`.
4. Внесите service check с точной stable command и полями evidence: cwd, Python version, exit code, output, SHA/diff, confidence, failure owner.
5. Добавьте optional Playwright branch: только после появления утвержденных URL/UI scope. Укажите user action, accessible locator, expected visible state и trace/screenshot при failure; не делайте ее обязательной.
6. Зафиксируйте `UI check: not applicable` для текущего стенда и передайте report coordinator-у без release decision.

### Необязательный prompt для живого агента

```text
Работай как QA/SDET только read/search/run scope. Прочитай projects/training-task-app/requirements.md,
projects/training-task-app/api/openapi.yaml, projects/training-task-app/tests/test_service.py и agents/qa-sdet.md. Не меняй файлы,
не добавляй HTTP server/UI, не commit/push и не выдавай release approval. Верни
workflow с API schema review, stable pytest evidence fields, optional Playwright
branch, STOP при contract conflict и один receiver coordinator.
```

## Проверка результата

```bash
test -f artifacts/module-05/test-agent-workflow.md
for term in "Trigger" "Preconditions" "Steps" "Branches" "Gates" "Output" \
  "Recovery" "QA/SDET" "coordinator" "201" "400" "404" \
  "Playwright" "not applicable" "confidence"; do
  grep -qi "$term" artifacts/module-05/test-agent-workflow.md || exit 1
done
PYTHONPATH=projects/training-task-app/src python3 -m pytest projects/training-task-app/tests -q
# Текущее ожидаемое наблюдение неизмененного стенда: 11 passed.
```

Наблюдаемые критерии: workflow содержит все ветви и evidence fields; API schema review отделен от HTTP-run; UI branch optional и не требует URL, ключа или сети; результат pytest сопровождается реальным output. Если pytest падает, сохраните output и передайте coordinator-у; QA/SDET не исправляет тест или сервис.

Локальный маршрут исправления: при отсутствии поля workflow скопируйте его из `templates/workflow.md` и заполните только пропуск. Если OpenAPI/requirements конфликтуют, замените verdict на STOP, приложите оба пути и назначьте Product owner. Если UI branch требует несуществующий элемент, оставьте `not applicable` до отдельного approved UI assignment. При несовпадающих повторах передайте runs в flaky triage, не добавляйте retry как маскировку.

## Типичные ошибки

- **Unit test выдан за HTTP test.** Исправление: оставьте service evidence и отдельный schema review.
- **Playwright обязателен без UI.** Исправление: пометьте ветвь `not applicable` и назовите входы будущего scope.
- **В отчете нет cwd или output.** Исправление: добавьте deterministic evidence fields и повторите command.
- **QA/SDET исправляет падение.** Исправление: назовите failure owner и передайте coordinator-у.
- **Повторная попытка скрывает flaky.** Исправление: сохраните все runs и классифицируйте instability.

## Контрольные вопросы

1. Какие части OpenAPI можно проверить без HTTP-сервера?
2. Почему `11 passed` не доказывает 201/400/404 responses?
3. Когда UI check становится применимым?
4. Какие поля превращают test run в воспроизводимое evidence?
5. Кому QA/SDET передает failed run и почему не исправляет его сам?

## Официальные источники

- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) - нормативное описание paths, operations, responses и schemas.
- [pytest documentation](https://docs.pytest.org/) - официальный справочник test run и report output; локальный suite и count определены в репозитории.
- [Playwright for Python](https://playwright.dev/python/docs/intro) - официальный источник browser automation; в уроке он остается необязательным расширением без существующего UI.
