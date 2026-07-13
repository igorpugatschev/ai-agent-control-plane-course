# Documentary historical case: отчёт о дефекте

## Provenance и stop-gate

Этот файл документирует historical case, но не содержит pinned defective revision,
архива исходников или исполняемого defect fixture. Поэтому он не доказывает
воспроизводимый defect в current checkout. Если stable suite дает `11 passed`,
evidence package записывает `not reproduced`, missing revision/fixture и `STOP`:
запросить pinned artifact до утверждения, что defect reproducible. Не меняйте
current code или tests, чтобы искусственно получить failure.

Учебная ценность reproduction сохраняется: после получения pinned defective
artifact условия, steps и minimal check ниже можно выполнить против него и
зафиксировать actual output.

## Заголовок

После завершения задачи она всё ещё считается активной при проверке дубликата.

## Условия

- Python 3.11+;
- чистый экземпляр `TaskService`;
- одна задача с названием `Проверить контракт`.

## Шаги воспроизведения

```python
from task_app import TaskService

service = TaskService()
task = service.create_task("Проверить контракт")
service.complete_task(task.id)
service.create_task("проверить КОНТРАКТ")
```

## Ожидаемый результат

Завершённая задача больше не является активной, поэтому вторая задача создаётся с новым идентификатором.

## Документированный фактический результат historical case

Сервис повторно отклоняет создание с ошибкой `Активная задача с таким названием уже существует`, потому что проверка дубликата учитывает все задачи, а не только статус `open`.

## Доказательство

Этот minimal check показывает форму evidence для pinned defective artifact: на нем
он должен падать, а после исправления проходить. В текущий stable suite его не
добавляют и current code для него не меняют:

```python
def test_done_title_can_be_reused():
    service = TaskService()
    task = service.create_task("Проверить контракт")
    service.complete_task(task.id)
    replacement = service.create_task("проверить КОНТРАКТ")
    assert replacement.id == 2
```

Этот тест является отдельным учебным примером и не добавляется в стабильный набор стенда.
