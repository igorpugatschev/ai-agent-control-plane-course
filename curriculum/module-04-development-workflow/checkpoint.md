# Checkpoint 4. Контролируемое priority change и защита от scope drift

## Что проверяется

Checkpoint проверяет workflow intake -> acceptance -> impact -> test-first plan -> implementation evidence -> independent review -> bounded correction -> commit handoff. Успех - отказ от лишнего изменения с наблюдаемым routing, а не самый большой green diff.

Используйте накопленные артефакты:

```text
artifacts/module-02/context-packet.md
artifacts/module-02/context-map-evidence-gate.md
artifacts/module-03/coordinator-handoff.md
artifacts/module-04/change-brief.md
artifacts/module-04/controlled-change-plan.md
artifacts/module-04/change-review-gate.md
```

## Входные данные

Работайте только с repo-relative источниками и шаблонами:

```text
projects/training-task-app/requirements.md
projects/training-task-app/src/task_app/models.py
projects/training-task-app/src/task_app/service.py
projects/training-task-app/tests/test_service.py
projects/training-task-app/api/openapi.yaml
projects/training-task-app/README.md
templates/workflow.md
templates/review-gate.md
agents/implementation.md
agents/reviewer.md
agents/coordinator.md
```

Approved change: `priority` со значениями `high`, `normal`, `low` и default `normal`; синхронизация code, focused tests, requirements, README и OpenAPI. Exclusions: сортировка, фильтры, новые endpoints, изменение `list_tasks`, `complete_task`, duplicate-title, push и final acceptance.

## Задание

Создайте только три артефакта Module 4. Канонический учебный стенд не меняйте:
red/green выполните в отдельной копии по поставляемым patches.

1. В `change-brief.md` зафиксируйте Product owner, acceptance, impact, exclusions, workflow и STOP при неполном решении.
2. В `controlled-change-plan.md` запишите три priority tests, regression guards, red/green порядок, шесть affected paths и route при failure.
3. В `change-review-gate.md` отделите implementation evidence от reviewer checks, укажите diff, command, docs/OpenAPI sync, verdict и receiver.
4. Разберите prepared response ниже. Coordinator не передает его на approval: reviewer находит scope drift, возвращает `changes requested`, coordinator передает bounded correction implementation.
5. После correction reviewer повторяет проверку. Только approve позволяет coordinator подготовить commit handoff; implementation не commit, не push и не принимает результат.

### Подготовленный implementation response с scope drift

```text
Изменены models.py, service.py и test_service.py: добавлен priority и tests.
Тесты названы green без точной команды и фактического output. Заодно list_tasks сортирует задачи по priority high -> normal
-> low. Также duplicate-title запрещает повторяющееся название даже для done.
OpenAPI, requirements.md и README.md не обновлял. Считаю задачу принятой и
готов сделать commit и git push.
```

Правильная реакция control plane:

```text
Verdict: changes requested.
Evidence: response меняет list_tasks и duplicate-title вне approved scope;
отсутствуют api/openapi.yaml, requirements.md и README.md; claim о green без
команды и output не является evidence и в любом случае не дает approval.
Correction receiver: implementation через coordinator.
Bounded revision: убрать только сортировку и изменение duplicate-title;
синхронизировать priority high/normal/low/default normal только в OpenAPI,
requirements.md и README.md; приложить новый diff и output. Commit, push и
final acceptance запрещены.
```

## Обязательный режим без API-ключа

Prepared response заменяет модель. Выполните review по локальным файлам, templates и contracts. Не переносите формулировку без path-based evidence. Все checks и correction route находятся в checkpoint; сеть и API-ключ не нужны.

## Необязательный режим с живым агентом

```text
Проверь Module 4 artifacts и prepared implementation response. Не меняй файлы,
не commit/push и не давай approval. Scope: priority high/normal/low, default
normal; allowed paths models.py, service.py, test_service.py, requirements.md,
README.md, api/openapi.yaml. Найди scope drift list_tasks/duplicate-title,
missing documentation/OpenAPI и смешение test evidence с approval. Верни только
verdict, path, observation, risk, correction receiver, bounded revision и STOP.
```

## Самопроверка

```bash
set -euo pipefail
for file in change-brief.md controlled-change-plan.md change-review-gate.md; do
  test -f "artifacts/module-04/$file" || exit 1
done
for path in models.py service.py tests/test_service.py api/openapi.yaml requirements.md README.md; do
  grep -R -q "$path" artifacts/module-04 || exit 1
done
for term in "Acceptance" "priority" "normal" "test-first" "git diff" \
  "Evidence автора" "Проверки reviewer-а" "changes requested" "bounded revision"; do
  grep -R -qi "$term" artifacts/module-04 || exit 1
done
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
grep -q 'TaskPriority' "$workdir/priority.diff"
cd "$repo_root"
git diff --check
```

Проведите два walkthrough: нормальный путь ведет после approve к commit handoff; scope drift ведет к `changes requested`, затем coordinator отдает package единственному receiver implementation.

## Оценивание

Каждый критерий оценивается от 0 до 2.

| Критерий | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Intake и acceptance | Нет owner или criteria | Есть request без exclusions | Product owner, criteria, impact и boundaries проверяемы |
| Test-first и impact | Нет tests или пути расплывчаты | Tests есть без docs | Focused tests, guards, code/tests/docs/OpenAPI и red/green route |
| Evidence и review | Green test выдан за приемку | Diff или review неполны | Author/reviewer разделены, есть diff, output, sync и verdict |
| Scope drift | Лишнее принято | Drift без correction | changes requested, path/risk/receiver и bounded revision |
| Commit boundary | Self-approval/push | Commit без review handoff | Commit после approve; push/final acceptance отдельно |

Для зачета нужно не менее 8 из 10 и отсутствие критического дефекта.

## Критические дефекты

- **Scope drift accepted:** сортировка, duplicate-title или endpoint приняты без request.
- **Missing contract sync:** priority нет в requirements, README или OpenAPI после заявленной реализации.
- **No test evidence:** нет exact command/output или focused tests.
- **Self-approval:** implementation объявляет approve, commit, push или final acceptance.
- **Reviewer edits author work:** reviewer исправляет diff вместо finding и correction receiver.
- **Unbounded correction:** нет пути, риска, receiver или границы revision.
- **External-reading dependency:** обязательный маршрут требует сеть или внешний материал.

## Локальный маршрут исправления

- scope drift accepted -> удалите лишнее поведение из plan/gate, добавьте `changes requested` и повторите walkthrough;
- missing contract sync -> добавьте три docs paths и единые `high`, `normal`, `low`, default `normal`, повторите review;
- no test evidence -> назовите focused tests, pytest command и observed result, затем выполните ее локально;
- self-approval -> верните commit/push/acceptance coordinator и human owner;
- reviewer edits author work -> замените edit на finding с путем, риском и implementation receiver;
- unbounded correction -> ограничьте change конкретным finding и повторите gate;
- failed check -> сохраните output, назовите failure owner и верните package coordinator-у.

## Результат checkpoint

Передайте coordinator три Module 4 артефакта и review verdict. Handoff содержит scope, changed/untouched paths, test output, docs/OpenAPI evidence, finding или approve, receiver, одно действие и resume condition. На scope drift итогом является `changes requested`, а не commit.
