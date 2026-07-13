# Модуль 4. Контролируемый workflow разработки

Модуль переводит согласованное изменение из запроса в проверяемый handoff. Сквозная задача: добавить к `Task` поле приоритета `high`, `normal` или `low`, сохранив существующее поведение названия, идентификатора и завершения задачи. Это учебный request, а не разрешение менять стенд без артефактов и review.

К концу модуля вы создадите три связанных артефакта:

1. [Прием задачи, acceptance и impact](lesson-10-task-intake.md) - `artifacts/module-04/change-brief.md`.
2. [Контролируемое test-first изменение](lesson-11-controlled-code-change.md) - `artifacts/module-04/controlled-change-plan.md`.
3. [Engineering gates и handoff](lesson-12-engineering-gates.md) - `artifacts/module-04/change-review-gate.md`.
4. [Checkpoint 4](checkpoint.md) - отказ от scope drift и bounded revision.

## Обязательный локальный маршрут

Начните с `artifacts/module-02/context-packet.md`, `artifacts/module-02/context-map-evidence-gate.md` и `artifacts/module-03/coordinator-handoff.md`. Затем прочитайте `projects/training-task-app/requirements.md`, `src/task_app/models.py`, `src/task_app/service.py`, `tests/test_service.py`, `api/openapi.yaml` и `README.md`. Форму процесса и независимой проверки берите из `templates/workflow.md` и `templates/review-gate.md`.

Обязательный путь полностью локальный и не требует платного API-ключа или облачного аккаунта: уроки дают request, подготовленные ответы и проверяемые команды. Live agent допустим только для черновика. Его текст не является acceptance, approval, test evidence или commit evidence. Implementation вносит только согласованную обратимую правку; reviewer независимо выдает verdict; approval commit или внешнего действия не появляется из green test и не принадлежит implementation.

## Готовность модуля

Модуль завершен, если:

- change brief связывает request, acceptance, exclusions, repo-relative impact и named decision owner;
- план требует сначала сфокусированные тесты, затем минимальную реализацию, а также называет код, тесты, документацию и OpenAPI;
- review gate хранит diff, test output, документационную сверку, SHA и раздельные evidence implementation/reviewer;
- scope drift приводит к `changes requested` и bounded revision, а не к частичному approve;
- в handoff видны receiver, одно следующее действие, STOP или resume condition и отсутствие self-approval.
