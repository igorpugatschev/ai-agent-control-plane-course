# Урок 10. Прием инженерной задачи, acceptance и impact

## Результат урока

Вы превратите входящий request в ограниченный change brief. Результат - `artifacts/module-04/change-brief.md`, где запрос на поле `priority` связан с acceptance criteria, impact, exclusions и владельцем решения.

## Зачем это инженеру

«Добавить приоритет» не говорит, какие значения допустимы, что произойдет с уже созданными задачами и надо ли менять API. Без явной границы implementer может одновременно добавить сортировку, новые статусы или изменить запрет дублей. Green test такого расширения не делает приемлемым.

Intake превращает просьбу в контракт следующей работы. Он сохраняет источник, решение, затронутые пути и то, что намеренно не меняется. Поэтому reviewer проверяет не только качество кода, но и верность цели.

## Теория

### Intake до реализации

Сначала зафиксируйте request: новая задача имеет `priority` со значениями `high`, `normal`, `low`; если значение не передано, используется `normal`. Product owner утверждает это дополнение. В `requirements.md` поля пока нет, поэтому его нельзя вывести из текущей реализации.

### Acceptance и границы

Acceptance должен наблюдаться: допустимые значения сохраняются в `Task`; default равен `normal`; неизвестное значение отвергается; title, id, status и `complete_task` не меняются. Exclusions: сортировка, фильтры, новые endpoint, миграция, изменение duplicate-title, commit approval и `git push`.

### Анализ влияния

Пройдите путь данных. `src/task_app/models.py` определяет `Task`; `src/task_app/service.py` создает его; `tests/test_service.py` наблюдает поведение; `api/openapi.yaml` описывает API; `requirements.md` и `README.md` объясняют контракт. Каждый путь имеет причину, иначе исключается. При неполном request `templates/workflow.md` требует STOP, а не догадки модели.

## Ключевые термины

- **Intake** - проверка полноты request до реализации.
- **Acceptance criteria** - наблюдаемые условия приемки.
- **Impact analysis** - связь request с конкретными файлами и причиной.
- **Scope** - разрешенные файлы и поведение изменения.
- **Exclusion** - явно неразрешенная часть работы.
- **Decision owner** - Product owner, утверждающий продуктовые правила.
- **Scope drift** - изменение поведения вне принятых criteria.

## Рабочий пример

```md
# Change brief: поле priority

## Acceptance criteria
- `TaskService.create_task("Проверить gate")` получает `priority == "normal"`.
- Значение `high` сохраняется; неизвестное значение отвергается.
- title, id, status и `complete_task` не меняются.

## Affected paths
- `projects/training-task-app/src/task_app/models.py`: модель и значения.
- `projects/training-task-app/src/task_app/service.py`: input и validation.
- `projects/training-task-app/tests/test_service.py`: focused tests.
- `projects/training-task-app/api/openapi.yaml`: request и Task schema.
- `projects/training-task-app/requirements.md`, `projects/training-task-app/README.md`: контракт.

## Exclusions
- Нет сортировки, фильтра, endpoint, смены duplicate-title, migration, push.
```

### Подготовленный ответ агента без API-ключа

```text
Статус: NEEDS DECISION. В requirements.md нет priority, поэтому нельзя угадать
значения или default. Нужен Product owner. После решения план ограничен
models.py, service.py, test_service.py, openapi.yaml, requirements.md и README.md.
Сортировка list_tasks и duplicate-title не входят в request. До acceptance - STOP.
```

Это off-line черновик: студент сверяет пути по локальным файлам и не выдает текст за approval.

## Практика

1. Создайте `artifacts/module-04/change-brief.md` по `templates/workflow.md`.
2. Заполните trigger, preconditions, steps, branches, gates, output и recovery; назовите Product owner.
3. Перенесите acceptance рабочего примера и добавьте минимум пять exclusions.
4. Добавьте impact-таблицу для `models.py`, `service.py`, `test_service.py`, `openapi.yaml`, `requirements.md`, `README.md` с причиной и действием `read`, `modify` или `verify`.
5. Зафиксируйте: стенд не меняется до отдельного assignment implementation; сейчас создается только плановый артефакт.

### Необязательный prompt для живого агента

```text
Прочитай только requirements.md, src/task_app/models.py, src/task_app/service.py,
tests/test_service.py, api/openapi.yaml и README.md в projects/training-task-app.
Подготовь change brief для priority high/normal/low с default normal. Не меняй
файлы и не добавляй сортировку, фильтры, endpoints, duplicate-title, commit или
push. Верни acceptance, exclusions, repo-relative impact, вопросы и STOP.
```

## Проверка результата

```bash
test -f artifacts/module-04/change-brief.md
for term in "Acceptance" "Affected" "Exclusion" "Product owner" "STOP"; do
  grep -qi "$term" artifacts/module-04/change-brief.md || exit 1
done
for path in models.py service.py tests/test_service.py api/openapi.yaml requirements.md README.md; do
  grep -q "$path" artifacts/module-04/change-brief.md || exit 1
done
```

Наблюдаемые критерии: есть default `normal`, три значения, конкретные пути, exclusions и condition для реализации. При спорном acceptance запишите STOP, вопрос и receiver вместо нового требования.

## Типичные ошибки

- **Impact без причины.** Добавьте связь пути с полем или наблюдением.
- **Тест назван approval.** Тест дает evidence; правила утверждает Product owner.
- **Сортировка добавлена «заодно».** Перенесите ее в exclusion и запросите отдельный request.
- **Current code назван требованием.** Отделите live state от нового решения.

## Контрольные вопросы

1. Почему `priority` нельзя вывести из текущей модели?
2. Какие criteria защищают старое поведение?
3. Зачем называть документацию и OpenAPI в impact?
4. Когда coordinator возвращает package sender-у?
5. Почему commit не часть реализации по умолчанию?

## Официальные источники

- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) - нормативный источник API-контракта; локальный YAML остается объектом проверки.
- [Python documentation: dataclasses](https://docs.python.org/3/library/dataclasses.html) - официальный справочник модели данных; правило priority задано в уроке.
- [OpenAI Agents guide](https://developers.openai.com/api/docs/guides/agents) - контекст управляемых workflow; intake и STOP объяснены внутри курса.
