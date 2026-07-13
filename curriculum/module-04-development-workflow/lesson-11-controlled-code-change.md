# Урок 11. Малое контролируемое test-first изменение

## Результат урока

Вы создадите `artifacts/module-04/controlled-change-plan.md`: test-first последовательность для `priority`, минимальный разрешенный diff и route при ошибке. Артефакт не меняет учебный стенд сам по себе.

## Зачем это инженеру

Большой «умный» diff трудно связать с acceptance. Если сначала переписать сервис, а потом подобрать test, проверка доказывает уже измененное поведение, а не request. Малое изменение с заранее названными tests удерживает границу и делает correction локальным.

Test-first здесь означает порядок рассуждения: сначала наблюдение нового контракта, затем минимальная реализация, затем focused test. Он не дает implementation права менять API или документацию без impact и не превращает green run в self-approval.

## Теория

### От acceptance к тесту

Один criterion получает один test: default priority, допустимый priority и неверное значение. Существующие `test_create_task_assigns_integer_id`, `test_complete_task_records_done_status` и duplicate-title tests являются regression guards, потому что change brief запрещает менять их поведение.

### Минимальный diff

В `models.py` появляется ограниченный тип или enum и поле с default. В `service.py` только `create_task` принимает и валидирует priority. В `test_service.py` добавляются focused cases. Сортировка `list_tasks`, новые статусы, изменение `complete_task` и переписывание старых tests не нужны.

### Порядок и correction

Implementation добавляет tests, запускает их и записывает expected red evidence. Затем делает малый diff, запускает focused и полный test suite. Failure не лечится расширением scope: сохраните output, `git diff`, named failure owner и передайте package coordinator-у.

## Ключевые термины

- **Test-first** - сначала проверяемое ожидаемое поведение, потом минимальный код.
- **Focused test** - проверка одного request и его ближайших границ.
- **Regression guard** - существующий test, защищающий нецелевое поведение.
- **Minimal diff** - наименьший набор правок для criteria.
- **Red/green evidence** - результаты до и после реализации.
- **Failure owner** - владелец следующего действия по сбою.
- **Bounded revision** - исправление только named finding без нового поведения.

## Рабочий пример

```python
# projects/training-task-app/tests/test_service.py: proposed focused tests
def test_create_task_uses_normal_priority_by_default():
    assert TaskService().create_task("Проверить gate").priority.value == "normal"

def test_create_task_keeps_allowed_priority():
    assert TaskService().create_task("Срочно", priority="high").priority.value == "high"

def test_create_task_rejects_unknown_priority():
    with pytest.raises(ValueError, match="Недопустимый приоритет"):
        TaskService().create_task("Проверить gate", priority="urgent")
```

Разрешенный code impact: `projects/training-task-app/src/task_app/models.py`, `src/task_app/service.py`, `tests/test_service.py`. Documentation impact после green tests: `requirements.md`, `README.md`, `api/openapi.yaml`; они используют те же три значения и default. Нельзя менять `list_tasks`, `complete_task`, duplicate-title или endpoints.

### Подготовленный ответ агента без API-ключа

```text
Сначала добавляю три focused test и фиксирую red evidence. Затем добавляю
TaskPriority и default normal в models.py, принимаю и проверяю priority только
в service.py, запускаю focused и полный pytest. После green синхронизирую
requirements.md, README.md и api/openapi.yaml. Не меняю list_tasks,
complete_task, duplicate-title, endpoints, commit и push. Handoff - reviewer.
```

Ответ является off-line черновиком: фактический diff, commands и independent review остаются обязанностью студента.

## Практика

1. Создайте `artifacts/module-04/controlled-change-plan.md` с тремя named focused tests и тремя regression guards.
2. Назовите code/test paths `models.py`, `service.py`, `test_service.py`; docs/OpenAPI paths - `requirements.md`, `README.md`, `api/openapi.yaml`.
3. Запишите порядок: test -> red evidence -> minimal code -> focused green -> full green -> docs/OpenAPI sync -> `git diff` -> handoff reviewer.
4. Выполните изменение в отдельной учебной копии. Канонический стенд остается
   исходником для сравнения:

   ```bash
   set -euo pipefail
   repo_root=$PWD
   workdir=$(mktemp -d)
   cp -R projects/training-task-app "$workdir/training-task-app"
   cd "$workdir/training-task-app"
   git apply "$repo_root/curriculum/module-04-development-workflow/fixtures/priority-tests.patch"
   set +e
   PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest tests -q -p no:cacheprovider \
     > "$workdir/red.txt" 2>&1
   red_status=$?
   set -e
   test "$red_status" -ne 0
   git apply --unidiff-zero "$repo_root/curriculum/module-04-development-workflow/fixtures/priority-implementation.patch"
   PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest tests -q -p no:cacheprovider \
     | tee "$workdir/green.txt"
   diff_status=0
   git diff --no-index "$repo_root/projects/training-task-app" . \
     > "$workdir/priority.diff" || diff_status=$?
   test "$diff_status" -eq 1
   test -s "$workdir/red.txt"
   test -s "$workdir/green.txt"
   test -s "$workdir/priority.diff"
   ```

   В evidence перенесите фактический вывод pytest из `red.txt` и `green.txt`,
   exit status и `priority.diff`, не подставляя заранее заданное число passed.

5. Укажите correction: при падении regression guard implementation не меняет scope, сохраняет output и передает coordinator-у.

### Необязательный prompt для живого агента

```text
На основе approved change brief предложи только test-first plan для priority
high/normal/low с default normal. Разрешены models.py, service.py,
test_service.py, requirements.md, README.md и api/openapi.yaml. Покажи focused
tests, regression guards, red/green evidence и minimal diff. Не редактируй
файлы, не меняй list_tasks, complete_task, duplicate-title, endpoints, commit,
push и не выдавай approve.
```

## Проверка результата

```bash
test -f artifacts/module-04/controlled-change-plan.md
for term in "test-first" "models.py" "service.py" "test_service.py" "openapi.yaml" \
  "requirements.md" "README.md" "git diff" "фактический вывод pytest" "coordinator"; do
  grep -qi "$term" artifacts/module-04/controlled-change-plan.md || exit 1
done
test -s curriculum/module-04-development-workflow/fixtures/priority-tests.patch
test -s curriculum/module-04-development-workflow/fixtures/priority-implementation.patch
```

Наблюдаемые критерии: есть red/green, три новых tests, guards, шесть путей и correction route. Если новый test проходит до реализации или старый падает, зафиксируйте output и остановите plan до выяснения причины.

## Типичные ошибки

- **Test добавлен после реализации.** Восстановите expected behavior в focused test и red evidence.
- **Existing test изменен ради green.** Верните guard; меняйте его только по отдельному requirement.
- **OpenAPI обновлен иначе.** Синхронизируйте значения и default с acceptance.
- **Failure лечится refactor.** Передайте output coordinator-у и запросите bounded revision.

## Контрольные вопросы

1. Какой test доказывает default priority?
2. Почему `complete_task` - regression guard?
3. Когда документация и OpenAPI входят в change?
4. Что делать при падении старого test?
5. Почему implementation не approve свой green run?

## Официальные источники

- [pytest documentation](https://docs.pytest.org/) - официальный справочник тестов; локальная command и output даны в уроке.
- [Python documentation: enum](https://docs.python.org/3/library/enum.html) - справочник ограниченных значений; конкретный priority request определен здесь.
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) - официальный источник схемы API; локальный контракт проверяется по YAML.
