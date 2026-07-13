# Урок 13. От требований к проверяемым условиям и трассировке

## Результат урока

Вы создадите `artifacts/module-05/traceability-matrix.md`: матрицу, которая связывает требование учебного стенда с проверяемым условием, локальным источником, test evidence, риском и владельцем следующего действия.

## Зачем это инженеру

Тест с удачным названием еще не доказывает, что продукт соответствует требованию. Green проверка создания задачи не доказывает, что пустое название отклоняется, а OpenAPI не заменяет наблюдение Python-сервиса. Без трассировки команда не знает, что проверить после изменения и почему release можно или нельзя продолжать.

Проверяемое условие превращает фразу из требования в наблюдение: заданное действие, конкретный результат и источник истины. Матрица оставляет путь от решения о выпуске назад к требованиям и вперед к тестам. Если условия нет теста, это не зеленый результат, а риск для triage или STOP.

## Теория

### От требования к condition

Условие формулируется как `given -> when -> then` и не добавляет новой продуктовой логики. Для `create_task` из локального `requirements.md`: given чистый `TaskService`, when создается задача, then `id == 1` и `status == open`. Другое условие: given название из пробелов, when вызывается `create_task`, then поднимается `ValueError` с документированным сообщением.

### Выбор по риску

Сначала выбирайте условия, где ошибка затронет контракт, данные, критический путь или уже менялась. Для стенда высокий риск у идентификатора, валидации title, duplicate rule, статуса `done` и неизвестного `task_id`: эти факты доступны клиенту и связаны с несколькими правилами. Низкий риск не означает «не тестировать»; он определяет глубину проверки и порядок запуска при ограниченном времени.

### Трассировка и доказательство

Строка traceability содержит source path, condition, test или planned check, фактическое observation, risk и owner. `requirements.md` задает продуктовое правило, `api/openapi.yaml` задает HTTP-представление, а `tests/test_service.py` показывает текущий test suite. Command/output без source не доказывает coverage, а source без observation не доказывает текущий запуск.

## Ключевые термины

- **Проверяемое условие** - наблюдаемое правило с входом и ожидаемым результатом.
- **Traceability (трассировка)** - связь требования, контракта, проверки, результата и риска.
- **Test evidence** - команда, окружение, выход и наблюдение, которые можно повторить.
- **Risk-based selection** - выбор и упорядочивание checks по последствиям сбоя и неопределенности.
- **Regression guard** - test, сохраняющий ранее подтвержденное поведение.
- **Coverage gap** - условие без достаточной проверки или evidence.
- **Failure owner** - роль следующего безопасного анализа или correction, а не виновник.

## Рабочий пример

```md
| Источник и условие | Проверка | Наблюдение и риск | Owner |
| --- | --- | --- | --- |
| `requirements.md`: пустой title отклоняется | `test_empty_title_is_rejected` | pytest: `11 passed`; высокий риск валидации input | QA/SDET при failure |
| `requirements.md`: done-title можно использовать снова | `test_title_can_be_reused_after_task_is_done` | pytest: `11 passed`; current checkout: `not reproduced` для documentary historical case без pinned defect artifact | implementation через coordinator |
| `api/openapi.yaml`: `POST /tasks` возвращает Task или Error | schema review: 201/400, `title`, `id`, `status`, `message` | API contract check, HTTP server отсутствует | QA/SDET |
| `requirements.md`: list идет по `id` | `test_list_tasks_returns_tasks_in_id_order` | pytest: `11 passed`; средний риск порядка | QA/SDET |
```

### Подготовленный ответ агента без API-ключа

```text
Coverage gap: `api/openapi.yaml` задает HTTP-коды 201/400/404, но стенд не
запускает HTTP-сервер. Не объявляю endpoint проверенным по Python unit tests.
Добавляю schema review в матрицу, сохраняю exact pytest output как service
evidence и передаю QA/SDET. Для фактического HTTP-check нужен отдельный server
scope; до него endpoint-level release claim запрещен.
```

Это prepared output, а не актуальный verdict: студент сверяет каждый путь и собственный output локально.

## Практика

1. Создайте `artifacts/module-05/traceability-matrix.md` и внесите источники `requirements.md`, `api/openapi.yaml` и `tests/test_service.py` с repo-relative путями.
2. Запишите минимум шесть conditions: первый ID/status, пустой title, duplicate active title, `done` title reuse, порядок `list_tasks`, unknown integer ID. Для каждого укажите given/when/then.
3. Сопоставьте каждое condition с named test или schema review. Не присваивайте Python test несуществующему HTTP-response.
4. Оцените риск как высокий, средний или низкий и назовите reason: контракт, валидация, статус, порядок или error path.
5. Добавьте column `Observed evidence`: пока вы не запускали suite, пишите `not run`, а не `passed`.
6. Запустите stable command, перепишите реальный count и добавьте SHA/дату проверки. В текущем неизмененном стенде ожидается `11 passed`.

### Необязательный prompt для живого агента

```text
Прочитай только projects/training-task-app/requirements.md,
projects/training-task-app/api/openapi.yaml и projects/training-task-app/tests/test_service.py. Не меняй
файлы и не запускай release. Верни Markdown-матрицу source -> given/when/then
-> named test или schema review -> риск -> coverage gap. Отдели Python service
checks от HTTP contract checks и верни STOP для неподтвержденного endpoint.
```

## Проверка результата

```bash
test -f artifacts/module-05/traceability-matrix.md
for term in "requirements.md" "openapi.yaml" "test_service.py" \
  "given" "when" "then" "Risk" "Observed evidence" "Coverage gap"; do
  grep -qi "$term" artifacts/module-05/traceability-matrix.md || exit 1
done
PYTHONPATH=projects/training-task-app/src python3 -m pytest projects/training-task-app/tests -q
# Текущее ожидаемое наблюдение неизмененного стенда: 11 passed.
```

Наблюдаемые критерии: у каждого release-relevant condition есть source, check, risk и observation; API schema review не выдан за живой HTTP-test; пробел имеет owner или STOP. Если команда показывает не `11 passed`, сохраните полный output, не переписывайте expected count и передайте package coordinator-у.

Локальный маршрут исправления: если строка не содержит source или expected result, вернитесь к `requirements.md` либо `api/openapi.yaml` и уточните только эту строку. Если test отсутствует, отметьте coverage gap и предложите scope для implementation; не меняйте стенд в уроке. Если source и test противоречат друг другу, зафиксируйте STOP и запросите решение Product owner через coordinator.

## Типичные ошибки

- **Тест назван требованием.** Исправление: добавьте путь requirements или OpenAPI и отдельное condition.
- **Green suite закрывает все API claims.** Исправление: отделите service evidence от schema review и HTTP gap.
- **Риск равен эмоции.** Исправление: назовите контракт, данные, critical path или неопределенность.
- **`11 passed` вписано без запуска.** Исправление: поставьте `not run`, затем выполните command.
- **Пробел скрыт.** Исправление: внесите coverage gap, owner и STOP/next action.

## Контрольные вопросы

1. Чем проверяемое condition отличается от названия test?
2. Почему OpenAPI schema review не доказывает работу HTTP endpoint?
3. Какие условия стенда первыми попадут в high-risk regression scope?
4. Что должна содержать строка traceability помимо test name?
5. Как действовать при расхождении source и текущего test?

## Официальные источники

- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) - официальный нормативный источник структуры HTTP-контракта; локальный YAML остается проверяемым источником курса.
- [pytest documentation](https://docs.pytest.org/) - официальный справочник запуска и наблюдения тестов; exact command и expected count заданы локально.
- [Python documentation: exceptions](https://docs.python.org/3/library/exceptions.html) - официальный справочник исключений; сообщения и правила учебного сервиса определены локальными requirements.
